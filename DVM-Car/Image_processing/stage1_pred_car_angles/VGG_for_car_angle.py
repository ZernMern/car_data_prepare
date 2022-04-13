import os
import sys
import tensorflow as tf
import numpy as np
from own_pathes import own_path_d

#=================================================Variable Setting=============================================================

print(sys.argv)
test_data_ = sys.argv[1]
data_size_ = int(sys.argv[2])
saved_model_pa = sys.argv[3]
iden_rst_pa = sys.argv[4]

batch_size_ = 10
last_layer_label_length_ = 9
input_label_length_ = 1
low_conv_train_ = True
int_label_ = False
lr_ = 0.0001

#================================================= Graph ===============================================================
def read_single_example(file_que):
    filename_queue = tf.train.string_input_producer(file_que, num_epochs=None)
    reader = tf.TFRecordReader()

    _, seri_example = reader.read(filename_queue)
    if int_label_:
        fea_d = {'label': tf.FixedLenFeature([input_label_length_], tf.int64),  'image': tf.FixedLenFeature([224 * 224 * 3], tf.float32)}
    else:
        fea_d = {'label': tf.FixedLenFeature([input_label_length_], tf.float32), 'image': tf.FixedLenFeature([224 * 224 * 3], tf.float32)}

    features = tf.parse_single_example(seri_example, features=fea_d)
    label = features['label']
    image = features['image']
    return label, image

def get_batch_data():
    fn_queues = [test_data_]
    label, image = read_single_example(fn_queues)
    images_batch, labels_batch = tf.train.batch([image, label], batch_size=batch_size_, capacity=100, allow_smaller_final_batch=True)
    return images_batch, labels_batch

def def_conv_layer(in_data,name_scope,k_shape):
    global parameters
    with tf.name_scope(name_scope) as scope:
        kernel = tf.Variable(tf.truncated_normal(k_shape, dtype=tf.float32, stddev=1e-1), trainable=low_conv_train_ ,name='weights')
        biases = tf.Variable(tf.constant(0.0, shape=[k_shape[-1]], dtype=tf.float32), trainable=low_conv_train_, name='biases')

        conv = tf.nn.conv2d(in_data, kernel, [1, 1, 1, 1], padding='SAME')
        out = tf.nn.bias_add(conv, biases)

        parameters += [kernel, biases]
        return tf.nn.relu(out, name=scope)


def deal_class(probs_in, labels,rst_l):
    for row in range(batch_size_):
        try:
            this_r = []
            pred_idx = np.argmax(probs_in[row,:])
            rst_l.append([labels[row][0], pred_idx, probs_in[row, pred_idx]])
        except:
            None
    return rst_l





images_batch, labels_batch = get_batch_data()
images_batch = tf.cast(images_batch,tf.float32)

input_layer = tf.reshape(images_batch, [-1, 224, 224,3])
parameters = []

# zero-mean input
with tf.name_scope('preprocess') as scope:
    mean = tf.constant([123.68, 116.779, 103.939], dtype=tf.float32, shape=[1, 1, 1, 3], name='img_mean')
    images = input_layer-mean



conv1_1 = def_conv_layer(images,'conv1_1',k_shape=[3, 3, 3, 64])

conv1_2 = def_conv_layer(conv1_1,'conv1_2',k_shape=[3, 3, 64, 64])

