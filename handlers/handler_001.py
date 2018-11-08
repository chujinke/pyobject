# encoding=utf-8
from handlers.public import Request
from tornado import gen

class GetHandler(Request):
    '''该Handler完成云图生成协议：'''
    @gen.coroutine
    def get(self):
        """处理GET请求,允许url带参数school=河北大学"""
        run = Getdata()
        protocol =  self.request.protocol
        url = self.request.host
        arg = self.get_argument("school")
        res = run.run(arg)
        for i in range(len(res)):
            res[i] = protocol +"://"+ url + res[i]

        res_data = {"wordcloud_url":res}
        self.set_header("Content-Type", "application/json")
        self.write( res_data)




import jieba
from collections import Counter
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from os import path
import pymysql
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud, ImageColorGenerator

class Getdata():

    def data(self,name, tihao):
        # 打开数据库连接
        db = pymysql.connect(host='localhost', user='root', passwd='root', db='shengshuju', charset='utf8')

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # SQL 查询语句
        sql = "SELECT " + tihao + ",专业代码 FROM shengzongshuju WHERE (" + tihao + "!='无')and(" + tihao + "!='(空)')and(学校名称='"+name+"')"
        txt = ""
        zydaima  =''
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            zydaima = results[0][1]
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
        return txt, name, th,zydaima

    def get_words(self,txt, name, th,zydaima):
        th = th.decode("utf-8")
        tihao = {"七十三":73,"七十四":74}
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
        list = []
        for (k, v) in c.most_common(60):
            list.append(k)
        wl = " ".join(list)
        d = path.dirname(__file__)
        alice_coloring = np.array(Image.open(path.join(r"./configfiles/abc.jpg")))
        wc = WordCloud(background_color="#263661",  # 设置背景颜色
                       mask=alice_coloring,  # 设置背景图片
                       max_words=2000,  # 设置最大显示的字数
                       font_path=r"./configfiles/STCAIYUN.TTF", # 设置中文字体，使得词云可以显示（词云默认字体是“DroidSansMono.ttf字体库”，不支持中文）
                       max_font_size=100,  # 设置字体最大值
                       random_state=30,  # 设置有多少种随机生成状态，即有多少种配色方案
                       )
        myword = wc.generate(wl)  # 生成词云
        bg = np.array(Image.open(r"./configfiles/bg.png"))
        image_colors = ImageColorGenerator(bg)
        plt.imshow(myword.recolor(color_func=image_colors))
        wc.to_file(r"./img/2017_" + zydaima + "_" + str(tihao[th]) + ".png")
        return r"/static/2017_" + zydaima + "_" + str(tihao[th]) + ".png"

    def run(self,xuexiaoname):
        img_url = []
        tihao = ["qishisan", "qishisi"]
        for j in range(len(tihao)):
            txt = self.data(xuexiaoname, tihao[j])
            img_url.append(self.get_words(txt[0], txt[1], txt[2].encode("utf-8"),txt[3]))
        return img_url




