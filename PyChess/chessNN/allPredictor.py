import tensorflow as tf
import numpy as np
import sys


def piece_neural_network_model(self, data):

    n_nodes_hl1 = 500
    n_nodes_hl2 = 500
    n_nodes_hl3 = 500

    n_classes = 6

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

def filerank_neural_network_model(self, data):

    n_nodes_hl1 = 500
    n_nodes_hl2 = 500
    n_nodes_hl3 = 500

    n_classes = 8

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

def piece_neural_network(self, boardArray):

    containerArr = []

    i = [0.0] * 64
    for x in range(len(boardArray)):
        i[x] = boardArray[x]
    containerArr.append(i)
    finalArr = np.array(containerArr)

    saver = tf.train.Saver()

    piece_prediction = self.piece_neural_network_model(self.data)

    config = tf.ConfigProto(
        device_count={'GPU': 0}
    )
    sess = tf.Session(config=config)

    saver.restore(sess, "./chessNN/chessModel/PieceNN/chessmodel.ckpt")

    predicted = sess.run(piece_prediction, feed_dict={self.data: finalArr})[0].tolist()

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

    return maxIndex, secondIndex, thirdIndex

def rank_neural_network(self, boardArray):

    containerArr = []

    i = [0.0] * 64
    for x in range(len(boardArray)):
        i[x] = boardArray[x]
    containerArr.append(i)
    finalArr = np.array(containerArr)

    saver = tf.train.Saver()

    rank_prediction = self.filerank_neural_network_model(self.data)

    config = tf.ConfigProto(
        device_count={'GPU': 0}
    )
    sess = tf.Session(config=config)

    saver.restore(sess, "./chessNN/chessModel/RankNN/chessmodel.ckpt")

    predicted = sess.run(rank_prediction, feed_dict={self.data: finalArr})[0].tolist()

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

    return maxIndex, secondIndex, thirdIndex

def file_neural_network(self, boardArray):

    containerArr = []

    i = [0.0] * 64
    for x in range(len(boardArray)):
        i[x] = boardArray[x]
    containerArr.append(i)
    finalArr = np.array(containerArr)

    saver = tf.train.Saver()

    file_prediction = self.filerank_neural_network_model(self.data)

    config = tf.ConfigProto(
        device_count={'GPU': 0}
    )
    sess = tf.Session(config=config)

    saver.restore(sess, "./chessNN/chessModel/FileNN/chessmodel.ckpt")

    predicted = sess.run(file_prediction, feed_dict={self.data: finalArr})[0].tolist()

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

    return maxIndex, secondIndex, thirdIndex

