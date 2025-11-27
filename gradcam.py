import numpy as np
import tensorflow as tf
import cv2

def get_last_conv_layer(model):
    """
    Finds the last convolutional layer automatically.
    Works for VGG, ResNet, DenseNet, EfficientNet.
    """
    for layer in reversed(model.layers):
        if 'conv' in layer.name or 'stem' in layer.name:
            return layer.name
    raise ValueError("No convolutional layer found")


def generate_gradcam_heatmap(model, img_array):
    """
    Generates a Grad-CAM heatmap for a given image.
    """
    last_conv_layer_name = get_last_conv_layer(model)
    last_conv_layer = model.get_layer(last_conv_layer_name)

    grad_model = tf.keras.models.Model(
        [model.inputs],
        [last_conv_layer.output, model.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        class_score = predictions[0][0]

    grads = tape.gradient(class_score, conv_outputs)

    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]
    heatmap = tf.reduce_sum(tf.multiply(pooled_grads, conv_outputs), axis=-1)

    heatmap = np.maximum(heatmap, 0)
    heatmap /= heatmap.max() + 1e-6

    return heatmap
