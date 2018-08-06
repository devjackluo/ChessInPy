import tensorflow as tf
import numpy as np
import sys

class PiecePredictor:

    n_nodes_hl1 = 500
    n_nodes_hl2 = 500
    n_nodes_hl3 = 500

    n_classes = 6
    batch_size = 100

    x = tf.placeholder('float', [None, 64])
    y = tf.placeholder('float')

    prediction = None
    sess = None
    saver = None

    def __init__(self):
        self.prediction = self.neural_network_model(self.x)

        self.saver = tf.train.Saver()

        config = tf.ConfigProto(
            device_count={'GPU': 0}
        )
        self.sess = tf.Session(config=config)


    def neural_network_model(self, data):
        hidden_1_layer = {'weights': tf.Variable(tf.random_normal([64, self.n_nodes_hl1])),
                          'biases': tf.Variable(tf.random_normal([self.n_nodes_hl1]))}

        hidden_2_layer = {'weights': tf.Variable(tf.random_normal([self.n_nodes_hl1, self.n_nodes_hl2])),
                          'biases': tf.Variable(tf.random_normal([self.n_nodes_hl2]))}

        hidden_3_layer = {'weights': tf.Variable(tf.random_normal([self.n_nodes_hl2, self.n_nodes_hl3])),
                          'biases': tf.Variable(tf.random_normal([self.n_nodes_hl3]))}

        output_layer = {'weights': tf.Variable(tf.random_normal([self.n_nodes_hl3, self.n_classes])),
                        'biases': tf.Variable(tf.random_normal([self.n_classes])), }

        l1 = tf.add(tf.matmul(data, hidden_1_layer['weights']), hidden_1_layer['biases'])
        l1 = tf.nn.relu(l1)

        l2 = tf.add(tf.matmul(l1, hidden_2_layer['weights']), hidden_2_layer['biases'])
        l2 = tf.nn.relu(l2)

        l3 = tf.add(tf.matmul(l2, hidden_3_layer['weights']), hidden_3_layer['biases'])
        l3 = tf.nn.relu(l3)

        output = tf.matmul(l3, output_layer['weights']) + output_layer['biases']

        return output

    def test_neural_network(self, boardArray):

        containerArr = []

        i = [0.0] * 64
        for x in range(len(boardArray)):
            i[x] = boardArray[x]
        containerArr.append(i)
        finalArr = np.array(containerArr)

        self.saver.restore(self.sess, "./chessNN/chessModel/PieceNN/chessPieceModel.ckpt")

        predicted = self.sess.run(self.prediction, feed_dict={self.x: finalArr})[0].tolist()
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

        return maxIndex, secondIndex, thirdIndex