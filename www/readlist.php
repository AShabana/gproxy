<?php
include 'popup.js';
echo "<html>";
echo "<title>G-Proxy Lists</title>";
echo "<body>";
echo "<link href=\"readlist.css\" rel=\"stylesheet\">";
#$myip = "localhost";
$myip = $_SERVER['HTTP_HOST'];
$listrec = "";
#########################################
#	ALL FUNCTIONS START		#
#########################################
# call url
function callurl($url)
{
$ch=curl_init();
curl_setopt($ch, CURLOPT_URL,$url);  
curl_setopt($ch, CURLOPT_HEADER, 0);  
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);  
$lists=curl_exec($ch);
curl_close($ch);
return $lists;
}

# convert all.py lines to , separated lines
function cleanme ($rawline)
{
# split the raw list response   
$cleanline=substr($rawline,2); # remove ['
#$cleanline=preg_replace("/=', '/","-",$cleanline);
$cleanline=preg_replace("/', '/","-",$cleanline);
$cleanline=preg_replace("/']/","-",$cleanline);
$cleanline=(explode("-", $cleanline));
return $cleanline;
}

# display list from gproxy lists
function dislist($listid){
		global $myip;
		$url="http://".$myip.":3325/DisList?list=" . $listid;
		global $listrec,$return_res;
		$listrec  = callurl($url);
		echo'<div id="bg" class="popup_bg"></div>
	     	<div id="popup1" class="popup">
		' . $listrec . '
	     	</div>
             	<script type="text/javascript">
                 openpopup(\'popup1\');
             	</script>';
		#echo $listrec;
}

# add sender to gproxy list
function addtolist($sender,$listid){
		global $myip;
		$url="http://".$myip.":3325/AddToList?listid=" . $listid ."&sender=". $sender;
                $res=callurl($url);
		# to hide add _GET args to avoid accedintly submits
		header("Location: http://".$myip . rtrim(dirname($_SERVER['PHP_SELF']), '/\\') . "/readlist.php?dislist=".$listid);
		exit();
}

# delete sender from gproxy list
function delfromlist($sender_del,$listid_del){
		global $myip;
	        $url="http://".$myip.":3325/DelFromList?listid_del=" . $listid_del ."&sender_del=". $sender_del;
		$res=callurl($url);
		if ($res == "error")
		header("Location: http://".$myip . rtrim(dirname($_SERVER['PHP_SELF']), '/\\') . "/readlist.php?error=Error:sender_not_in_list");
		else
		# to hide add _GET args to avoid accedintly submits
                header("Location: http://".$myip . rtrim(dirname($_SERVER['PHP_SELF']), '/\\') . "/readlist.php?dislist=".$listid_del);
		exit();
}

function error_msg($errormsg){
		echo'<div id="bg" class="popup_bg"></div>
                <div id="popup1" class="popup">
                ' . $errormsg . '
                </div>
                <script type="text/javascript">
                 openpopup(\'popup1\');
                </script>';
}
	
#########################################
#       ALL FUNCTIONS END             #
#########################################

# get all lists from gproxy
$alllists=callurl("http://".$myip.":3325/ShowLists?listall=yes"); # raw list from python
$final_list=cleanme($alllists); # 

# handle GET requsets called by: javascrip prompt and href buttons
if($_GET){
	if(isset($_GET['dislist'])){
		dislist($_GET['dislist']);
	    }
	else if(isset($_GET['sender']) && isset($_GET['listid']))
		addtolist($_GET['sender'],$_GET['listid']);
	else if(isset($_GET['sender_del']) && isset($_GET['listid_del']))
		delfromlist($_GET['sender_del'],$_GET['listid_del']);
	else if(isset($_GET['error']))
		error_msg($_GET['error']);
}

# create table header
echo "<table>";
echo "<thead>";
echo "<tr><th colspan=\"3\">Gproxy Lists</th></tr>";
echo "<tr>";
echo "<th>ID</th>";
echo "<th colspan=\"2\">List Name</th>";
echo "</tr>";
echo "</thead>";
echo "<tbody>";

# fetch list names from array to html table
$counter=0;
$end=count($final_list); #no of lines in array
foreach ($final_list as $listid){
        # ignore the last empty line in list
        if (($end-1) == $counter)
                break;
        echo "<tr>";
        echo "<td>" . $counter++ . "</td>";
        echo "<td>" . $listid . "</td>";
        echo "<td>";
        $dislink="readlist.php?dislist=".$listid;
        $dellink="readlist.php?delflist=".$listid;
	echo "<a href='".$dislink."'><button class=\"button\">show</button></a>";
	echo '<button class="button" onclick="addto(\''.$listid.'\')">Addto</button>';
        echo '<button class="button" onclick="delfrom(\''.$listid.'\')">DelFrom</button>';
	echo "</td>";
        echo "</tr>";
}

echo "</tbody>";
echo "</table>";


echo "</body>";
echo "</html>";
?>
