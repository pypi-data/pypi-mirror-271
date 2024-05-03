from typing import Any, Optional
from sklearn.metrics import f1_score, accuracy_score
import logging

logger = logging.getLogger("ruleopt")

def get_params(RUG: Any, log: bool = True) -> Any:
    """
    Retrieve parameters from a given object.
    
    Args:
        RUG (Any): Object to retrieve parameters from.
        log (bool, optional): Whether to log the operation. Defaults to True.
        
    Returns:
        Any: The parameters of the object, or "failed" if an error occurred.
    """
    try:
        params = RUG.get_params()
        if log:
            logger.info(f"Params: {params}")
        return params
    except Exception as e:
        if log:
            logger.critical(f"Params retrieval failed with exception: {str(e)}")
        return "failed"

def get_accuracy_score(pred: Any, true: Any, log: Optional[str] = None) -> Any:
    """
    Calculate the accuracy score of predictions.
    
    Args:
        pred (Any): The predicted values.
        true (Any): The true values.
        log (str, optional): Optional log message. Defaults to None.
        
    Returns:
        Any: The accuracy score, or "failed" if an error occurred.
    """
    try:
        score = accuracy_score(pred, true)
        if log:
            logger.info(f"{log} accuracy score: {score:.3f}")
        return score
    except Exception as e:
        if log:
            logger.critical(f"{log} accuracy score calculation failed with exception: {str(e)}")
        return "failed"

def get_f1_score(pred: Any, true: Any, log: bool = False) -> Any:
    """
    Calculate the F1 score of predictions.
    
    Args:
        pred (Any): The predicted values.
        true (Any): The true values.
        log (bool, optional): Whether to log the operation. Defaults to False.
        
    Returns:
        Any: The F1 score, or "failed" if an error occurred.
    """
    try:
        if true.nunique() > 2:
            score = f1_score(pred, true, average="weighted")
        else:
            score = f1_score(pred, true)
        if log:
            logger.info(f"{log} F1 score: {score:.3f}")
        return score
    except Exception as e:
        if log:
            logger.critical(f"{log} F1 score calculation failed with exception: {str(e)}")
        return "failed"

def get_n_rules(RUG: Any, log: bool = True) -> Any:
    """
    Retrieve the number of rules from a given object.
    
    Args:
        RUG (Any): Object to retrieve the number of rules from.
        log (bool, optional): Whether to log the operation. Defaults to True.
        
    Returns:
        Any: The number of rules, or "failed" if an error occurred.
    """
    try:
        num_rules = RUG.get_num_of_rules()
        if log:
            logger.info(f"Number of rules: {num_rules}")
        return num_rules
    except Exception as e:
        if log:
            logger.critical(f"Number of rules retrieval failed with exception: {str(e)}")
        return "failed"

def get_n_missed(RUG: Any, log: bool = True) -> Any:
    """
    Retrieve the number of missed instances from a given object.
    
    Args:
        RUG (Any): Object to retrieve the number of missed instances from.
        log (bool, optional): Whether to log the operation. Defaults to True.
        
    Returns:
        Any: The number of missed instances, or "failed" if an error occurred.
    """
    try:
        num_missed = RUG.get_num_of_missed()
        if log:
            logger.info(f"Number of missed: {num_missed}")
        return num_missed
    except Exception as e:
        if log:
            logger.critical(f"Number of missed retrieval failed with exception: {str(e)}")
        return "failed"
