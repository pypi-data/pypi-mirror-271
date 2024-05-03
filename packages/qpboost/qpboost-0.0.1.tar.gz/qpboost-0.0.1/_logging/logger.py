from typing import Any
from .utils import *
from .timer import Timer
from .logging_config import setup_logging
import json
import datetime
import pandas as pd
import logging

from ruleopt import Explainer

logger = logging.getLogger("ruleopt")

setup_logging()

class Logger:
    """
    A Logger class that logs information related to a model, its parameters, and performance metrics.
    
    Attributes:
        log_file (str): Path to the log file.
        
    Args:
        log_file (str, optional): Path to the log file. Defaults to "logger.json".
    """
    def __init__(self, log_file: str = "logger.json") -> None:
        self.log_file = log_file
       
    def __call__(self, RUG: Any, X_train: Any, X_test: Any, 
                 y_train: Any, y_test: Any, info: str) -> None:
        """
        Logs the parameters and performance metrics of a model.
        
        Args:
            RUG (Any): The model.
            X_train (Any): The training data.
            X_test (Any): The test data.
            y_train (Any): The training labels.
            y_test (Any): The test labels.
            info (str): Additional information to be logged.
        """
        try:
            with open(self.log_file, "r", encoding='utf8') as log_file:
                log_data = json.load(log_file)
                logger.warning(f"Logs will be appended to {self.log_file} file.")
        except:
            log_data = dict()
            logger.warning(f"{self.log_file} file not found. A new one will be created.")

        with Timer(log = "Fitting") as fit_time:
            RUG.fit(X_train, y_train)
            
        with Timer(log = "Train data's predicting") as train_predict_time:
            train_pred = RUG.predict(X_train)
        
        with Timer(log = "Test data's predicting") as test_predict_time:
            test_pred = RUG.predict(X_test)
            
        exp = Explainer(RUG)
        rule_metrics = exp.summarize_rule_metrics(info=False)
        rule_details = exp.retrieve_rule_details(info=False)

        output = dict(info = info,
                      #params = get_params(RUG),
                      fit_duration = fit_time.total_time,
                      train_predict_duration = train_predict_time.total_time,
                      test_predict_duration = test_predict_time.total_time,
                      train_accuracy = get_accuracy_score(train_pred, y_train, log="Train"),
                      test_accuracy = get_accuracy_score(test_pred, y_test, log="Test"),
                      train_f1 = get_f1_score(train_pred, y_train, log="Train"),
                      test_f1 = get_f1_score(test_pred, y_test, log="Test"),
                      num_of_rules = rule_metrics.get("num_of_rules"),
                      avg_rule_length  = rule_metrics.get("avg_rule_length"),
                      rule_details = rule_details,
                      )
        
        logger.info(f"Number of rules: {rule_metrics.get('num_of_rules')}")
        logger.info(f"Average rule lenght: {rule_metrics.get('avg_rule_length'):.2f}")
        
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        log_data.update({current_time: output})
        
        with open(self.log_file, "w", encoding='utf8') as log_file:
            json.dump(log_data, log_file, indent=4, ensure_ascii=False)

    @staticmethod
    def as_table(log_file: str = "logger.json") -> pd.DataFrame:
        """
        Converts the log data in the specified file to a pandas DataFrame.
        
        Args:
            log_file (str, optional): Path to the log file. Defaults to "logger.json".
            
        Returns:
            pd.DataFrame: The log data as a pandas DataFrame.
        """
        return pd.read_json(log_file, orient="index")
