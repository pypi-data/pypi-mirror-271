import tensorflow as tf
from tensorflow.keras.layers import *

# CTC loss
class CTCLayer(Layer):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.loss_function = tf.keras.backend.ctc_batch_cost
    def call(self, y_true, y_hat):
        batch_len = tf.cast(tf.shape(y_true)[0], dtype="int64")
        input_len = tf.cast(tf.shape(y_hat)[1], dtype='int64') * tf.ones(shape=(batch_len, 1), dtype='int64')
        label_len = tf.cast(tf.shape(y_true)[1], dtype='int64') * tf.ones(shape=(batch_len, 1), dtype='int64')
        loss = self.loss_function(y_true, y_hat, input_len, label_len)
        self.add_loss(loss)
        return y_hat

def create_model(input_shape, num_classes):
    # Input Layers
    input_images = Input(shape=input_shape, name="image")
    input_labels = Input(shape=(None,), name="label")

    # Convolutional layers
    # Layer 1
    conv_1 = Conv2D(64, 3, strides=1, padding="same", kernel_initializer="he_normal", activation="relu", name="conv_1")(input_images)
    # Layer 2
    conv_2 = Conv2D(16, 3, strides=1, padding="same", kernel_initializer="he_normal", activation="relu", name="conv_2")(conv_1)
    max_pool_1 = MaxPool2D(pool_size=(2, 2), strides=(2, 2))(conv_2)
    # Layer 3
    conv_3 = Conv2D(64, 3, strides=1, padding='same', activation='relu', kernel_initializer='he_normal', name="conv_3")(max_pool_1)
    conv_4 = Conv2D(32, 3, strides=1, padding='same', activation='relu', kernel_initializer='he_normal', name="conv_4")(conv_3)
    max_pool_2 = MaxPool2D(pool_size=(2, 2), strides=(2, 2))(conv_4)

    # Encoding
    reshape = Reshape(target_shape=((input_shape[0] // 4), (input_shape[1] // 4) * 32), name="reshape_layer")(max_pool_2)
    dense_encoding = Dense(64, kernel_initializer="he_normal", activation="relu", name="enconding_dense")(reshape)
    dense_encoding_2 = Dense(64, kernel_initializer="he_normal", activation="relu", name="enconding_dense_2")(dense_encoding)
    dropout = Dropout(0.4)(dense_encoding_2)

    # Decoder
    lstm_1 = Bidirectional(LSTM(128, return_sequences=True, dropout=0.25), name="bidirectional_lstm_1")(dropout)
    lstm_2 = Bidirectional(LSTM(64, return_sequences=True, dropout=0.25), name="bidirectional_lstm_2")(lstm_1)

    # Final Output layer
    output = Dense(num_classes + 1, activation="softmax", name="output_dense")(lstm_2)  # Plus one for CTC blank label

    # Add the CTC loss
    ctc_loss_layer = CTCLayer()(input_labels, output)

    # Define the final model
    model = tf.keras.Model(inputs=[input_images, input_labels], outputs=[ctc_loss_layer], name='ocr_model')
    
    return model

