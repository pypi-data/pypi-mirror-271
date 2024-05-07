import numpy as np

def decoder_prediction(pred_label, num_to_char, max_label_length):
    input_len = np.ones(shape=pred_label.shape[0]) * pred_label.shape[1]
    decode = tf.keras.backend.ctc_decode(pred_label, input_length=input_len, greedy=True)[0][0][:, :max_label_length]
    chars = num_to_char(decode)
    texts = [tf.strings.reduce_join(inputs=char).numpy().decode('UTF-8') for char in chars]
    filtered_texts = [text.replace('[UNK]', " ").strip() for text in texts]
    return filtered_texts

