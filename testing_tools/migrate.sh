cd /root/CCSKannelProxy_V2.1/gproxy/runtime/ 
for i in *.py
do 
	cat $i  | perl -pe 's/Config\.([0-9A-Za-z_]+)/Config\[\"$1\"\]/g' > /root/devel/gproxy/runtime/$i
done 
cd -
