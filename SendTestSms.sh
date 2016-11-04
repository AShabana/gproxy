# Configuration part #
# SAMPLE :
#curl "http://localhost:12014/cgi-bin/sendsms?username=nemra1&password=koko88&uptoworksmsc=GNCheck_test12&account=ccsTest&from=FACEBOOK&to=966557225741&coding=2&udh=%05%00%03%F7%02%01&text=%06%46%06%48%06%39%00%20%06%27%06%44%06%39%06%45%06%44%06%4A%06%29%00%3A%00%20%06%33%06%2F%06%27%06%2F%00%20%06%28%06%37%06%27%06%42%06%29%00%20%06%27%06%26%06%2A%06%45%06%27%06%46%00%0D%00%0A%06%31%06%42%06%45%00%20%06%27%06%44%06%2D%06%33%06%27%06%28%00%20%00%3A%00%20%00%33%00%36%00%39%00%39%00%34%00%30%00%2A%00%2A%00%2A%00%0D%00%0A&dlr-mask=7&dlr-url=http://54.243.194.42:2052/dlr?dlrip%3d54.243.194.42%26dlrport%3d2052%26smppport%3d2011%26account%3dalerts%26msgid%3d859af78c-6a50-4a42-a4e3-dc52e68ec473%26to%3d%25P%26from%3d%25p%26statusid%3d%25d%26statusmsg%3d%25a%26timestamp%3d%25t%26smsc%3d%25i%26mcc%3d420%26mnc%3d4%26cost%3d0.0559%26clientdlr%3d0%26ds%3d2014-11-30T08:33:13.002"
#curl "http://localhost:12014/cgi-bin/sendsms?username=nemra2&password=koko88uptowork&smsc=GNCheck_test12&account=ccsTest&from=FACEBOOK&to=966557225741&coding=2&udh=%05%00%03%F7%02%02&text=%06%46%06%48%06%39%00%20%06%27%06%44%06%39%06%45%06%44%06%4A%06%29%00%3A%00%20%06%33%06%2F%06%27%06%2F%00%20%06%28%06%37%06%27%06%42%06%29%00%20%06%27%06%26%06%2A%06%45%06%27%06%46%00%0D%00%0A%06%31%06%42%06%45%00%20%06%27%06%44%06%2D%06%33%06%27%06%28%00%20%00%3A%00%20%00%33%00%36%00%39%00%39%00%34%00%30%00%2A%00%2A%00%2A%00%0D%00%0A&dlr-mask=7&dlr-url=http://54.243.194.42:2052/dlr?dlrip%3d54.243.194.42%26dlrport%3d2052%26smppport%3d2011%26account%3dalerts%26msgid%3d859af78c-6a50-4a42-a4e3-dc52e68ec473%26to%3d%25P%26from%3d%25p%26statusid%3d%25d%26statusmsg%3d%25a%26timestamp%3d%25t%26smsc%3d%25i%26mcc%3d420%26mnc%3d4%26cost%3d0.0559%26clientdlr%3d0%26ds%3d2014-11-30T08:33:13.002"

#exit 0
# Edit it as you wish to run your test
IP="localhost" # review /etc/hosts to know servers name i.e. stc
# ksa=8002 , main=8001 ,
PORT="12014" 
SMSC="GNCheck_B1"
SENDER="Verify"
MOBILE_NO="201098824365"
CODING=0 # 0: english, 1:binary, 2:unicocde !! reveiw kannel userguid for more information 
MSG="test please ignore"
#UDH="%05%00%03%F7%02%02"
UDH=""
DLRPART="&dlr-url=http%3a%2f%2f10.245.211.80%3a3900%2fdlr%3finterface%3dhttpinterface%26port%3d80%26aid%3d%26kport%3d3900%26statusid%3d%25d%26msgid%3d04bad587-0ede-4dba-b344-98d853ff7275%26requestid%3d%26to%3d%25P%26from%3d%25p%26timestamp%3d%25t%26smsc%3d%25i%26smscid%3d%25I%26statusmsg%3d%25A%26smscprovidedID%3d%25F%26mpslinkid%3dzain_ksa2%26MNum%3d1%26INT%3dhttpinterface%26account%3dadmin%26clienturl%3d"

## End of configution part




MSG="$(perl -MURL::Encode -e 'print URL::Encode::url_encode($ARGV[0]);' "$MSG")"
URL="http://$IP:$PORT/cgi-bin/sendsms?username=nemra1&password=koko88&smsc=$SMSC&udh=$UDH&account=testingAccount&from=$SENDER&to=$MOBILE_NO&coding=$CODING&text=$MSG&dlr-mask=7$DLRPART"
curl  $URL
