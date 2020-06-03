from bs4 import BeautifulSoup
import lxml
import os 
import sqlite3
import pymongo
import numpy as np
import sklearn
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
import functools
import json
import re

class MS(object):
    def __init__(self):
        self.stringtag=[
            'WSZZDW',  #文书种类
            'FYWSZL',  #法院文书种类   
            # 'JBFY',    #经办法院
            'FYJB',    #法院级别
            'XZQH_P',  #行政区划 省      
            'XZQH_C',  #行政区划 市      
            'WSMC',    #文书名称   
            'AJLB',    #案件类别    
            'WSZL',    #法院文书种类    
            'SPCX',    #审判程序   
            'AY',      #案由  
            'LAND',    #立案年度    
            'CPSJ',    #裁判时间    
            'AH',      #案号  
        ]
        self.dlrtag=[
            'QSF',
            'YSF',
            'DLR',
        ]
        self.fttag='FLFTYY' #法律法条引用
        self.rytag='SPRYXM' #审判人员姓名
        self.xml=['xml_1','xml_2','xml_3','xml_4',]
        # self.xml=['xml_4']

    def link(self):
        self.myclient = pymongo.MongoClient('mongodb://localhost:27017/')

        self.dblist = self.myclient.list_database_names()
        print('current db',self.dblist)
        self.mydb = self.myclient['law']
        self.cllist = self.mydb.list_collection_names()
        print('current collection',self.cllist)
        self.wscl = self.mydb['ws']
        self.invcl = self.mydb['inv']
        self.addrcl = self.mydb['addr']
        self.tlcl = self.mydb['search']
        # self.conn = sqlite3.connect('law.db')
        # cursor = self.conn.cursor()
        # sql = '''create table if not exists test (
        #     id INTEGER primary key, 
        #     WSZZDW text,  
        #     FYWSZL text,    
        #     FYJB text,    
        #     XZQH_P text,       
        #     XZQH_C text,    
        #     WSMC text,      
        #     AJLB text,       
        #     WSZL text,   
        #     SPCX text,      
        #     AY text,      
        #     LAND text,       
        #     CPSJ text,       
        #     xml text
        #     );'''
        # cursor.execute(sql)

    def build(self):
        self.xmlnum=0
        validxml=[]
        cutted=[]
        for dirpath in self.xml:
            print(f'in dir {dirpath}')
            names = os.listdir('./'+dirpath)
            xmlpath=None
            sets = []
            for name in names:
                if 'xml' in name:
                    xmlpath='./'+dirpath+'/'+name
                    # print(xmlpath)
                    try:
                        res = self.read(xmlpath)
                        sets.append(res[0])
                        cutted.append(res[1])
                    except Exception as e:
                        print(e)
                    if len(sets)==1000 and len(sets)!=0:
                        print(f'{self.xmlnum} passage')
                        print(f'{len(cutted)} passage for check')
                        # self.wscl.insert_many(sets)
                        # self.addrcl.insert_many(sets)
                        self.tlcl.insert_many(sets)
                        print('inserted')
                        sets=[]
                elif os.path.isdir('./'+dirpath+'/'+name):
                    innames = os.listdir('./'+dirpath+'/'+name)
                    for inname in innames:
                        if 'xml' in inname:
                            xmlpath='./'+dirpath+'/'+name+'/'+inname
                            # print(xmlpath)
                            try:
                                res = self.read(xmlpath)
                                sets.append(res[0])
                                cutted.append(res[1])
                                validxml.append(xmlpath)
                            except Exception as e:
                                print(e)
                            if len(sets)==1000 and len(sets)!=0:
                                print(f'{self.xmlnum} passage')
                                print(f'{len(cutted)} passage for check')
                                # self.wscl.insert_many(sets)
                                # self.addrcl.insert_many(sets)
                                self.tlcl.insert_many(sets)
                                print('inserted')
                                sets=[]
            if len(sets)!=0:
                # self.wscl.insert_many(sets)
                # self.addrcl.insert_many(sets)
                self.tlcl.insert_many(sets)
                print(f'{self.xmlnum} passage')
                print(f'{len(cutted)} passage for check')
        # print('save valid')
        # validtxt = open('./valid.txt','w+')
        # for one in validxml:
        #     validtxt.write(f'{one}\n')
        # validtxt.close()
        # self.get_inv(cutted)

    def read(self,xmlpath):

        sets={}
        xmlfile = open(xmlpath)
        soup = BeautifulSoup(xmlfile,'xml')
        # basic case info
        '''
        for tag in self.stringtag:
            found = soup.findAll(tag)
            if len(found) != 0:
                for subtag in found:
                    if subtag.attrs.__contains__('value'):
                        if not sets.__contains__(tag):
                            sets[tag]=subtag['value']
            if len(found) != 0:
                if not sets.__contains__(tag):
                    sets[tag]='NOTFOUND'

        # participants
        found = soup.find('DSR')
        for iden in self.dlrtag:
            sets.setdefault(iden,[])
        if found is not None:
            for participant in found.children:
                if participant.name=='QSF' or participant.name=='YSF' or participant.name=='DLR':
                    iden = participant.name
                    name = participant.SSCYR['value']
                    sets[iden].append(name)
                else:
                    continue
        # print(sets['QSF'])
        # print(sets['YSF'])
        # print(sets['DLR'])
        # laws
        found = soup.find(self.fttag)
        sets.setdefault(self.fttag,[])
        if found is not None:
            for ft in found.findAll('FLFTFZ'):
                if len(ft)!=0:
                    Ts = ft.findAll('T')
                    if len(Ts)==0:
                        if ft.attrs.__contains__('MC'):
                            sets[self.fttag].append(ft.MC['value'])
                    else:
                        for T in Ts:
                            Ks = T.findAll('K')
                            if len(Ks)==0:
                                sets[self.fttag].append(ft.MC['value']+T['value'])
                            else:
                                for K in Ks:
                                    sets[self.fttag].append(ft.MC['value']+T['value']+K['value'])
        # print(sets[self.fttag])

        found = soup.findAll(self.rytag)
        sets.setdefault(self.rytag,[])
        if found is not None:
            for ry in found:
                # print(ry['value'])
                sets[self.rytag].append(ry['value'])

        # sets['xml']=soup.prettify()
        # sets['xml']=xmlpath
        '''
        found = soup.find('WS')
        if found is not None:
            if found.attrs.__contains__('value'):
                sets['title']=found['value']
        else:
            found = soup.find('QW')

            if found.attrs.__contains__('oValue'):
                tt = str(found['oValue'])
                end = min(30,len(tt))
                sets['title']=tt[0:end]

            elif found.attrs.__contains__('value'):
                tt = str(found['value'])
                end = min(30,len(tt))
                sets['title']=tt[0:end]
            else:
                raise Exception()

        # for k,v in sets.items():
        #     if k!='xml':
        #         print(k,v)
        # print(cutted)
        # a=input('\nanything\n')
        '''
        found = soup.find('QW')

        if found.attrs.__contains__('oValue'):
            doc = jieba.cut_for_search(found['oValue'])
        elif found.attrs.__contains__('value'):
            doc = jieba.cut_for_search(found['value'])
        else:
            raise Exception()

        term_str=" ".join(doc)
        '''
        term_str=""
        # print(term_str)
        # cutted.append(term_str)
        sets['id']=self.xmlnum
        self.xmlnum+=1
        # for k,v in sets.items():
        #     if 'xml' in k:
        #         continue
        #     print(k,v)
        # a=input('any')
        return sets,term_str

    def get_inv(self,docs):
        print('start inverse index')
        inverse_idx={}
        f = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
        tfidf = f.fit_transform(docs)
        terms = f.get_feature_names()
        mat = tfidf.tocoo()    
        print('got tfidf')
        for i,j,v in zip(mat.row, mat.col, mat.data):
            inverse_idx.setdefault(terms[j],[])
            inverse_idx[terms[j]].append((int(i),float(v)))
        print('expand')
        def cmp(p1,p2):
            if p1[1]<p2[1]:
                return 1
            elif p1[1]>p2[1]:
                return -1
            else:
                return 0
        invs=[]
        for k,v in inverse_idx.items():
            v=sorted(v,key=functools.cmp_to_key(cmp))
            invs.append({'term':k,'doc':v})
        print('sorted')
        self.invcl.insert_many(invs)
        print('inserted')

    def tag_query(self,kv):
        if kv.get('LAND',None) is not None:
            return {'LAND':{'$gte' : kv['LAND'][0], "$lte" : kv['LAND'][1]}}
        elif kv.get('CPSJ',None) is not None:
            return {'CPSJ':{'$gte' : kv['CPSJ'][0], "$lte" : kv['CPSJ'][1]}}
        else:
            return {kv}

    def kw_query(self,kw):
        kw = list(jieba.cut_for_search(kw))
        terms = []
        for k in kw:
            terms.append({'term':k})
        query={
            '$or':terms
        }
        return query

    def searchb(self,kw=''):
        # query=[]
        if kw!='':
            query=self.kw_query(kw)

            return self.invcl.find(query)
        else:
            return None

    def get_tag(self,name):
        ans = self.addrcl.find({name:{'$exists':1}},{'_id':0,name:1})
        ex_set ={}
        for x in ans:
            if not ex_set.__contains__(x[name]):
                ex_set[x[name]]=1
            else:
                ex_set[x[name]]+=1
        return ex_set

    def get_passage(self,xmlpath):
        x = [
            'WS'
            ,'DSR'
            ,'SSJL'
            ,'AJJBQK'
            ,'PJJG'
            ,'WW'
        ]
        y= {
            'WS':'文首',
            'DSR':'当事人',
            'SSJL':'诉讼记录',
            'AJJBQK':'案件基本情况',
            'PJJG':'判决结果',
            'WW':'文尾',            
        }
        ans={}
        xmlfile = open(xmlpath)
        soup = BeautifulSoup(xmlfile,'xml')
        found = soup.find('QW')
        if found.attrs.__contains__('oValue'):
            print('n')
            ans['n']=1
            tt = str(found['oValue'])
            tt = re.sub('[^\u4e00-\u9fa5]*', '',tt,count=1)
            ans['title']='全文'
            ans['value']=tt
            tagfound = found.findAll(x)
            for i in tagfound:
                tmp = re.sub('[^\u4e00-\u9fa5]*', '',i['value'],count=1)
                ans[y[i.name]]=tmp
                # print(i.name,i['value'])
            
        elif found.attrs.__contains__('value'):
            print('a')
            ans['n']=0
            tt = str(found['value'])
            ans['title']='全文'
            tt = re.sub(r'{(\s+\w)*}', '', tt)
            ans['value']=tt
        # print(ans)
        return ans

