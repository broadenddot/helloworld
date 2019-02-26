# !/usr/bin/env python
# encoding:utf-8
import os  
import json
import re
import configparser
import os
from hamcrest.core.core.isnone import none
from sqlalchemy.sql.operators import isnot
import pandas as pd
import numpy as np
from _ast import If
#dic ={}
os.chdir("./")
cf = configparser.ConfigParser()
cf.read("path.conf")

#读取文件配置路径
scanFile = cf.get("path", "scanFile")#扫描路径
targetFilePath = cf.get("path", "targetFilePath") #演员actors文件保存路径
#tempFilePath = cf.get("path", "tempFilePath") #备份保存路径文件夹
configurationCount = cf.get("path", "configurationCount")#配置最大条数

#directorFilePath = cf.get("path", "directorFilePath") #导演director文件保存路径
#读取文件
def read(path):
    path = scanFile #文件夹目录  
    files= os.listdir(path) #得到文件夹下的所有文件名称  
    director = []  
    actors =[]
    jsons=[]
    flag =0;
    fileNum =0
    tempsDataTarget={}
    for file in files: #遍历文件夹  
        if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开  
          f = open(path+"/"+file,'r', encoding='UTF-8'); #打开文件  
          iter_f = iter(f); #创建迭代器  
          str = ""  
          for line in iter_f: #遍历文件，一行行遍历，读取文本  
                  fileNum=fileNum+1
                  print("read the filenum =%d"%fileNum)
                  str = str.join(line)  
                  director.append(str) #每个文件的文本存到list中  
                  #if(fileNum%50==0):
                  #director=[]
                      #保存文件
    print("read the dataFile end start to deal the data...")
    if isinstance(director,list):
                  dicts ={}
                  for i in range(len(director)):
                      tempsData = director[i];
                      jsons = json.loads(''.join(tempsData))
                      dicts = dealDate(jsons,dicts)
                  tempsDataTarget = dicts;   
    #print(tempsDataTarget)
    #backItems = sort_by_value(tempsDataTarget)  
    #print(backItems)
    list1 = sorted(dict2list(tempsDataTarget), key=lambda x:x[1], reverse=True)
    flag = 0;
    targetList =[]
    targetString =""
    for i, value in list1:
        #print('%s %s'%(i, value)) 冯成明 41
        #print(i); #冯成明
        if(flag>=int(configurationCount)):
            break
        targetList.append(i)
        targetList.append("|")
        flag = flag+1;
    targetString = ''.join(targetList)
    print("Number to display =%d "%int(configurationCount))
    print("The file has been generated. Please view the directory=> %s"%targetFilePath)    
           #生成文件
           #便利这些文件处理数据
           #生成目标文件
    saveactors(targetString)
    #return director,actors;
def dict2list(dic:dict):
    ''' 将字典转化为列表 '''
    keys = dic.keys()
    vals = dic.values()
    lst = [(key, val) for key, val in zip(keys, vals)]    
    return lst
#此项为多余项
def sort_by_value(d): 
    items=d.items() 
    backitems=[[v[1],v[0]] for v in items] 
    backitems.sort() 
    print(backitems)
    return [ backitems[i][1] for i in range(0,len(backitems))] 
#处理数据
def dealDate(director,dictss):
    dicts =dictss
    if isinstance(director,list):
        for i in range(len(director)):
            tempData = director[i]
            if isinstance(tempData,dict):
                if ('actors' in tempData) : 
                    # 逗号 和重复 名字去除
                    mstr = tempData['actors'];
                    dicts = delRepeat(dicts,mstr)
                if ('director' in tempData) :
                    dicts = delRepeat(dicts,tempData['director'])
    return dicts
def delRepeat(dict,mstr):
    if(" " in mstr):    #空格处理
        lists = re.split(" ",mstr)
        for i in range(len(lists)):
            if(lists[i] in dict.keys()):
               dict[lists[i]] =  dict[lists[i]]+1
            else:
               dict[lists[i]] =1
    elif("，" in mstr):  #中文逗号处理
        listss = re.split("，",mstr)
        for i in range(len(listss)):
            if(listss[i] in dict.keys()):
               dict[listss[i]] =  dict[listss[i]]+1
            else:
               dict[listss[i]] =1
    elif("," in mstr):  #英文逗号处理
        listsss = re.split(",",mstr)
        for i in range(len(listsss)):
            if(listsss[i] in dict.keys()):
               dict[listsss[i]] =  dict[listsss[i]]+1
            else:
               dict[listsss[i]] =1
    elif("、" in mstr):
        listssss = re.split("、",mstr)
        for i in range(len(listssss)):
            if(listssss[i] in dict.keys()):
               dict[listssss[i]] =  dict[listssss[i]]+1
            else:
               dict[listssss[i]] =1
    elif mstr.strip()=='':
        mstr =""
    else:
        if(mstr in dict.keys()):
               dict[mstr] =  dict[mstr]+1
        else:
               dict[mstr] =1
    return dict
#保存文件
def saveactors(re):
    file = open(targetFilePath, "wb+")
    #re =' '.join(re)
    re = re.encode('utf-8')
    file.write(re)
    file.close()  
#testJson(tempData, name)
if __name__ == "__main__": 
    actors =""
    director=""
    read("")
    # save(result, "digit")