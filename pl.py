# from bs4 import BeautifulSoup
# import lxml
# import os 
# import pymongo

# soup = BeautifulSoup(open('./content.xml'),'xml')
# ww = open('./content.txt','w+')
# lines = []
# tags = ['WS','DSR','SSJL','AJJBQK','CPFXGC','PJJG','WW']
# for tag in tags:
#     res = soup.find(tag)
#     title = res['nameCN']
#     value = res['value']
#     sp='\',\''
#     value1 = value.split(' ')
#     value1 = '\''+ sp.join(value1)+'\''
#     value2 = '\\n'.join(value.split(' '))
#     # lines.append('{'+f'title:\'{title}\',value:\'{value2}\'' +'},\n')
#     # print('{'+f'title:\'{title}\',value:\'{value}\'' +'}\'')
#     lines.append('{'+f'title:\'{title}\',value:[{value1}]' +'},\n')

# ww.writelines(lines)

# def cmp(p1,p2):
#     if p1[1]<p2[1]:
#         return 1
#     elif p1[1]>p2[1]:
#         return -1
#     else:
#         return 0

# v=[(0,2),(0,3),(1,4)]
# v=sorted(v,key=functools.cmp_to_key(cmp))
# print(v)

import re

ss ='．Msoomal{magi-top：0cm；magi-bottom：0px}'

print(re.sub('[^\u4e00-\u9fa5]*', '',ss,count=1))