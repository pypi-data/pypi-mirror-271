from typing import Tuple
import numpy as np
from .base import OptimizationSolver
from scipy.optimize import fmin_l_bfgs_b


class LBFGSBSolver(OptimizationSolver):
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
        func = lambda x: -sample_weight @ x + 0.5 * (x.T @ T) @ (T.T @ x)
        dfunc = lambda x: -sample_weight + (T @ (T.T @ x))
        
        bounds = [(0.0, 1.0/self.penalty) for i in range(n)]
        x0 = np.random.rand(n) * (1.0/self.penalty) # Aslında bir önceki betas başlangıç olarak verilebilir
        betas, objval, info = fmin_l_bfgs_b(func, x0=x0, fprime=dfunc, bounds=bounds, pgtol=1.0e-4)
        
        # print('Dual objective: ', -objval)

        return betas

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
