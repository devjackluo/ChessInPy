import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

n_nodes_hl1 = 500
n_nodes_hl2 = 500
n_nodes_hl3 = 500

n_classes = 2
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

    allBoardStrings = sys.argv[1]

    #inputs = boardStrings.split('\n')
    # for _ in range(len(inputs)):
    #     input = boardStrings.split(' ')
    #     i = [0.0] * 64
    #     for x in range(len(input)):
    #         i[x] = input[x]
    #
    #     inputArr.append(i)

    inputs = allBoardStrings.split('\n')
    for i in range(len(inputs) - 1):
        #print(inputs[i])
        input = inputs[i].split(' ')
        b = [0.0] * 64
        for x in range(len(input)):
            b[x] = input[x]
        inputArr.append(b)

    return np.array(inputArr)

def test_neural_network(x):

    prediction = neural_network_model(x)

    saver = tf.train.Saver()

    config = tf.ConfigProto(
        device_count={'GPU': 0}
    )

    with tf.Session() as sess:

        sess = tf.Session(config=config)

        saver.restore(sess, "./chessNN/chessModel/SideNN/chessSideModel.ckpt")
        it = getTestDataArrays()

        #spot = 0

        predicted = sess.run(prediction, feed_dict={x: it})

        for i in predicted:
            #print(np.argmax(i))
            #print(predicted)
            max = -sys.maxsize
            maxIndex = 0

            for j in range(len(i)):
                if i[j] > max:
                    max = i[j]
                    maxIndex = j

            print(maxIndex)


test_neural_network(x)