from typing import Tuple
import numpy as np
from gurobipy import Model, GRB
from .base import OptimizationSolver


class GurobiSolver(OptimizationSolver):
    """
    A solver wrapper class for linear optimization using the Gurobi solver.

    The solver supports both dense and sparse matrix representations.
    """

    def __init__(
        self,
        penalty: float = 1.0,
    ) -> None:
        """
        Parameters
        ----------
        penalty : float, default=1.0
            Penalty parameter for the cost in the objective function.

        use_sparse : bool, default=False
            Determines whether to use a sparse matrix representation for the optimization
            problem. Using sparse matrices can significantly reduce memory usage and improve
            performance for large-scale problems with many zeros in the data.
        """
        self.penalty = penalty
        super().__init__()

    def _solve_dual(self, T, sample_weight, n):
        dual_model = Model("QP Dual")
        dual_model.setParam("OutputFlag", False)
        betas = dual_model.addMVar(
            shape=int(n), name="betas", ub=(1.0 / self.penalty) * np.ones(n)
        )

        dual_model.setObjective(
            sample_weight @ betas - (0.5 * (betas.T @ T) @ (T.T @ betas)), GRB.MAXIMIZE
        )

        dual_model.optimize()
        
        # print('Dual objective: ', dual_model.ObjVal)

        return betas.X

    def _solve_primal(self, T, sample_weight, m, n):
        primal_model = Model("QP Primal")
        primal_model.setParam("OutputFlag", False)
        vs = primal_model.addMVar(shape=int(n), name="vs")
        ws = primal_model.addMVar(shape=int(m), name="ws", lb=-GRB.INFINITY)
        primal_model.addConstr(T @ ws + vs >= 1.0, name="T Constraints")
        primal_model.setObjective(
            (0.5 * self.penalty * ws.T) @ ws + sample_weight @ vs,
            GRB.MINIMIZE,
        )
        primal_model.optimize()

        return ws.X

    def __call__(
        self,
        T: np.ndarray,
        sample_weight: np.ndarray,
        primal = False,
        *args,
        **kwargs,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Parameters
        ----------
        coefficients : object
            An object containing the sparse matrix coefficients ('yvals', 'rows', 'cols'),
            and costs associated with each rule ('costs').
        k : float
            A scaling factor for the coefficients.
        ws0 : array-like, optional
            Initial weights for the optimization process. If provided, should have the same
            length as the number of rules. Otherwise, weights are initialized to ones.

        Returns
        -------
        ws : numpy.ndarray
            The optimized weights for each rule after the optimization process.
        betas : numpy.ndarray
            The betas values indicating constraint violations for the optimized solution.
        """
        n, m = T.shape

        if primal:
            return self._solve_primal(T, sample_weight, m, n) #ws
        else:
            return self._solve_dual(T, sample_weight, n) #betas
