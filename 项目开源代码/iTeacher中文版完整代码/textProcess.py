# -*- coding:utf-8 -*-
import jieba
import jieba.posseg as pseg
import os
import sys
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import tensorflow as tf
import pickle
import sqlite3
def genWordVec(texts):
    resultTexts = []
    for text in texts:
        words = pseg.cut(text)
        result = ""
        for key in words:
            result = result+" "+key.word
        resultTexts.append(result)

    #该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer()
    #该类会统计每个词语的tf-idf权值
    transformer = TfidfTransformer()
    #第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    tfidf = transformer.fit_transform(vectorizer.fit_transform(resultTexts))
    wordBag = vectorizer.get_feature_names()
    length = len(wordBag)
    resultVec = []
    for text in texts:
        words = pseg.cut(text)
        temp = [0] * length
        i = 0
        for key in words:
            if key.word in wordBag:
                temp[i] = temp[i] + 1
            i = i + 1
        resultVec.append(temp)
    return resultVec,wordBag

def getTF_IDF(texts):
    resultTexts = []
    for text in texts:
        words = pseg.cut(text)
        result=""
        for key in words:
            result = result+" "+key.word
        resultTexts.append(result)

    #该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer()
    #该类会统计每个词语的tf-idf权值
    transformer = TfidfTransformer()
    #第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    tfidf = transformer.fit_transform(vectorizer.fit_transform(resultTexts))
    '''
    获取词袋模型中的所有词语
    词袋中不保留停用词和长度小于2的词语
    '''
    wordBag = vectorizer.get_feature_names()

    '''
    提取将tf-idf矩阵
    元素a[i][j]表示j词在i类文本中的tf-idf权重
    '''
    weight=tfidf.toarray()
    return weight,wordBag

# Method to generate a DNN layer
def add_layer(input,input_size,output_size,activation_function = None):
    Weights = tf.Variable(tf.random_normal([input_size,output_size],seed=2))
    bias = tf.Variable(tf.zeros([1,output_size])+0.01)
    Wx_plus_b = tf.matmul(input,Weights) + bias
    if activation_function is None:
        return Wx_plus_b
    else:
        return activation_function(Wx_plus_b)

if __name__ == "__main__":

    Xdata = []
    label_list = []
    conn = sqlite3.connect('db.sqlite3')

    cursor = conn.execute("SELECT * from model_bookinfo")
    cursor2 = conn.execute("SELECT * from model_labels")
    for row in cursor:
        Xdata.append(row[3])
    for row in cursor2:
        if row[2] not in label_list:
            label_list.append(row[2])

    Ydata = []
    label_num = len(label_list)

    cursor2 = conn.execute("SELECT * from model_labels")
    for row in cursor2:
        temp = [0] * label_num
        for i in range(label_num):
            if row[2] == label_list[i]:
                temp[i] = 1
        print temp
        Ydata.append(temp)

    print "Operation done successfully";
    cursor.close()
    conn.commit()
    conn.close()

    texts = Xdata
    labels = Ydata
    # weight,words = getTF_IDF(texts)
    weight,words = genWordVec(texts)
    wordsFile = file('model/words.pkl', 'wb') 
    pickle.dump(words,wordsFile)

    # Define the model params
    x_data = weight
    y_data = labels
    input_size = len(x_data[0])
    print 'size:',input_size
    output_size = label_num

    layer_dimension = [1000, 2000 ,1000]
    num_of_layers = len(layer_dimension)

    step_num = 100
    batch_size = 5

    all_dataset_size = len(x_data)
    dataset_size = all_dataset_size
    xs = tf.placeholder(tf.float32, [None, input_size], name='x')
    ys = tf.placeholder(tf.float32, [None, output_size], name='y')

    '''    Define the model structure     '''
    cur_layer = add_layer(xs, input_size, layer_dimension[0], activation_function=tf.nn.relu)

    in_dimension = layer_dimension[0]
    out_dimension = layer_dimension[1]

    for i in range(1, num_of_layers):
        out_dimension = layer_dimension[i]
        cur_layer = add_layer(cur_layer, in_dimension, out_dimension, activation_function=tf.nn.relu)
        in_dimension = out_dimension

    prediction = add_layer(cur_layer, out_dimension, output_size, activation_function=tf.nn.softmax)
    loss = -tf.reduce_sum(ys*tf.log(prediction+0.000001)) 
    # loss = tf.reduce_mean(tf.reduce_sum(ys*tf.log(prediction+0.000001), reduction_indices=[1]))
    # loss = tf.nn.softmax_cross_entropy_with_logits(prediction+1e-10,ys)
    cost = tf.reduce_mean(loss)
    # Using decayed learning rate
    global_step = tf.Variable(0)
    #learning_rate = tf.train.exponential_decay(2.0, global_step, 128, 0.96, staircase=True)
    train = tf.train.GradientDescentOptimizer(learning_rate=0.5).minimize(cost, global_step=global_step)
    #模型保存加载工具
    saver = tf.train.Saver()

    #判断模型保存路径是否存在，不存在就创建
    if not os.path.exists('model/'):
        os.mkdir('model/')
    # saver = tf.train.Saver()
    init = tf.initialize_all_variables()
    with tf.Session() as sess:

        sess.run(init)

        for i in range(step_num):

            start = (i * batch_size) % dataset_size
            end = min(start + batch_size, dataset_size)

            sess.run(train, feed_dict={xs: x_data[start:end], ys: y_data[start:end]})
            if i % 10 == 0:
                print 'Training Loss:', sess.run(loss, feed_dict={xs: x_data[start:end], ys: y_data[start:end]})
        saver_path = saver.save(sess, "model/model2.ckpt")
        print("Model saved in file:", saver_path)