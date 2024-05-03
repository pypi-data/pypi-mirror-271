from __future__ import annotations
import warnings
from typing import Union, Dict

import numpy as np
from numpy.typing import ArrayLike
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.class_weight import compute_sample_weight

from ..utils import check_inputs, check_sample_weight
from ..solver.base import OptimizationSolver


class _QPBASE(BaseEstimator, ClassifierMixin):
    """
    The foundational class for all estimators in the ruleopt library. `_RUGBASE` provides
    the core framework that every model in ruleopt builds upon.

    Parameters
    ----------
    solver : OptimizationSolver
        An instance of a derived class inherits from the 'Optimization Solver' base class.
        The solver is responsible for optimizing the rule set based on the cost function
        and constraints.

    rule_cost : RuleCost or int
        Defines the cost of rules, either as a specific calculation method (RuleCost instance)
        or a fixed cost

    class_weight: dict, "balanced" or None
        A dictionary mapping class labels to their respective weights, the string "balanced"
        to automatically adjust weights inversely proportional to class frequencies,
        or None for no weights. Used to adjust the model in favor of certain classes.

    threshold : float
        The minimum weight threshold for including a rule in the final model

    random_state : int or None, default=None
        Seed for the random number generator to ensure reproducible results.
    """

    def __init__(
        self,
        solver: OptimizationSolver,
        class_weight: Dict[int, float],
        random_state: Union[None, int],
    ):

        self._validate_qpboost_parameters(
            random_state=random_state,
            solver=solver,
            class_weight=class_weight,
        )
        self.solver = solver
        self.random_state = random_state
        self.class_weight = class_weight

        # Additional initializations
        self._rng = np.random.default_rng(
            random_state if random_state is not None else None
        )
        self.decision_trees_ = []

        self._is_fitted: bool = False
        self.k_: float = None
        self.classes_: np.array = None

    def _cleanup(self) -> None:
        """
        Clean up the model by resetting all of its attributes.
        """
        # Resetting all dictionaries
        self.decision_trees_ = []

        # Resetting the random number generator
        self._rng = np.random.default_rng(self.random_state)

    def _get_class_infos(self, y: np.ndarray) -> None:
        """
        Computes and stores information about the classes in the dataset.

        This method calculates the majority class, its probability, the total number
        of unique classes, and stores an array of unique class labels.

        Parameters
        ----------
        y : np.ndarray
            The target values, expected to be a 1D numpy array of class labels.

        Sets Attributes
        ---------------
        majority_class_ : int
            The class label with the highest frequency in `y`.
        majority_probability_ : float
            The proportion of samples in `y` belonging to the majority class,
            calculated as the count of the majority class divided by the total number of samples.
        k_ : float
            The total number of unique classes in `y`.
        classes_ : np.array
            An array of the unique class labels present in the dataset.
        """
        classes, _ = np.unique(y, return_counts=True)
        self.k_ = classes.shape[0]
        self.classes_ = classes

    def _preprocess(self, y: np.ndarray) -> np.ndarray:
        """
        Transforms the target values into a vector. If the target
        class is k and there are K classes, then all components but
        the kth are set to -1/(K-1) and the kth component is set to 1.

        Parameters
        ----------
        y : np.ndarray
            The target values as a 1D numpy array of class labels.

        Returns
        -------
        np.ndarray
            The preprocessed target values in a one-hot-encoded format, adjusted for the model's
            optimization process.
        """

        # Convert the labels into kth unit vector
        vec_y = np.eye(self.k_)[y]

        # Replace 0s with -1/(K-1)
        vec_y[vec_y == 0] = -1 / (self.k_ - 1)

        return vec_y

    def _predict_base(self, x: np.ndarray) -> np.ndarray:
        """
        Calculates the base class weights for each instance based on selected rules.
        Optionally returns additional prediction info.

        Parameters
        ----------
        x : np.ndarray
            The feature matrix for the instances to predict.

        Returns
        -------
        np.ndarray
            An array of raw class weights for each instance, used as the basis for final
            prediction.
            If predict_info is True, also returns arrays containing indices of samples
            with missed values, number of rules applied per sample, and average rule
            length per sample.
        """
        if not self._is_fitted:
            raise ValueError("You need to fit the RUG model first")

        sum_class_weights_arr = np.zeros(shape=(x.shape[0], self.k_), dtype=np.float32)
        indexs = np.arange(x.shape[0])

        for fit_tree, ws in zip(self.decision_trees_, self.ws):
            preds = fit_tree.predict(x).astype(np.int8)
            sum_class_weights_arr[indexs, preds] += ws

        return sum_class_weights_arr

    def predict(self, x: ArrayLike) -> np.ndarray:
        """
        Predicts class labels for the given data, optionally returning
        additional prediction info.

        Parameters
        ----------
        x : array-like of shape (n_samples, n_features)
            The training input samples. Internally, it will be converted to dtype=np.float32.

        Returns
        -------
        np.ndarray
            An array of predicted class labels for each instance in `x`.
            If predict_info is True, also returns arrays containing indices
            of samples with missed values, number of rules applied per sample,
            and average rule length per sample.
        """
        x = check_inputs(x)

        sum_class_weights_arr = self._predict_base(x)
        predictions = np.argmax(sum_class_weights_arr, axis=1)

        return predictions

    def predict_proba(self, x: ArrayLike):
        """
        Predicts class probabilities for the given data, optionally
        returning additional prediction info.

        Parameters
        ----------
        x : array-like of shape (n_samples, n_features)
            The training input samples. Internally, it will be converted to dtype=np.float32.

        Returns
        -------
        np.ndarray
            An array where each row corresponds to a sample in `x` and each column
            to a class, containing the probability of each class for each sample.
            If predict_info is True, also returns arrays containing indices of samples
            with missed values, number of rules applied per sample, and average rule
            length per sample.
        """
        x = check_inputs(x)

        sum_class_weights_arr = self._predict_base(x)

        total_weights = np.sum(sum_class_weights_arr, axis=1)
        predictions = np.divide(sum_class_weights_arr, total_weights.reshape(-1, 1))

        return predictions

    def _get_sample_weight(self, sample_weight, y):
        """
        Calculates the final sample weights based on initial sample weights, class weights and
        target values.

        Parameters
        ----------
        sample_weight : array-like, shape (n_samples,) or None
            Initial weights of samples. If None, all samples are assumed to have weight one.
        class_weight : dict, "balanced" or None
            Weights associated with classes in the form {class_label: weight}. Can be "balanced"
            to automatically adjust weights inversely proportional to class frequencies in the input data
            or None for equal weights.
        y : array-like, shape (n_samples,)
            Array of target values (class labels).

        Returns
        -------
        final_sample_weights : array-like, shape (n_samples,) or None
            The computed array of weights for each sample in the dataset. Returns None if all computed
            weights are equal to one, indicating no weighting is necessary.
        """
        final_sample_weights = np.ones_like(y, dtype=np.float32)

        if sample_weight is not None:
            sample_weight = check_sample_weight(sample_weight)
            if sample_weight.shape != y.shape or sample_weight.min() < 0:
                raise ValueError(
                    "sample_weight must be a non-negative numpy array of the same shape as y."
                )

            final_sample_weights *= sample_weight

        if self.class_weight is not None:
            if isinstance(self.class_weight, dict):
                if len(self.class_weight.keys()) != np.unique(y).size:
                    raise ValueError(
                        "The class_weight dictionary must have a key for each unique value in y."
                    )

            final_sample_weights *= compute_sample_weight(self.class_weight, y)

        return final_sample_weights

    def _validate_qpboost_parameters(
        self,
        solver: OptimizationSolver,
        class_weight: Dict[int:float],
        random_state: int | None,
    ):

        if not isinstance(solver, (OptimizationSolver)):
            raise TypeError("solver should be inherited from OptimizationSolver.")

        if not (isinstance(random_state, int) or random_state is None):
            raise TypeError("random_state must be an integer or None.")

        # class_weight check
        if not isinstance(class_weight, (dict, str, type(None))) or (
            (type(class_weight) == str) and (class_weight != "balanced")
        ):
            raise ValueError("class_weight must be a dictionary, 'balanced', or None.")

        if isinstance(class_weight, dict):
            if not all(isinstance(k, int) for k in class_weight.keys()):
                raise ValueError("class_weight keys must be integer.")
            if not all(isinstance(v, (int, float)) for v in class_weight.values()):
                raise ValueError("class_weight values must be integer or float.")
            if any(v < 0 for v in class_weight.values()):
                raise ValueError("class_weight values must be non-negative.")

    @property
    def is_fitted(self):
        """
        Indicates whether the model is fitted.

        Returns
        -------
        bool
            True if the model is fitted, False otherwise.
        """

        return self._is_fitted

    @property
    def decision_trees(self):
        """
        Returns dictionary that stores the decision tree models.

        Returns
        -------
        Dict[int, Any]
            A dictionary containing decision tree models, with identifiers as keys
            and decision
            tree instances as values.
        """
        return self.decision_trees_

    @property
    def k(self):
        """
        Returns the total number of unique classes in the dataset.

        Returns
        -------
        float
            The total number of unique classes.
        """

        return self.k_

    @property
    def classes(self):
        """
        Returns unique class labels in the dataset.

        Returns
        -------
        np.ndarray
            An array containing the unique class labels of the dataset.
        """

        return self.classes_
