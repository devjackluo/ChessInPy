import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
import sys

n_nodes_hl1 = 500
n_nodes_hl2 = 500
n_nodes_hl3 = 500

n_classes = 6
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
    outputArr = []
    with open("./chessNN/piece.txt") as f:
        for line in f:
            inputOutput = line.split("=")
            inputOutput[0] = inputOutput[0].replace("[", "").replace("]", "")
            input = inputOutput[0].split(',')

            i = [0.0] * 64
            for x in range(len(input)):
                i[x] = input[x]

            output = int(inputOutput[1])
            o = [0.0] * 6
            o[output-1] = 1.0

            inputArr.append(i)
            outputArr.append(o)

            if len(inputArr) > 10:
                return np.array(inputArr), np.array(outputArr)

        return np.array(inputArr), np.array(outputArr)

def test_neural_network(x):

    prediction = neural_network_model(x)

    saver = tf.train.Saver()

    config = tf.ConfigProto(
        device_count={'GPU': 0}
    )

    with tf.Session() as sess:

        sess = tf.Session(config=config)

        saver.restore(sess, "./chessNN/chessModel/PieceNN/chessPieceModel.ckpt")
        it, ot = getTestDataArrays()

        spot = 8

        predicted = sess.run(prediction, feed_dict={x: it})[spot].tolist()
        print(predicted)

        max = -sys.maxsize
        second = -sys.maxsize
        maxIndex = 0
        secondIndex = 0
        for i in range(len(predicted)):
            if predicted[i] > max:
                second = max
                secondIndex = maxIndex
                max = predicted[i]
                maxIndex = i
            elif predicted[i] > second:
                second = predicted[i]
                secondIndex = i

        print(maxIndex+1)
        print(secondIndex+1)
        print(ot[spot])

test_neural_network(x)