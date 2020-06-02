from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .settings import BASE_DIR
from .dump_mongo import MS



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

def jumpsearch(request):
    return render(request ,'law.html')

def lawinit(request):
    print('lawinit')
    with open(BASE_DIR+'/vtag.json') as jsfile:
        c = json.load(jsfile)
        print(c)
        return JsonResponse(c)

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
    if kw!='':
        docs=[]
        query=ms.kw_query(kw)
        inv = ms.invcl.find(query,{'_id':0,'doc':1})
        for a in inv:
            docs.extend(a['doc'])
        # print(docs)
        idxs=[]
        for x in docs:
            idxs.append({'id':x[0]})
        fi={'$and':[{'$or':idxs},fi]}

    print('filter',fi)
    print('limit:',pagesize,'skip:',pagen*pagesize)
    ans = ms.tlcl.find(fi,{'_id':0,'id':1,'title':1}).limit(pagesize).skip(pagen*pagesize)
    res = {}
    res['passage']=[]
    for x in ans:
        print(x)
        res['passage'].append({'id':x['id'],'title':x['title']})
    return JsonResponse(res)


