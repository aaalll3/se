from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .settings import BASE_DIR
from .dump_mongo import MS
import re
import functools
from .recommendation import search_text

ms = MS()
ms.link()

# Create your views here.
def index(request):
    print('hello')
    # return render(request ,'index.html')
    return HttpResponse("Hello, world. You're at the polls index.")

def law(request):
    print('law')
    print(BASE_DIR)
    return render(request ,'law.html')

def page(request,idx=0):
    print('page')
    ans = ms.addrcl.find({'id':idx})
    addr = list(ans)[0]['xml']
    addr='.'+addr
    passage = ms.get_passage(addr)
    context={}
    context['qwtitle'] = '全文'
    context['qwvalue'] = passage
    return render(request ,'page.html',context=context)

def content(request,idx=0):
    print('page')
    ans = ms.addrcl.find({'id':idx})
    addr = list(ans)[0]['xml']
    addr='.'+addr
    passage = ms.get_passage(addr)
    content={}
    # content['qwtitle'] = '全文'
    # content['qwvalue'] = passage['value']
    # content['full']=passage
    return JsonResponse(passage)

def jumpsearch(request,idx):
    return render(request ,'law.html')

def lawinit(request):
    print('lawinit')
    with open(BASE_DIR+'/vtag.json') as jsfile:
        c = json.load(jsfile)
        print(c)
        return JsonResponse(c)

cac={}
kwl=[]
@csrf_exempt
def search(request,pagen=0):
    pagesize=20
    content = request.body
    content = str(content,encoding='utf-8')
    content = json.loads(content)
    print(content)
    fi={}
    for k,v in content.items():
        if k == 'kw' or k=='pagen':
            continue
        if v!='':
            fi[k.upper()]=v
    if content.__contains__('pagen'):
        pagen = content['pagen']
    if content.__contains__('kw'):
        kw=content['kw']
    # kw = '青岛'
    print('kw',kw)
    skip = pagen*pagesize
    if kw!='':
        if len(kw)>40:
            ans = search_text(text=kw,count=5)
            print(ans[0],ans[1])
            rpa=[]
            for xmlpath in ans[0]:
                xmlpath=xmlpath[9:]
                xmlpath='.'+xmlpath
                print(xmlpath)
                try:
                    for x in ms.addrcl.find({'xml':xmlpath},{'_id':0,'id':1}):
                        print(x)
                        rpa.append(x['id'])
                except Exception:
                    pass
            print(rpa)
            rrpa=[]
            for ids in rpa:
                tit = ms.tlcl.find({'id':ids},{'_id':0,'id':1,'title':1})
                for x in tit:
                    print(x)
                    rrpa.append(dict(x))
            print(rrpa)
            return JsonResponse({'passage':rrpa})
            
        kwl.append(kw)
        docs=[]
        query=ms.kw_query(kw)
        start = int(skip/len(query))
        end = start + int(100/len(query)) 
        print('query:',query)
        if not cac.__contains__(kw):
            cac.setdefault(kw,[])
            inv = ms.invcl.find(query,{'_id':0,'doc':1})
            for a in inv:
                docs.extend(a['doc'])
            def cmp(p1,p2):
                if p1[1]<p2[1]:
                    return 1
                elif p1[1]>p2[1]:
                    return -1
                else:
                    return 0
            docs=sorted(docs,key=functools.cmp_to_key(cmp))
            print(docs)
            cac[kw].extend(docs)
        idxs=[]
        print(pagen*pagesize,pagen*pagesize+pagesize)
        for x in cac[kw][pagen*pagesize:pagen*pagesize+pagesize]:
            idxs.append({'id':x[0]})
        fi={'$and':[{'$or':idxs},fi]}
        ans = ms.tlcl.find(fi,{'_id':0,'id':1,'title':1})
        res = {}
        res['passage']=[]
        for x in ans:
            print(x)
            try:
                tt=re.sub('[^\u4e00-\u9fa5]*', '',x['title'],count=1)
                # print(x)
                res['passage'].append({'id':x['id'],'title':tt})
            except Exception:
                pass
        return JsonResponse(res)

    print('filter',fi)
    print('limit:',pagesize,'skip:',pagen*pagesize)
    ans = ms.tlcl.find(fi,{'_id':0,'id':1,'title':1}).limit(pagesize).skip(pagen*pagesize)
    res = {}
    res['passage']=[]
    for x in ans:
        print(x)
        tt=re.sub('[^\u4e00-\u9fa5]*', '',x['title'],count=1)
        # print(x)
        res['passage'].append({'id':x['id'],'title':tt})
    return JsonResponse(res)

def get_reco(request,idx):
    print('reco')
    ans = ms.addrcl.find({'id':idx})
    addr = list(ans)[0]['xml']
    addr='.'+addr
    passage = ms.get_passage(addr)
    ans = search_text(text=passage['value'],count=5)
    print(ans[0],ans[1])
    rpa=[]
    for xmlpath in ans[0]:
        xmlpath=xmlpath[9:]
        xmlpath='.'+xmlpath
        print(xmlpath)
        try:
            for x in ms.addrcl.find({'xml':xmlpath},{'_id':0,'id':1}):
                print(x)
                rpa.append(x['id'])
        except Exception:
            pass
    print(rpa)
    rrpa=[]
    for ids in rpa:
        tit = ms.tlcl.find({'id':ids},{'_id':0,'id':1,'title':1})
        for x in tit:
            print(x)
            rrpa.append(dict(x))
    print(rrpa)
    return JsonResponse({'rw':ans[1],'passage':rrpa})