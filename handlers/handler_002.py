# encoding=utf-8
from handlers.public import Request
from tornado import gen

class GetHandler(Request):
    '''该Handler完成主观题词频协议：'''
    @gen.coroutine
    def get(self):
        """处理GET请求,允许url带参数 school=河北大学&tihao=qishisan"""
        run = Getdata()
        school = self.get_argument("school")
        tihao = self.get_argument("tihao")
        res = run.run(school,tihao)
        self.set_header("Content-Type", "application/json")
        self.write({"qishisan":str(res)})


import jieba
from collections import Counter
import pymysql
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

class Getdata():

    def data(self,name, tihao):
        # 打开数据库连接
        db = pymysql.connect(host='localhost', user='root', passwd='root', db='shengshuju', charset='utf8')

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # SQL 查询语句
        sql = "SELECT " + tihao + " FROM shengzongshuju WHERE (" + tihao + "!='无')and(" + tihao + "!='(空)')and(学校名称='"+name+"')"
        txt = ""
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                qishisan = row[0]
                # 打印结果
                txt += qishisan
        except:
            print("Error: unable to fetch data")

        # 关闭数据库连接
        db.close()
        if tihao == "qishisan":
            th = "七十三"
        else:
            th = "七十四"
        return txt, name, th

    def get_words(self,txt, name, th):

        # 使用cursor()方法获取操作游标
        # 词权重
        list1 = []
        zidian = {}
        seg_list1 = jieba.cut_for_search(txt)
        list1.append(" ".join(seg_list1))
        vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
        transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
        tfidf = transformer.fit_transform(
            vectorizer.fit_transform(list1))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
        word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
        weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
        for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
            for j in range(len(word)):
                zidian[word[j]] = weight[i][j]
        # 词频
        seg_list = jieba.cut(txt)
        c = Counter()
        stopwords = [line.strip() for line in open("./configfiles/stopdata.txt", 'r', encoding='utf-8').readlines()]
        del stopwords[0]
        for x in seg_list:
            if x not in stopwords:
                if len(x) > 1 and x != '\r\n':
                    c[x] += 1

        ths = ""
        if th == "七十四":
            ths = "qishisi"
        else:
            ths = "qishisan"
        indata = {}
        for (k, v) in c.most_common(100):
            if k in zidian:
                indata[k] = [str(v), str(round(zidian[k], 5))]
            else:
                indata[k] = [str(v), "null"]
        return indata

    def run(self, xuexiaoname,tihao):
            txt = self.data(xuexiaoname, tihao)
            return self.get_words(txt[0], txt[1], txt[2])