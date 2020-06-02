# build web pages
cd law/
npm run build
mv ./dist/index.html ./dist/law.html
cp -f -r ./dist/* ../lawsite/template

cd ../page/
npm run build
mv ./dist/index.html ./dist/page.html
cp -f -r ./dist/* ../lawsite/template