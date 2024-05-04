from typing import Optional, Type, Union

import torch

from tensordict import TensorDict

from rl4co.envs import RL4COEnvBase, get_env
from rl4co.models.common import NonAutoregressiveDecoder
from rl4co.models.zoo.deepaco.antsystem import AntSystem
from rl4co.utils.utils import merge_with_defaults


class DeepACODecoder(NonAutoregressiveDecoder):
    """Decoder utilizing Ant Colony Optimization (ACO) for constructing solutions for combinatorial optimization problems.
    This decoder extends the functionality of NonAutoregressiveDecoder by incorporating ACO algorithms.

    Args:
        env_name: Environment name to solve.
        aco_class: Class representing the ACO algorithm to be used. Defaults to :class:`AntSystem`.
        n_ants: Number of ants to be used in the ACO algorithm. Can be an integer or dictionary. Defaults to 20.
        n_iterations: Number of iterations to run the ACO algorithm. Can be an integer or dictionary. Defaults to `dict(train=1, val=20, test=100)`.
        **aco_args: Additional arguments to be passed to the ACO algorithm.
    """

    def __init__(
        self,
        env_name: str = "tsp",
        aco_class: Optional[Type[AntSystem]] = None,
        n_ants: Optional[Union[int, dict]] = None,
        n_iterations: Optional[Union[int, dict]] = None,
        **aco_args,
    ):
        super(DeepACODecoder, self).__init__()
        self.env_name = env_name
        self.aco_class = AntSystem if aco_class is None else aco_class
        self.aco_args = aco_args
        self.n_ants = merge_with_defaults(n_ants, train=20, val=20, test=20)
        self.n_iterations = merge_with_defaults(n_iterations, train=1, val=20, test=100)

    def forward(
        self,
        td_initial: TensorDict,
        heatmaps_logits: torch.Tensor,  # type: ignore
        env: Union[str, RL4COEnvBase, None] = None,
        calc_reward: bool = True,
        phase: str = "train",
        **kwargs,
    ):
        if phase == "train":
            # use the procedure inherited from NonAutoregressiveDecoder for training
            return super().forward(
                td_initial,
                heatmaps_logits,
                env,
                decode_type="multistart_sampling",
                calc_reward=calc_reward,
                phase=phase,
                num_starts=self.n_ants[phase],
                **kwargs,
            )

        # Instantiate environment if needed
        if env is None or isinstance(env, str):
            env_name = self.env_name if env is None else env
            env = get_env(env_name)

        aco = self.aco_class(heatmaps_logits, n_ants=self.n_ants[phase], **self.aco_args)
        td, actions, reward = aco.run(td_initial, env, self.n_iterations[phase])

        if calc_reward:
            td.set("reward", reward)

        return None, actions, td
