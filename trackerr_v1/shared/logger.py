#!/usr/bin/python3
import logging
from pathlib import Path

def setUp_logger(module, pathToFile):
    logger = logging.getLogger(module)
    BASEDIR = Path(__file__).resolve().parent
    path = BASEDIR / 'logs' / pathToFile
    
    file_handler = logging.FileHandler(path)
    
    # Define a custom date format for the log messages
    formatter = logging.Formatter('%(name)s : %(filename)s :%(module)s : %(funcName)s: %(lineno)s: :%(levelname)s %(levelno)s: %(message)s : %(asctime)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    
    # Set the formatter for the file handler
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    # Set the logging level to INFO (or your preferred level)
    logger.setLevel(logging.INFO)
    
    return logger
