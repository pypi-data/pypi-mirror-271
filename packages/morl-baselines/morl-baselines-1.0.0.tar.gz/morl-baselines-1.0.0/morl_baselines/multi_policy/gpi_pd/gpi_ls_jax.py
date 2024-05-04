import random
from typing import Callable, List, Optional
from functools import partial
import os
import cvxpy as cp
from cvxpylayers.jax import CvxpyLayer
import gymnasium as gym
import numpy as np
import jax
import jax.numpy as jnp
import optax
import flax
import flax.linen as nn
from flax.training.train_state import TrainState
from flax.training import checkpoints, orbax_utils
flax.config.update('flax_use_orbax_checkpointing', True)
import orbax

import wandb as wb
from rl.dynamics.mixture_density_net import MixtureDensityNet
from rl.dynamics.ensemble_model_jax import ProbabilisticEnsemble
from rl.dynamics.util_jax import ModelEnv
from rl.rl_algorithm import RLAlgorithm
from rl.utils.buffer import ReplayBuffer
from rl.utils.eval import eval_mo, visualize_eval_jax
from rl.utils.prioritized_buffer import PrioritizedReplayBuffer
from rl.utils.utils import (get_grad_norm, huber, layer_init,
                            linearly_decaying_epsilon, polyak_update,
                            random_weights)


class Psi(nn.Module):
    action_dim: int
    rew_dim: int
    dropout_rate: Optional[float] = 0.01
    use_layer_norm: bool = True
    num_hidden_layers: int = 4
    hidden_dim: int = 256
    image_obs: bool = False

    @nn.compact
    def __call__(self, obs: jnp.ndarray, w: jnp.ndarray, deterministic: bool):
        if self.image_obs:
            if len(obs.shape) == 3:
                obs = obs[None]
            x = jnp.transpose(obs, (0, 2, 3, 1))
            x = x / (255.0)
            x = nn.Conv(32, kernel_size=(8, 8), strides=(4, 4), padding=0)(x)
            if self.use_layer_norm:
                x = nn.LayerNorm()(x)
            x = nn.relu(x)
            x = nn.Conv(64, kernel_size=(4, 4), strides=(2, 2), padding=0)(x)
            if self.use_layer_norm:
                x = nn.LayerNorm()(x)
            x = nn.relu(x)
            x = nn.Conv(64, kernel_size=(3, 3), strides=(1, 1), padding=0)(x)
            if self.use_layer_norm:
                x = nn.LayerNorm()(x)
            x = nn.relu(x)
            x = x.reshape((x.shape[0], -1))
            x = nn.Dense(self.hidden_dim)(x)
            if self.use_layer_norm:
                x = nn.LayerNorm()(x)
            h_obs = nn.relu(x)
        else:
            h_obs = nn.Dense(self.hidden_dim)(obs)
            if self.dropout_rate is not None and self.dropout_rate > 0:
                h_obs = nn.Dropout(rate=self.dropout_rate)(h_obs, deterministic=deterministic)
            if self.use_layer_norm:
                h_obs = nn.LayerNorm()(h_obs)
            h_obs = nn.relu(h_obs)

        h_w = nn.Dense(self.hidden_dim)(w)
        if self.dropout_rate is not None and self.dropout_rate > 0:
            h_w = nn.Dropout(rate=self.dropout_rate)(h_w, deterministic=deterministic)
        if self.use_layer_norm:
            h_w = nn.LayerNorm()(h_w)
        h_w = nn.relu(h_w)

        h = h_obs * h_w
        for _ in range(self.num_hidden_layers - 1):
            h = nn.Dense(self.hidden_dim)(h)
            if self.dropout_rate is not None and self.dropout_rate > 0:
                h = nn.Dropout(rate=self.dropout_rate)(h, deterministic=deterministic)
            if self.use_layer_norm:
                h = nn.LayerNorm()(h)
            h = nn.relu(h)
        x = nn.Dense(self.action_dim * self.rew_dim)(h)
        return x

class VectorPsi(nn.Module):
    action_dim: int
    rew_dim: int
    use_layer_norm: bool = True
    dropout_rate: Optional[float] = 0.01
    n_critics: int = 2
    num_hidden_layers: int = 4
    hidden_dim: int = 256
    image_obs: bool = False

    @nn.compact
    def __call__(self, obs: jnp.ndarray, w: jnp.ndarray, deterministic: bool):
        vmap_critic = nn.vmap(
            Psi,
            variable_axes={"params": 0},  # parameters not shared between the critics
            split_rngs={"params": True, "dropout": True},  # different initializations
            in_axes=None,
            out_axes=0,
            axis_size=self.n_critics,
        )
        q_values = vmap_critic(
            action_dim=self.action_dim,
            rew_dim=self.rew_dim,
            dropout_rate=self.dropout_rate,
            use_layer_norm=self.use_layer_norm,
            num_hidden_layers=self.num_hidden_layers,
            hidden_dim=self.hidden_dim,
            image_obs=self.image_obs,
            )(obs, w, deterministic)
        return q_values.reshape((self.n_critics, -1, self.action_dim, self.rew_dim))

class TrainState(TrainState):
    target_params: flax.core.FrozenDict


