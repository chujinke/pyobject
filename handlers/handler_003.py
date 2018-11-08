# encoding=utf-8
from handlers.public import Request
from tornado import gen

class PostHandler(Request):
    """
    处理关联性分析，和回归分析，参数school=河北大学&tihao=qishisan&all=0
    """

    @gen.coroutine
    def get(self):
        """处理POST请求 """
        school = self.get_argument("school")##学校
        tihao = self.get_argument("tihao")##题号
        all = int(self.get_argument("all"))##是否显示全部
        data = {"julei":run(school, tihao, all)}
        self.write(data)




##聚类
from collections import Counter
import jieba
import numpy as np
import math
import pymysql


def data(name,tihao):
    # 打开数据库连接

    db = pymysql.connect(host='localhost', user='root', passwd='root', db='shengshuju', charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT " + tihao +" FROM shengzongshuju WHERE (" + tihao + "!='无')and(" + tihao + "!='(空)')and(学校名称='" + name + "')"
    txt = ""
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            qishisan = row[0]
            # 打印结果
            txt +=qishisan+"\n"
    except:
        print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()
    return txt ,name

# 向量的模
def mo(list):
    x = 0
    for i in list:
        x = x + i**2
    return  math.sqrt(x)

def run(school,tihao,all):
    # 将文本中的词语转换为词频矩阵
    shili = data(school, tihao)
    txt = shili[0]
    seg_list = jieba.cut(txt)
    c = Counter()
    stopwords = [line.strip() for line in open("./configfiles/stopword2.txt", 'r', encoding='utf-8').readlines()]
    del stopwords[0]
    for x in seg_list:
        if x not in stopwords:
            if len(x) > 1 and x != '\r\n':
                c[x] += 1
    list = []
    for (k, v) in c.most_common(40):
        list.append(k)
    cen = txt.split("\n")
    cen1 = []
    cen2 = []
    sy = 0
    for i in cen:
        sy = sy + 1
        if i != '(空)' and i != "无" and i != "":
            cen1.append(str(sy) + " " + i)
            cen2.append(i)
    textxl = []
    for i in cen2:  # 词向量化
        textxl1 = []
        for j in list:
            if j in i:
                textxl1.append(1)
            else:
                textxl1.append(0)
        textxl.append(textxl1)
    Y = np.array(textxl)
    textxl20 = []
    for i in range(len(textxl)):  # 根据向量化的词矩阵，计算每条评论的词相似度
        textxl21 = []
        for j in range(i, len(textxl)):
            xlcj = np.dot(Y[i], Y[j])
            xlmc = mo(Y[i]) * mo(Y[j])
            if xlmc != 0:
                textxl21.append(xlcj / xlmc)
            else:
                textxl21.append(0)
        textxl20.append(textxl21)
    result = []
    result_item = []
    for i in range(len(textxl20)):  # 将评论之间的词相似度大于0.6（可以更改）的归并为一类。
        result1 = []
        if i in result_item:
            continue
        else:
            for j in range(len(textxl20[i]) - i):
                if textxl20[i][j] > 0.6:
                    result1.append(cen2[j + i])
                    result_item.append((j + i))
        result.append(result1)
    indata = []
    for i in range(len(result)):
        if len(result[i]) > 0:
            indata1 = [result[i][0], len(result[i])]
            indata.append(indata1)

    indata = sorted(indata, key=(lambda x: x[1]),reverse=True)
    if all !=1:
        indata = indata[0:10]



    return indata
