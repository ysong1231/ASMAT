import os
import json
from predict.model.Models import LSTM_Numerical
from predict.preprocessing.PreProcess import DataProcessor

configs = json.load(open('/Users/mac/Desktop/ASMAT/predict/config.json', 'r'))

model = LSTM_Numerical()
model.load_model(configs['model_for_prediction'])

dp = DataProcessor(
    configs['predict_data_dir'],
    configs['data_tickers']
)

data, _ = dp.split_data(1)

data, bench_marks = dp.prepare_prediction_data(data, 49)

dp.interpret_prediction(bench_marks, data, model.predict_next(data)[0])

