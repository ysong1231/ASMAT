import os
import json
from model.Models import LSTM_Numerical
from preprocessing.PreProcess import DataProcessor

configs = json.load(open('config.json', 'r'))

dp = DataProcessor(
    configs['data_dir'],
    configs['data_train_tickers']
)

data_train, data_test = dp.split_data(configs['data_split'])

train_x, train_y = dp.prepare_data(
    data_train,
    configs['data_window_size']
)

model = LSTM_Numerical()

model.build_model(
    configs['model_network'],
    configs['model_loss'],
    configs['model_optimizer']
)

model.train(
    train_x,
    train_y,
    configs['training_epochs'],
    configs['training_batch_size'],
    configs['training_model_save_dir']
)