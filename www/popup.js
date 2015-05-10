<script language="javascript">
function openpopup(id){
      //Calculate Page width and height
      var pageWidth = window.innerWidth;
      var pageHeight = window.innerHeight;
      if (typeof pageWidth != "number"){
      if (document.compatMode == "CSS1Compat"){
            pageWidth = document.documentElement.clientWidth;
            pageHeight = document.documentElement.clientHeight;
      } else {
            pageWidth = document.body.clientWidth;
            pageHeight = document.body.clientHeight;
      }
      } 
      //Make the background div tag visible...
      var divbg = document.getElementById('bg');
      divbg.style.visibility = "visible";
       
      var divobj = document.getElementById(id);
      divobj.style.visibility = "visible";
      if (navigator.appName=="Microsoft Internet Explorer")
      computedStyle = divobj.currentStyle;
      else computedStyle = document.defaultView.getComputedStyle(divobj, null);
      //Get Div width and height from StyleSheet
      var divWidth = computedStyle.width.replace('px', '');
      var divHeight = computedStyle.height.replace('px', '');
      var divLeft = (pageWidth - divWidth) / 2;
      var divTop = (pageHeight - divHeight) / 2;
      //Set Left and top coordinates for the div tag
      divobj.style.left = divLeft + "px";
      divobj.style.top = divTop + "px";
      //Put a Close button for closing the popped up Div tag
      if(divobj.innerHTML.indexOf("closepopup('" + id +"')") < 0 )
      divobj.innerHTML = "<a href=\"#\" onclick=\"closepopup('" + id +"')\"><span class=\"close_button\">X</span></a>" + divobj.innerHTML;
}
function closepopup(id){
      var divbg = document.getElementById('bg');
      divbg.style.visibility = "hidden";
      var divobj = document.getElementById(id);
      divobj.style.visibility = "hidden";
}

function addto(listid) {
            var sender = prompt("Enter Sender Name");           
		if (sender != null) {
                    window.location.href="readlist.php?sender="+sender+"&listid="+listid;
			return false;
		}
}

function delfrom(listid_del) {
            var sender_del = prompt("##Delete## Enter Sender Name");
                if (sender_del != null) {
                    window.location.href="readlist.php?sender_del="+sender_del+"&listid_del="+listid_del;
                        return false;
                }
}

</script> 

<style type="text/css">
<!--
.popup {
      background-color: #FFFFFF;
      height: 500px; width: 800px;
      border: 5px solid #428BCA;
      position: absolute; visibility: hidden;
      font-family: Arial;
      font-size: large; text-align: justify;
      padding: 5px; overflow: auto;
      z-index: 2;
      word-wrap:break-word;
}
.popup_bg {
      position: absolute;
      visibility: hidden;
      height: 100%; width: 100%;
      left: 0px; top: 0px;
      filter: alpha(opacity=70); /* for IE */
      opacity: 0.7; /* CSS3 standard */
      background-color: #999;
      z-index: 1;
}
.close_button {
      font-family: Verdana, Geneva, sans-serif;
      font-size: small; font-weight: bold;
      float: right; color: #666;
      display: block; text-decoration: none;
      border: 2px solid #666;
      padding: 0px 3px 0px 3px;
}
body { margin: 0px; }
-->
</style>

