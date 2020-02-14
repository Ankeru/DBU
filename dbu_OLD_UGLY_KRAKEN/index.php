<html>
    <head>
	<title>Учет системных плат и комплектующих</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<script type="text/javascript"> //js функции
		        <!--
		        var Otype,Id;
		        function f_open1(){//Функция перехода на страницу просмотра объектов
				document.cookie = "type="+ document.getElementById("objType").value;		        
				document.location = "/view.php";
		        }

		        function f_open2(){////Функция для просмотра истории конкретного объекта
		                if (document.getElementById("serialNumber").value != "")
					{
					document.cookie = "type="+ document.getElementById("objType").value;
					document.cookie = "serialNumber="+ document.getElementById("serialNumber").value;				
					document.location = "/history.php";
					}
				 else {
					window.alert("Введите код объекта!");			
				}
		        }

			function f_open3(){
				document.cookie = "type="+ document.getElementById("objType").value;
		        	document.location = "/edit.php";//Функция перехода на страницу просмотра объектов
		        }

                        function f_hide(){
				document.getElementById("myShowBlock").style.display = "none";		
			}
	
                        function f_show(){
				document.getElementById("myShowBlock").style.display = "block";
			}
			function f_typeUpdate(){
				document.cookie = "type="+ document.getElementById("objType").value;
				document.location = "/index.php";
			}
			function f_serialUpdate(flag){
				document.cookie = "type="+ document.getElementById("objType").value;
				document.cookie = "serialNumber="+ document.getElementById("serialNumber").value;
				document.cookie = "isFree="+ flag;
				document.location = "/index.php";
			}
		        //-->
		</script>
		<style>
		</style> 
    </head>
    <body>
	<script type="text/javascript">// Объявление глобальных переменных js
		<!--
		var Otype,Id;
		//-->
	</script>
	<font size="5"><it><b>Учет системных плат и комплектующих</b></it></font>
	<hr>
	<form  method="POST">
		Тип объекта <br><select id="objType"  name="objType" onchange="f_typeUpdate();">
		<?php 	
			//if (isset($_POST['go']){}
			//$cookieType = $_POST['objType'];
			//}
			//else		
			$cookieType = trim($_COOKIE['type']);
			
			$cookieId = trim($_COOKIE['id']);
			$cookieSerialNumber = trim($_COOKIE['serialNumber']);
			$action = trim($_COOKIE['isFree']);
			$nameCookie = trim($_COOKIE['name']);
			$locationCookie = trim($_COOKIE['location']);
			$commentCookie = trim($_COOKIE['comment']);
//echo "<script type='text/javascript'>\n";//Для обновления страницы после submit'а
		//					echo 'window.alert(document.cookie);';
