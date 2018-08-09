import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
from random import randint

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


def getDataArrays():
    inputArr = []
    outputArr = []
    with open("piece.txt") as f:
        for line in f:
            if randint(0, 9) > 6:
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

    return np.array(inputArr), np.array(outputArr)


def train_neural_network(x):

    prediction = neural_network_model(x)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))
    optimizer = tf.train.AdamOptimizer().minimize(cost)

    saver = tf.train.Saver()

    hm_epochs = 200
    with tf.Session() as sess:

        sess.run(tf.global_variables_initializer())


        #loads old model
        try:
            saver.restore(sess, "./chessModel/PieceNN/chessPieceModel.ckpt")
            print("Model Loaded")
        except:
            pass


        # for epoch in range(hm_epochs):
        #
        #     epoch_loss = 0
        #
        #     epoch_x, epoch_y = getDataArrays()
        #
        #     for _ in range(100):
        #
        #         _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})
        #
        #         epoch_loss += c
        #
        #     print('Epoch', epoch, 'completed out of', hm_epochs, 'loss:', epoch_loss)
        #     saver.save(sess, "./chessModel/PieceNN/chessPieceModel.ckpt")

        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))

        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))

        tI, tO = getDataArrays()
        print('Accuracy:', accuracy.eval({x: tI, y: tO}))


train_neural_network(x)