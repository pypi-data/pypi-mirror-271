from time import perf_counter
from typing import Optional
import logging

# Set up a logger
logger = logging.getLogger("ruleopt")
logger.setLevel(logging.INFO)

class Timer:
    """
    A Timer class that can be used as a context manager to measure the 
    execution time of a block of code. Optionally logs the start and end times
    and the total execution time.
    
    Attributes:
        log (str): An optional message to be logged at the start and end of the timed block.
        start_time (float): The time at which the Timer was started, in seconds.
        total_time (float): The total time that has passed between the start and end of the Timer, in seconds.
    
    Args:
        log (str, optional): An optional message to be logged at the start and end of the timed block.
    """
    def __init__(self, log: Optional[str] = None) -> None:
        self.log = log
        self.start_time: float = 0.0
        self.total_time: float = 0.0

    def __enter__(self) -> 'Timer':
        """
        Starts the timer and logs the start message, if provided.
        
        Returns:
            The Timer instance.
        """
        self.start_time = perf_counter()
        if self.log:
            logger.info(f"{self.log} started.")
        return self
        
    def __exit__(self, type: Optional[Exception], value: Optional[Exception], traceback: Optional[Exception]) -> None:
        """
        Stops the timer, calculates the total time elapsed, and logs the end message and total time, if a log message was provided.
        
        Args:
            type (Exception, optional): The type of exception that caused the context to be exited, if any.
            value (Exception, optional): The instance of the exception that caused the context to be exited, if any.
            traceback (Exception, optional): A traceback from the exception, if any.
        """
        self.exit = perf_counter()
        self.total_time = self.exit - self.start_time
        if self.log:
            logger.info(f"{self.log} finished. Total time: {self.total_time:.3f} seconds.")
