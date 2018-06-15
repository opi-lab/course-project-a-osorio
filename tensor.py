#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 18:50:00 2018

@author: alexanderosorio
"""

import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
from sklearn.metrics import confusion_matrix
from tensorflow.examples.tutorials.mnist import input_data
data = input_data.read_data_sets("data/MNIST/", one_hot=True)
print("Size of:")
print("- Training-set:\t\t{}".format(len(data.train.labels)))
print("- Test-set:\t\t{}".format(len(data.test.labels)))
print("- Validation-set:\t{}".format(len(data.validation.labels)))
data.test.labels[0:5, :]
data.test.cls = np.array([label.argmax() for label in data.test.labels])
print (data.test.cls[0:5])
# Tamaño de imagen de 28 pixeles.
img_size = 28

# Aplanando la imagen en una dimensión.
img_size_flat = img_size * img_size

# Tupla ancho  y alto de la imagen para reconstruir en el array.
img_shape = (img_size, img_size)

# Numero de clases por cada digito.
num_classes = 10
def plot_images(images, cls_true, cls_pred=None):
    assert len(images) == len(cls_true) == 9

    # Creando figura de 3x3.
    fig, axes = plt.subplots(3, 3)
    fig.subplots_adjust(hspace=0.5, wspace=0.5)

    for i, ax in enumerate(axes.flat):
        # dibujando la imagen
        ax.imshow(images[i].reshape(img_shape), cmap='binary')

        # Mostrando las imaganes verdaderas y las predichas.
        if cls_pred is None:
            xlabel = "Verdaderos: {0}".format(cls_true[i])
        else:
            xlabel = "Verdaderos: {0}, Predichos: {1}".format(cls_true[i], cls_pred[i])

        ax.set_xlabel(xlabel)

        
        ax.set_xticks([])
        ax.set_yticks([])

images = data.test.images[0:9]

# Obteniendo las clases verdaderas.
cls_true = data.test.cls[0:9]

# Dibujando las imagenes y las etiquetas.
plot_images(images=images, cls_true=cls_true)

x = tf.placeholder(tf.float32, [None, img_size_flat])
y_true = tf.placeholder(tf.float32, [None, num_classes])
y_true_cls = tf.placeholder(tf.int64, [None])
w = tf.Variable(tf.zeros([img_size_flat, num_classes]))
b = tf.Variable(tf.zeros([ num_classes]))
logits = tf.matmul(x, w) + b
y_pred = tf.nn.softmax(logits)
y_pred_cls = tf.argmax(y_pred, dimension=1)
cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=logits,labels=y_true)
cost = tf.reduce_mean(cross_entropy)
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.5).minimize(cost)
correct_prediction = tf.equal(y_pred_cls, y_true_cls)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
session = tf.Session()
session.run(tf.global_variables_initializer())


batch_size = 100  

def optimize(num_iterations):
    for i in range(num_iterations):
        # obteniendo el batch de las imagenes dfe prueba
        # x_batch now holds a batch of images and
        # y_true_batch are the true labels for those images.
        x_batch, y_true_batch = data.train.next_batch(batch_size)

        # Put the batch into a dict with the proper names
        # for placeholder variables in the TensorFlow graph.
        # Note that the placeholder for y_true_cls is not set
        # because it is not used during training.
        feed_dict_train = {x: x_batch,
                           y_true: y_true_batch}

        # Run the optimizer using this batch of training data.
        # TensorFlow assigns the variables in feed_dict_train
        # to the placeholder variables and then runs the optimizer.
        session.run(optimizer, feed_dict=feed_dict_train)
        
feed_dict_test = {x: data.test.images,
                  y_true: data.test.labels,
                  y_true_cls: data.test.cls}
def print_accuracy():
    # Use TensorFlow to compute the accuracy.
    acc = session.run(accuracy, feed_dict=feed_dict_test)

    # Print the accuracy.
    print("Presición sobre el conjunto de datos: {0:.1%}".format(acc))

def print_confusion_matrix():
    # Get the true classifications for the test-set.
    cls_true = data.test.cls

    # Get the predicted classifications for the test-set.
    cls_pred = session.run(y_pred_cls, feed_dict=feed_dict_test)

    # Get the confusion matrix using sklearn.
    cm = confusion_matrix(y_true=cls_true,
                          y_pred=cls_pred)

    # Print the confusion matrix as text.
    print(cm)

    # Plot the confusion matrix as an image.
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)

    # Make various adjustments to the plot.
    plt.tight_layout()
    plt.colorbar()
    tick_marks = np.arange(num_classes)
    plt.xticks(tick_marks, range(num_classes))
    plt.yticks(tick_marks, range(num_classes))
    plt.xlabel('Predichos')
    plt.ylabel('Verdaderos')

def plot_weights():
    # Obtener los pesos de las imagenes.
    wi = session.run(w)

    # Obtener el valor mas pequeño y más alto de los pesos.
    # Es usado para corregir el color 
    # de esta manera poder comparar una imagen con otra.
    w_min = np.min(wi)
    w_max = np.max(wi)

    # Crea una figura de 3x4,
    
    fig, axes = plt.subplots(3, 4)
    fig.subplots_adjust(hspace=0.3, wspace=0.3)

    for i, ax in enumerate(axes.flat):
        # usa solo los pesos menores de 10.
        if i<10:
            # Get the weights for the i'th digit and reshape it.
            # Note that w.shape == (img_size_flat, 10)
            image = wi[:, i].reshape(img_shape)

            # Set the label for the sub-plot.
            ax.set_xlabel("Pesos: {0}".format(i))

            # Plot the image.
            ax.imshow(image, vmin=w_min, vmax=w_max, cmap='seismic')

        # Remove ticks from each sub-plot.
        ax.set_xticks([])
        ax.set_yticks([])
        
print_accuracy()

optimize(num_iterations=1)
print_accuracy()
plot_weights()
# We have already performed 1 iteration.
optimize(num_iterations=9)
print_accuracy()
plot_weights()
optimize(num_iterations=5000)
print_accuracy()
plot_weights()
print_confusion_matrix()
session.close()