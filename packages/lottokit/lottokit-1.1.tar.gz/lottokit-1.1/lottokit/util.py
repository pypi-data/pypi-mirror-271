#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : nickdecodes
@Email   : nickdecodes@163.com
@Usage   :
@FileName: util.py
@DateTime: 2023/8/23 23:13
@SoftWare: 
"""

import re
import sys
import csv
import math
import time
import json
import datetime
import logging
import logging.handlers
from abc import ABC, abstractmethod
from typing import Iterable, List, Tuple, Any, Optional, Union, Set, Dict
import random
import numpy as np
import pandas as pd
from pmdarima import auto_arima
from selenium import webdriver
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import RandomizedSearchCV
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class IOUtil:
    @classmethod
    def get_logger(
            cls,
            log_file: str = None
    ) -> logging.Logger:
        # Choose a unique logger name based on the log_file argument
        logger_name = log_file if log_file is not None else 'default_logger'
        # Get the logger instance by name
        logger = logging.getLogger(logger_name)

        # Check if the logger already has handlers to prevent adding them again
        if not logger.handlers:
            if log_file is None:
                # Configuration for logging to the terminal
                # log_format = '%(asctime)s [%(levelname)s] <%(lineno)d> %(funcName)s: %(message)s'
                log_format = '%(message)s'
                handler = logging.StreamHandler(sys.stdout)
            else:
                # Configuration for logging to a file with rotation at midnight
                log_format = ('%(asctime)s [%(levelname)s] %(process)d %(thread)d '
                              '%(filename)s <%(lineno)d> %(funcName)s: %(message)s')
                handler = logging.handlers.TimedRotatingFileHandler(log_file, when='midnight', backupCount=7)

            # Set the formatter for the handler
            formatter = logging.Formatter(log_format)
            handler.setFormatter(formatter)

            # Optionally set a different log level for the handler
            handler.setLevel(logging.INFO)

            # Add the handler to the logger
            logger.addHandler(handler)
            # Set the log level for the logger
            logger.setLevel(logging.INFO)

        # Return the configured logger
        return logger

    @classmethod
    def list_to_int(
            cls,
            numbers: List[int],
            zero_replacement: str = '',
            **kwargs: Any
    ) -> int:
        """
        Convert a list of integers to a single integer, with an optional replacement for zeros.

        :param numbers: list of integers
        :param zero_replacement: string to replace zeros with, defaults to an empty string
        :return: single integer formed by concatenating the list elements
        """
        # Validate input data is a list
        if not isinstance(numbers, List):
            raise ValueError("Input 'numbers' must be a list.")

        # Validate all elements in the list are integers
        if not all(isinstance(x, int) for x in numbers):
            raise ValueError("All elements in the 'numbers' list must be integers.")

        # Convert list elements to strings, replacing zeros with zero_replacement
        parts = [zero_replacement if x == 0 else str(x) for x in numbers]

        # Join the parts and convert to an integer
        return int(''.join(parts))

    @classmethod
    def int_to_list(
            cls,
            number: int,
            modulus: int = 10,
            **kwargs: Any
    ) -> List[int]:
        """
        Convert an integer to a list of digits, each digit is the remainder of division by a modulus.

        :param number: The integer to be converted into a list of digits.
        :param modulus: The divisor used for the modulo operation on each digit, defaults to 10.
        :return: A list of integers, where each integer is a digit of the original number after the modulo operation.
        """
        # Validate input data is an integer
        if not isinstance(number, int):
            raise ValueError("Input 'number' must be an integer.")

        # Validate modulus is a positive integer
        if not isinstance(modulus, int) or modulus <= 0:
            raise ValueError("Input 'modulus' must be a positive integer.")

        # Convert the integer to a list of digits using the modulus
        digit_list = [int(d) % modulus for d in str(abs(number))]

        # Return the list of digits
        return digit_list

    @classmethod
    def write_data_to_file(
            cls,
            file_path: str,
            data: List[str],
            app_log: Optional[logging.Logger] = None,
            mode: str = 'a+',
            **kwargs: Any
    ) -> bool:
        """
        Write data to a file.

        :param file_path: Path to the file where data will be written.
        :param data: List of data to write to the file.
        :param app_log: Optional logger for logging information, defaults to None.
        :param mode: Mode in which the file should be opened, defaults to 'a+' for append.
        :return: bool weather success or failed
        """
        if app_log is None:
            app_log = cls.get_logger()

        if not data:
            app_log.warning("No data provided to write to the file.")
            return False

        try:
            with open(file_path, mode) as fp:
                app_log.info(f'Writing to file: {fp.name}')
                for line in data:
                    if line is not None:
                        fp.write(f'{line}\n')
        except Exception as ex:
            app_log.exception(f"An error occurred while writing to the file: {ex}")
            return False

        return True

    @classmethod
    def read_data_from_file(
            cls,
            file_path: str,
            app_log: Optional[logging.Logger] = None,
            mode: str = 'r'
    ) -> Optional[List[str]]:
        """
        Read data from a file and return a list of non-empty lines.

        :param file_path: Path to the file to be read.
        :param app_log: Optional logger for logging information, defaults to None.
        :param mode: Mode in which the file should be opened, defaults to 'r' for read only.
        :return: List of non-empty lines from the file or None if an exception occurs.
        """
        if app_log is None:
            app_log = cls.get_logger()

        data = []
        try:
            with open(file_path, mode) as fp:
                app_log.info(f'Opening file: {fp.name}')
                data = [line.strip() for line in fp if line.strip()]
        except Exception as ex:
            app_log.exception(f"An error occurred while reading the file: {ex}")
            return None

        app_log.info(f'Number of non-empty lines read: {len(data)}')
        return data

    @classmethod
    def write_csv_data_to_file(
            cls,
            file_path: str,
            data: List[List[Any]],
            app_log: Optional[logging.Logger] = None,
            mode: str = 'a+',
            newline: str = '',
            **kwargs: Any
    ) -> bool:
        """
        Write data to a CSV file.

        :param file_path: Path to the file where CSV data will be written.
        :param data: List of rows (where each row is a list) to write to the CSV file.
        :param app_log: Optional logger for logging information, defaults to None which will create a new logger.
        :param mode: Mode in which the file should be opened, defaults to 'a+' for append.
        :param newline: Controls how universal newlines works (it only applies to text mode). It defaults to ''.
        :return: bool weather success or failed
        """
        if app_log is None:
            app_log = cls.get_logger()

        if not data:
            app_log.warning("No data provided to write to the file.")
            return False

        try:
            with open(file_path, mode=mode, newline=newline) as fp:
                app_log.info(f'Writing to CSV file: {fp.name}')
                writer = csv.writer(fp, **kwargs)
                writer.writerows(data)
        except Exception as ex:
            app_log.exception(f"An error occurred while writing to the CSV file: {ex}")
            return False

        return True

    @classmethod
    def read_csv_data_from_file(
            cls,
            file_path: str,
            app_log: Optional[logging.Logger] = None,
            mode: str = 'r',
            **kwargs: Any
    ) -> Optional[List[List[str]]]:
        """
        Read CSV data from a file and return a list of rows.

        :param file_path: Path to the CSV file to be read.
        :param app_log: Optional logger for logging information, defaults to a new logger if None.
        :param mode: Mode in which the file should be opened, defaults to 'r' for read only.
        :return: List of rows from the CSV file or None if an exception occurs.
        """
        if app_log is None:
            app_log = cls.get_logger()

        try:
            with open(file_path, mode=mode, **kwargs) as fp:
                app_log.info(f'Reading CSV file: {fp.name}')
                reader = csv.reader(fp, **kwargs)
                data = [row for row in reader]
        except Exception as ex:
            app_log.exception(f"An error occurred while reading the CSV file: {ex}")
            return None

        return data

    @classmethod
    def write_json_data_to_file(
            cls,
            file_path: str,
            data: Any,
            app_log: Optional[logging.Logger] = None,
            mode: str = 'w',
            **kwargs: Any
    ) -> bool:
        """
        Write data to a JSON file.

        :param file_path: Name of the JSON file.
        :param data: Data to write (usually a dict or a list).
        :param app_log: Optional logger for logging information, defaults to a new logger if None.
        :param mode: Mode in which the file should be opened, defaults to 'w' for write (overwriting).
        :return: bool weather success or failed
        """
        if app_log is None:
            app_log = cls.get_logger()

        app_log.info(f'Writing to JSON file: {file_path}')
        try:
            with open(file_path, mode, encoding='utf-8') as fp:
                json.dump(data, fp, ensure_ascii=False, indent=4, **kwargs)
        except Exception as ex:
            app_log.exception(f"An error occurred while writing to the JSON file: {ex}")
            return False

        return True

    @classmethod
    def read_json_data_from_file(
            cls,
            file_path: str,
            app_log: Optional[logging.Logger] = None,
            mode: str = 'r',
            **kwargs: Any
    ) -> Optional[Any]:
        """
        Read data from a JSON file.

        :param file_path: Name of the JSON file.
        :param app_log: Optional logger for logging information, defaults to a new logger if None.
        :param mode: Mode in which the file should be opened, defaults to 'r' for read.
        :return: Data read from the JSON file or None if an exception occurs.
        """
        if app_log is None:
            app_log = cls.get_logger()

        try:
            with open(file_path, mode, encoding='utf-8', **kwargs) as fp:
                app_log.info(f'Reading from JSON file: {file_path}')
                return json.load(fp)
        except Exception as ex:
            app_log.exception(f"An error occurred while reading the JSON file: {ex}")
            return None


class ModelUtil:
    @staticmethod
    def exponential_moving_average_next_value(
            numeric_sequence: List[int],
            span: int = 5,
            enable_rolling_difference: bool = False
    ) -> int:
        """
        Calculate the Exponential Moving Average (EMA) and use rolling difference to predict the next value of a sequence.

        EMA is a type of moving average that places a greater weight and significance
        on the most recent data points. It's more responsive to new information compared
        to a simple moving average (SMA).

        :param numeric_sequence: A list or sequence of numbers for which the EMA is to be calculated.
        :param span: The number of periods over which to calculate the EMA. Default is 5.
        :param enable_rolling_difference: weather to enable rolling. default is False
        :return: Predicted next value of the sequence based on EMA and rolling difference.
        :raises ValueError: If the input list is empty or contains non-numeric values.
        """
        if not numeric_sequence:
            raise ValueError("The numeric sequence cannot be empty.")
        if not all(isinstance(x, (int, float)) for x in numeric_sequence):
            raise ValueError("All elements in the numeric sequence must be numbers.")

        # Convert the numeric sequence into a pandas Series object
        series = pd.Series(numeric_sequence)

        # Calculate the EMA using pandas' ewm method
        # Adjust 'min_periods' to handle shorter sequences gracefully
        ema = series.ewm(span=span, min_periods=min(span, len(numeric_sequence)), adjust=False).mean()

        # Calculate rolling difference
        rolling_difference = series.diff()

        # Predict the next value by extrapolating the last rolling difference and the last EMA value
        if len(rolling_difference) > 1 and enable_rolling_difference is True:
            predicted_next_value = ema.iloc[-1] + rolling_difference.iloc[-1]
        else:
            # If there's no enough data to calculate difference, use the last EMA as the prediction
            predicted_next_value = ema.iloc[-1]

        # Return the predicted next value rounded to the nearest integer
        return round(predicted_next_value)

    @staticmethod
    def linear_regression_next_value_by_index(numeric_sequence: List[int]) -> int:
        """
        Predicts the next value in a sequence using linear regression.

        Linear regression involves fitting a line to the data points in such a way
        that the distance between the data points and the line is minimized. This function
        uses the method to predict the next value in a given sequence of numbers by fitting
        a model to the sequence and examining the slope of the line.

        :param numeric_sequence: A list or sequence of numbers to model.
        :return: The predicted next value in the sequence as an integer.
        :raises ValueError: If the input sequence is empty or too short for regression analysis.
        """
        if not numeric_sequence:
            raise ValueError("The numeric sequence cannot be empty.")
        if len(numeric_sequence) < 2:
            raise ValueError("The numeric sequence must contain at least two elements for linear regression.")

        # Convert the numeric sequence into a numpy array and reshape for sklearn
        data = np.array(numeric_sequence).reshape(-1, 1)

        # Create an array representing time or the independent variable, reshaped as a column
        index = np.array(range(len(data))).reshape(-1, 1)

        # Create a LinearRegression model and fit it to the data
        model = LinearRegression()
        model.fit(index, data)

        # Predict the next value in the sequence using the fitted model
        prediction = model.predict([[len(data)]])[0][0]

        # Return the predicted value as an integer
        return round(prediction)

    @staticmethod
    def multivariate_polynomial_regression_next_value(
            numeric_sequence: List[int],
            rolling_size: int,
            degrees: int = 3,
    ) -> float:
        """
        Predicts the next value in a numeric sequence using multivariate polynomial regression.

        This method applies a polynomial regression model to a numeric sequence to predict the next value.
        It utilizes a rolling window approach to create datasets, scales the features, and fits a polynomial
        regression model to make the prediction.

        Args:
            numeric_sequence (List[int]): The list of integers representing the sequence.
            rolling_size (int): The number of elements in each rolling window.
            degrees (int): The degree of the polynomial regression. Defaults to 3.

        Returns:
            float: The predicted next value in the sequence.

        Raises:
            ValueError: If the rolling_size is larger than the size of numeric_sequence.
        """
        if rolling_size > len(numeric_sequence):
            raise ValueError("rolling_size cannot be larger than the size of numeric_sequence")

        # Generate datasets with the specified rolling size
        train_x, train_y = CalculateUtil.generate_datasets_with_rolling_size(
            data=numeric_sequence, rolling_size=rolling_size
        )

        # Preparing input data for model training
        input_x = np.array(train_x)
        output_y = np.array(train_y)

        # Scaling the features
        scaler = StandardScaler()
        input_x_scaled = scaler.fit_transform(input_x)

        # Creating and training the polynomial regression model
        model = make_pipeline(PolynomialFeatures(degrees), LinearRegression())
        model.fit(input_x_scaled, output_y)

        # Preparing the last rolling window of data for prediction
        test_x = np.array([numeric_sequence[-rolling_size:]])
        test_x_scaled = scaler.transform(test_x)

        # Predicting the next value
        pred_y = model.predict(test_x_scaled)
        return pred_y[0]

    @staticmethod
    def harmonic_regression_next_value_by_index(numeric_sequence: List[int], frequency: float = 1.0) -> int:
        """
        Predicts the next value in a sequence using harmonic regression.

        Harmonic regression involves fitting a model with sine and cosine components to capture
        periodic patterns in the data. This function predicts the next value in a given sequence
        of numbers by fitting a harmonic model to the sequence.

        :param numeric_sequence: A list or sequence of numbers to model.
        :param frequency: The frequency of the periodic component to model.
        :return: The predicted next value in the sequence as an integer.
        """
        # Convert the numeric sequence into a numpy array
        data = np.array(numeric_sequence).reshape(-1, 1)

        # Create an array representing time or the independent variable
        index = np.array(range(len(data))).reshape(-1, 1)

        # Generate sine and cosine features based on the time array and given frequency
        sine_feature = np.sin(2 * np.pi * frequency * index)
        cosine_feature = np.cos(2 * np.pi * frequency * index)

        # Combine sine and cosine features into a single feature matrix
        features = np.hstack((sine_feature, cosine_feature))

        # Create a LinearRegression model and fit it to the data with harmonic features
        model = LinearRegression()
        model.fit(features, data)

        # Predict the next value in the sequence using the fitted model
        next_time_point = np.array([[len(data)]])
        next_sine_feature = np.sin(2 * np.pi * frequency * next_time_point)
        next_cosine_feature = np.cos(2 * np.pi * frequency * next_time_point)
        next_features = np.hstack((next_sine_feature, next_cosine_feature))

        prediction = model.predict(next_features)[0][0]

        # Return the predicted value as an integer
        return round(prediction)

    @staticmethod
    def random_forest_regressor_transformer(
            numeric_sequence: List[int],
            rolling_size: int,
            warm_start: bool = False,
            random_state: int = 12,
            param_distributions: Optional[Dict] = None,
            param_overrides: Optional[Dict] = None
    ) -> float:
        train_x, train_y = CalculateUtil.generate_datasets_with_rolling_size(
            data=numeric_sequence, rolling_size=rolling_size
        )

        # Convert lists to numpy arrays for compatibility with scikit-learn
        input_x = np.array(train_x)
        output_y = np.array(train_y)

        # Scale the features to normalize data
        scaler = StandardScaler()
        input_x_scaled = scaler.fit_transform(input_x)

        # Initialize and train the Random Forest Regressor
        model = RandomForestRegressor(warm_start=warm_start, random_state=random_state)
        if param_distributions:
            param_overrides = param_overrides or {}
            random_search = RandomizedSearchCV(estimator=model, param_distributions=param_distributions,
                                               **param_overrides)
            random_search.fit(input_x_scaled, output_y)
            model = RandomForestRegressor(warm_start=warm_start, random_state=random_state,
                                          **random_search.best_params_)

        model_pipline = Pipeline([
            ('prediction_transformer', RandomForestRegressorTransformer(model)),
            ('prediction_transformer_two', RandomForestRegressor(warm_start=warm_start, random_state=random_state)),
            # ('poly_features', PolynomialFeatures(degree=2)),
            # ('linear_regression', LinearRegression())
        ])
        model_pipline.fit(input_x_scaled, output_y)

        # Prepare the last rolling window of data for prediction
        test_x = np.array([numeric_sequence[-rolling_size:]])
        test_x_scaled = scaler.transform(test_x)

        # Predicting the next value
        pred_y = model_pipline.predict(test_x_scaled)
        return pred_y

    @staticmethod
    def random_forest_regressor_next_value(
            numeric_sequence: List[int],
            rolling_size: int,
            warm_start: bool = False,
            random_state: int = 12,
            param_distributions: Optional[Dict] = None,
            param_overrides: Optional[Dict] = None
    ) -> float:
        """
        Predicts the next value in a numeric sequence using a Random Forest Regressor model.

        This method uses a Random Forest Regressor to predict the next value in a sequence based on
        the values in a rolling window. The sequence is first transformed into a dataset suitable for
        regression by creating overlapping windows of specified size.

        Args:
            numeric_sequence (List[int]): The list of integers representing the sequence.
            rolling_size (int): The number of elements in each rolling window.
            warm_start (bool): Whether to reuse the solution of the previous call to fit and add more estimators to the ensemble.
            random_state (int): Controls both the randomness of the bootstrapping of the samples used when building trees
                                (if `bootstrap=True`) and the sampling of the features to consider when looking for the best split at each node.
            param_distributions (Optional[Dict]): The distribution of parameters to try in randomized search.
                                                eg: {
                                                    'n_estimators': stats.randint(100, 500),
                                                    'max_depth': [None, ] + [i for i in range(10, 100)],
                                                    'max_features': ['sqrt', 'log2'],
                                                    'min_samples_split': stats.randint(2, 80),
                                                    'min_samples_leaf': stats.randint(1, 40)
                                                }
            param_overrides (Optional[Dict]): Additional parameters for the RandomizedSearchCV.
                                                eg: {
                                                    'n_iter': 100,
                                                    'cv': 3,
                                                    'scoring': 'neg_mean_squared_error',
                                                    'verbose': 0,
                                                    'random_state': 12,
                                                    'n_jobs': -1
                                                }

        Returns:
            float: The predicted next value in the sequence.

        Raises:
            ValueError: If the rolling_size is larger than the size of numeric_sequence.
        """
        if rolling_size > len(numeric_sequence):
            raise ValueError("rolling_size cannot be larger than the size of numeric_sequence")

        # Generate datasets with the specified rolling size
        train_x, train_y = CalculateUtil.generate_datasets_with_rolling_size(
            data=numeric_sequence, rolling_size=rolling_size
        )

        # Convert lists to numpy arrays for compatibility with scikit-learn
        input_x = np.array(train_x)
        output_y = np.array(train_y)

        # Scale the features to normalize data
        scaler = StandardScaler()
        input_x_scaled = scaler.fit_transform(input_x)

        # Initialize and train the Random Forest Regressor
        model = RandomForestRegressor(warm_start=warm_start, random_state=random_state)
        if param_distributions:
            param_overrides = param_overrides or {}
            random_search = RandomizedSearchCV(estimator=model, param_distributions=param_distributions,
                                               **param_overrides)
            random_search.fit(input_x_scaled, output_y)
            model = RandomForestRegressor(warm_start=warm_start, random_state=random_state,
                                          **random_search.best_params_)
        model.fit(input_x_scaled, output_y)

        # Prepare the last rolling window of data for prediction
        test_x = np.array([numeric_sequence[-rolling_size:]])
        test_x_scaled = scaler.transform(test_x)

        # Predicting the next value
        pred_y = model.predict(test_x_scaled)
        return pred_y[0]

    @staticmethod
    def random_forest_regressor_next_value_by_index(numeric_sequence: List[int]) -> int:
        """
        Predicts the next value in a sequence using a Random Forest Regressor.

        A Random Forest Regressor is a type of ensemble machine learning model that uses
        multiple decision trees to make predictions. It is particularly useful for regression
        tasks on complex datasets because it can capture non-linear relationships between
        variables. This function applies the model to a sequence of numbers to predict the
        next value based on the observed trend.

        :param numeric_sequence: A list or sequence of numbers to model.
        :return: The predicted next value in the sequence as an integer.
        """
        # Convert the numeric sequence into a numpy array and reshape for sklearn
        data = np.array(numeric_sequence).reshape(-1, 1)

        # Create an array representing time or the independent variable, reshaped as a column
        time_feature = np.array(range(len(data))).reshape(-1, 1)

        # Create a RandomForestRegressor model and fit it to the data
        model = RandomForestRegressor()
        model.fit(time_feature, data.ravel())  # Flatten the array to fit the model

        # Predict the next value in the sequence using the fitted model
        future_time = np.array([len(data)]).reshape(-1, 1)
        future_pred = model.predict(future_time)

        # Return the predicted value as an integer
        return round(future_pred[0])

    @staticmethod
    def relative_strength_index(numeric_sequence: List[int], period: int = 14) -> float:
        """
        Calculate the Relative Strength Index (RSI) using Exponential Moving Average (EMA).

        :param numeric_sequence: A list of prices for a particular stock or asset.
        :param period: The period over which to calculate the RSI, typically 14.
        :return: The calculated RSI value.
        """
        if len(numeric_sequence) < period:
            raise ValueError("Not enough data points to calculate RSI")

        deltas = [numeric_sequence[i + 1] - numeric_sequence[i] for i in range(len(numeric_sequence) - 1)]
        gains = [max(delta, 0) for delta in deltas]
        losses = [max(-delta, 0) for delta in deltas]

        # Initialize EMA with SMA for the first 'period'
        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period

        # Apply EMA formula for gains and losses
        ema_factor = 2 / (period + 1)
        for i in range(period, len(deltas)):
            avg_gain = (gains[i] * ema_factor) + (avg_gain * (1 - ema_factor))
            avg_loss = (losses[i] * ema_factor) + (avg_loss * (1 - ema_factor))

        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi = 100 - (100 / (1 + rs)) if avg_loss != 0 else 100

        return rsi

    @staticmethod
    def seasonal_autoregressive_integrated_moving_average_next_value(numeric_sequence: List[int]) -> int:
        """
        Fit a Seasonal Autoregressive Integrated Moving Average (SARIMA) model to
        the provided time series data and predict the next value in the series.

        SARIMA models are used to forecast future points in a time series. They are
        capable of modeling complex seasonal patterns by incorporating both non-seasonal
        (ARIMA) and seasonal elements.

        :param numeric_sequence: A list of numerical values representing a time series.
        :return: The next integer value predicted by the SARIMA model.
        """
        # Convert the data to a numpy array for time series analysis
        timeseries = np.array(numeric_sequence)

        # Automatically discover the optimal order for the SARIMA model
        stepwise_model = auto_arima(timeseries, start_p=2, start_q=2,
                                    max_p=3, max_q=3, m=12,
                                    start_P=1, start_Q=1, max_P=3, max_Q=3,
                                    seasonal=True,
                                    d=1, D=1, trace=False,
                                    error_action='ignore',
                                    suppress_warnings=True,
                                    stepwise=True)

        # Fit the SARIMA model to the time series data
        model = stepwise_model.fit(timeseries)

        # Predict the next value in the time series
        forecast = model.predict(n_periods=1)

        # Return the predicted value as an integer
        return round(forecast[0])


class SpiderUtil(ABC):
    """
    Mostly crawling data
    """
    url = 'https://www.lottery.gov.cn/kj/kjlb.html?dlt'

    def __init__(self, **kwargs):
        """
        Initialize the SpiderUtil object with a URL.

        :param kwargs: A dictionary of keyword arguments where:
            - 'url': str is the URL to fetch the data from. If not provided, it defaults to an empty string.
        """
        self.url = kwargs.get('url', '') or self.url

    def spider_chrome_driver(self) -> webdriver.Chrome:
        """
        Initialize a Chrome WebDriver with headless option and navigate to the URL.

        :return: An instance of Chrome WebDriver.
        """
        # Import browser configuration
        options = webdriver.ChromeOptions()
        # Set headless mode
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(self.url)
        return driver

    @abstractmethod
    def spider_recent_data(self) -> List[List[str]]:
        """
        Fetch the recent data from the web page.

        :return: A list of lists containing recent data entries.
        """
        driver = self.spider_chrome_driver()
        time.sleep(1)  # Allow time for the page to load
        frame = driver.find_element(By.XPATH, '//iframe[@id="iFrame1"]')
        driver.switch_to.frame(frame)
        content = driver.find_element(By.XPATH, '//tbody[@id="historyData"]')
        recent_data = [x.split(' ')[:9] for x in content.text.split('\n')]
        return recent_data

    @abstractmethod
    def spider_latest_data(self) -> Optional[List[str]]:
        """
        Fetch the latest single data entry.

        :return: A list containing the latest data entry, or None if there is no data.
        """
        recent_data = self.spider_recent_data()
        return recent_data[0] if recent_data else None

    @abstractmethod
    def spider_full_data(self) -> List[List[str]]:
        """
        Load the full set of data from the source.

        :return: A list of lists containing all data entries.
        """
        # The implementation should be provided by the subclass.
        full_data = []
        driver = self.spider_chrome_driver()
        time.sleep(1)  # Allow time for the page to load
        frame = driver.find_element(By.XPATH, '//iframe[@id="iFrame1"]')
        driver.switch_to.frame(frame)
        matches = re.findall(r'goNextPage\((\d+)\)', driver.page_source)
        page_index = [int(match) for match in matches]
        for index in range(max(page_index)):
            # wait data load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//tbody[@id="historyData"]'))
            )

            # extract data
            content = driver.find_element(By.XPATH, '//tbody[@id="historyData"]')
            full_data.extend([x.split()[:9] for x in content.text.split('\n') if len(x.split()) >= 9])

            # wait next page load
            try:
                # try to find element of position == 13
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/ul/li[position()=13]"))
                )
            except Exception as ex:
                # try to find element of position == 8
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/ul/li[position()=8]"))
                )

            # click to next page
            next_button.click()
            time.sleep(3)  # loading
        driver.quit()
        sorted_full_data = sorted(full_data, key=lambda x: int(x[0]))

        return sorted_full_data


class CalculateUtil(ABC):
    """
    Compute features based on a single or multi of data
    """

    @staticmethod
    def generate_datasets_with_rolling_size(data: List[int],
                                            rolling_size: int = 5,
                                            adjust: bool = False) -> Tuple[List[List[int]], List[int]]:
        """
        Generates sequential test and validation datasets from a list of integers. It optionally adjusts
        test datasets by removing extreme values.

        The function iterates over the data to create overlapping test sets of a specified size. Each test set is
        followed by a validation set which is the next single element in the list. If the 'adjust' flag is True,
        the maximum and minimum values are removed from each test set.

        Args:
            data (List[int]): The input data list from which datasets are generated.
            rolling_size (int): The number of elements in each test set. Defaults to 5.
            adjust (bool): Whether to remove the maximum and minimum values from each test set. Defaults to False.

        Returns:
            Tuple[List[List[int]], List[int]]: A tuple containing two lists:
                - The first list contains the test sets, possibly adjusted.
                - The second list contains the single-element validation sets.
        """
        x_sets = []  # List to hold the test sets
        y_sets = []  # List to hold the validation sets

        # Iterate over the data to form test and validation sets
        for i in range(len(data) - rolling_size):
            test_set = data[i:i + rolling_size]  # Extract size elements for the test set
            validation_set = data[i + rolling_size]  # Take the next element as the validation set

            if len(test_set) > 2 and adjust:
                # Remove the maximum and minimum values if adjusting
                max_val = max(test_set)
                min_val = min(test_set)
                max_index = test_set.index(max_val)
                min_index = test_set.index(min_val)
                filtered_test_set = [x for idx, x in enumerate(test_set) if idx != max_index and idx != min_index]
                x_sets.append(filtered_test_set)
            else:
                x_sets.append(test_set)  # Append the test set as is if not adjusting

            y_sets.append(validation_set)  # Append the validation element

        return x_sets, y_sets

    @classmethod
    def calculate_zone_ratio(
            cls,
            number_combination: Iterable[int],
            zone_ranges: List[Tuple[int, int]],
            **kwargs: Any
    ) -> Tuple[int, ...]:
        """
        Calculate the counts of numbers within predefined zones for a given sequence of numbers.
        This class method determines the distribution of the numbers in the input sequence across specified zones.
        Each zone is defined by a range, and this method counts how many numbers fall into each zone.

        :param number_combination: An iterable of numbers (like a list or tuple) from which the method will count how many
                                    numbers fall into each zone.
        :param zone_ranges: A list of tuples where each tuple contains two numbers representing the start and end of a
                            zone range, respectively. These ranges define the zones for categorizing the numbers.
        :param kwargs: Additional keyword arguments that may be used for future extensions of the method.
        :return: A tuple containing the count of numbers that fall within each specified zone.
        """

        # Check if zone ranges are defined, if not, raise an exception.
        if not zone_ranges:
            raise ValueError('Zone ranges must be provided.')

        # Initialize counters for each zone to zero.
        ratio = [0] * len(zone_ranges)

        # Iterate through each number and check which zone it falls into.
        for num in map(int, number_combination):  # Convert each number to an integer once before the loop.
            for i, (start, end) in enumerate(zone_ranges):
                if start <= num <= end:
                    ratio[i] += 1  # Increment the counter for the current zone.
                    break  # If the number is within the current zone, no need to check further zones.

        # Return the counts as a tuple, with each element representing the count for a respective zone.
        return tuple(ratio)

    @classmethod
    def calculate_big_small_ratio(
            cls,
            number_combinations: Iterable[int],
            big_small_ranges: List[Tuple[int, int]],
            **kwargs: Any
    ) -> Tuple[int, ...]:
        """
        Calculate the counts of numbers within predefined size ranges for a sequence of numbers.
        This class method assesses how many numbers from the input sequence fall within each of the specified size ranges.
        Each range represents a 'zone', which could correspond to a concept like 'big' or 'small' numbers.

        :param number_combinations: An iterable of numbers (like a list or tuple) from which the method will count how many
                                    numbers fall into each size range.
        :param big_small_ranges: A list of tuples where each tuple contains two numbers representing the start and end of a
                                 range, respectively. These ranges define the zones for categorizing the numbers.
        :param kwargs: Additional keyword arguments that may be used for future extensions of the method.
        :return: A tuple containing the count of numbers that fall within each specified range or 'zone'.
        """

        # Check if size ranges are defined, if not, raise an exception.
        if not big_small_ranges:
            raise ValueError('Size ranges for big and small numbers must be provided.')

        # Initialize counters for each range to zero.
        ratio = [0] * len(big_small_ranges)

        # Iterate through each number and check which range it falls into.
        for num in map(int, number_combinations):  # Convert each number to an integer once before the loop.
            for i, (start, end) in enumerate(big_small_ranges):
                if start <= num <= end:
                    ratio[i] += 1  # Increment the counter for the current range.
                    break  # If the number is within the current range, no need to check further ranges.

        # Return the counts as a tuple, with each element representing the count for a respective range or 'zone'.
        return tuple(ratio)

    @classmethod
    def calculate_road_012_ratio(
            cls,
            number_combination: Iterable[int],
            road_012_ranges: List[tuple[int, ...]],
            **kwargs: Any
    ) -> Tuple[int, ...]:
        """
        Calculate the count of numbers within predefined zones (referred to as 'roads') for a given sequence of numbers.
        This class method determines how many numbers from the input fall within each of the specified ranges. Each range
        represents a 'road', which is a segment of the overall data set.

        :param number_combination: A list, tuple, or other iterable of numbers. The method will iterate through this
                                   collection to count how many numbers fall into each 'road' as defined by the ranges.
        :param road_012_ranges: A list of range objects or sequences defining the 'roads'. Each element in this list
                                corresponds to a different 'road', and the numbers in 'number_combination' are checked
                                against these ranges to determine their counts.
        :param kwargs: Additional keyword arguments that are not used in this method but are included for potential
                       future extensibility of the method.
        :return: A tuple containing the count of numbers in each 'road'.
        """

        # Validate the presence of 'road_012_ranges'.
        if not road_012_ranges:
            raise ValueError('Road 012 ranges must be provided.')

        # Initialize counters for each 'road' to zero.
        ratio = [0] * len(road_012_ranges)

        # Count the numbers in each 'road' by iterating through the input numbers and the defined ranges.
        for num in map(int, number_combination):  # Convert each number to an integer once, before the loop.
            for i, vals in enumerate(road_012_ranges):
                if num in vals:
                    ratio[i] += 1
                    break  # Once the number is found in a 'road', stop checking the remaining 'roads'.

        # Return the counts as a tuple, with each element representing the count for a respective 'road'.
        return tuple(ratio)

    @classmethod
    def calculate_odd_even_ratio(
            cls,
            number_combination: Iterable[int],
            **kwargs: Any
    ) -> Tuple[int, int]:
        """
        Calculate the ratio of odd to even numbers within a given sequence of numbers.
        This method is designed to be called on the class itself rather than on an instance of the class. It can be
        used to analyze a collection of numbers (number_combination) and determine the count of odd and even numbers.

        :param number_combination: A list, tuple, or other iterable of integers. The method will iterate through
                                   this collection to determine the count of odd and even numbers.
        :param kwargs: Additional keyword arguments that are not used in this method but are included for potential
                       future extensibility of the method.
        :return: A tuple containing two elements; the first is the count of odd numbers and the second is the
                 count of even numbers in the number_combination.
        """

        # Count the number of odd numbers in the number_combination
        # A number is considered odd if the remainder of the division by 2 is 1 (num % 2 evaluates to True)
        odd_count = sum(1 for num in number_combination if num % 2)

        # Count the number of even numbers in the number_combination
        # It's calculated by subtracting the odd count from the total length of the number_combination
        even_count = len(list(number_combination)) - odd_count

        # Return a tuple of odd and even counts
        return odd_count, even_count

    @classmethod
    def calculate_prime_composite_ratio(
            cls,
            number_combination: Iterable[int],
            **kwargs: Any
    ) -> Tuple[int, int]:
        """
        Calculate the ratio of prime to composite numbers in a sequence of numbers provided in the number_combination.
        In this context, the number 1 is considered a prime number.

        :param number_combination: A list or tuple of numerical values. The method will determine which numbers are
                                   prime (including 1) and which are composite, and compute their counts.
        :param kwargs: Additional keyword arguments, not used in this function but included for potential future
                       extensibility of the method.
        :return: A tuple containing two elements; the first is the count of prime numbers (including 1) and the
                 second is the count of composite numbers in the number_combination.
        """

        def is_prime(num: int) -> bool:
            # Consider 1 as a prime number for the purpose of this calculation
            if num == 1:
                return True
            # Exclude numbers less than 1 and even numbers greater than 2 as they are not prime
            if num < 1 or (num % 2 == 0 and num > 2):
                return False
            # Check for factors from 3 to the square root of num
            for i in range(3, int(num ** 0.5) + 1, 2):
                if num % i == 0:
                    return False
            return True

        # Count prime numbers in the number_combination
        prime_count = sum(1 for num in number_combination if is_prime(num))
        # Count composite numbers as the remaining numbers in the number_combination
        composite_count = len(list(number_combination)) - prime_count

        # Return a tuple of prime and composite counts
        return prime_count, composite_count

    @classmethod
    def calculate_span(
            cls,
            number_combination:
            Iterable[int],
            **kwargs: Any
    ) -> int:
        """
        Calculate the span of a sequence of numbers provided in the number_combination. The span is defined as the
        difference between the maximum and minimum values in the set of numbers.

        :param number_combination: A list or tuple of numerical values. The method will find the maximum and minimum
                                   values in this collection and calculate the difference (span) between them.
        :param kwargs: Additional keyword arguments, not used in this function but included for potential future
                       extensibility of the method.
        :return: The span of the numbers in the number_combination as an integer. If the input contains floating
                 point numbers, the span is cast to an integer before being returned.
        """

        # Find the maximum and minimum values in the number combination
        max_value = max(number_combination)
        min_value = min(number_combination)

        # Calculate the span by subtracting the minimum value from the maximum value
        span = max_value - min_value

        # Cast the span to an integer and return it
        return int(span)

    @classmethod
    def calculate_sum_total(
            cls,
            number_combination: Iterable[Union[int, float]],
            **kwargs: Any
    ) -> Union[int, float]:
        """
        Calculate the total sum of a sequence of numbers provided in the number_combination. This method
        aggregates all the numerical values in the list or tuple passed as an argument and returns their sum.

        :param number_combination: A list or tuple of numerical values. The method will sum these values and return
                                   the result.
        :param kwargs: Additional keyword arguments, not used in this function but included for potential future
                       extensibility of the method.
        :return: The sum total of the numbers in the number_combination as an integer or float, depending on the
                 input values.
        """

        # Calculate the sum of the numbers in the combination using the built-in sum function
        total_sum = sum(number_combination)

        # Return the sum total
        return total_sum

    @classmethod
    def calculate_sum_tail(
            cls,
            number_combination: Iterable[int],
            **kwargs: Any
    ) -> int:
        """
        Calculate the last digit (tail) of the sum of a given number combination. The tail is the unit's place
        of the sum, which can be useful for certain types of numerical analysis or pattern recognition.

        :param number_combination: A list or tuple of numerical values. The sum of these numbers will be calculated,
                                   and the tail of this sum (last digit) will be returned.
        :param kwargs: Additional keyword arguments, not used in this function but included for potential future
                       extensibility of the method.
        :return: The last digit of the sum of the number combination as an integer.
        """

        # Calculate the sum of the numbers in the combination
        total_sum = cls.calculate_sum_total(number_combination)

        # Return the last digit of this sum
        return total_sum % 10

    @classmethod
    def calculate_weekday(
            cls,
            date: str,
            date_format: str = '%Y-%m-%d',
            **kwargs: Any
    ) -> int:
        """
        Calculate the weekday number from a date string.

        :param date: Date string.
        :param date_format: default 'YYYY-MM-DD' format
        :return: Weekday number where 1 represents Monday and 7 represents Sunday.
        """
        date = datetime.datetime.strptime(date, date_format).date()
        return date.weekday() + 1

    @classmethod
    def calculate_ac(
            cls,
            number_combination: Iterable[int],
            **kwargs: Any
    ) -> int:
        """
        Compute the complexity of a given number combination. Complexity is defined as the number of distinct
        absolute differences between each pair of numbers in the combination, excluding the number of elements minus one.

        :param number_combination: A list or tuple of numerical values for which the complexity will be calculated.
        :param kwargs: Additional keyword arguments, not used in this function but allows for extensibility.
        :return: An integer representing the complexity of the number combination.
        """

        # Initialize a set to store distinct absolute differences
        distinct_diffs = set()

        # Count the number of elements in the number combination
        number_combination_list = list(number_combination)
        num_count = len(number_combination_list)

        # Iterate over each unique pair of numbers to calculate absolute differences
        for i in range(num_count):
            for j in range(i + 1, num_count):
                # Calculate the absolute difference between the two numbers
                diff = abs(number_combination_list[j] - number_combination_list[i])
                # Add the absolute difference to the set of distinct differences
                distinct_diffs.add(diff)

        # Return the number of distinct differences minus the number of elements minus one
        return len(distinct_diffs) - (num_count - 1)

    @classmethod
    def calculate_avg(cls, number_combination: Iterable[int], **kwargs: Any) -> int:
        return math.floor(sum(number_combination) / len(list(number_combination)))

    @classmethod
    def calculate_consecutive_numbers(
            cls,
            number_combination: Iterable[int],
            **kwargs: Any
    ) -> List[List[int]]:
        """
        Calculate the sequences of consecutive numbers in a given iterable of integers.

        :param number_combination: An iterable of integers to compute consecutive numbers from.
        :param kwargs: Additional keyword arguments.
        :return: A list of lists, each containing a sequence of consecutive numbers.
        """
        # Convert the input iterable to a list to support indexing
        number_combination_list = list(number_combination)
        sequences = []
        current_sequence = [number_combination_list[0]]  # Initialize with the first number

        for i in range(1, len(number_combination_list)):
            if number_combination_list[i] == current_sequence[-1] + 1:
                current_sequence.append(number_combination_list[i])
            else:
                if len(current_sequence) > 1:
                    sequences.append(current_sequence)
                current_sequence = [number_combination_list[i]]

        if len(current_sequence) > 1:
            sequences.append(current_sequence)

        return sequences

    @classmethod
    def calculate_repeated_numbers(
            cls,
            number_combinations: Iterable[Iterable[int]],
            window: int = 2,
            **kwargs: Any
    ) -> List[int]:
        """
        Calculate the numbers that appear in all given iterable of integers (intersection).

        :param number_combinations: An iterable of integers to find common numbers.
        :param window: The number of recent periods to process.
        :param kwargs: Additional keyword arguments.
        :return: A list containing the numbers that are common in all given iterables.
        """
        # Initialize the set with the first iterable to start the intersection process
        repeated_numbers: Set[int] = set(next(iter(number_combinations[-window:]), []))

        # Perform intersection with the subsequent iterables
        for number_combination in number_combinations:
            repeated_numbers.intersection_update(set(number_combination))

        # Return the result as a list
        return list(repeated_numbers)

    @classmethod
    def calculate_edge_numbers(
            cls,
            number_combinations: Iterable[Iterable[int]],
            window: int = 2,
            **kwargs: Any
    ) -> List[int]:
        """
        Calculate 'edge numbers' which are present in consecutive iterables where each number from the first iterable
        is either one less or one more than the numbers in the following iterable.

        :param number_combinations: An iterable of iterables of integers to find 'edge numbers'.
        :param window: The number of recent periods to process.
        :param kwargs: Additional keyword arguments.
        :return: A list containing the 'edge numbers'.
        """
        # Convert the input to a list for indexed access
        number_combinations_list = list(number_combinations[-window:])

        # Initialize an empty set for the edge numbers
        edge_numbers: Set[int] = set()

        # Iterate over each number combination, starting from the second one
        for index in range(1, len(number_combinations_list)):
            # Create a set of potential edge numbers from the previous combination
            last_number_set = set(num + i for i in [-1, 0, 1]
                                  for num in number_combinations_list[index - 1]
                                  if (num + i) > 0)
            # Create a set from the current combination
            current_number_set = set(number_combinations_list[index])
            # Find the intersection of the two sets
            intersection = current_number_set.intersection(last_number_set)
            # Update the edge numbers set with the intersection
            edge_numbers.update(intersection)

        # Return the result as a sorted list to maintain a consistent order
        return sorted(edge_numbers)

    @classmethod
    def calculate_cold_hot_numbers(
            cls,
            number_combinations: Iterable[Iterable[int]],
            all_numbers: Iterable[int],
            window: int = 5,
            **kwargs: Any
    ) -> Tuple[List[int], List[int]]:
        """
        Calculate and return 'cold numbers' and 'hot numbers' from a series of number combinations.
        'Cold numbers' are those that did not appear in the last 5 iterations,
        and 'hot numbers' are those that appeared at least once in the last 5 iterations.

        :param number_combinations: An iterable of iterables of integers to analyze numbers.
        :param all_numbers: An iterable of all possible numbers that could appear.
        :param window: default 5
        :param kwargs: Additional keyword arguments.
        :return: A tuple containing two lists - the first with 'cold numbers' and the second with 'hot numbers'.
        """
        # Convert the input to a list for indexed access
        number_combinations_list = list(number_combinations[-window:])

        # Determine the range for the last 5 periods
        last_five_periods = number_combinations_list if len(
            number_combinations_list) >= window else number_combinations_list

        # Flatten the list of last five periods and convert to a set to remove duplicates
        numbers_in_last_five_periods: Set[int] = set(num for period in last_five_periods for num in period)

        # Convert all_numbers to a set for efficient lookup
        all_numbers_set: Set[int] = set(all_numbers)

        # 'Cold numbers' are those that are not in the last five periods
        cold_numbers: List[int] = sorted(list(all_numbers_set - numbers_in_last_five_periods))

        # 'Hot numbers' are those that are in the last five periods
        hot_numbers: List[int] = sorted(list(numbers_in_last_five_periods))

        # Return the cold numbers and hot numbers
        return cold_numbers, hot_numbers

    @classmethod
    def calculate_omitted_numbers(
            cls,
            number_combinations: Iterable[Iterable[int]],
            all_numbers: Iterable[int],
            window: int = 10,
            **kwargs: Any
    ) -> Dict[int, int]:
        """
        Update and return the omission values for each number in all_numbers.

        :param number_combinations: A list of lists of integers representing past number draws.
        :param all_numbers: A list of all possible numbers that could appear.
        :param window: default 10
        :return: A dictionary with numbers as keys and their omission values as values.
        """
        # Initialize the omission values for each number to 0
        omission_values: Dict[int, int] = {number: -1 for number in all_numbers}

        # Convert the input to a list for indexed access
        number_combinations_list = list(number_combinations[-window:])

        # Determine the range for the last 5 periods
        last_ten_periods = number_combinations_list if len(
            number_combinations_list) >= window else number_combinations_list

        # The number of draws since the last appearance
        draws_since_last_appearance = 0

        # Iterate over the past draws in reverse order (most recent first)
        for draw in reversed(last_ten_periods):
            # Check each number in all_numbers
            for number in all_numbers:
                # If the number is in the current draw and its omission value is -1 (hasn't appeared yet)
                if number in draw and omission_values[number] == -1:
                    # Set the omission value to the number of draws since it last appeared
                    omission_values[number] = draws_since_last_appearance
            # Increment the count of draws since the last appearance
            draws_since_last_appearance += 1

        # For any number that hasn't appeared yet, set its omission value to the total number of draws
        for number in all_numbers:
            if omission_values[number] == -1:
                omission_values[number] = draws_since_last_appearance

        return omission_values

    @staticmethod
    def calculate_standard_deviation_welford(numeric_sequence: List[Union[int, float]],
                                             decay_factor: Union[int, float] = 0.95) -> Union[int, float]:
        """
        Calculates the standard deviation of a numeric sequence using Welford's method.

        This method is an online algorithm designed to compute the standard deviation of a sequence of numbers
        iteratively, which can be useful for large datasets where all data cannot be loaded into memory at once.

        Args:
            numeric_sequence (List[Union[int, float]]): The sequence of numbers (integers or floats) for which the standard deviation is to be calculated.
            decay_factor (Union[int, float]): The decay factor for weighting recent values more heavily. Defaults to 0.95.

        Returns:
            float: The standard deviation of the sequence. Returns 0 if the sequence contains fewer than two elements.

        Notes:
            This function uses an exponential decay to weight recent observations more heavily in the calculation
            of the mean and variance, which makes it sensitive to recent changes in the sequence.
        """

        if len(numeric_sequence) == 0:
            raise ValueError("The numeric sequence cannot be empty.")
        n = 0
        mean = 0.0
        M2 = 0.0
        weighted_n = 0.0  # Weighted sample count

        for x in numeric_sequence:
            n += 1
            weight = decay_factor ** (len(numeric_sequence) - n)  # Compute weight, newer data has higher weight
            delta = x - mean
            weighted_n += weight
            mean += (delta * weight) / weighted_n
            delta2 = x - mean
            M2 += delta * delta2 * weight

        if weighted_n < 2:
            return 0.0  # Not enough samples to compute standard deviation
        variance = M2 / weighted_n  # Compute variance using weighted sample count
        return math.sqrt(variance)

    @staticmethod
    def calculate_standard_deviation(numeric_sequence: List[Union[int, float]]) -> Union[int, float]:
        """
        Calculates the standard deviation of a numeric sequence.

        This method computes the standard deviation by first calculating the mean of the numbers,
        then the variance as the average of the squared differences from the mean, and finally
        taking the square root of the variance.

        Args:
            numeric_sequence (List[Union[int, float]]): The sequence of numbers (integers or floats) for which the standard deviation is to be calculated.

        Returns:
            float: The standard deviation of the sequence.

        Raises:
            ValueError: If the numeric_sequence is empty, as standard deviation cannot be calculated.
        Notes:
            This function uses an exponential decay to weight recent observations more heavily in the calculation
            of the mean and variance, which makes it sensitive to recent changes in the sequence.
        """
        if len(numeric_sequence) == 0:
            raise ValueError("The numeric sequence cannot be empty.")

        # Calculate the mean of the sequence
        mean = sum(numeric_sequence) / len(numeric_sequence)

        # Calculate the squared differences from the mean
        squared_diffs = [(x - mean) ** 2 for x in numeric_sequence]

        # Calculate the variance
        variance = sum(squared_diffs) / len(numeric_sequence)

        # Calculate and return the standard deviation
        standard_deviation = math.sqrt(variance)
        return standard_deviation

    @abstractmethod
    def calculate_winning_amount(
            self,
            winning_number_combination: List[int],
            purchase_number_combinations: List[List[int]],
            **kwargs: Any
    ) -> Tuple[float, int]:
        """
        Calculate the winning amount based on matching combinations.

        :param winning_number_combination: Winning number combination.
        :param purchase_number_combinations: Purchase number combinations.
        :param kwargs: Additional keyword arguments.
        :return: The total winning amount and the count of winning combinations
        """
        pass


class AnalyzeUtil(ABC):
    """
    Analyze based on multiple data
    """

    @abstractmethod
    def analyze_same_period_numbers(self, **kwargs: Any) -> None:
        """
        Analyze same period number in the last period.
        """
        pass

    @abstractmethod
    def analyze_same_weekday_numbers(self, **kwargs: Any) -> None:
        """
        Analyze same weekday number in the last period.
        """
        pass

    @abstractmethod
    def analyze_repeated_numbers(self, **kwargs: Any) -> None:
        """
        Analyze the number that appeared twice in the last two period.
        """
        pass

    @abstractmethod
    def analyze_edge_numbers(self, **kwargs: Any) -> None:
        """
        Analyze Also called adjacent number, plus or minus 1 with the winning number issued in the previous period
        """
        pass

    @abstractmethod
    def analyze_cold_hot_numbers(self, **kwargs: Any) -> None:
        """
        Analyze Numbers that have appeared in the last period
        Analyze Numbers that have not appeared in the last period
        """
        pass

    @abstractmethod
    def analyze_omitted_numbers(self, **kwargs: Any) -> None:
        """
        Analyze.
        Omission: The number of periods since the previous opening to the current period.
        Average omission: The average number of omissions in the statistical period
                          (calculation formula: Average omission =
                          total number of omissions in the statistical period / (number of occurrences +1))
        Maximum missed value: Indicates the maximum value of all missed values in the statistical period.
        Current omission: The number of periods between the last occurrence and the present, if the missing object
                          appeared in the current period, the current omission value is 0
        Previous period omission: The interval between the last two periods (excluding the current period)
        Theoretical number: The theoretical number refers to the number of times the missing object should
                            theoretically appear, = the total number of t times * theoretical probability
        Desired probability: Desired probability reflects the ideal occurrence probability of the missing object.
                             The formula is (current omission/average omission * theoretical probability)
        """
        pass


class GeneticsUtil:
    def __init__(self, refers: list, data: list, min_num: int, max_num: int, fitness_params: dict,
                 population_size: int = 100, num_genes: int = 5, tournament_size: int = 3,
                 mutation_rate: float = 0.1, epoch_count: int = 100):
        """
        Initializes the GeneticsUtil class with the necessary parameters for the genetic algorithm.

        Args:
        refers (list): Reference matrix or data used for creating the reference matrix.
        data (list): Dataset from which genes are selected.
        min_num (int): Minimum allowable value for a gene.
        max_num (int): Maximum allowable value for a gene.
        fitness_params (dict): Parameters used for calculating fitness.
        population_size (int): Number of individuals in the population.
        num_genes (int): Number of genes in each individual.
        tournament_size (int): Size of the tournament for selection process.
        mutation_rate (float): Probability of mutation per gene.
        epoch_count (int): Number of generations or epochs the algorithm will run.
        """
        self.refers = refers
        self.data = data
        self.min_num = min_num
        self.max_num = max_num
        self.fitness_params = fitness_params
        self.population_size = population_size
        self.num_genes = num_genes
        self.tournament_size = tournament_size
        self.mutation_rate = mutation_rate
        self.epoch_count = epoch_count
        self.population = self.init_population()  # Initializes the population
        self.refers_matrix = self.create_refers_matrix()  # Creates a matrix from reference data

    def init_population(self) -> list:
        """
        Initializes the population with randomly selected, non-repeating genes from the data set.

        Returns:
        list: A list of individuals, each represented as a sorted list of genes.
        """
        population = [np.random.choice(self.data, self.num_genes, replace=False) for _ in range(self.population_size)]
        sorted_population = [np.sort(row) for row in population]
        return sorted_population

    def create_refers_matrix(self) -> list:
        """
        Creates a matrix based on the reference data provided during initialization.

        Returns:
        list: A matrix where each row corresponds to an item in the reference data,
              with binary encoding based on the presence of elements within the specified range.
        """
        refers_matrix = []
        for row in self.refers:
            vector = [0] * self.max_num  # Initialize vector of length max_num with zeros
            for num in row:
                if self.min_num <= num <= self.max_num:
                    vector[num - 1] = 1  # Set the corresponding position to 1
            refers_matrix.append(vector)
        return refers_matrix

    def check_diagonal(self, individual: list, dfs_size: tuple = (3, 3)) -> float:
        """
        Checks diagonal alignments in a dynamically updated matrix based on the individual's genes
        and evaluates their fitness based on the alignment.

        Args:
        individual (list): List of gene indices representing an individual in the population.
        dfs_size (tuple): Size of the matrix region to check for diagonal alignments (rows, cols).

        Returns:
        float: A fitness value modified based on the presence of diagonal alignments.
        """
        fitness_value = 1
        pre_index = individual[0] - 1  # Previous index for diagonal checking

        for indi in individual:
            if not (self.min_num <= indi <= self.max_num):
                return 1  # Return a default fitness value if gene is out of valid range

            num_index = indi - 1
            rows = len(self.refers_matrix)
            cols = self.max_num
            dfs_row, dfs_col = dfs_size
            is_balance = dfs_row == dfs_col  # Check if the area to be checked is a square
            target = min(dfs_size)

            if dfs_row > rows or dfs_col > cols:
                continue  # Skip if the matrix is smaller than the dfs size

            # Create a new matrix including a new row for the current gene
            new_matrix = [row[:] for row in self.refers_matrix]  # Copy the existing matrix
            new_row = [0] * self.max_num
            new_row[num_index] = 1
            new_matrix.append(new_row)  # Add the new row correctly

            # Check diagonals, only upwards
            for dr in [-1]:  # Only need to check the upper diagonals
                move_r = False
                move_r_count = 0
                move_c_count = 0
                for dc in [-1, 1]:  # Check both left and right diagonals
                    count = 0
                    r, c = rows, num_index
                    while rows - dfs_row <= r <= rows + 1 and pre_index - dfs_col <= c <= num_index + dfs_col:
                        if new_matrix[r][c] == 1:
                            count += 1
                        if is_balance:
                            r += dr
                            c += dc
                        else:
                            if move_r:
                                if new_matrix[r][c] == 1:
                                    move_c_count += 1
                                r += dr
                                move_r = False
                            else:
                                if new_matrix[r][c] == 1:
                                    move_r_count += 1
                                c += dc
                                move_r = True

                    if is_balance and count == target:
                        fitness_value *= 0.1  # Decrease fitness if a balanced diagonal is found
                    elif not is_balance and max(move_r_count, move_c_count) == target - 1:
                        fitness_value *= 0.3  # Decrease fitness if an unbalanced diagonal is found

            pre_index = num_index  # Update previous index for the next gene

        return fitness_value

    def check_vertical(self, individual: list) -> float:
        """
        Checks vertical alignments in a dynamically updated matrix based on the individual's genes
        and evaluates their fitness based on the alignment.

        Args:
        individual (list): List of gene indices representing an individual in the population.

        Returns:
        float: A fitness value modified based on the presence of vertical alignments.
        """
        fitness_value = 1
        pre_index = individual[0] - 1  # Previous index, unused in vertical checking

        for indi in individual:
            if not (self.min_num <= indi <= self.max_num):
                return 1  # Return a default fitness value if gene is out of valid range

            num_index = indi - 1
            rows = len(self.refers_matrix)

            # Create a new matrix including a new row for the current gene
            new_matrix = [row[:] for row in self.refers_matrix]  # Copy the existing matrix
            new_row = [0] * self.max_num
            new_row[num_index] = 1
            new_matrix.append(new_row)  # Add the new row correctly

            # Check vertical alignment
            for dr in [-1]:  # Only need to check the upward vertical line
                count = 0
                r, c = rows, num_index
                while 0 <= r < len(new_matrix):
                    if new_matrix[r][c] == 1:
                        count += 1
                    else:
                        # Check if there are no genes in the current column in the original matrix
                        if sum(new_matrix[row][c] for row in range(rows)) == 0:
                            fitness_value *= 0.5
                        elif count > 1:
                            fitness_value *= 0.4
                        else:
                            fitness_value = 1
                    r += dr

                # Adjust fitness based on the count of vertical alignments
                if count in range(1, 3):
                    fitness_value *= 0.1
                else:
                    fitness_value *= 0.7

            pre_index = num_index  # Update previous index for the next gene

        return fitness_value

    def fitness(self, individual: list, dfs_size: tuple = (2, 2)) -> float:
        """
        Calculates the fitness of an individual based on the alignment of genes in a dynamically
        updated matrix. Fitness is evaluated based on specific alignment patterns and parameters.

        Args:
        individual (list): List of gene indices representing an individual in the population.
        dfs_size (tuple): Size of the matrix region to check for alignments (rows, cols).

        Returns:
        float: A fitness value modified based on the presence of specific alignments.
        """
        # return np.linalg.norm(individual - target)
        # Check for duplicate genes, which are not allowed
        if len(set(individual)) < self.num_genes:
            return 10000  # High penalty for duplicate genes

        fitness_value = 1
        pre_index = individual[0] - 1  # Previous index for alignment checking

        for indi in individual:
            # Check if the gene is within the valid range
            if not (self.min_num <= indi <= self.max_num):
                return 10000  # High penalty for out-of-range genes

            num_index = indi - 1
            rows, cols = len(self.refers_matrix), self.max_num
            (dfs_row, dfs_col), target = dfs_size, min(dfs_size)

            # Check if the dfs_size is larger than the matrix dimensions
            if dfs_row > rows or dfs_col > cols:
                return 1  # Return default fitness if the dfs size is too large

            # Create a new matrix including a new row for the current gene
            new_matrix = [row[:] for row in self.refers_matrix]  # Copy the existing matrix
            new_row = [0] * self.max_num
            new_row[num_index] = 1
            new_matrix.append(new_row)  # Add the new row correctly

            # Check alignments only upwards
            for dr in [-1]:  # Only need to check the upward direction
                # Check diagonals
                move_r = False
                move_r_count = 0
                move_c_count = 0
                for dc in [-1, 1]:  # Check both left and right diagonals
                    count = 0
                    r, c = rows, num_index
                    while rows - dfs_row <= r <= rows + 1 and pre_index - dfs_col <= c <= min(num_index + dfs_col,
                                                                                              cols - 1):
                        if new_matrix[r][c] == 1:
                            count += 1
                        if dfs_row == dfs_col:
                            r += dr
                            c += dc
                        else:
                            if move_r:
                                if new_matrix[r][c] == 1:
                                    move_c_count += 1
                                r += dr
                                move_r = False
                            else:
                                if new_matrix[r][c] == 1:
                                    move_r_count += 1
                                c += dc
                                move_r = True

                    # Adjust fitness based on the count of diagonal alignments
                    if dfs_row == dfs_col and count == target:
                        fitness_value *= self.fitness_params[0]
                    elif not dfs_row == dfs_col and max(move_r_count, move_c_count) == target - 1:
                        fitness_value *= self.fitness_params[1]

                # Check vertical alignment
                count = 0
                r, c = rows, num_index
                while 0 <= r < len(new_matrix):
                    if new_matrix[r][c] == 1:
                        count += 1
                    else:
                        # Check if there are no genes in the current column in the original matrix
                        if sum(new_matrix[row][c] for row in range(rows)) == 0:
                            fitness_value *= self.fitness_params[2]
                        elif count > 1:
                            fitness_value *= self.fitness_params[3]
                        else:
                            fitness_value = self.fitness_params[4]
                    r += dr

                # Adjust fitness based on the count of vertical alignments
                if count in range(1, 3):
                    fitness_value *= self.fitness_params[5]
                else:
                    fitness_value *= self.fitness_params[6]

            pre_index = num_index  # Update previous index for the next gene

        return fitness_value

    def tournament_selection(self) -> np.ndarray:
        """
        Tournament selection method. Randomly selects k individuals from the population
        and returns the individual with the highest fitness.

        Returns:
        np.ndarray: The individual with the highest fitness from the selected sample.
        """
        # Select the individual with the highest fitness from a random sample
        selected = max(random.sample(self.population, self.tournament_size), key=lambda ind: 1 / self.fitness(ind))
        # Sort the selected individual for consistency
        sorted_selected = np.sort(selected)
        return sorted_selected

    def crossover(self, parent1: np.ndarray, parent2: np.ndarray) -> np.ndarray:
        """
        Two-point crossover. Randomly selects two points and swaps the genes between the two parents
        to create a child.

        Args:
        parent1 (np.ndarray): The first parent.
        parent2 (np.ndarray): The second parent.

        Returns:
        np.ndarray: The child created by crossover.
        """
        # Randomly select two points for crossover
        points = sorted(random.sample(range(0, self.num_genes), 2))
        # Create new child by combining parts of both parents
        return np.concatenate([parent1[:points[0]], parent2[points[0]:points[1]], parent1[points[1]:]])

    def mutate(self, individual: np.ndarray) -> np.ndarray:
        """
        Mutation operation. Mutates an individual's gene with a certain probability.

        Args:
        individual (np.ndarray): The individual to mutate.

        Returns:
        np.ndarray: The mutated individual.
        """
        # Mutate a gene with a given probability
        if random.random() < self.mutation_rate:
            index = random.randint(0, len(individual) - 1)
            individual[index] = random.choice(self.data)
        # Return the sorted individual
        return np.sort(individual)

    def genetic(self) -> list:
        """
        Main loop of the genetic algorithm. Performs genetic operations over multiple generations
        to find the optimal solution.

        Returns:
        np.ndarray: The best individual found after all generations.
        """
        # Iterate over multiple generations
        for _ in range(self.epoch_count):
            new_population = []
            for _ in range(self.population_size // 2):
                # Select parents and create children
                parent1 = self.tournament_selection()
                parent2 = self.tournament_selection()
                child1 = self.crossover(parent1, parent2)
                child2 = self.crossover(parent1, parent2)
                # Mutate children and add to new population
                new_population.extend([self.mutate(child1), self.mutate(child2)])
            # Update population
            self.population = new_population

        # Find and return the best individual based on fitness
        best_individual = min([list(item) for item in self.population], key=self.fitness)
        return best_individual


class RandomForestRegressorTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, model: RandomForestRegressor):
        """
        Initialize the transformer with a RandomForestRegressor model and a StandardScaler for feature scaling.

        Parameters:
        model (RandomForestRegressor): The RandomForestRegressor model to be used for predictions.
        """
        self.calculate_util = CalculateUtil
        self.model_util = ModelUtil
        self.model = model
        self.scaler = StandardScaler()

    def fit(self, X: np.ndarray, y: Optional[np.ndarray] = None) -> 'RandomForestRegressorTransformer':
        """
        Fit the RandomForest model and the scaler on the training data.

        Parameters:
        X (np.ndarray): Training data features.
        y (Optional[np.ndarray]): Training data labels.

        Returns:
        RandomForestRegressorTransformer: The instance of this transformer.
        """
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """
        Transform the input data by scaling, making predictions, and calculating per-row statistics.

        Parameters:
        X (np.ndarray): Data to transform.

        Returns:
        np.ndarray: Transformed data including last elements, predictions, standard deviations, and RSI values.
        """
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)

        # Calculate standard deviation and RSI for each row
        sd_per_row = np.array([self.calculate_util.calculate_standard_deviation_welford(row) for row in X])
        rsi_per_row = np.array([self.model_util.relative_strength_index(row, period=len(row) // 2) for row in X])

        # Extract the last element from each row
        last_elements = X[:, -1]

        # Combine all the computed features into a single array
        transformed_data = np.c_[last_elements, predictions, sd_per_row, rsi_per_row]
        return transformed_data


if __name__ == '__main__':
    pass