pool1 = tf.nn.max_pool(conv1_2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', name='pool1')

conv2_1 = def_conv_layer(pool1,'conv2_1',k_shape=[3, 3, 64, 128])

conv2_2 = def_conv_layer(conv2_1,'conv2_2',k_shape=[3, 3, 128, 128])

pool2 = tf.nn.max_pool(conv2_2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', name='pool2')

conv3_1 = def_conv_layer(pool2,'conv3_1',k_shape=[3, 3, 128, 256])

conv3_2 = def_conv_layer(conv3_1,'conv3_2',k_shape=[3, 3, 256, 256])

conv3_3 = def_conv_layer(conv3_2,'conv3_3',k_shape=[3, 3, 256, 256])

pool3 = tf.nn.max_pool(conv3_3,ksize=[1, 2, 2, 1],strides=[1, 2, 2, 1],padding='SAME',name='pool3')

conv4_1 = def_conv_layer(pool3,'conv4_1',k_shape=[3, 3, 256, 512])

conv4_2 = def_conv_layer(conv4_1,'conv4_2',k_shape=[3, 3, 512, 512])

conv4_3 = def_conv_layer(conv4_2,'conv4_3',k_shape=[3, 3, 512, 512])

pool4 = tf.nn.max_pool(conv4_3, ksize=[1, 2, 2, 1],strides=[1, 2, 2, 1],padding='SAME',name='pool4')

conv5_1 = def_conv_layer(pool4,'conv5_1',k_shape=[3, 3, 512, 512])

conv5_2 = def_conv_layer(conv5_1,'conv5_2',k_shape=[3, 3, 512, 512])

conv5_3 = def_conv_layer(conv5_2,'conv5_3',k_shape=[3, 3, 512, 512])

pool5 = tf.nn.max_pool(conv5_3,ksize=[1, 2, 2, 1],strides=[1, 2, 2, 1],padding='SAME',name='pool5')

with tf.name_scope('fc1') as scope:
    shape = int(np.prod(pool5.get_shape()[1:]))
    fc1w = tf.Variable(tf.truncated_normal([shape, 4096],dtype=tf.float32,stddev=1e-1), name='weights')
    fc1b = tf.Variable(tf.constant(1.0, shape=[4096], dtype=tf.float32), trainable=True, name='biases')
    pool5_flat = tf.reshape(pool5, [-1, shape])
    fc1l = tf.nn.bias_add(tf.matmul(pool5_flat, fc1w), fc1b)
    fc1 = tf.nn.relu(fc1l)
    parameters += [fc1w, fc1b]

# fc2
with tf.name_scope('fc2') as scope:
    fc2w = tf.Variable(tf.truncated_normal([4096, 4096], dtype=tf.float32,stddev=1e-1), name='weights')
    fc2b = tf.Variable(tf.constant(1.0, shape=[4096], dtype=tf.float32), trainable=True, name='biases')
    fc2l = tf.nn.bias_add(tf.matmul(fc1, fc2w), fc2b)
    fc2 = tf.nn.relu(fc2l)
    parameters += [fc2w, fc2b]

# fc3
with tf.name_scope('fc3') as scope:
    fc3w = tf.Variable(tf.truncated_normal([4096, last_layer_label_length_],dtype=tf.float32,stddev=1e-1), name='weights')
    fc3b = tf.Variable(tf.constant(1.0, shape=[last_layer_label_length_], dtype=tf.float32),trainable=True, name='biases')
    fc3l = tf.nn.bias_add(tf.matmul(fc2, fc3w), fc3b)
    parameters += [fc3w, fc3b]

probs = tf.nn.softmax(fc3l)

# loss = tf.reduce_mean(tf.square(fc3l- labels_batch))

which_neuro =  tf.constant([0])
this_n_val = tf.reduce_mean(conv5_1[:, :, :, which_neuro[0]])

# this_n_val = tf.reduce_mean(fc3w[:,:,which_neuro[0]])

loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = fc3l,labels = labels_batch))

grads = tf.gradients(this_n_val,input_layer)

trainable_v =[v.name for v in tf.trainable_variables()]

#================================================= Runing =================================================


saver = tf.train.Saver(max_to_keep=100)
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    saver.restore(sess, saved_model_pa)
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord = coord)

    one_round_epoch = int(round(data_size_/float(batch_size_)))
    rst_l = []
    for epoch in range(one_round_epoch):
        pass_rst = sess.run([probs, labels_batch])
        rst_l = deal_class(pass_rst[0], pass_rst[1], rst_l)

    with open(iden_rst_pa, 'w') as f_out:
        f_out.write(str(rst_l))
    coord.request_stop()
    coord.join(threads)
