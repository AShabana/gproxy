# TODO convert this to a backup tool
git add -- `find ./*.py counters/*  config/lists/all.py  proxylib/*.py  runtime/*.py`
echo Please Enter a discription for changes to be commited in one line 
read comment
echo git commit -m -- "$comment"
git log