if __name__=='__main__':
    ms = MS()
    ms.link() 

    xmls=[
        './xml_1/51669f8f-a108-4c1e-a93e-49b100d8defb/030133604cdc9906e540680165edee70827.xml',
        './xml_2/646a8497-7a4e-4bee-a905-65c111f3ecc6/01716664979222cd7c7d58a401c5b077732.xml',
        './xml_3/27570e96-a17a-40ba-a71f-e27b38830501/053e38c3776007226106863bd5f4385e38c.xml',
        './xml_4/206809AAF9A7218B23DF879C130F5A49.xml',
        ]
    for xml in xmls:
        ms.get_passage(xml)
    # batch =[]
    # for x in ms.wscl.find():
    #     batch.append[x[]]

    # ms.build()
    # ms.mydb.drop_collection('ws')
    # ms.mydb.drop_collection('inv')
    # print(ms.kw_query('山东省青岛市黄岛区人民法院'))
    # doc = ms.invcl.find({'$or':[{'term':'山东'},{'term':'青岛'}]})
    # doc = ms.searchb('山东青岛')
    # for x in doc:
    #     for idx,i in enumerate(x['doc']):
    #         print(idx)
    #         print(i)
    #         if idx == 20:
    #             break
    # for ans in ms.addrcl.find({'id':53547},{'xml':1}):
    #     print(ans)
    # for ans in ms.tlcl.find({'id':53547},{'title':1}):
    #     print(ans)
    # def dump_vtag(dic,path='./vtag.json'):
    #     with open(path,'w') as jsfile:
    #         json.dump(dic,jsfile)
    # valid tags
    # jssv = {}
    # for tag in ms.stringtag:
    #     if tag == 'AH' or tag =='AY' or tag=='WSMC' or tag=='LAND' or tag=='CPSJ':
    #         continue
    #     ans = ms.get_tag(tag)
    #     jssv[tag]=list(ans.keys())
    #     print('save',tag)
    # dump_vtag(jssv)