//							echo "</script>";
			//setrawcookie("type","");
			setrawcookie("id","");
			setrawcookie("serialNumber",""); 
			setrawcookie("isFree","");
			setrawcookie("name","");
			setrawcookie("location","");
			setrawcookie("comment","");

			date_default_timezone_set('Europe/Moscow');
                        function f_winToUTF($str){
				return mb_convert_encoding($str,"UTF-8",mb_detect_encoding($str)); 
			}

                        function f_ToUTF($str){
				return iconv(mb_detect_encoding($str),'UTF-8',$str);
			}
			if ($db=mysqli_connect("localhost","mysql_boards","75020141551q1619w","boardsDataBase")) #подключение к бд: хост,логин,пароль, название бд
		        	{   
				 mb_regex_encoding('UTF-8');      
				 mysqli_query($db,"SET NAMES utf8");
				 mb_internal_encoding('UTF-8'); 
				 if (!mysqli_set_charset($db,'utf8'))
		       		 	echo 'Charset setting fail';
				 if (trim($cookieId)!=""){	#запрашиваем серийник по айди, если есть айди
					$sql = 'SELECT `serialNumber` FROM `objects` WHERE `objId`="'.$cookieId.'"';
					$rs = mysqli_query($db,$sql);
		               		$newidid = mysqli_fetch_array($rs);	
					$cookieSerialNumber = $newidid[0];
					mysqli_free_result($rs);		
   				 }
		                 $sql = 'SELECT `type` FROM `objectTypes` ORDER BY `objectTypes`.`type` ASC ';
				 $rs = mysqli_query($db,$sql);
			/////////////////Сделано так ради того, чтобы тип был выбран если куки Типа чистые
		                 $pole = mysqli_fetch_array($rs); 
				 if (trim($cookieType)==="") 
				 	$cookieType = $pole[0];
				 echo '<option value="'.f_winToUTF($pole[0]);
		                 if ($cookieType===$pole[0]) 
				 	echo '" selected>';//Для автоматического выбора значения при переходе со страницы "Просмотр объектов"
		                 else 
					echo '">';
		                 echo f_winToUTF($pole[0]);
				 echo '</option>';
			/////////////////Сделано так ради того, чтобы тип был выбран если куки типа чистые
		                 while ($pole = mysqli_fetch_array($rs)){
				         echo '<option value="'.f_winToUTF($pole[0]);
				         if ($cookieType===$pole[0]) 
					 	echo '" selected>';//Для автоматического выбора значения при переходе со страницы "Просмотр объектов"
				         else
						echo '">';
				         echo f_winToUTF($pole[0]).'</option>';
		                 }
		                 echo '</select>';
		                 mysqli_free_result($rs);
			echo '<input type="button" name="search" value="Просмотр" onclick="f_open1();"><input type="button" name="objRegButt" value="Добавление новых объектов" onclick="f_open3();"><br>';
			echo 'Серийный номер объекта';
			$sql = 'SELECT `serialNumber`,`isFree` FROM `objects` WHERE `type`="'.$cookieType.'" ORDER BY `objects`.`serialNumber` ASC ';
		 	$rs = mysqli_query($db,$sql);
			$pole = mysqli_fetch_array($rs);
 			if (trim($cookieSerialNumber)===""){
				$cookieSerialNumber = $pole[0];
				$action = $pole[1];} 
		 	while ($pole = mysqli_fetch_array($rs)){
				if ($cookieSerialNumber===$pole[0]) {
					$action = $pole[1];			
				}
			}
			mysqli_free_result($rs);

  
			$GlobalStyle = 'style="color:green;"';
			$ifVerifiedObject = false;
			$sql = 'SELECT `serialNumber`,`isFree`,`isVerified` FROM `objects` WHERE `type`="'.$cookieType.'" ORDER BY `objects`.`serialNumber` ASC ';
			$rs = mysqli_query($db,$sql);
			while ($pole = mysqli_fetch_array($rs)){
				if ($cookieSerialNumber===$pole[0])
					if (trim($pole[2])==="1"){
					$ifVerifiedObject = true;
					break;
					}
			}

			$sql = 'SELECT `serialNumber`,`isFree`,`isVerified`,`objComment` FROM `objects` WHERE `type`="'.$cookieType.'" ORDER BY `objects`.`serialNumber` ASC ';
                        $rs = mysqli_query($db,$sql);
                        $pole = mysqli_fetch_array($rs);
				
			
			echo '<br><select ';
			if ($ifVerifiedObject)
				echo $GlobalStyle;
			echo ' id="serialNumber"  name="serialNumber" onchange="f_serialUpdate('.$action.');"><br>';

			if (trim($pole[2])==="1")
				$freeStyler =  $GlobalStyle;
			else 
				$freeStyler ='';

                        echo '<option '.$freeStyler.' value="'.f_winToUTF($pole[0]);
		        if ($cookieSerialNumber===$pole[0]){
				echo '" selected>';//Для автоматического выбора значения при переходе со страницы "Просмотр объектов"
			       	$action = $pole[1];
				$comment = $pole[3];
			} 
		        else 
				echo '">';
		        echo f_winToUTF($pole[0]);
		        echo '</option>';
		        while ($pole = mysqli_fetch_array($rs)){
				if (trim($pole[2])==="1")
                                 $freeStyler =  $GlobalStyle;
                        	else
                                $freeStyler ='';

				echo '<option '.$freeStyler.' value="'.f_winToUTF($pole[0]);
				if ($cookieSerialNumber===$pole[0]) {
					echo '" selected>';//Для автоматического выбора значения при переходе со страницы "Просмотр объектов"
				       	$action = $pole[1];
					$comment = $pole[3];
				} 
				else
					echo '">';
				echo f_winToUTF($pole[0]).'</option>';
		                }
		        echo '</select>';
			mysqli_free_result($rs);	
  			echo '<input type="button" name="history" value="История" onclick="f_open2();"><br>';
			echo '<textarea disabled>'.$comment.'</textarea><br>';
			if ($action==="") 
				$action = trim($_COOKIE['isFree']);
			setrawcookie("isFree",$action);
			if (trim($action)==="0"){
				$sql = 'SELECT `objId` FROM (SELECT * FROM `objects` WHERE `type`="'.$cookieType.'") AS tab1  WHERE `serialNumber`="'.$cookieSerialNumber.'"';
				$rs = mysqli_query($db,$sql);
				$pole = mysqli_fetch_array($rs);
				$selId = $pole[0];
				mysqli_free_result($rs); 
				setrawcookie("isFree", $action);
				$sql = 'SELECT `location` FROM `records` WHERE `objId`="'.$selId.'"  ORDER BY `records`.`recordId` DESC ';
				$rs = mysqli_query($db,$sql);
				$pole = mysqli_fetch_array($rs);
				$loci = $pole[0];
				mysqli_free_result($rs); 
				echo 'Забран       <br><input id="location" type="text" name="location" value="'.$loci.'" disabled><br>';
				
				/*echo 'Дата        <br> <input id="date" type="datetime" name="date" value="'.date("d").'-'.date("m").'-'.date("Y").'"><br>';*/
					$quantity = 1;
                                        echo 'Дата <br><select name="date">';
                                                        while($quantity<32){
                                                                        if (date("d") == $quantity){
                                                                        echo '<option value="'.$quantity.'" selected>'.$quantity.'</option>';
                                                                        }
                                                                        else{
                                                                        echo '<option value="'.$quantity.'">'.$quantity.' </option>';
                                                                        }
                                                                $quantity = $quantity +1;
                                                                }
                                        echo '</select>';
                                        $quantity = 1;
                                        echo '<select name="month">';
                                                        while($quantity<13){
                                                                        if (date("m") == $quantity){
                                                                        echo '<option value="'.$quantity.'" selected>'.$quantity.'</option>';
                                                                        }
                                                                        else{
                                                                        echo '<option value="'.$quantity.'">'.$quantity.' </option>';
                                                                        }
                                                                $quantity = $quantity +1;
                                                                }
                                        echo '</select>';
                                        $quantity = date("Y");
                                        echo '<select name="year">';
                                                        while($quantity>1999){
                                                                        if (date("Y") == $quantity){
                                                                        echo '<option value="'.$quantity.'" selected>'.$quantity.'</option>';
                                                                        }
                                                                        else{
                                                                        echo '<option value="'.$quantity.'">'.$quantity.' </option>';
                                                                        }
                                                                $quantity = $quantity - 1;
                                                                }
                                        echo '</select><br>';

				echo '<input type="submit" id="go" name="go" value="Cдать"><br>';
			}
			else 
				if (trim($action)==="1"){
					echo 'ФИО         <br><input id="name" type="text" name="name" ';
					if ($nameCookie!="") 
						echo 'value="'.$nameCookie.'"><br>'; 
					else echo '><br>';
					echo 'Куда        <br><input id="location" type="text" name="location" ';
					if ($locationCookie!="") 
						echo 'value="'.$locationCookie.'"><br>'; 
					else echo '><br>';

					/* echo 'Дата        <br> <input id="date" type="datetime" name="date" value="'.date("d").'-'.date("m").'-'.date("Y").'"><br>'; */
					 $quantity = 1;
					echo 'Дата <br><select name="date">';
							while($quantity<32){
									if (date("d") == $quantity){
									echo '<option value="'.$quantity.'" selected>'.$quantity.'</option>';
									}
									else{
									echo '<option value="'.$quantity.'">'.$quantity.' </option>';
									}
								$quantity = $quantity +1;
								}
					echo '</select>';   
					$quantity = 1;
                                        echo '<select name="month">';
                                                        while($quantity<13){
                                                                        if (date("m") == $quantity){
                                                                        echo '<option value="'.$quantity.'" selected>'.$quantity.'</option>';
                                                                        }
                                                                        else{
                                                                        echo '<option value="'.$quantity.'">'.$quantity.' </option>';
                                                                        }
                                                                $quantity = $quantity +1;
                                                                }
                                        echo '</select>';
					$quantity = date("Y");
					echo '<select name="year">';
                                                        while($quantity>1999){
                                                                        if (date("Y") == $quantity){
                                                                        echo '<option value="'.$quantity.'" selected>'.$quantity.'</option>';
                                                                        }
                                                                        else{
                                                                        echo '<option value="'.$quantity.'">'.$quantity.' </option>';
                                                                        }
                                                                $quantity = $quantity - 1;
                                                                }
                                        echo '</select><br>';



					echo 'Примечание <br><input type="textarea" name="comments" ';
					if ($commentCookie!="") 
						echo 'value="'.$commentCookie.'"><br>'; 
					else echo '><br>';
					echo '<input type="submit" id="go" name="go" value="Взять"><br>';
					setrawcookie("type","");
				}
				else
					echo "Нет доступных объектов";
			mysqli_close($db);
		 	}
			else{
                        	echo "fail!";
                        }
		if (isset($_POST['go'])){
				if ($db=mysqli_connect("localhost","mysql_boards","75020141551q1619w","boardsDataBase")) #подключение к бд: хост,логин,пароль, название бд
						 {      #делаются 3 запроса на получение актуальной информации об объекте
							$action = trim($_COOKIE['isFree']);
							mb_regex_encoding('UTF-8');
							mysqli_query($db,"SET NAMES utf8");
							mb_internal_encoding('UTF-8'); 
							if (!mysqli_set_charset($db,'utf8'))
					       		echo 'Charset setting fail';
							$cookieSerialNumber = $_POST['serialNumber'];
							$sql = 'SELECT `objId` FROM (SELECT * FROM `objects` WHERE `type`="'.$_POST['objType'].'") AS tab2 WHERE `serialNumber`="'.$cookieSerialNumber.'"';
							$rs = mysqli_query($db,$sql);
					       		$rightId = mysqli_fetch_array($rs);
							mysqli_free_result($rs);
							mysqli_query($db,"SET NAMES utf8"); 
							$sql = 'SELECT `isFree`,`type` FROM `objects` WHERE `objId`="'.trim($rightId[0]).'"';
							$rs = mysqli_query($db,$sql);
					       		$object = mysqli_fetch_array($rs);
                                                        $action = $object[0];
							mysqli_free_result($rs);
							$sql = 'SELECT `recordId`,`name`,`location`,`takingDate`,`comments` FROM `records` WHERE `objId`="'.trim($rightId[0]).'" ORDER BY `records`.`recordId` DESC';
							$rs = mysqli_query($db,$sql);
						       	$record = mysqli_fetch_array($rs);
							mysqli_free_result($rs);
							$sql = 'SELECT `spareSamples` FROM `objectTypes` WHERE `type`="'.$object[1].'"';
							$rs = mysqli_query($db,$sql);
						       	$free = mysqli_fetch_array($rs);
							mysqli_free_result($rs);
						        echo "<script type='text/javascript'>\n";
                                                        echo "document.cookie = 'type='".$object[1].";";
                                                        echo "</script>";

					               	if ($action==="1"){
								 if (trim($_POST['name'])!="" && trim($_POST['location'])!="" ){
									 /*$sql = 'INSERT INTO `records`(`recordId`, `objId`, `name`, `location`, `takingDate`, `comments`) VALUES ("'.f_ToUTF($record[0]+1).'","'.f_ToUTF($rightId[0]).'","'.f_ToUTF($_POST['name']).'","'.f_ToUTF($_POST['location']).'","'.f_ToUTF($_POST['date']).'","'.f_ToUTF($_POST['comments']).'")';*/
									 $dayMonthYear = f_ToUTF($_POST['date'])."-".f_ToUTF($_POST['month'])."-".f_ToUTF($_POST['year']);
									 $sql = 'INSERT INTO `records`(`recordId`, `objId`, `name`, `location`, `takingDate`, `comments`) VALUES ("'.f_ToUTF($record[0]+1).'","'.f_ToUTF($rightId[0]).'","'.f_ToUTF($_POST['name']).'","'.f_ToUTF($_POST['location']).'","'.$dayMonthYear.'","'.f_ToUTF($_POST['comments']).'")';

									 mysqli_query($db,$sql);
						       			 mysqli_free_result($rs);
									 $sql = 'UPDATE `objectTypes` SET `spareSamples`="'.($free[0]-1).'" WHERE `type`="'.$object[1].'"';
									 mysqli_query($db,$sql);
						       			 mysqli_free_result($rs);
									 $sql = 'UPDATE `objects` SET `isFree`="'."0".'" WHERE `objId`="'.$rightId[0].'"';
									 if (trim(mysqli_query($db,$sql))==="1"){ 
									 echo 'База обновлена';
									 setrawcookie("type",$object[1]);
									 #setrawcookie("id",$rightId[0]);
									 setrawcookie("serialNumber",$cookieSerialNumber ); 
									 setrawcookie("isFree",0);
									 }
									 else echo 'Ошибка';
						       			 mysqli_free_result($rs);
								}else{
									setrawcookie("type",$object[1]);
									setrawcookie("id",$rightId[0]);
									setrawcookie("serialNumber",$cookieSerialNumber ); 
									setrawcookie("isFree",1);
									setrawcookie("name",$_POST['name']);
									setrawcookie("location",$_POST['location']);
									setrawcookie("comment",$_POST['comments']);
									echo "<script type='text/javascript'>\n";
									echo "window.alert('Поля Имя, Куда и Дата обязательны для заполнения')\n";
									echo "document.location = '/index.php';\n";
									echo "</script>";
									}	
		 					}else if ($action==="0"){
								 $sql = 'UPDATE `objectTypes` SET `spareSamples`="'.($free[0]+1).'" WHERE `type`="'.$object[1].'"';
								 mysqli_query($db,$sql);
								 $sql = 'SELECT MAX(`recordId`) FROM `records` WHERE `objId`="'.$rightId[0].'"';
								 $rs = mysqli_query($db,$sql);
								 $maxid = mysqli_fetch_array($rs);
								 mysqli_free_result($rs);
								 $dayMonthYear = f_ToUTF($_POST['date'])."-".f_ToUTF($_POST['month'])."-".f_ToUTF($_POST['year']);
								 $sql = 'UPDATE `records` SET `returnDate`="'.$dayMonthYear.'" WHERE `records`.`objId`="'.$rightId[0].'" AND `records`.`recordId`="'.$maxid[0].'" ';
								 mysqli_query($db,$sql);
					       			 $sql = 'UPDATE `objects` SET `isFree`="'."1".'" WHERE `objId`="'.$rightId[0].'"';
								 if (trim(mysqli_query($db,$sql))==="1"){  
									 echo 'База обновлена';
									 setrawcookie("type",$object[1]);
									 setrawcookie("serialNumber",$cookieSerialNumber ); 
									 setrawcookie("isFree",1);
								 }
								 else echo 'Ошибка: нет доступных объектов';
					    			 mysqli_free_result($rs); 
								}else{
									setrawcookie("type",$object[1]);
									setrawcookie("serialNumber",$cookieSerialNumber ); 
									setrawcookie("isFree",0);
									setrawcookie("location",$_POST['location']);
									echo "<script type='text/javascript'>\n";
									echo "window.alert('Введите корректную дату сдачи в форме yyyy-mm-dd!')\n";
									echo "document.location = '/index.php';\n";
									echo "</script>";
									}
							}else{
								echo "fail!";
								} 
							mysqli_free_result($rs);
							setrawcookie("type",$_POST['objType']);
		  					echo "<script type='text/javascript'>\n";//Для обновления страницы после submit'а
							//echo "document.cookie = 'type='+".$object[1].";\n";
							echo "document.location = '/index.php';\n";
							echo "</script>";
			       		
		}
		?>
	</form>
    </body>
<html>
	
