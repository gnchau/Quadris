import os
from pathlib import Path
import tensorflow as tf
from numpy import array, max
from tensorflow.keras.layers import Dense
from random import choice


class QNetwork:
    def __init__(self, number_inputs=4,
                 activation_functions=None,
                 neurons_per_layer=None,
                 optimizer=None,
                 loss=None,
                 model_path=None,
                 gamma=0.95):

        # Set defaults
        if neurons_per_layer is None:
            neurons_per_layer = [64, 64]
        if activation_functions is None:
            activation_functions = ['relu', 'relu', 'linear']
        if optimizer is None:
            optimizer = 'adam'
        if loss is None:
            loss = 'mse'
        if model_path is None:
            model_path = 'models/model1.h5'

        self.number_inputs = number_inputs
        self.activation_functions = activation_functions
        self.neurons_per_layer = neurons_per_layer
        self.optimizer = optimizer
        self.loss_function = loss
        self.model_path = model_path
        self.gamma = gamma

        if len(self.activation_functions) != len(self.neurons_per_layer) + 1:
            raise ValueError("There must be one more activation functions than there are layers.")

        self.model = self.build_model()

    def build_model(self):
        model = tf.keras.models.Sequential()
        model.add(Dense(self.neurons_per_layer[0], input_dim=self.number_inputs,
                        activation=self.activation_functions[0]))

        # Make the model from the values given to the constructor
        for i in range(1, len(self.neurons_per_layer)):
            model.add(Dense(self.neurons_per_layer[i], activation=self.activation_functions[i]))

        # Add the last layer
        model.add(Dense(1, activation=self.activation_functions[-1]))

        # Finish configuring the model
        model.compile(optimizer=self.optimizer, loss=self.loss_function)
        model.summary()

        return model

    def predict_with_moves(self, states):
        inputs = array(states)
        outputs = self.model.predict(inputs)
        return [output[0] for output in outputs]

    def get_state_with_move(self, states, will_explore=False):
        if will_explore:
            return choice(list(states))
        max_output = None
        best_state = None

        outputs = self.predict_with_moves([state for action, state in states])

        for i, (action, properties) in enumerate(states):
            output = outputs[i]
            if not max_output or output > max_output:
                max_output = output
                best_state = (action, properties)
        return best_state

    def learn(self, batch, batch_size, experiences_length, epochs):
        if batch is None or experiences_length < batch_size:
            return

        next_properties = array([mem[2] for mem in batch])

        outputs = [x[0] for x in self.model.predict(next_properties)]
        properties, qs = [], []

        for i, (props, _, _, reward, terminal) in enumerate(batch):
            if not terminal:
                q = reward + self.gamma * max(outputs[i])
            else:
                q = reward

            properties.append(props)
            qs.append(q)

        self.model.fit(array(properties), array(qs), batch_size=batch_size,
                       epochs=epochs, verbose=0)

    def save_model(self):
        if not os.path.exists(os.path.dirname(self.model_path)):
            os.makedirs(os.path.dirname(self.model_path))

        self.model.save_weights(self.model_path)

    def load_model(self):
        if Path(self.model_path).is_file():
            self.model.load_weights(self.model_path)
            print("Successfully loaded model {}".format(Path(self.model_path)))
