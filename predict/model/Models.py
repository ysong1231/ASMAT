import os
import numpy as np
import datetime as dt
from keras.layers import Dense, Activation, Dropout, LSTM
from keras.models import Sequential, load_model
from keras.callbacks import EarlyStopping, ModelCheckpoint

class LSTM_Numerical:
    def __init__(self):
        self.model = Sequential()
    
    def load_model(self, filepath):
        print(f'[Model] Loading model from file {filepath}')
        self.model = load_model(filepath)

    def build_model(self, network, loss, optimizer):
        for layer in network:
            neurons = layer['neurons'] if 'neurons' in layer else None
            dropout_rate = layer['rate'] if 'rate' in layer else None
            activation = layer['activation'] if 'activation' in layer else None
            return_seq = layer['return_seq'] if 'return_seq' in layer else None
            input_timesteps = layer['input_timesteps'] if 'input_timesteps' in layer else None
            input_dim = layer['input_dim'] if 'input_dim' in layer else None
            
            if layer['type'] == 'dense':
                self.model.add(
                    Dense(
                        neurons,
                        activation = activation
                    )
                )
            if layer['type'] == 'lstm':
                self.model.add(
                    LSTM(
                        neurons,
                        input_shape = (input_timesteps, input_dim),
                        return_sequences = return_seq
                    )
                )
            if layer['type'] == 'dropout':
                self.model.add(
                    Dropout(dropout_rate)
                )
        self.model.compile(
            loss = loss,
            optimizer = optimizer
        )
        print('[Model] Model Compiled')

    def train(self, x, y, epochs, batch_size, save_dir):
        print('[Model] Training Started')
        print(f'[Model] Epochs: {epochs}, Batch Size: {batch_size}')

        save_fname = os.path.join(save_dir, f'{dt.datetime.now().strftime("%d%m%Y-%H%M%S")}-e{epochs}.h5')
        callbacks = [
            EarlyStopping(
                monitor = 'loss',
                patience = 2
            ),
            ModelCheckpoint(
                filepath = save_fname,
                monitor = 'loss',
                save_best_only = True
            )
        ]
        
        self.model.fit(
            x,
            y,
            epochs = epochs,
            batch_size = batch_size,
            callbacks = callbacks
        )
        
        self.model.save(save_fname)
        print(f'[Model] Training Completed. Model saved as {save_fname}')

    def predict_next(self, data):
        predicted = self.model.predict(data)
        predicted = np.reshape(predicted, (predicted.size,))
        return predicted