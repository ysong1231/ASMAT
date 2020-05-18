import os
import json
from predict.model.Models import LSTM_Numerical
from predict.preprocessing.PreProcess import DataProcessor

configs = json.load(open('predict/config.json', 'r'))

model = LSTM_Numerical()
model.load_model(configs['model_for_prediction'])

dp = DataProcessor(
    configs['predict_data_dir'],
    configs['data_tickers']
)

data, _ = dp.split_data(1)

data = dp.prepare_prediction_data(data, 49)

print(model.predict_next(data))

