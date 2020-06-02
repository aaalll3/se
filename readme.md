现存的问题
page页面为显示文章内容的页面
law页面为显示搜索内容的页面
我想从django直接在渲染时候把page页面的文章内容传给浏览器，但是还不成功

0.目录结构
root    xml_1/
        xml_2/
        xml_3/
        xml_4/
          law/
         page/
      lawsite/
       run.sh
     build.sh
        br.sh
requirements.txt
    vtag.json
 
1.运行mongodb


```
brew install mongodb-community@4.2

brew services start mongodb-community@4.2

brew services stop mongodb-community@4.2
```

1.1 mongodb 配置

# in /usr/local/etc/mongod.conf
# change dpath to your root dir
# like
storage:
  dbPath: /Users/lwd/Desktop/X/6/搜索引擎/prj/

或者 运行 ./dump_mongo.py 
耗时大约40min

2.python 依赖

```
pip3 install -r requirements.txt
```

3.npm install
```
cd page/
npm install
cd ../law
npm install
```

4.shell 
```
chmod +x ./build.sh # build vue and copy to django dir
chmod +x ./run.sh
chmod +x ./br.sh # build and run 
./build.sh
```