import tensorflow as tf

def load_image(image_path, img_height, img_width):
    image = tf.io.read_file(image_path)
    decoded_image = tf.image.decode_jpeg(contents=image, channels=1)
    convert_image = tf.image.convert_image_dtype(image=decoded_image, dtype=tf.float32)
    resized_image = tf.image.resize(images=convert_image, size=(img_height, img_width))
    image = tf.transpose(resized_image, perm=[1, 0, 2])

    return image

def encode_single_sample(image_path, label, char_to_num, img_height, img_width, max_label_length):
    image = load_image(image_path, img_height, img_width)
    chars = tf.strings.unicode_split(label, input_encoding='UTF-8')
    vecs = char_to_num(chars)
    pad_size = max_label_length - tf.shape(vecs)[0]
    vecs = tf.pad(vecs, paddings=[[0, pad_size]])

    return {'image': image, 'label': vecs}

