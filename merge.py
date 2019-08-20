# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 21:54:39 2019

@author: Ge
"""
import os
import csv

# 已删除的图片的文件夹路径
source_path = "//Users/qpple/Desktop/Dissertation/flickrSpider/0627/0628delete/"
# csv的存放路径
source_csv = "//Users/qpple/Desktop/Dissertation/flickrSpider/0627/newpicinfo.csv"
target_csv = "//Users/qpple/Desktop/Dissertation/flickrSpider/0627/del_newpicinfo.csv"
filelist = os.listdir(source_path)
for i in range(len(filelist)):
    filelist[i] =filelist[i].split('.')[0]
# print(filelist)

csv_reader = csv.reader(open(source_csv, 'r'))
csv_writer = csv.writer(open(target_csv, 'w'))

with open(target_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for line in csv_reader:
        if line[0] in filelist:
            continue
        writer.writerow(line)