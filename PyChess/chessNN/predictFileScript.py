import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

n_nodes_hl1 = 500
n_nodes_hl2 = 500
n_nodes_hl3 = 500

n_classes = 8
batch_size = 100

x = tf.placeholder('float', [None, 64])
y = tf.placeholder('float')


def neural_network_model(data):
    hidden_1_layer = {'weights': tf.Variable(tf.random_normal([64, n_nodes_hl1])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl1]))}

    hidden_2_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl1, n_nodes_hl2])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl2]))}

    hidden_3_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl2, n_nodes_hl3])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl3]))}

    output_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl3, n_classes])),
                    'biases': tf.Variable(tf.random_normal([n_classes])), }

    l1 = tf.add(tf.matmul(data, hidden_1_layer['weights']), hidden_1_layer['biases'])
    l1 = tf.nn.relu(l1)

    l2 = tf.add(tf.matmul(l1, hidden_2_layer['weights']), hidden_2_layer['biases'])
    l2 = tf.nn.relu(l2)

    l3 = tf.add(tf.matmul(l2, hidden_3_layer['weights']), hidden_3_layer['biases'])
    l3 = tf.nn.relu(l3)

    output = tf.matmul(l3, output_layer['weights']) + output_layer['biases']

    return output

def getTestDataArrays():

    inputArr = []

    boardString = sys.argv[1]

    input = boardString.split(' ')

    i = [0.0] * 64
    for x in range(len(input)):
        i[x] = input[x]

    inputArr.append(i)

    return np.array(inputArr)

def test_neural_network(x):

    prediction = neural_network_model(x)

    saver = tf.train.Saver()

    config = tf.ConfigProto(
        device_count={'GPU': 0}
    )

    with tf.Session() as sess:

        sess = tf.Session(config=config)

        saver.restore(sess, "./chessNN/chessModel/FileNN/chessFileModel.ckpt")
        it = getTestDataArrays()

        spot = 0

        predicted = sess.run(prediction, feed_dict={x: it})[spot].tolist()
        #print(predicted)

        max = -sys.maxsize
        second = -sys.maxsize
        third = -sys.maxsize

        maxIndex = 0
        secondIndex = 0
        thirdIndex = 0

        for i in range(len(predicted)):
            if predicted[i] > max:
                second = max
                secondIndex = maxIndex
                max = predicted[i]
                maxIndex = i
            elif predicted[i] > second:
                third = second
                thirdIndex = secondIndex
                second = predicted[i]
                secondIndex = i
            elif predicted[i] > third:
                third = predicted[i]
                thirdIndex = i

        print(maxIndex+1)
        print(secondIndex+1)
        print(thirdIndex+1)
        # print(ot[spot])

test_neural_network(x)