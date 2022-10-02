"""
主要处理.origin
按照a无趣的书写习惯转义Markdown
"""

import os
import re
from tkinter import font
fapath = "../.origin"
gpath = "../YY向"


def dev(filepath):
    TFile = open(filepath, 'r', encoding='utf-8')  # 打开文件(只读)
    content = TFile.readlines()  # 按行读取
    l = 0  # 上一章的开始
    r = 0  # 本章的开始
    cnt = 0
    fcontent = '' # 新内容
    fname = '' # 文件名称
    lfpath = '' # 具体目录是推书还是排雷
    con = "\n> 内容整理自： a无趣" # 版权
    tmfm = [] # front-matter
    reg = [r"\*\*[一二两三四五六七八九十○零百千0-9１２３４５６７８９０]+.*", "分类"]
    ts = [''] # 分类
    for i in range(len(content)):
        line = content[i]
        if re.search(reg[0], line):
            r = i + 2
            if r != l:
                fcontent = ''.join(tmfm) + "# " + fname + "\n" +''.join(content[l + 2: r - 2]) + con
                # print(fcontent)
                tf = open(gpath + '/' + lfpath + '/' + fname +'.md', 'w', encoding='utf-8')
                tf.writelines(fcontent)
                tf.close()
            fname = content[r].strip().replace(":","：").replace("/","&")
            tmfm = ["---\n", "title: " + fname + "\n", "categories:\n", "- YY向\n", "tags:\n", "---\n"]
            ts = []
            if content[r].find("排雷") != -1:
                lfpath = "排雷"
            else :
                lfpath = "扫书"
            tmfm.insert(tmfm.index("tags:\n") + 1, "- " + lfpath + "\n")
            l = r
        if line.find(reg[1]) != -1:
            ts = line[3:].split('/')
            for sta in ts:
                tmfm.insert(tmfm.index("tags:\n") + 1, "- " + sta)
    # 单独处理最后一个
    fcontent = ''.join(tmfm) + "# " + fname + "\n" +''.join(content[r + 2:]) + con
    # print(fcontent)
    tf = open(gpath + '/' + lfpath + '/' + fname +'.md', 'w', encoding='utf-8')
    tf.writelines(fcontent)
    tf.close()
    TFile.close()  # 关闭文件


for folderName, subfolders, filenames in os.walk(fapath):
    for filename in filenames:
        # 获取前缀（文件名称）
        tname = os.path.splitext(filename)[0]
        if tname.find("a无趣") != -1 and os.path.splitext(filename)[-1][1:] == "md":
            rpath = os.path.relpath(folderName, fapath)  # 获取相对路径
            filepath = fapath + rpath + "\\" + filename  # 获取文件的相对路径
            print(filepath)
            dev(filepath)
