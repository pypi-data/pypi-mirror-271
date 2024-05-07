import numpy as np
import os
import tensorflow as tf

def decode_prediction(pred_label, num_to_char, max_label_length):
    input_len = np.ones(shape=pred_label.shape[0]) * pred_label.shape[1]
    decode = tf.keras.backend.ctc_decode(pred_label, input_length=input_len, greedy=True)[0][0][:,:max_label_length]
    chars = num_to_char(decode)
    texts = [tf.strings.reduce_join(inputs=char).numpy().decode('UTF-8') for char in chars]
    filtered_texts = [text.replace('[UNK]', " ").strip() for text in texts]
    return filtered_texts

def single_sample_prediction(model, path, num_to_char, max_label_length, IMG_HEIGHT, IMG_WIDTH):
    image_loading = tf.io.read_file(path)
    decoded_image = tf.image.decode_jpeg(contents=image_loading, channels=1)
    convert_image = tf.image.convert_image_dtype(image=decoded_image, dtype=tf.float32)
    resized_image = tf.image.resize(images=convert_image, size=(IMG_HEIGHT, IMG_WIDTH))
    resized_image = tf.transpose(resized_image, perm=[1, 0, 2])
    image_array = tf.cast(resized_image, dtype=tf.float32)
    single_image_data_with_batch = np.expand_dims(image_array, axis=0)
    prediction = decoder_prediction(model.predict(single_image_data_with_batch), num_to_char, max_label_length)
    return prediction

def batch_prediction(model, folder_path, output_file, num_to_char, max_label_length, IMG_HEIGHT, IMG_WIDTH):
    image_files = sorted([filename for filename in os.listdir(folder_path) if filename.endswith(".png")])
    with open(output_file, "w") as f:
        for filename in image_files:
            image_path = os.path.join(folder_path, filename)
            prediction = single_sample_prediction(model, image_path, num_to_char, max_label_length, IMG_HEIGHT, IMG_WIDTH)
            f.write(f"{prediction[0]}\n")
    print(f"Predictions saved to {output_file}")

