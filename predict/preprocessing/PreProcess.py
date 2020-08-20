import os
import math
import numpy as np
import pandas as pd

class DataProcessor:
    def __init__(self, directory, tickers):
        dataframe = pd.read_csv(os.path.join(directory, tickers[0] + '.csv')).set_index('Date')
        dataframe = dataframe[['Open', 'High', 'Low', 'Close', 'Volume']]
        dataframe.columns = map(lambda x: tickers[0] + x, dataframe.columns)
        for ticker in tickers[1:]:
            df = pd.read_csv(os.path.join(directory, ticker +'.csv')).set_index('Date')
            if ticker == '^VIX':
                df = df[['Open', 'High', 'Low', 'Close']]
            else:
                df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
            df.columns = map(lambda x: ticker + x, df.columns)
            dataframe = dataframe.join(df, on = 'Date')
        self.data = dataframe.dropna()
    
    def split_data(self, split, data = None):
        if not data:
            data = self.data
        i_split = int(len(data) * split)
        data_train = data.values[:i_split]
        data_test = data.values[i_split:]
        return data_train, data_test

    def prepare_data(self, data, window_size):
        x = []
        y = []
        for i in range(len(data) - window_size):
            window = data[i:i + window_size]
            window = self._normalize(window)
            x.append(window[:-1])
            y.append(window[-1, 0])
        return np.array(x), np.array(y)
    
    def prepare_prediction_data(self, data, window_size):
        window = data[-window_size:]
        bench_mark = window[0]
        window = self._normalize(window)
        return np.array([window]), bench_mark
    
    def _normalize(self, data):
        normalised_window = []
        for col in range(data.shape[1]):
            normalised_col = [((float(p) / float(data[0, col])) - 1) for p in data[:, col]]
            normalised_window.append(normalised_col)
        normalised_window = np.array(normalised_window).T # reshape and transpose array back into original multidimensional format
        return np.array(normalised_window)
    
    def interpret_prediction(self, bench_marks, original_data, prediction, predict_col = 0):
        bench_mark = bench_marks[predict_col]
        today = (original_data[-1, -1, predict_col] + 1) * bench_mark
        prediction = (prediction + 1) * bench_mark
        change = (prediction - today) / today * 100
        print(f'Today: {round(today, 2)}, Next Day: {round(prediction, 2)}, Change Rate: {round(change, 2)}%')