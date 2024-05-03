from abc import ABC, abstractmethod
from typing import Any

class OptimizationSolver(ABC):
    """
    This abstract base class defines the interface for a generic solver.
    Implementations of this class must provide the `__call__` method,
    allowing the solver to be invoked as if it were a function.
    """

    def __init__(self) -> None:
        super().__init__()
        self.penalty: float | int
        self._check_params()

    @abstractmethod
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        """
        Executes the solver using the provided arguments and keyword arguments.

        Parameters:
            *args (Any): Positional arguments required for solving the problem.
            **kwds (Any): Keyword arguments required for solving the problem.

        Returns:
            Any: The result of the solving process.
        """
        pass

    def _check_params(self):
        if not hasattr(self, "penalty"):
            raise AttributeError("Subclasses must define 'penalty'")

        if not isinstance(self.penalty, (float, int)) or self.penalty <= 0:
            raise TypeError("penalty must be a positive float.")
