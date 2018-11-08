# encoding=utf-8
from config.rewrite import RequestHandler
from tornado import gen
class GetHandler(RequestHandler):
    """  处理关联性分析，和回归分析，参数school=河北大学&all=0"""

    @gen.coroutine
    def get(self):
        """处理GET请求"""
        # 获取题目
        title_list = []
        with open('./configfiles/title_list.txt') as f:
            title = f.readlines()
            for i in title:
                title_list.append(i.strip())
        school = self.get_argument("school")##学校
        all = int(self.get_argument("all"))##是否显示全部
        answer, word = load_data(school)
        entire, question = cal_data(answer, title_list)
        xiangguanresult = cal_confidence(school, entire, title_list, answer, question,all)
        regression1 = regression(answer, title_list,all)
        data = {"guanlian":xiangguanresult,"regression":regression1}
        self.write(data)


import pymysql
import numpy
from sklearn.linear_model import LinearRegression
def load_data(school):
    # 打开数据库连接
    db = pymysql.connect(host='localhost', user='root', passwd='root', db='shengshuju', charset='utf8')

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT * FROM shengzongshuju where 学校名称='%s'" %(school)

    # answer_list包含选择题答案
    answer_list = []
    # word_list包含71,72主观题
    word_list = []
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            answer = []
            for col in range(2, 74):
                answer.append(row[col])
            answer_list.append(answer)
            word = []
            for colu in range(74, 76):
                word.append(row[colu])
            word_list.append(word)
    except:
        print("Error: unable to fetch data")
    db.close()
    return answer_list, word_list

#计算答案比例,输入参数答案列表，题目列表，返回数据字典
def cal_data(answer,title):
    # print(answer[0])
    # 整体分析部分，{第一题：{满意1:10，一般：20}，第二题：{满意1:10，一般：20}}
    entire = {}
    #s设置默认字典格式
    for i in title:
        entire.setdefault(i,{})
    #计算每一个选项出现的次数
    for row in range(len(answer)):
        for i in range(72):
            if answer[row][i] in entire[title[i]]:
                entire[title[i]][answer[row][i]] +=1
            else:
                entire[title[i]][answer[row][i]] = 1
    #计算每一题答案的比例P(A)
    for m in range(len(entire)):
        for n in entire[title[m]].keys():
            entire[title[m]][n] = round(entire[title[m]][n]/len(answer),4)

    # print(entire[title[0]][answer[0][0]])
    #统计题目和答案
    question = {}
    for key,value in entire.items():
        list1 = []
        for i in value.keys():
            list1.append(i)
        question[key] = list1
    return entire,question
#统计比例，传入每一题选项个数字典，问题，答案，返回比例
def analyze(data,question,answer):
    a = round(data[question][answer]/2534,4)
def cal_confidence(school,entire,title,answer,question,all):

    result = {}
    #confidence = P(B|A) = P(AB)/P(A)
    answer72 = ['1. 非常不符合', '2. 不符合',  '3. 不确定（说不好）','4. 符合', '5. 非常符合']
    for i in range(len(title)-1):
        for j in range(len(entire[title[i]])):
            for h in range(len(entire[title[i]])):
                # 第i题j选项----->72题m选项的置信度
                try:
                    confidence = conf(i, question[title[i]][j], answer72[h], answer)/entire[title[i]][question[title[i]][j]]
                    if confidence >= 0.5 and confidence < 0.9999:
                        result[title[i]+question[title[i]][j]+'-->'+answer72[h]] = round(confidence,4)
                except:
                    pass
    result_list = sorted(result.items(), key=lambda x: x[1],reverse=True)
    if all!=1:
        result_list = result_list[0:10]
    return result_list

def conf(i,j,h,answer):
    count = 0
    for m in range(len(answer)):
        if answer[m][i] == j and answer[m][71] == h:
            count += 1
    return count/len(answer)
    # print(j)

def regression(answer,title,all):
    #传入answer（72列n行），title（72列1行）,计算每道题回归系数，排序，以字典形式输出
    #将数据集转换成矩阵形式
    result = []
    for i in range(71):
        answer_list = []
        result_list = []
        for row in range(len(answer)):
            answer_list.append(int(answer[row][i][0]))
            result_list.append(int(answer[row][-1][0]))
        answer_mat = numpy.mat(answer_list).T
        result_mat = numpy.mat(result_list).T
        linreg = LinearRegression()
        model = linreg.fit(answer_mat, result_mat)
        a = linreg.coef_.tolist()[0][0]
        a = round(a,4)
        result.append(a)
        # print(title[i],a)
    #将题目和回归系数存进字典
    result_dict = {}
    for m in range(len(title)-1):
        result_dict[title[m]] = result[m]
    #将字典按value排序生成list
    value = sorted(result_dict.items(),key=lambda item:item[1],reverse=True)
    if all!=1:
        value = value[0:10]

    return value