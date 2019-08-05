# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine


def listdir(path, list_name):  # 传入存储的list
    for file in os.listdir(path):
        file_path = os.path.join(path , file)
        if os.path.isdir(file_path):
            listdir(file_path , list_name)
        else:
            list_name.append(file_path)
    # print(list_name)  # 虽然打印出来，但是最后的打印才是return的最后结果
    return list_name


# 获取一个路径下第一层，相同后缀的文件名列表
# 获取所有标注文件
def get_filenames(rootDir):
    L=[]
    list = os.listdir(rootDir) # 列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
        if os.path.splitext(list[i])[1] == '.csv':
            path = os.path.join(rootDir,list[i])
            L.append(path)
    return L
# 其中os.path.splitext()函数将路径拆分为文件名+扩展名


def data_read(rootDir):
    # engine = create_engine('mysql+pymysql://root:13787441982qq,,@localhost:3306/DeecampData?charset=utf8')
    list_name = []  # 需要在外层定义，才能获取当前路径所有文件名,试想在内层定义会如何
    list_name = listdir(rootDir, list_name)  # 返回当前路径下所有文件路径列表
    data_list = []
    for i in range(0, len(list_name)):
        if os.path.splitext(list_name[i])[1] == '.json':
            with open(list_name[i],'r',encoding='utf-8') as f:
                data = f.read()
                data_list.append(data)
            # df = data.astype(object).where(pd.notnull(data) , None)
            # tableName = os.path.splitext(list_name[i])[0].split('\\').pop()
            # df.to_sql(tableName, engine,if_exists='replace',index=False)
    return data_list


