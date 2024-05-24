import tensorflow as tf

from tensorflow import keras
from tensorflow.keras.layers import Dense, BatchNormalization, Dropout
from tensorflow.keras import Input, Model


def create_dense_stack(tensor: tf.Tensor,
                       nhidden: [int],
                       activation='elu',
                       **kwargs) -> tf.Tensor:
    '''
    Create a stack of hidden layers

    :param tensor: Input tensor
    :param nhidden: List of unit numbers for each layer
    :param activation: activation for each layer

    optional kwargs:
    - batch_normalization: True -> use batch normalization
    - dropout: Float dropout probability

    :return: Output tensor

    '''
    # Loop over layers
    for i, n in enumerate(nhidden):
        # Add BN?
        if 'batch_normalization' in kwargs.keys() and kwargs['batch_normalization']:
            tensor = BatchNormalization()(tensor)

        # Dense layer: assume 'activation' in kwargs
        tensor = Dense(n, activation=activation, use_bias=True,
                       kernel_initializer='random_normal',
                       bias_initializer='zeros', name='D%d' % i)(tensor)

        # Dropout?
        if kwargs['dropout'] is not None:
            tensor = Dropout(kwargs['dropout'])(tensor)

    return tensor


def create_model(n_inputs,
                 n_outputs,
                 hidden_layers,
                 hidden_activation='elu',
                 output_activation='elu',
                 dropout=None,
                 batch_normalization=False):
    input_tensor = Input(shape=(n_inputs,))
    tensor = input_tensor

    tensor = create_dense_stack(tensor=tensor,
                                nhidden=hidden_layers,
                                activation=hidden_activation,
                                dropout=dropout,
                                batch_normalization=batch_normalization)

    tensor = Dense(n_outputs, activation=output_activation)(tensor)
    output_tensor = tensor

    model = Model(inputs=input_tensor, outputs=output_tensor)
    return model


