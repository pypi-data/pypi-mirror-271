import tensorflow as tf

def load_image(image_path, IMG_HEIGHT, IMG_WIDTH):
    image = tf.io.read_file(image_path)
    decoded_image = tf.image.decode_jpeg(contents=image, channels=1)
    convert_image = tf.image.convert_image_dtype(image=decoded_image, dtype=tf.float32)
    resized_image = tf.image.resize(images=convert_image, size=(IMG_HEIGHT, IMG_WIDTH))
    resized_image = tf.transpose(resized_image, perm=[1, 0, 2])
    image_array = tf.cast(resized_image, dtype=tf.float32)
    return image_array

