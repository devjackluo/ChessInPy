import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
from random import randint

n_classes = 2
batch_size = 128

x = tf.placeholder('float', [None, 64])
y = tf.placeholder('float')

# dropout?
keep_rate = 0.8
keep_prob = tf.placeholder(tf.float32)


def conv2d(x, W):
    return tf.nn.conv2d(x, W,strides=[1,1,1,1], padding='SAME')

def maxpool2d(x):
    # ksize = size of window, stride is movement of window
    return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')

def convolutional_neural_network(x):

    weights = {'W_conv1': tf.Variable(tf.random_normal([2,2,1,16])),
               'W_conv2': tf.Variable(tf.random_normal([2,2,16,32])),
               'W_fc': tf.Variable(tf.random_normal([2*2*32, 256])),
               'out': tf.Variable(tf.random_normal([256, n_classes]))}

    biases = {'B_conv1': tf.Variable(tf.random_normal([16])),
               'B_conv2': tf.Variable(tf.random_normal([32])),
               'B_fc': tf.Variable(tf.random_normal([256])),
               'out': tf.Variable(tf.random_normal([n_classes]))}

    x = tf.reshape(x, shape=[-1,8,8,1])

    conv1 = conv2d(x, weights['W_conv1'])
    conv1 = maxpool2d(conv1)

    conv2 = conv2d(conv1, weights['W_conv2'])
    conv2 = maxpool2d(conv2)

    fc = tf.reshape(conv2, [-1, 2*2*32])
    fc = tf.nn.relu(tf.matmul(fc, weights['W_fc']) + biases['B_fc'])

    fc = tf.nn.dropout(fc, keep_rate)

    output = tf.matmul(fc, weights['out']) + biases['out']

    return output

def getDataArrays():
    inputArr = []
    outputArr = []
    with open("side.txt") as f:
        for line in f:
            if randint(0, 9) > 6:
                inputOutput = line.split("=")
                inputOutput[0] = inputOutput[0].replace("[", "").replace("]", "")
                input = inputOutput[0].split(',')

                i = [0.0] * 64
                for x in range(len(input)):
                    i[x] = input[x]

                output = int(inputOutput[1])
                o = [0.0] * 2
                o[output] = 1.0

                inputArr.append(i)
                outputArr.append(o)

    return np.array(inputArr), np.array(outputArr)

def train_neural_network(x):

    prediction = convolutional_neural_network(x)
    # OLD VERSION:
    # cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(prediction,y) )
    # NEW:
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))
    optimizer = tf.train.AdamOptimizer().minimize(cost)

    saver = tf.train.Saver()

    hm_epochs = 10
    with tf.Session() as sess:
        # OLD:
        # sess.run(tf.initialize_all_variables())
        # NEW:
        sess.run(tf.global_variables_initializer())


        # #loads old model
        # try:
        #     saver.restore(sess, "./chessModel/SideNN/chessSideModel.ckpt")
        #     print("Model Loaded")
        # except:
        #     pass


        for epoch in range(hm_epochs):
            epoch_loss = 0
            epoch_x, epoch_y = getDataArrays()
            for _ in range(2):
                _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})
                epoch_loss += c

            print('Epoch', epoch, 'completed out of', hm_epochs, 'loss:', epoch_loss)
            #saver.save(sess, "./chessModel/SideNN/chessSideModel.ckpt")

        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))

        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))

        tI, tO = getDataArrays()
        print('Accuracy:', accuracy.eval({x: tI, y: tO}))


train_neural_network(x)