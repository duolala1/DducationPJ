# coding:utf-8
'''
author:Fang
date:2017/5/3
function:文本分类

本程序先使用结巴分词将所有文本分割成词语形式；
然后在去除停用词和长度过小词语过后生成词袋
使用TF-IDF算法给出词袋中所有词语在某个特定文本中的TF-IDF值
以此数值结合阈值可提取文本中关键词

而TF-IDF矩阵本身则反映了各个文本的特征，并且稀疏
因此可直接使用DNN对文本内容进行分析
'''
import pickle
import jieba
import jieba.posseg as pseg
import os
import sys
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import tensorflow as tf

def getTF_IDF(texts):
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
# 将测试数据和词袋传入，返回TF-IDF数值
def testTF_IDF(sample,words):
    resultTexts = []
    sampleCut = pseg.cut(sample[0])
    result = ""
    for key in sampleCut:
        result = result+" "+key.word
    resultTexts.append(result)

    vectorizer = CountVectorizer()
    #该类会统计每个词语的tf-idf权值
    transformer = TfidfTransformer()
    #第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    tfidf = transformer.fit_transform(vectorizer.fit_transform(resultTexts))
    wordBag = vectorizer.get_feature_names()
    weight=tfidf.toarray()

    resultWeight = [0]*len(words)
    for j in range(len(wordBag[0])):
        print (wordBag[j],weight[0][j])
        for t in range(len(words)):
            if words[t] == wordBag[j]:
                resultWeight[t] = weight[0][j]
    return resultWeight

# Method to generate a DNN layer
def add_layer(input,input_size,output_size,activation_function = None):
    Weights = tf.Variable(tf.random_normal([input_size,output_size]))
    bias = tf.Variable(tf.zeros([1,output_size])+0.01)
    Wx_plus_b = tf.matmul(input,Weights) + bias
    if activation_function is None:
        return Wx_plus_b
    else:
        return activation_function(Wx_plus_b)

def makePrediction(testText):
    wordsFile = file('words.pkl', 'rb') 
    words = pickle.load(wordsFile)
    testWeight = testTF_IDF(testText,words)
    # for i in range(len(weight)):
    #     print(u"-------这里输出第",i,u"类文本的词语tf-idf权重------" )
    #     for j in range(len(words)):
    #         print (words[j],weight[i][j])
    return words
    x_data = [testWeight]
    input_size = len(x_data[0])
    print 'size:',input_size
    output_size = 60

    layer_dimension = [10,20,10]
    num_of_layers = len(layer_dimension)

    step_num = 1000
    batch_size = 2

    all_dataset_size = len(x_data)
    dataset_size = all_dataset_size
    xs = tf.placeholder(tf.float32, [None, input_size], name='x')

    '''    Define the model structure     '''
    cur_layer = add_layer(xs, input_size, layer_dimension[0], activation_function=tf.nn.relu)

    in_dimension = layer_dimension[0]
    out_dimension = layer_dimension[1]

    for i in range(1, num_of_layers):
        out_dimension = layer_dimension[i]
        cur_layer = add_layer(cur_layer, in_dimension, out_dimension, activation_function=tf.nn.relu)
        in_dimension = out_dimension

    prediction = add_layer(cur_layer, out_dimension, output_size, activation_function=tf.nn.softmax)
    #模型保存加载工具
    saver = tf.train.Saver()

    #init = tf.initialize_all_variables()
    with tf.Session() as sess:
        #aver.restore(sess, "model/model.ckpt")
        #sess.run(init)
        result = sess.run(prediction, feed_dict={xs: x_data})
    return result

if __name__ == "__main__":
    texts = ["我来自中华人民共和国，为人民服务，为党的事业，成为党的事业接班人。",
             "天文知识是科学的一部分，我们要好好学习",
             "今天又学习了毛泽东概论，感觉我仿佛要升仙",
             "第一次来天文博物馆，贼球无聊，不就是几张照片吗，我儿子P的都比他好。"]
    testText = ["第一次来天文博物馆，贼球无聊，不就是几张照片吗，我儿子P的都比他好。"]
    labels = [0, 1, 0, 1]
    #weight,words = getTF_IDF(texts)
    print 'Prediction:', makePrediction(testText)