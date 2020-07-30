# 功能清单
# 1.查找985院校的投档分数线，排名
# 2.查找211院校的投档分数线，排名
# 3.查找湖北一本院校投档分数线，排名
# 4.输入分数，排名，查找最接近的985，211，湖北一本院校
# 查找过程
# 1.加载院校名称txt
# 2.生成院校EXCEL模板文件
# 3.根据院校名称到相应的工作簿里依次查找相应分数
# 4.根据分数查找当年的一分一段表的排名及人数，计算排名平均值，即当前排名加分数段人数的一半
# 5.根据生成结果计算四年的平均分，平均排名等
# 6.根据输入分数，查找合适的院校

import xlrd
import xlwt
import requests
from lxml import etree

workbook = xlrd.open_workbook("14-19一分一段表及16-19一批投档线(理工).xlsx")
sheet_names = workbook.sheet_names()


def getScore(schoolName):
    scores = []
    for i in range(len(sheet_names) - 1):
        sheet = workbook.sheet_by_name(sheet_names[i + 1])
        for j in range(sheet.nrows):
            for k in range(sheet.ncols):
                cell_value = sheet.cell_value(j, k)
                if schoolName == str(cell_value):
                    if "普通类" in sheet.cell_value(j,k+1):
                        score = {
                            "schoolName":cell_value,
                            "score":int(float(sheet.cell_value(j,k+2))),
                            "years":2019 - i
                        }
                        scores.append(score)
    return scores

def getRating(score):
    sheet = workbook.sheet_by_index(0)
    if score['score'] > 680:
        return 1.0

    if(score['years'] == 2019):
        for i in range(sheet.nrows - 50):
            if str(score["score"]) in str(sheet.cell_value(i + 10,0)):
                return float(sheet.cell_value(i + 10,2)) + (float(sheet.cell_value(i + 10,1))/2)

    if(score['years'] == 2018):
        for i in range(sheet.nrows -50):
            if str(score["score"]) in str(sheet.cell_value(i + 10,4)):
                return float(sheet.cell_value(i + 10,6)) + (float(sheet.cell_value(i + 10,5))/2)

    if(score['years']== 2017):
        for i in range(sheet.nrows - 50):
            if str(score["score"]) in str(sheet.cell_value(i + 10,8)):
                return float(sheet.cell_value(i + 10,10)) + (float(sheet.cell_value(i + 10,9))/2)

    if(score['years'] == 2016):
        for i in range(sheet.nrows - 50):
            if str(score["score"]) in str(sheet.cell_value(i + 10,12)):
                return float(sheet.cell_value(i + 10,14)) + (float(sheet.cell_value(i + 10,13))/2)

    print ( score["schoolName"] + str(score['years']) + '分数查不到：' + str(score['score']) )
    return 0.0

def getSchoolName(fileName):
    f = open(fileName,'r',encoding='utf-8')
    return f.readlines()

def getSchoolAll():
    sheet = workbook.sheet_by_name(sheet_names[1])
    f = open("collegeAll.txt",'w',encoding='utf-8')
    for i in range(sheet.nrows - 2):
        if sheet.cell_value(i + 2,1) != "":
            #print(i)
            #print(sheet.cell_value(i+2,1))
            f.write(sheet.cell_value(i+2,1) + "\n")
    f.close()

def getCollegeList():
    headers = {  
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363'
    }
    response = requests.get("http://www.moe.gov.cn/srcsite/A22/s7065/200512/t20051223_82762.html", headers = headers)
    text = response.content.decode('utf-8')
    html = etree.HTML(text)
    nameStrings = html.xpath("//table[@class='MsoNormalTable']/tbody//span//text()") #xpath语法
    with open("collegeName.txt",'w',encoding='utf-8') as fp:
        print("ready!")
        i = 0
        for nameString in nameStrings:
            fp.write(nameString + '\n')
            print("写入第{}行".format(i))
            i = i + 1
        print("OK!")
        fp.close()

def single(school):
    scores = getScore(school)
    if(len(scores) == 0):
        print(school + "此学校在湖北不招理科生！！！")
    schoolRating = 0.0
    numbers = []
    for score in scores:
        r = getRating(score)
        schoolRating += r / float(len(scores))
        numbers.append(score["score"])
        numbers.append(r)
        print(score)
    print(numbers)

    if schoolRating == 0:
        print("学校排名出错！！")
    else:
        schoolMessage = {
            "school":school,
            "rating": int(schoolRating) - 1
        }
        print(schoolMessage)

if __name__ == "__main__":
    schoolRatings = []
    f = open("collegeOfAll.txt",'w',encoding='utf-8')
    for school in getSchoolName("collegeAll.txt"):
        # 得到分数
        schoolName = school.strip()
        scores = getScore(schoolName)
        if(len(scores) == 0):
            print(schoolName + " 此学校在湖北不招理科生！！！")

        # 得到排名
        schoolRating = 0.0
        for score in scores:
            r = getRating(score)
            schoolRating += r / float(len(scores))

        # 储存信息
        if schoolRating < 0:
            print(schoolName + " 学校排名出错！！")
        else:
            schoolMessage = {
                "school":school,
                "rating": int(schoolRating) - 1
            }
            schoolRatings.append(schoolMessage)

            # 根据一定的要求筛选学校信息
            if (schoolMessage["rating"] > 19000) and (schoolMessage["rating"] < 22000):
                print(schoolMessage)
                f.write(school)
    
    print(schoolRatings)
    f.close()