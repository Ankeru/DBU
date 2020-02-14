<html>
    <head>
	<title>Добавление</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<script type="text/javascript"> //js функции
		<!--
		function f_open1(){// Переход на страницу "Учет системных плат и комплектующих" для кнопки "Страница регистрации"
			document.cookie = "type="+ document.getElementById("objType").value;
			document.location = "/index.php";
		}
		function f_open2(){// Переход на страницу "Просмотр объектов" для кнопки "Просмотр объектов"
			document.cookie = "type="+ document.getElementById("objType").value;
			document.location = "/view.php";
		}
                function f_update(){// Фактически переход на ту же самую страницу с новыми параметрами 
			document.cookie = "num ="+ document.getElementById("objNum").value+";";
			document.location = "/edit.php";
		}
		
		function f_change(){// Смена поля для ввода типа
			if (document.getElementById("myShowBlock1").style.display == "none"){
				document.getElementById("myShowBlock1").style.display = "block";
	   		} else {
				document.getElementById("myShowBlock1").style.display = "none";
			}
			if (document.getElementById("myShowBlock2").style.display == "none"){
				document.getElementById("myShowBlock2").style.display = "block";
	   		} else {
				document.getElementById("myShowBlock2").style.display = "none";
			}	
		}
		//-->
	</script>
    </head>
    <body>
	<font size="5"><it><b>Добавление новых объектов</b></it></font>
 	<input type="button" name="regButt" value="Страница учета" onclick="f_open1();"><input type="button" name="objWiewButt" value="Просмотр объектов" onclick="f_open2();"><hr>
        <?php
		$cookieType = trim($_COOKIE['type']);
		$cookieNum = 20;

		function f_winToUTF($str){
			return iconv(mb_detect_encoding($str),'UTF-8',$str);
		}
        	#if (trim($_COOKIE['num'])!="" && trim($_COOKIE['num'])!="0"){
		if ($db=mysqli_connect("localhost","mysql_boards","75020141551q1619w","boardsDataBase")) #подключение к бд: хост,логин,пароль, название бд
			{
				mb_regex_encoding('UTF-8'); 
				mysqli_query($db,"SET NAMES utf8");
				mb_internal_encoding('UTF-8'); 
				if (!mysqli_set_charset($db,'utf8'))
			       	echo 'Charset setting fail';
				echo '<form  method="POST">';
				echo 'Тип ';
				echo '<div id="myShowBlock1"> ';
		                echo '<select id="objType"  name="objType">';
				$sql = 'SELECT `type` FROM `objectTypes` ORDER BY `objectTypes`.`type` ASC';
				$rs = mysqli_query($db,$sql);
		                $pole = mysqli_fetch_array($rs);
				echo '<option value="'.f_winToUTF($pole[0]);
		                if ($cookieType===$pole[0])
					echo '" selected>';//Для автоматического выбора значения при переходе со страницы "Просмотр объектов"
		                else 
					echo '">';
		                echo f_winToUTF($pole[0]);
		                echo '</option>';
		                while ($pole = mysqli_fetch_array($rs)){
					echo '<option value="'.f_winToUTF($pole[0]);
				        if ($cookieType===$pole[0]) 
					 	echo '" selected>';//Для автоматического выбора значения при переходе со страницы "Просмотр объектов"
				        else
						echo '">';
				        echo f_winToUTF($pole[0]).'</option>';
		                 }
		                 echo '</select>';
				 echo '</div>';
				 echo '<div id="myShowBlock2"> ';
				 echo '<input type="text" id="typeName" name="typeName">';
				 echo '</div>';
				 echo ' Новый <input type="checkbox" name="check1" id="check1" value="yes" onclick="f_change();">';
				 echo "<script language='javascript'>"."\n";
				 echo "document.getElementById('myShowBlock1').style.display = 'block';"."\n";
				 echo "document.getElementById('myShowBlock2').style.display = 'none';"."\n";
				 echo '</script>'."\n";
				 echo '<br>';				 
		                 mysqli_free_result($rs); 
			for ($i=0,$c=$cookieNum;$i<$c;$i++){
				echo 'Серийный номер__';
				if ($i<9)
					echo '_';
				echo ($i+1).' ';
				echo '<input type="text" name="serialNumber'.($i+1).'tf">';
				echo '<input type="checkbox" id="box'.($i+1).'" name="checkbox'.($i+1).'" onclick="">';
				echo '<label for="box'.($i+1).'">Спецпроверенная</label> <br>';
			}
			setrawcookie("var",$cookieNum);
			setrawcookie("num","");
			setrawcookie("type","");
		
			echo '<input type="submit" name="go" value="Добавить"><br>';
			echo '</form>';
			mysqli_close($db);
		}else{
			echo "fail!";
		}
		#} else{echo 'Количество новых объектов <br><input type="text" id="objNum" name="objNum" value="0"><input type="button" name="numButt" value="Начать добавление" onclick="f_update();"><br>';} 
		if (isset($_POST['go'])){
		//	$number = trim($_COOKIE['var']);
                         $number =20;
			setrawcookie("var","");
			if ($db=mysqli_connect("localhost","mysql_boards","75020141551q1619w","boardsDataBase")) #подключение к бд: хост,логин,пароль, название бд
				{   
				//Шаманство с кодировками начато
				mb_regex_encoding('UTF-8'); 
				mysqli_query($db,"SET NAMES utf8");
				mb_internal_encoding('UTF-8'); 
				if (!mysqli_set_charset($db,'utf8'))
					echo 'Charset setting fail';  
				mysqli_query($db,"SET NAMES utf8");
				if (!mysqli_set_charset($db,'utf8'))
					echo 'Charset setting fail';
				//Шаманство с кодировками окончено
				$mark = 1;

				if (trim($_POST['check1'])==="yes")
					{
					$nameOfType = $_POST['typeName'];
				      	}
				else {
					$nameOfType =  $_POST['objType'];	
				}
				if (trim($nameOfType)===""){
						$mark = 0;
					}
				if ($mark!=0){
				$numofobjects = 0;
				for ($i=1,$c=$number+1;$i<$c;$i++){
					$str = 'serialNumber'.$i.'tf';
					if (trim($_POST[$str])!=""){
						$sql = 'SELECT `serialNumber` FROM (SELECT * FROM `objects` WHERE `type`="'.$nameOfType.'") AS tab WHERE `serialNumber`="'.$_POST[$str].'"';
						$arec = mysqli_query($db,$sql);
						$ifThereAreDuplicate = mysqli_fetch_array($arec);
						mysqli_free_result($arec);
					if  (trim($ifThereAreDuplicate[0])===""){
							$varCheckBoxName = 'checkbox'.$i;
							if (isset($_POST[$varCheckBoxName]))
							 $sql = 'INSERT INTO `objects` (`serialNumber`, `isFree`, `type`, `isVerified`) VALUES ("'.$_POST[$str].'", 1, "'.$nameOfType.'", 1)';
							else
							 $sql = 'INSERT INTO `objects` (`serialNumber`, `isFree`, `type`, `isVerified`) VALUES ("'.$_POST[$str].'", 1, "'.$nameOfType.'", 0)';

							if (trim(mysqli_query($db,$sql))!="1") $mark = 0; 
								else $numofobjects++;
						}
					}
				}
				if (trim($_POST['check1'])==="yes"){
					  $sql = 'INSERT INTO `objectTypes`(`type`, `spareSamples`) VALUES ("'.$_POST['typeName'].'","'.$numofobjects.'")';
					  mysqli_query($db,$sql);
				}else {
					  $sql = 'SELECT `spareSamples` FROM `objectTypes` WHERE `type`="'.$_POST['objType'].'"';
					  $rs = mysqli_query($db,$sql);
					  $free = mysqli_fetch_array($rs);
					  mysqli_free_result($rs);
					  $newvalue  = $free[0]+$numofobjects;
					  $sql = 'UPDATE `objectTypes` SET `spareSamples`="'.$newvalue.'" WHERE `type`="'.$_POST['objType'].'"';
					  mysqli_query($db,$sql);
				}
				if (trim($mark)==="1"){
					setrawcookie("type",$nameOfType);
					echo "<script type='text/javascript'>\n";
					echo "window.alert('Операция прошла успешно, добавлено ".$numofobjects." объектов!')\n";
					echo 'document.cookie = "type="+ document.getElementById("objType").value;';
					echo "document.location = '/index.php';\n";
					echo "</script>";
				}else {
					echo "<script type='text/javascript'>\n";
					echo "window.alert('Ошибка!')\n";
					echo 'document.cookie = "type="+ document.getElementById("objType").value;';
					echo "document.location = '/index.php';\n";
					echo "</script>";
				}
				} else {
					echo "<script type='text/javascript'>\n";
					echo "window.alert('Введите название типа')\n";
					echo "</script>";
				}
			}else {
				echo 'fail!';}
		}
        ?>
    </body>
</html>
