from bs4 import BeautifulSoup
import lxml
import os 
import pymongo

picktag=[
    'AJLB',
    'AL',
    'ALYZ',
    'HXSY',
    'LB',
    'LY',
    'ZYJD',
    'QW',
    'AH',
    'BG',
    'DLLS',
    'DLR',
    'DSR',
    'FYGD',
    'FYJB',
    'JBFY',
    'WZZM',
    'SPCX',
    'WS',
    'AY',
    'WW',
    'CPSJ',
    'FGCY',
    'SSCY',
    'AY',
    'PJJG',
    'WZZM',
]

xml=['xml_1','xml_2','xml_3','xml_4',]
pretty =False


if not pretty:
    cnts={}
    xmlnum=0
    for dirpath in xml:
        print(f'in dir {dirpath}')
        names = os.listdir('./'+dirpath)
        for tag in picktag:
            cnts.setdefault(tag,0)
        xmlpath=None
        for name in names:
            if 'xml' in name:
                xmlpath='./'+dirpath+'/'+name
            elif os.path.isdir('./'+dirpath+'/'+name):
                innames = os.listdir('./'+dirpath+'/'+name)
                for inname in innames:
                    if 'xml' in inname:
                        xmlpath='./'+dirpath+'/'+name+'/'+inname
            if xmlpath is not None:   
                xmlnum+=1
                sets={}
                # for tag in picktag:
                    # cnts.setdefault(tag,0)
                    # sets.setdefault(tag,False)
                soup = BeautifulSoup(open(xmlpath),'xml')
                # find = soup.findAll(picktag)
                find =soup.descendants
                for a in find:
                    if not sets.__contains__(a.name):
                        sets[a.name]=True
                        if cnts.__contains__(a.name):
                            cnts[a.name]+=1
                        else:
                            cnts[a.name]=1
                    # print(a.name,[i for i in a.attrs.keys()],' type:',type(a))

                if xmlnum%1000==0:
                    print(f'in {xmlnum} passages:')
                    for k,v in cnts.items():
                        print(f'{k}:{v}',end=' ')
    os.mknod("res.txt")
    res = open('./res.txt','w+')
    print(f'in {xmlnum} passages:\n')
    res.write(f'in {xmlnum} passages:')
    for k,v in cnts.items():
        print(f'{k}:{v}',end=' ')
        res.write(f'{k}:{v}\n')

if pretty:
    for dirpath in xml:
        print(f'in dir {dirpath}')
        names = os.listdir('./'+dirpath)
        cnts={}
        for tag in picktag:
            cnts.setdefault(tag,0)
        xmlnum=0
        for name in names:
            if 'xml' in name:
                soup = BeautifulSoup(open('./'+dirpath+'/'+name),'xml')
                print(soup.prettify())
            elif os.path.isdir('./'+dirpath+'/'+name):
                innames = os.listdir('./'+dirpath+'/'+name)
                for inname in innames:
                    if 'xml' in inname:
                        soup = BeautifulSoup(open('./'+dirpath+'/'+name+'/'+inname),'xml')
                        print(soup.prettify())
            a = input('\nanything')
                    
            