class USFA(RLAlgorithm):
    def __init__(
        self,
        env,
        learning_rate: float = 3e-4,
        initial_epsilon: float = 0.01,
        final_epsilon: float = 0.01,
        ucb_exploration: float = 0.0,
        epsilon_decay_steps: int = None,  # None == fixed epsilon
        tau: float = 1.0,
        target_net_update_freq: int = 1000,  # ignored if tau != 1.0
        buffer_size: int = int(1e6),
        net_arch: List = [256, 256],
        num_nets: int = 1,
        batch_size: int = 256,
        learning_starts: int = 100,
        gradient_updates: int = 1,
        gamma: float = 0.99,
        max_grad_norm: Optional[float] = None,
        use_gpi: bool = True,
        n_step: int = 1,
        gpi_type: str = "gpi",
        ugpi_temp: float = 1.0,
        lcb_pessimism: float = 0.0,
        dyna: bool = False,
        per: bool = False,
        gper: bool = False,
        alpha_per: float = 0.6,
        envelope: bool = False,
        min_priority: float = 1.0,
        drop_rate: float = 0.01,
        layer_norm: bool = True,
        dynamics_mdn: bool = False,
        dynamics_ensemble_size: int = 7,
        dynamics_num_elites: int = 5,
        dynamics_normalize_inputs: bool = False,
        dynamics_uncertainty_threshold: float = 0.5,
        dynamics_train_freq: Callable = lambda x: 1000,
        dynamics_rollout_len: int = 1,
        dynamics_rollout_starts: int = 5000,
        dynamics_rollout_freq: int = 250,
        dynamics_rollout_batch_size: int = 10000,
        dynamics_buffer_size: int = 400000,
        dynamics_net_arch: List = [200, 200, 200, 200],
        real_ratio: float = 0.05,
        reset_mode = None,
        seed: int = 0,
        project_name: str = "usfa",
        experiment_name: str = "usfa",
        log: bool = True,
        device = None
        ):
        super().__init__(env, experiment_name=experiment_name, project_name=project_name, device=device)
        self.phi_dim = len(self.env.w)
        self.learning_rate = learning_rate
        self.initial_epsilon = initial_epsilon
        self.epsilon = initial_epsilon
        self.epsilon_decay_steps = epsilon_decay_steps
        self.final_epsilon = final_epsilon
        self.ucb_exploration = ucb_exploration
        self.tau = tau
        self.target_net_update_freq = target_net_update_freq
        self.gamma = gamma
        self.max_grad_norm = max_grad_norm
        self.use_gpi = use_gpi
        self.cgpi_layer = None
        self.min_phi = -np.ones(self.phi_dim)
        self.gpi_type = gpi_type
        self.include_w = False
        self.ugpi_temp = ugpi_temp
        self.lcb_pessimism = lcb_pessimism
        self.n_step = n_step
        self.buffer_size = buffer_size
        self.net_arch = net_arch
        self.dynamics_net_arch = dynamics_net_arch
        self.learning_starts = learning_starts
        self.batch_size = batch_size
        self.gradient_updates = gradient_updates
        self.num_nets = num_nets
        self.drop_rate = drop_rate
        self.layer_norm = layer_norm
        self.reset_mode = reset_mode

        key = jax.random.PRNGKey(seed)
        self.key, psi_key, dropout_key = jax.random.split(key, 3)

        obs = env.observation_space.sample()
        self.image_obs = len(obs.shape) > 2
        self.psi = VectorPsi(self.action_dim, self.phi_dim, self.layer_norm, self.drop_rate, self.num_nets, num_hidden_layers=len(self.net_arch), hidden_dim=self.net_arch[0], image_obs=self.image_obs)
        self.psi_state = TrainState.create(
            apply_fn=self.psi.apply,
            params=self.psi.init(
                {"params": psi_key, "dropout": dropout_key},
                obs,
                env.w,
                deterministic=False,
            ),
            target_params=self.psi.init(
                {"params": psi_key, "dropout": dropout_key},
                obs,
                env.w,
                deterministic=False,
            ),
            tx=optax.adam(learning_rate=self.learning_rate),
        )
        self.psi.apply = jax.jit(self.psi.apply, static_argnames=("dropout_rate", "use_layer_norm", "deterministic"))

        self.per = per
        self.gper = gper
        self.envelope = envelope
        if self.per:
            self.replay_buffer = PrioritizedReplayBuffer(self.observation_shape, 1, rew_dim=self.phi_dim, max_size=buffer_size, action_dtype=np.uint8)
        else:
            self.replay_buffer = ReplayBuffer(self.observation_shape, 1, rew_dim=self.phi_dim, max_size=buffer_size, action_dtype=np.uint8)
        self.min_priority = min_priority
        self.alpha = alpha_per
        self.M = []

        self.log = log
        if log:
            self.setup_wandb(project_name, experiment_name)

    def get_config(self):
        return {
            "env_id": self.env.unwrapped.spec.id,
            "learning_rate": self.learning_rate,
            "initial_epsilon": self.initial_epsilon,
            "epsilon_decay_steps:": self.epsilon_decay_steps,
            "batch_size": self.batch_size,
            "per": self.per,
            "alpha_per": self.alpha,
            "min_priority": self.min_priority,
            "tau": self.tau,
            "num_nets": self.num_nets,
            "clip_grand_norm": self.max_grad_norm,
            "target_net_update_freq": self.target_net_update_freq,
            "gamma": self.gamma,
            "net_arch": self.net_arch,
            "model_arch": self.dynamics_net_arch,
            "gradient_updates": self.gradient_updates,
            "buffer_size": self.buffer_size,
            "learning_starts": self.learning_starts,
            "drop_rate": self.drop_rate,
            "layer_norm": self.layer_norm,
        }

    def save(self, save_dir="weights/", filename=None):
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)

        saved_params = {}
        saved_params["psi_net_state"] = self.psi_state
        saved_params["M"] = self.M
        if self.dyna:
            saved_params.update(self.dynamics.get_params())

        filename = self.experiment_name if filename is None else filename
        orbax_checkpointer = orbax.checkpoint.PyTreeCheckpointer()
        save_args = orbax_utils.save_args_from_target(saved_params)
        orbax_checkpointer.save(save_dir + filename, saved_params, save_args=save_args, force=True)

    def load(self, path, step=None):
        target = {"psi_net_state": self.psi_state, "M": self.M}
        if self.dyna:
            target.update(self.dynamics.get_params())
        restored = checkpoints.restore_checkpoint(ckpt_dir=path, target=None, step=step)
        target['M'] = restored['M'] # for some reason I need to do this
        if self.dyna:
            target['elites'] = restored['elites']
            target['inputs_mu'] = restored['inputs_mu']
            target['inputs_sigma'] = restored['inputs_sigma']
        restored = checkpoints.restore_checkpoint(ckpt_dir=path, target=target, step=step)
        self.psi_state = restored["psi_net_state"]
        self.M = [w for w in restored["M"].values()]
        #self.M = [w for w in restored["M"]]
        if self.dyna:
            self.dynamics.ensemble_state = restored["ensemble_state"]
            self.dynamics.elites = restored["elites"]
            self.dynamics.inputs_mu = restored["inputs_mu"]
            self.dynamics.inputs_sigma = restored["inputs_sigma"]
        self.cgpi_layer = None  # reset cgpi layer

    def sample_batch_experiences(self):
        if not self.dyna or self.num_timesteps < self.dynamics_rollout_starts or len(self.dynamics_buffer) == 0:
            return self.replay_buffer.sample(self.batch_size, to_tensor=False, device=self.device)
        else:
            num_real_samples = int(self.batch_size * self.real_ratio)  # real_ratio% of real world data
            if self.per:
                s_obs, s_actions, s_rewards, s_next_obs, s_dones, idxes = self.replay_buffer.sample(num_real_samples, to_tensor=False, device=self.device)
            else:
                s_obs, s_actions, s_rewards, s_next_obs, s_dones = self.replay_buffer.sample(num_real_samples, to_tensor=False, device=self.device)
            m_obs, m_actions, m_rewards, m_next_obs, m_dones = self.dynamics_buffer.sample(self.batch_size - num_real_samples, to_tensor=False, device=self.device)
            experience_tuples = (
                np.concatenate([s_obs, m_obs], axis=0),
                np.concatenate([s_actions, m_actions], axis=0),
                np.concatenate([s_rewards, m_rewards], axis=0),
                np.concatenate([s_next_obs, m_next_obs], axis=0),
                np.concatenate([s_dones, m_dones], axis=0),
            )
            if self.per:
                return experience_tuples + (idxes,)
            return experience_tuples

    @staticmethod
    @partial(jax.jit, static_argnames=["psi", "pessimism", "return_q_values"])
    def batch_gpi(psi, psi_state, obs, w, pessimism, M, key, return_q_values=False):
        #key, subkey = jax.random.split(key)
        M_stack = jnp.stack(M)
        M_stack = M_stack.reshape(1, M_stack.shape[0], M_stack.shape[1]).repeat(len(obs), axis=0)
        obs_m = obs.reshape(obs.shape[0], 1, *obs.shape[1:]).repeat(M_stack.shape[1], axis=1)

        psi_values = psi.apply(psi_state.params, obs_m, M_stack, deterministic=True)
        q_values = (psi_values * w).sum(axis=3).reshape(psi_values.shape[0], obs.shape[0], len(M), -1)
        q_values = q_values.mean(axis=0) #- pessimism*q_values.std(axis=0)

        max_q = jnp.max(q_values, axis=2)
        pi = jnp.argmax(max_q, axis=1)
        best_q_values = q_values[jnp.arange(q_values.shape[0]), pi]
        acts = best_q_values.argmax(axis=1)

        if return_q_values:
            return acts, best_q_values[jnp.arange(q_values.shape[0]), acts], key

        return acts, key

    def rollout_dynamics(self, w):
        # Dyna Planning
        num_times = int(np.ceil(self.dynamics_rollout_batch_size / 10000))
        batch_size = min(self.dynamics_rollout_batch_size, 10000)
        num_added_imagined_transitions = 0
        for iteration in range(num_times):
            obs = self.replay_buffer.sample_obs(batch_size, to_tensor=False)
            model_env = ModelEnv(self.dynamics, self.env.unwrapped.spec.id, rew_dim=len(w))

            for h in range(self.dynamics_rollout_len):
                actions, self.key = USFA.batch_gpi(self.psi, self.psi_state, obs, w, 0.0, self.M, self.key)
                actions_one_hot = nn.one_hot(actions, num_classes=self.action_dim)

                next_obs_pred, r_pred, dones, info = model_env.step(obs, actions_one_hot, deterministic=True)
                uncertainties = info['uncertainty']
                obs, actions = jax.device_get(obs), jax.device_get(actions)

                for i in range(len(obs)):
                    if uncertainties[i] < self.dynamics_uncertainty_threshold:
                        self.dynamics_buffer.add(obs[i], actions[i], r_pred[i], next_obs_pred[i], dones[i])
                        num_added_imagined_transitions += 1

                nonterm_mask = ~dones.squeeze(-1)
                if nonterm_mask.sum() == 0:
                    break
                obs = next_obs_pred[nonterm_mask]

        if self.log:
            self.writer.add_scalar("dynamics/uncertainty_mean", uncertainties.mean(), self.num_timesteps)
            self.writer.add_scalar("dynamics/uncertainty_max", uncertainties.max(), self.num_timesteps)
            self.writer.add_scalar("dynamics/uncertainty_min", uncertainties.min(), self.num_timesteps)
            self.writer.add_scalar("dynamics/model_buffer_size", len(self.dynamics_buffer), self.num_timesteps)
            self.writer.add_scalar("dynamics/imagined_transitions", num_added_imagined_transitions, self.num_timesteps)

    @staticmethod
    @partial(jax.jit, static_argnames=["psi", "gamma", "min_priority"])
    def update(psi, psi_state, w, obs, actions, rewards, next_obs, dones, gamma, min_priority, key):
        key, inds_key, dropout_key_target, dropout_key_current = jax.random.split(key, 4)

        # DroQ update
        if psi.n_critics >= 2:
            psi_values_next = psi.apply(psi_state.target_params, next_obs, w, deterministic=False, rngs={"dropout": dropout_key_target})
            if psi_values_next.shape[0] > 2:
                inds = jax.random.randint(inds_key, (2,), 0, psi_values_next.shape[0])
                psi_values_next = psi_values_next[inds]
            q_values_next = (psi_values_next * w.reshape(w.shape[0], 1, w.shape[1])).sum(axis=3)
            min_inds = q_values_next.argmin(axis=0)
            min_psi_values = jnp.take_along_axis(psi_values_next, min_inds[None,...,None], 0).squeeze(0)
            
            max_q = (min_psi_values * w.reshape(w.shape[0], 1, w.shape[1])).sum(axis=2)
            max_acts = max_q.argmax(axis=1)
            target = min_psi_values[jnp.arange(min_psi_values.shape[0]), max_acts]

            def mse_loss(params, droptout_key):
                psi_values = psi.apply(params, obs, w, deterministic=False, rngs={"dropout": droptout_key})
                psi_values = psi_values[:, jnp.arange(psi_values.shape[1]), actions.squeeze()]
                tds = psi_values - target_psi
                loss = jnp.abs(tds)
                loss = jnp.where(loss < min_priority, 0.5 * loss ** 2, loss * min_priority)
                return loss.mean(), tds
        # DDQN update
        else:
            psi_values_next = psi.apply(psi_state.target_params, next_obs, w, deterministic=True)[0]
            psi_values_not_target = psi.apply(psi_state.params, next_obs, w, deterministic=True)
            q_values_next = (psi_values_not_target * w.reshape(w.shape[0], 1, w.shape[1])).sum(axis=3)[0]
            max_acts = q_values_next.argmax(axis=1)
            target = psi_values_next[jnp.arange(psi_values_next.shape[0]), max_acts]

            def mse_loss(params, droptout_key):
                psi_values = psi.apply(params, obs, w, deterministic=True)
                psi_values = psi_values[:, jnp.arange(psi_values.shape[1]), actions.squeeze()]
                tds = psi_values - target_psi
                loss = jnp.abs(tds)
                loss = jnp.where(loss < min_priority, 0.5 * loss ** 2, loss * min_priority)
                return loss.mean(), tds

        target_psi = rewards + (1 - dones) * gamma * target

        (loss_value, td_error), grads = jax.value_and_grad(mse_loss, has_aux=True)(psi_state.params, dropout_key_current)
        psi_state = psi_state.apply_gradients(grads=grads)

        return psi_state, loss_value, td_error, key

    def train(self, weight):
        critic_losses = []
        for g in range(self.gradient_updates if self.num_timesteps >= self.dynamics_rollout_starts else 1):
            if self.per:
                s_obs, s_actions, s_rewards, s_next_obs, s_dones, idxes = self.sample_batch_experiences()
            else:
                s_obs, s_actions, s_rewards, s_next_obs, s_dones = self.sample_batch_experiences()

            if len(self.M) > 1:
                s_obs, s_actions, s_rewards, s_next_obs, s_dones = np.vstack([s_obs]*2), np.vstack([s_actions]*2), np.vstack([s_rewards]*2), np.vstack([s_next_obs]*2), np.vstack([s_dones]*2)
                w = np.vstack([weight for _ in range(s_obs.shape[0] // 2)] + random.choices(self.M, k=s_obs.shape[0] // 2))
            else:
                w = weight.repeat(s_obs.shape[0], 1)

            self.key, w_sample = jax.random.split(self.key)
            # w += jax.random.normal(w_sample, w.shape, dtype=jnp.float32) * 0.1

            self.psi_state, loss, td_error, self.key = USFA.update(self.psi, self.psi_state, w, s_obs, s_actions, s_rewards, s_next_obs, s_dones, self.gamma, self.min_priority, self.key)
            critic_losses.append(loss.item())

            if self.per:
                td_error = jax.device_get(td_error)
                td_error = np.abs((td_error[:,: len(idxes)] * w[: len(idxes)]).sum(axis=2))
                per = np.max(td_error, axis=0)
                priority = per.clip(min=self.min_priority)**self.alpha
                self.replay_buffer.update_priorities(idxes, priority)

        if self.tau != 1 or self.num_timesteps % self.target_net_update_freq == 0:
            self.psi_state = USFA.target_net_update(self.psi_state)

        if self.epsilon_decay_steps is not None:
            self.epsilon = linearly_decaying_epsilon(self.initial_epsilon, self.epsilon_decay_steps, self.num_timesteps, self.learning_starts, self.final_epsilon)

        if self.log and self.num_timesteps % 100 == 0:
            if self.per:
                self.writer.add_scalar("metrics/mean_priority", np.mean(priority), self.num_timesteps)
                self.writer.add_scalar("metrics/max_priority", np.max(priority), self.num_timesteps)
                self.writer.add_scalar("metrics/mean_td_error_w", np.mean(per), self.num_timesteps)
            if False and self.gper:
                self.writer.add_scalar("metrics/mean_gpriority", np.mean(gpriority), self.num_timesteps)
                self.writer.add_scalar("metrics/max_gpriority", np.max(gpriority), self.num_timesteps)
                self.writer.add_scalar("metrics/mean_gtd_error_w", gper.abs().mean().item(), self.num_timesteps)
                self.writer.add_scalar("metrics/mean_absolute_diff_gtd_td", (gper - per).abs().mean().item(), self.num_timesteps)
            self.writer.add_scalar("losses/critic_loss", np.mean(critic_losses), self.num_timesteps)
            self.writer.add_scalar("metrics/epsilon", self.epsilon, self.num_timesteps)

    @staticmethod
    @jax.jit
    def target_net_update(psi_state):
        psi_state = psi_state.replace(target_params=optax.incremental_update(psi_state.params, psi_state.target_params, 1))
        return psi_state

    @staticmethod
    @partial(jax.jit, static_argnames=["temperature"])
    def uncertainty(q_values, temperature):
        variances = q_values.var(axis=0).sum(axis=1)
        uncertainties = nn.softmax(-variances / temperature, axis=0)
        return uncertainties

    @staticmethod
    @partial(jax.jit, static_argnames=["psi", "model", "normalize_inputs", "ugpi_temp", "env_id", "gamma", "return_policy_index"])
    def old_ugpi_action(psi, psi_state, model, model_state, inputs_mu, inputs_sigma, normalize_inputs, elites, obs, w, ugpi_temp, M, env_id, gamma, key, return_policy_index):
        M = jnp.stack(M)

        action_dim = model.input_dim - obs.shape[0]
        rew_dim = w.shape[0]
        obs_modelo = obs.reshape(1, -1)
        actions = jnp.eye(action_dim).repeat(obs_modelo.shape[0], axis=0)
        obs_modelo = jnp.tile(obs_modelo, (action_dim, 1))
        obs_actions = jnp.concatenate([obs_modelo, actions], axis=1)
        sample, logvar = ProbabilisticEnsemble.forward(model, model_state, obs_actions, inputs_mu, inputs_sigma, normalize_inputs=normalize_inputs, deterministic=True, return_dist=True, key=key)
        sample, logvar = sample[elites], logvar[elites]
        #sample_mean, sample_std = sample.mean(axis=0), sample.std(axis=0)
        #sample_mean, sample_std = sample_mean[None], sample_std[None]
        rewards, next_obs = sample[:,:, : rew_dim], sample[:, :, rew_dim :]
        next_obs += obs_modelo

        #Ensemble Standard Deviation/Variance (Lakshminarayanan et al., 2017)
        """ vars = jnp.exp(logvar)
        mean_ensemble = sample.mean(axis=0)
        var_ensemble = (sample**2 + vars).mean(axis=0) - mean_ensemble**2
        std_ensemble = jnp.sqrt(var_ensemble + 1e-12)
        model_uncertainties = std_ensemble.sum(-1) """
        
        obs_m = obs.reshape(1,-1).repeat(M.shape[0], axis=0)
        psi_values = psi.apply(psi_state.params, obs_m, M, deterministic=True)[0]

        def compute_policy_targets(w):
            def target(reward, next_obs, this_w):
                next_psi = psi.apply(psi_state.params, next_obs, this_w, deterministic=True)[0]
                next_q = (next_psi * this_w).sum(axis=2)
                next_act = next_q.argmax(axis=1)
                next_psi = jnp.take_along_axis(next_psi, next_act[:,None,None], axis=1).squeeze(1)
                if env_id == "minecart-v0":
                    dones = termination_fn_minecart(obs_modelo, actions, next_obs)
                else:
                    dones = jnp.zeros(action_dim)
                return reward + gamma * (1 - dones) * next_psi

            targets = jax.vmap(target, (0, 0, None))(rewards, next_obs, w)
            return targets

        all_targets = jax.vmap(compute_policy_targets)(M)
        mean_target = (all_targets * w).sum(3).mean(1)

        q_values = (psi_values * w).sum(2)
        uncertainties = jnp.abs(q_values - mean_target)

        """ all_targets = jax.vmap(compute_policy_targets)(M)
        all_targets = (all_targets * w).sum(3)
        q_values = (psi_values * w).sum(2)
        uncertainties = (q_values[:,None,:] - all_targets).std(1) """

        if M.shape[0] > 1:
            # k = max(int(0.75 * M.shape[0]), 1)
            def zero_k_largest(x_column):
                # Get the indices of the k smallest values in the column
                #indices_to_zero = jnp.argsort(x_column)[:k]
                q1 = jnp.percentile(x_column, 25)
                q3 = jnp.percentile(x_column, 75)
                iqr = q3 - q1
                threshold = q3 + 1.5 * iqr
                mask = jnp.where(x_column <= threshold, 0, 1000000)
                #x_column = jnp.where(jnp.isin(jnp.arange(uncertainties.shape[0]), indices_to_zero), 0, 1000000)
                return mask
            mask = jax.vmap(zero_k_largest, 1)(uncertainties).T
            # mask *= jnp.where((jnp.zeros_like(uncertainties) + model_uncertainties) >= 0.2, 0, 1)
            #mask *= jnp.where(uncertainties < 0.005, 0, 1)
            #print(q_values)
            q_values -= mask

        # q_values -= ugpi_temp*uncertainties
        #uncertainties = USFA.uncertainty(q_values, ugpi_temp)
        #q_values = q_values[0] * uncertainties.reshape(q_values.shape[1], 1)

        max_q = q_values.max(axis=1)
        policy_index = max_q.argmax()  # max_i max_a q(s,a,w_i)
        action = q_values[policy_index].argmax()

        if return_policy_index:
            return action, policy_index, uncertainties, key 

        return action, uncertainties, key 
    
    @staticmethod
    @partial(jax.jit, static_argnames=["psi", "pessimism", "return_policy_index"])
    def lcbgpi_action(psi, psi_state, obs, w, M, pessimism, key, return_policy_index=False):
        M = jnp.stack(M)
        
        #key, subkey = jax.random.split(key)
        obs_m = obs.reshape(1,*obs.shape).repeat(M.shape[0], axis=0)
        psi_values = psi.apply(psi_state.params, obs_m, M, deterministic=True)
        q_values = (psi_values * w.reshape(1, 1, 1, w.shape[0])).sum(axis=3)

        q_values = q_values.mean(axis=0) - pessimism*q_values.std(axis=0)

        max_q = q_values.max(axis=1)
        policy_index = max_q.argmax()  # max_i max_a q(s,a,w_i)
        action = q_values[policy_index].argmax()

        if return_policy_index:
            return action, policy_index, key
        return action, key
    
    @staticmethod
    @partial(jax.jit, static_argnames=["psi", "pessimism", "return_policy_index"])
    def ugpi_action(psi, psi_state, obs, w, M, pessimism, key, return_policy_index=False):
        M = jnp.stack(M)
        
        #key, subkey = jax.random.split(key)
        obs_m = obs.reshape(1,*obs.shape).repeat(M.shape[0], axis=0)
        psi_values = psi.apply(psi_state.params, obs_m, M, deterministic=True)
        q_values = (psi_values * w.reshape(1, 1, 1, w.shape[0])).sum(axis=3)

        n = q_values.shape[0]
        # tinv(0.9, 9) = 1.383028, tinv(0.95, 9) = 1.833113, tinv(0.99, 9) = 2.821438
        if pessimism == 0.9:
            tinv = 1.383028
        elif pessimism == 0.95:
            tinv = 1.833113
        elif pessimism == 0.99:
            tinv = 2.821438
        # LB = v.mean() - stddev(v) / math.sqrt(n) * tinv(1.0 - delta, n - 1)
        # sqrt(10) = 3.162278
        if pessimism == 1.0 or pessimism == 2.0:
            q_values = q_values.mean(axis=0) - pessimism*q_values.std(axis=0)
        else:
            q_values = q_values.mean(axis=0) - q_values.std(axis=0) / jnp.sqrt(n) * tinv

        #q_low = jnp.percentile(q_values, 25, axis=0)
        #q_high = jnp.percentile(q_values, 75, axis=0)
        #iqr = q_high - q_low
        #threshold_high = q_high + pessimism * iqr
        #threshold_low = q_low - pessimism * iqr
        #mask = (q_values >= q_low) & (q_values <= q_high)
        # mask = (q_values <= q_high)
        #mask = (q_values <= threshold_high)  #& (q_values >= threshold_low)
        #q_values = jnp.sum(q_values * mask, axis=0) / jnp.sum(mask, axis=0)

        max_q = q_values.max(axis=1)
        policy_index = max_q.argmax()  # max_i max_a q(s,a,w_i)
        action = q_values[policy_index].argmax()

        if return_policy_index:
            return action, policy_index, key
        return action, key
    
    @staticmethod
    @partial(jax.jit, static_argnames=["psi", "return_policy_index"])
    def gpi_action(psi, psi_state, obs, w, M, key, return_policy_index=False):
        M = jnp.stack(M)
        
        #key, subkey = jax.random.split(key)
        obs_m = obs.reshape(1,*obs.shape).repeat(M.shape[0], axis=0)
        psi_values = psi.apply(psi_state.params, obs_m, M, deterministic=True)
        q_values = (psi_values * w.reshape(1, 1, 1, w.shape[0])).sum(axis=3)
        
        q_values = q_values.mean(axis=0)

        max_q = q_values.max(axis=1)
        policy_index = max_q.argmax()  # max_i max_a q(s,a,w_i)
        action = q_values[policy_index].argmax()

        if return_policy_index:
            return action, policy_index, key
        return action, key

    @staticmethod
    @partial(jax.jit, static_argnames=["psi", "return_policy_index"])
    def mingpi_action(psi, psi_state, obs, w, M, key, return_policy_index=False):
        M = jnp.stack(M)
        
        #key, subkey = jax.random.split(key)
        obs_m = obs.reshape(1,-1).repeat(M.shape[0], axis=0)
        psi_values = psi.apply(psi_state.params, obs_m, M, deterministic=True)
        q_values = (psi_values * w.reshape(1, 1, 1, w.shape[0])).sum(axis=3)
        
        q_values = q_values.min(axis=0)

        max_q = q_values.max(axis=1)
        policy_index = max_q.argmax()  # max_i max_a q(s,a,w_i)
        action = q_values[policy_index].argmax()

        if return_policy_index:
            return action, policy_index, key
        return action, key 

    @staticmethod
    @partial(jax.jit, static_argnames=["psi", "model", "normalize_inputs", "env_id", "n_step", "pessimism", "gamma"])
    def uhgpi(psi, psi_state, model, model_state, inputs_mu, inputs_sigma, normalize_inputs, elites, obs, w, M, env_id, n_step, pessimism, gamma, key):
        action_dim = model.input_dim - obs.shape[0]
        rew_dim = w.shape[0]
        obs = obs.reshape(1, -1)
        obs = obs.repeat(action_dim, axis=0)

        if n_step <= 5:  # Brute force all action sequences
            returns = jnp.zeros(action_dim)
            terminals = jnp.zeros(action_dim)
            for k in range(n_step):
                if k == 0:
                    actions = jnp.eye(action_dim) #.repeat(obs.shape[0], axis=0)
                else:
                    actions, q_values, key = USFA.batch_gpi(psi, psi_state, obs, w, 0.0, M, key, return_q_values=True)
                    actions = jax.nn.one_hot(actions, action_dim)

                # obs = jnp.tile(obs, (action_dim, 1))
                obs_actions = jnp.concatenate([obs, actions], axis=1)

                sample, logvar = ProbabilisticEnsemble.forward(model, model_state, obs_actions, inputs_mu, inputs_sigma, normalize_inputs=normalize_inputs, deterministic=True, return_dist=True, key=key)
                # sample = jnp.sign(sample) * (jnp.exp(jnp.abs(sample)) - 1)
                #key, subkey = jax.random.split(key)
                #el = jax.random.choice(subkey, elites, shape=(sample.shape[0],), replace=True)
                sample = sample[elites]
                logvar = logvar[elites]

                vars = jnp.exp(logvar)
                mean_ensemble = sample.mean(axis=0)
                var_ensemble = (sample**2 + vars).mean(axis=0) - mean_ensemble**2
                std_ensemble = jnp.sqrt(var_ensemble + 1e-12)
                model_uncertainties = std_ensemble.sum(-1).reshape(-1, 1)

                sample_mean, sample_std = sample.mean(axis=0), sample.std(axis=0)
                rewards, next_obs = sample_mean[:, : rew_dim] - pessimism*model_uncertainties, sample_mean[:, rew_dim :]
                next_obs += obs

                if env_id == "minecart-v0":
                    dones = termination_fn_minecart(obs, actions, next_obs).squeeze(1)
                else:
                    dones = jnp.zeros(action_dim)
                #returns = jnp.tile(returns, (action_dim, 1)).flatten()
                #terminals = jnp.tile(terminals, (action_dim, 1)).flatten()
                returns += gamma**k * (rewards * w).sum(axis=1) * (1 - terminals)
                terminals = (terminals + dones).clip(0, 1)
                obs = next_obs
    
            next_actions, q_values, key = USFA.batch_gpi(psi, psi_state, obs, w, 0.0, M, key, return_q_values=True)
            returns += gamma**n_step * q_values * (1 - terminals)
            trajectory_ind = returns.argmax(axis=0)
            best_action = trajectory_ind % action_dim

            return best_action, key
        
        else:  # Use MPC with random shooting [https://arxiv.org/pdf/1708.02596.pdf]
            n_samples = 10000
            obs = obs.repeat(n_samples, axis=0)
            key, subkey = jax.random.split(key)
            init_actions = jax.nn.one_hot(jax.random.randint(subkey, (n_samples,), minval=0, maxval=action_dim), action_dim)
            returns = jnp.zeros(n_samples)
            for k in range(n_step):
                if k == 0:
                    actions = init_actions
                else:
                    key, subkey = jax.random.split(key)
                    actions = jax.nn.one_hot(jax.random.randint(subkey, (n_samples,), minval=0, maxval=action_dim), action_dim)
                
                obs_actions = jnp.concatenate([obs, actions], axis=1)

                sample = ProbabilisticEnsemble.forward(model, model_state, obs_actions, inputs_mu, inputs_sigma, normalize_inputs=normalize_inputs, deterministic=True, return_dist=False, key=key)
                #key, subkey = jax.random.split(key)
                #el = jax.random.choice(subkey, elites, shape=(sample.shape[0],), replace=True)
                sample_mean, sample_std = sample.mean(axis=0), sample.std(axis=0)
                rewards, next_obs = sample_mean[:, : rew_dim] - pessimism*sample_std[:, : rew_dim], sample_mean[:, rew_dim :]               

                next_obs += obs
                if env_id == "minecart-v0":
                    dones = termination_fn_minecart(obs, actions, next_obs).squeeze(1)
                else:
                    dones = jnp.zeros(action_dim)
                
                returns += gamma**k * (rewards * w).sum(axis=1)
                obs = next_obs

            next_actions, q_values, key = USFA.batch_gpi(psi, psi_state, obs, w, 0.0, M, key, return_q_values=True)
            returns += gamma**n_step * q_values
            trajectory_ind = returns.argmax(axis=0)
            best_action = init_actions[trajectory_ind]
            best_action = best_action.argmax()
            return best_action, key

    @staticmethod
    @partial(jax.jit, static_argnames=["psi", "model", "normalize_inputs", "env_id", "n_step", "pessimism", "gamma"])
    def nstep_gpi_action(psi, psi_state, model, model_state, inputs_mu, inputs_sigma, normalize_inputs, elites, obs, w, M, env_id, n_step, pessimism, gamma, key):
        action_dim = model.input_dim - obs.shape[0]
        rew_dim = w.shape[0]
        obs = obs.reshape(1, -1)

        if n_step <= 5:  # Brute force all action sequences
            returns = jnp.zeros(1)
            terminals = jnp.zeros(1)
            for k in range(n_step):
                actions = jnp.eye(action_dim).repeat(obs.shape[0], axis=0)
                obs = jnp.tile(obs, (action_dim, 1))
                obs_actions = jnp.concatenate([obs, actions], axis=1)

                sample, logvar = ProbabilisticEnsemble.forward(model, model_state, obs_actions, inputs_mu, inputs_sigma, normalize_inputs=normalize_inputs, deterministic=True, return_dist=True, key=key)
                # sample = jnp.sign(sample) * (jnp.exp(jnp.abs(sample)) - 1)
                #key, subkey = jax.random.split(key)
                #el = jax.random.choice(subkey, elites, shape=(sample.shape[0],), replace=True)
                sample = sample[elites]
                logvar = logvar[elites]

                vars = jnp.exp(logvar)
                mean_ensemble = sample.mean(axis=0)
                var_ensemble = (sample**2 + vars).mean(axis=0) - mean_ensemble**2
                std_ensemble = jnp.sqrt(var_ensemble + 1e-12)
                model_uncertainties = std_ensemble.sum(-1).reshape(-1, 1)

                sample_mean, sample_std = sample.mean(axis=0), sample.std(axis=0)
                rewards, next_obs = sample_mean[:, : rew_dim] - pessimism*model_uncertainties, sample_mean[:, rew_dim :]
                next_obs += obs

                if env_id == "minecart-v0":
                    dones = termination_fn_minecart(obs, actions, next_obs).squeeze(1)
                else:
                    dones = jnp.zeros(action_dim)
                returns = jnp.tile(returns, (action_dim, 1)).flatten()
                terminals = jnp.tile(terminals, (action_dim, 1)).flatten()
                returns += gamma**k * (rewards * w).sum(axis=1) * (1 - terminals)
                terminals = (terminals + dones).clip(0, 1)
                obs = next_obs
    
            next_actions, q_values, key = USFA.batch_gpi(psi, psi_state, obs, w, 0.0, M, key, return_q_values=True)
            returns += gamma**n_step * q_values * (1 - terminals)
            trajectory_ind = returns.argmax(axis=0)
            best_action = trajectory_ind % action_dim

            return best_action, key
        
        else:  # Use MPC with random shooting [https://arxiv.org/pdf/1708.02596.pdf]
            n_samples = 10000
            obs = obs.repeat(n_samples, axis=0)
            key, subkey = jax.random.split(key)
            init_actions = jax.nn.one_hot(jax.random.randint(subkey, (n_samples,), minval=0, maxval=action_dim), action_dim)
            returns = jnp.zeros(n_samples)
            for k in range(n_step):
                if k == 0:
                    actions = init_actions
                else:
                    key, subkey = jax.random.split(key)
                    actions = jax.nn.one_hot(jax.random.randint(subkey, (n_samples,), minval=0, maxval=action_dim), action_dim)
                
                obs_actions = jnp.concatenate([obs, actions], axis=1)

                sample = ProbabilisticEnsemble.forward(model, model_state, obs_actions, inputs_mu, inputs_sigma, normalize_inputs=normalize_inputs, deterministic=True, return_dist=False, key=key)
                #key, subkey = jax.random.split(key)
                #el = jax.random.choice(subkey, elites, shape=(sample.shape[0],), replace=True)
                sample_mean, sample_std = sample.mean(axis=0), sample.std(axis=0)
                rewards, next_obs = sample_mean[:, : rew_dim] - pessimism*sample_std[:, : rew_dim], sample_mean[:, rew_dim :]               

                next_obs += obs
                if env_id == "minecart-v0":
                    dones = termination_fn_minecart(obs, actions, next_obs).squeeze(1)
                else:
                    dones = jnp.zeros(action_dim)
                
                returns += gamma**k * (rewards * w).sum(axis=1)
                obs = next_obs

            next_actions, q_values, key = USFA.batch_gpi(psi, psi_state, obs, w, 0.0, M, key, return_q_values=True)
            returns += gamma**n_step * q_values
            trajectory_ind = returns.argmax(axis=0)
            best_action = init_actions[trajectory_ind]
            best_action = best_action.argmax()
            return best_action, key

    @staticmethod
    @partial(jax.jit, static_argnames=["model", "normalize_inputs", "env_id", "n_step", "pessimism", "gamma"])
    def mpc_action(model, model_state, inputs_mu, inputs_sigma, normalize_inputs, elites, obs, w, env_id, n_step, pessimism, gamma, key):
        action_dim = model.input_dim - obs.shape[0]
        rew_dim = w.shape[0]
        obs = obs.reshape(1, -1)

        if n_step <= 5:  # Brute force all action sequences
            returns = jnp.zeros(1)
            for k in range(n_step):
                actions = jnp.eye(action_dim).repeat(obs.shape[0], axis=0)
                obs = jnp.tile(obs, (action_dim, 1))
                obs_actions = jnp.concatenate([obs, actions], axis=1)

                sample = ProbabilisticEnsemble.forward(model, model_state, obs_actions, inputs_mu, inputs_sigma, normalize_inputs=normalize_inputs, deterministic=True, return_dist=False, key=key)
                #key, subkey = jax.random.split(key)
                #el = jax.random.choice(subkey, elites, shape=(sample.shape[0],), replace=True)
                sample_mean, sample_std = sample.mean(axis=0), sample.std(axis=0)
                rewards, next_obs = sample_mean[:, : rew_dim] - pessimism*sample_std[:, : rew_dim], sample_mean[:, rew_dim :]

                next_obs += obs
                if env_id == "minecart-v0":
                    dones = termination_fn_minecart(obs, actions, next_obs).squeeze(1)
                else:
                    dones = jnp.zeros(action_dim)
                returns = jnp.tile(returns, (action_dim, 1)).flatten()
                returns += gamma**k * (rewards * w).sum(axis=1)
                obs = next_obs

            trajectory_ind = returns.argmax(axis=0)
            best_action = trajectory_ind % action_dim

            return best_action, key
        
        else:  # Use MPC with random shooting [https://arxiv.org/pdf/1708.02596.pdf]
            n_samples = 10000
            obs = obs.repeat(n_samples, axis=0)
            key, subkey = jax.random.split(key)
            init_actions = jax.nn.one_hot(jax.random.randint(subkey, (n_samples,), minval=0, maxval=action_dim), action_dim)
            returns = jnp.zeros(n_samples)
            for k in range(n_step):
                if k == 0:
                    actions = init_actions
                else:
                    key, subkey = jax.random.split(key)
                    actions = jax.nn.one_hot(jax.random.randint(subkey, (n_samples,), minval=0, maxval=action_dim), action_dim)
                
                obs_actions = jnp.concatenate([obs, actions], axis=1)

                sample = ProbabilisticEnsemble.forward(model, model_state, obs_actions, inputs_mu, inputs_sigma, normalize_inputs=normalize_inputs, deterministic=True, return_dist=False, key=key)
                #key, subkey = jax.random.split(key)
                #el = jax.random.choice(subkey, elites, shape=(sample.shape[0],), replace=True)
                sample_mean, sample_std = sample.mean(axis=0), sample.std(axis=0)
                rewards, next_obs = sample_mean[:, : rew_dim] - pessimism*sample_std[:, : rew_dim], sample_mean[:, rew_dim :]               

                next_obs += obs
                if env_id == "minecart-v0":
                    dones = termination_fn_minecart(obs, actions, next_obs).squeeze(1)
                else:
                    dones = jnp.zeros(action_dim)
                
                returns += gamma**k * (rewards * w).sum(axis=1)
                obs = next_obs
            
            trajectory_ind = returns.argmax(axis=0)
            best_action = init_actions[trajectory_ind]
            best_action = best_action.argmax()
            return best_action, key
        
    def cgpi_action(self, obs, w):
        if self.cgpi_layer is None:
            w_p = cp.Parameter(self.phi_dim)
            alpha = cp.Variable(len(self.M))
            W_ = np.vstack(self.M)
            W = cp.Parameter(W_.shape)
            V = cp.Parameter(len(self.M))
            objective = cp.Minimize(alpha @ V)
            constraints = [alpha @ W == w_p] #, alpha >= 0]
            problem = cp.Problem(objective, constraints)
            assert problem.is_dpp()
            self.cgpi_layer = CvxpyLayer(problem, parameters=[w_p, W, V], variables=[alpha])

        M = jnp.stack(self.M + [w])
        obs_m = obs.reshape(1,-1).repeat(M.shape[0], axis=0)
        psi_values = self.psi.apply(self.psi_state.params, obs_m, M, deterministic=True)
        psi_values = psi_values.mean(axis=0)
        q_values_w = (psi_values * w.reshape(1, 1, w.shape[0])).sum(axis=2)
        q_w, qs = q_values_w[-1], q_values_w[:-1]
        lower_bound = jnp.max(qs, axis=0)

        q_values = (psi_values * M.reshape(M.shape[0], 1, M.shape[1])).sum(axis=2)
        q_values_source = q_values[:-1]

        alphas = jnp.vstack(
            self.cgpi_layer(w.astype(jnp.float64), M[:-1].astype(jnp.float64), q_values_source.astype(jnp.float64)[:,a])
            for a in range(self.action_dim)
        ).T
        c_w = M[:-1] @ jnp.tile(self.min_phi, (self.action_dim, 1)).T
        upper_bound = jnp.maximum(q_values_source * alphas, c_w * alphas).sum(axis=0)

        c_qs = jnp.maximum(q_w, lower_bound)
        c_qs = jnp.minimum(c_qs, upper_bound)

        action = c_qs.argmax()
        return action

    def eval(self, obs: np.ndarray, w: np.ndarray) -> int:
        if type(obs) is gym.wrappers.frame_stack.LazyFrames:
            obs = np.array(obs)

        if self.include_w:
            self.M.append(w)

        if self.use_gpi:
            if self.gpi_type == "cgpi":
                action = self.cgpi_action(obs, w)
            elif self.gpi_type == "ngpi":
                action, self.key = USFA.nstep_gpi_action(self.psi, 
                                                         self.psi_state, 
                                                         self.dynamics.ensemble, 
                                                         self.dynamics.ensemble_state,
                                                         self.dynamics.inputs_mu,
                                                         self.dynamics.inputs_sigma,
                                                         self.dynamics.normalize_inputs,
                                                         self.dynamics.elites, 
                                                         obs, 
                                                         w, 
                                                         self.M,
                                                         self.env.spec.id, 
                                                         self.n_step, 
                                                         self.lcb_pessimism, 
                                                         self.gamma,
                                                         self.key)
            elif self.gpi_type == "uhgpi":
                action, self.key = USFA.uhgpi(self.psi, 
                                                         self.psi_state, 
                                                         self.dynamics.ensemble, 
                                                         self.dynamics.ensemble_state,
                                                         self.dynamics.inputs_mu,
                                                         self.dynamics.inputs_sigma,
                                                         self.dynamics.normalize_inputs,
                                                         self.dynamics.elites, 
                                                         obs, 
                                                         w, 
                                                         self.M,
                                                         self.env.spec.id, 
                                                         self.n_step, 
                                                         self.lcb_pessimism, 
                                                         self.gamma,
                                                         self.key)
            elif self.gpi_type == "mpc":
                action, self.key = USFA.mpc_action(self.dynamics.ensemble, 
                                                   self.dynamics.ensemble_state, 
                                                   self.dynamics.inputs_mu,
                                                   self.dynamics.inputs_sigma,
                                                   self.dynamics.normalize_inputs,
                                                   self.dynamics.elites, 
                                                   obs, 
                                                   w, 
                                                   self.env.spec.id, 
                                                   self.n_step, 
                                                   self.lcb_pessimism, 
                                                   self.gamma,
                                                   self.key)
            elif self.gpi_type == "mingpi":
                action, self.key = USFA.mingpi_action(self.psi, self.psi_state, obs, w, self.M, self.key)
            elif self.gpi_type == "ugpi":
                action, self.key = USFA.ugpi_action(self.psi, self.psi_state, obs, w, self.M, self.lcb_pessimism, self.key)
            elif self.gpi_type == "lcbgpi":
                action, self.key = USFA.lcbgpi_action(self.psi, self.psi_state, obs, w, self.M, self.lcb_pessimism, self.key)
            elif self.gpi_type == "oldugpi":
                action, policy_index, self.uncertainties, self.key = USFA.old_ugpi_action(self.psi, 
                                                    self.psi_state, 
                                                    self.dynamics.ensemble,
                                                    self.dynamics.ensemble_state,
                                                    self.dynamics.inputs_mu,
                                                    self.dynamics.inputs_sigma,
                                                    self.dynamics.normalize_inputs,
                                                    self.dynamics.elites,
                                                    obs, 
                                                    w, 
                                                    self.ugpi_temp,
                                                    self.M, 
                                                    self.env.spec.id,
                                                    self.gamma,
                                                    self.key,
                                                    return_policy_index=True)
                self.police_indices.append(policy_index)
            elif self.gpi_type == "gpi":
                action, policy_index, self.key = USFA.gpi_action(self.psi, self.psi_state, obs, w, self.M, self.key, return_policy_index=True)
                self.police_indices.append(policy_index)
        else:
            action, self.key = USFA.max_action(self.psi, self.psi_state, obs, w, self.key)

        if self.include_w:
            self.M.pop(-1)

        action = jax.device_get(action)            
        return action

    def act(self, obs, w) -> int:
        if np.random.random() < self.epsilon:
            return self.env.action_space.sample()
        else:
            if type(obs) is gym.wrappers.frame_stack.LazyFrames:
                obs = np.array(obs)
            if self.use_gpi:
                if self.ucb_exploration != 0.0:
                    action, policy_index, self.key = USFA.ugpi_action(self.psi, self.psi_state, obs, w, self.M, -self.ucb_exploration, self.key, return_policy_index=True)
                else:
                    action, policy_index, self.key = USFA.gpi_action(self.psi, self.psi_state, obs, w, self.M, self.key, return_policy_index=True)
                action, policy_index = jax.device_get(action), jax.device_get(policy_index)
                self.police_indices.append(policy_index)
            else:
                action, self.key = USFA.max_action(self.psi, self.psi_state, obs, w, self.key)
                action = jax.device_get(action)
            return action

    @staticmethod
    @partial(jax.jit, static_argnames=["psi"])
    def max_action(psi, psi_state, obs, w, key) -> int:
        # key, subkey = jax.random.split(key)
        psi_values = psi.apply(psi_state.params, obs, w, deterministic=True)
        q_values = (psi_values * w.reshape(1, w.shape[0])).sum(axis=3)
        q_values = q_values.mean(axis=0).squeeze(0)
        action = q_values.argmax()
        action = jax.device_get(action)
        return action, key

    """ @th.no_grad()
    def reset_priorities(self, w: th.Tensor):
        inds = np.arange(self.replay_buffer.size)
        priorities = np.repeat(0.1, self.replay_buffer.size)
        obs_s, actions_s, rewards_s, next_obs_s, dones_s, = self.replay_buffer.get_all_data(to_tensor=True, device=self.device)
        num_batches = int(np.ceil(obs_s.size(0) / 1000))
        for i in range(num_batches):
            b = i * 1000
            e = min((i + 1) * 1000, obs_s.size(0))
            obs, actions, rewards, next_obs, dones = obs_s[b:e], actions_s[b:e], rewards_s[b:e], next_obs_s[b:e], dones_s[b:e]
            psi = self.psi_nets[0](obs, w.repeat(obs.size(0), 1))
            psi_a = psi.gather(1, actions.long().reshape(-1, 1, 1).expand(psi.size(0), 1, psi.size(2))).squeeze(1)  # psi(s,a,w)

            if self.envelope or self.gper:
                max_next_psi, _ = self.envelope_target(next_obs, w.repeat(next_obs.size(0), 1), th.stack(self.GPI))
            else:
                psi_values = self.psi_nets[0](next_obs, w.repeat(next_obs.size(0), 1))
                max_psi = th.einsum("r,sar->sa", w, psi_values)
                max_acts = th.argmax(max_psi, dim=1)
                psi_targets = self.target_psi_nets[0](next_obs, w.repeat(next_obs.size(0), 1))
                psi_targets = psi_targets.gather(1, max_acts.long().reshape(-1, 1, 1).expand(psi_targets.size(0), 1, psi_targets.size(2)))
                max_next_psi = psi_targets.reshape(-1, self.phi_dim)

            gtderror = th.einsum("r,sr->s", w, (rewards + (1 - dones) * self.gamma * max_next_psi - psi_a)).abs()
            priorities[b:e] = gtderror.clamp(min=self.min_priority).pow(self.alpha).cpu().detach().numpy().flatten()

        self.replay_buffer.update_priorities(inds, priorities) """

    """ @th.no_grad()
    def envelope_target(self, obs: th.Tensor, w: th.Tensor, sampled_w: th.Tensor):
        # There must be a clearer way to write this without all the unsqueeze and expand
        W = sampled_w.unsqueeze(0).repeat(obs.size(0), 1, 1)
        next_obs = obs.unsqueeze(1).repeat(1, sampled_w.size(0), 1)

        next_psi_target = th.stack([target_net(next_obs, W).view(obs.size(0), sampled_w.size(0), self.action_dim, self.phi_dim) for target_net in self.target_psi_nets])
        
        #min_inds = th.argmin(q_values, dim=0)
        #min_inds = min_inds.reshape(1, psi_values.size(1), psi_values.size(2), 1).expand(1, psi_values.size(1), psi_values.size(2), psi_values.size(3))
        #psi_values = psi_values.gather(0, min_inds).squeeze(0)
        #max_q = th.einsum("sr,sar->sa", w, psi_values)
        #max_acts = th.argmax(max_q, dim=1)
        #psi_targets = psi_values.gather(1, max_acts.long().reshape(-1, 1, 1).expand(psi_values.size(0), 1, psi_values.size(2)))
        #target_psi = psi_targets.reshape(-1, self.phi_dim)

        q_values = th.einsum("sr,nspar->nspa", w, next_psi_target)
        min_inds = th.argmin(q_values, dim=0)
        min_inds = min_inds.reshape(1, next_psi_target.size(1), next_psi_target.size(2), next_psi_target.size(3), 1).expand(1, next_psi_target.size(1), next_psi_target.size(2), next_psi_target.size(3), next_psi_target.size(4))
        next_psi_target = next_psi_target.gather(0, min_inds).squeeze(0)

        q_values = th.einsum("sr,spar->spa", w, next_psi_target)
        max_q, ac = th.max(q_values, dim=2)
        pi = th.argmax(max_q, dim=1)

        max_next_psi = next_psi_target.gather(2, ac.unsqueeze(2).unsqueeze(3).expand(next_psi_target.size(0), next_psi_target.size(1), 1, next_psi_target.size(3))).squeeze(2)
        max_next_psi = max_next_psi.gather(1, pi.reshape(-1, 1, 1).expand(max_next_psi.size(0), 1, max_next_psi.size(2))).squeeze(1)
        return max_next_psi, next_psi_target

        W = sampled_w.unsqueeze(0).repeat(obs.size(0), 1, 1)
        next_obs = obs.unsqueeze(1).repeat(1, sampled_w.size(0), 1)

        next_psi_target = th.min(th.stack([target_net(next_obs, W).view(obs.size(0), sampled_w.size(0), self.action_dim, self.phi_dim) for target_net in self.target_psi_nets]), dim=0)[0]
        
        #next_psi = th.min(th.stack([net(next_obs, W).view(obs.size(0), sampled_w.size(0), self.action_dim, self.phi_dim) for net in self.psi_nets]), dim=0)[0]
        q_values = th.einsum("sr,spar->spa", w, next_psi_target)
        max_q, ac = th.max(q_values, dim=2)
        pi = th.argmax(max_q, dim=1)

        max_next_psi = next_psi_target.gather(2, ac.unsqueeze(2).unsqueeze(3).expand(next_psi_target.size(0), next_psi_target.size(1), 1, next_psi_target.size(3))).squeeze(2)
        max_next_psi = max_next_psi.gather(1, pi.reshape(-1, 1, 1).expand(max_next_psi.size(0), 1, max_next_psi.size(2))).squeeze(1)
        return max_next_psi, next_psi_target """

    def set_gpi_set(self, M: List[np.ndarray]):
        self.M = M.copy()

    def learn(
        self,
        total_timesteps: int,
        w: np.ndarray,
        M: List[np.ndarray],
        change_w_each_episode: bool = True,
        total_episodes: Optional[int] = None,
        reset_num_timesteps: bool = True,
        eval_env: Optional[gym.Env] = None,
        eval_freq: int = 1000,
        reset_learning_starts: bool = False,
    ):
        self.env.w = w
        self.M = M

        self.police_indices = []
        self.num_timesteps = 0 if reset_num_timesteps else self.num_timesteps
        self.num_episodes = 0 if reset_num_timesteps else self.num_episodes
        if reset_learning_starts:  # Resets epsilon-greedy exploration
            self.learning_starts = self.num_timesteps

        # TODO: check if reset priorities is good
        if self.per and len(self.replay_buffer) > 0:
            pass #self.reset_priorities(w)

        episode_reward = 0.0
        episode_vec_reward = np.zeros(w.shape[0])
        num_episodes = 0
        (obs, info), done = self.env.reset(), False
        for _ in range(1, total_timesteps + 1):
            if total_episodes is not None and num_episodes == total_episodes:
                break
            self.num_timesteps += 1

            if self.num_timesteps < self.learning_starts:
                action = self.env.action_space.sample()
            else:
                action = self.act(obs, w)

            next_obs, reward, terminated, truncated, info = self.env.step(action)
            done = terminated or truncated

            #transition = tuple(np.concatenate((obs, np.array([action]), next_obs)))
            #if transition not in self.visited:
            self.replay_buffer.add(obs, action, info["vector_reward"], next_obs, terminated)
            #    self.visited.add(transition)

            if self.num_timesteps >= self.learning_starts:
                if self.dyna:
                    if self.num_timesteps % self.dynamics_train_freq(self.num_timesteps) == 0:
                        m_obs, m_actions, m_rewards, m_next_obs, m_dones = self.replay_buffer.get_all_data(max_samples=int(2e5))
                        #m_obs, m_actions, m_rewards, m_next_obs, m_dones, idxes = self.replay_buffer.sample(batch_size=min(self.replay_buffer.size, 100000))
                        one_hot = np.zeros((len(m_obs), self.action_dim))
                        one_hot[np.arange(len(m_obs)), m_actions.astype(int).reshape((len(m_obs)))] = 1
                        X = np.hstack((m_obs, one_hot))
                        Y = np.hstack((m_rewards, m_next_obs - m_obs))
                        mean_loss, mean_holdout_loss = self.dynamics.fit(X, Y)
                        if self.log:
                            self.writer.add_scalar("dynamics/mean_loss", mean_loss, self.num_timesteps)
                            self.writer.add_scalar("dynamics/mean_holdout_loss", mean_holdout_loss, self.num_timesteps)
                        #print('numvisited', len(self.visited))

                    if self.num_timesteps >= self.dynamics_rollout_starts and self.num_timesteps % self.dynamics_rollout_freq == 0:
                        self.rollout_dynamics(w)

                self.train(w)

            if eval_env is not None and self.log and self.num_timesteps % eval_freq == 0:
                total_reward, discounted_return, total_vec_r, total_vec_return = eval_mo(self, eval_env, w)
                self.writer.add_scalar("eval/total_reward", total_reward, self.num_timesteps)
                self.writer.add_scalar("eval/discounted_return", discounted_return, self.num_timesteps)
                for i in range(episode_vec_reward.shape[0]):
                    self.writer.add_scalar(f"eval/total_reward_obj{i}", total_vec_r[i], self.num_timesteps)
                    self.writer.add_scalar(f"eval/return_obj{i}", total_vec_return[i], self.num_timesteps)
                if self.dyna and self.num_timesteps >= self.dynamics_rollout_starts:
                    plot = visualize_eval_jax(self, eval_env, self.dynamics, w, compound=False, horizon=1000)
                    wb.log({"dynamics/predictions": wb.Image(plot), "global_step": self.num_timesteps})
                    plot.close()

            episode_reward += reward
            episode_vec_reward += info["vector_reward"]
            if done:
                (obs, info), done = self.env.reset(), False
                num_episodes += 1
                self.num_episodes += 1

                if num_episodes % 100 == 0:
                    print(f"Episode: {self.num_episodes} Step: {self.num_timesteps}, Ep. Total Reward: {episode_reward}")
                if self.log:
                    wb.log({"metrics/policy_index": np.array(self.police_indices), "global_step": self.num_timesteps})
                    self.police_indices = []
                    self.writer.add_scalar("metrics/episode", self.num_episodes, self.num_timesteps)
                    self.writer.add_scalar("metrics/episode_reward", episode_reward, self.num_timesteps)
                    for i in range(episode_vec_reward.shape[0]):
                        self.writer.add_scalar(f"metrics/episode_reward_obj{i}", episode_vec_reward[i], self.num_timesteps)

                episode_reward = 0.0
                episode_vec_reward = np.zeros(w.shape[0])

                if change_w_each_episode:
                    w = random.choice(M)
                    self.env.w = w
            else:
                obs = next_obs

