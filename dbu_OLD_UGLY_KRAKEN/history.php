<html>
    <head>
	<title>История</title>	
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<style>
	p{
	color: green;
	
	}
	</style>
	<script type="text/javascript"> //js функции
		<!--
		function f_open1(){// Переход на страницу "Учет системных плат и комплектующих" для кнопки "Страница регистрации"
			document.location = "/index.php";
		}
		function f_open2(obj){// Переход на страницу "Просмотр объектов" для кнопки "Просмотр объектов"
			document.cookie = "type="+ obj;
			document.location = "/view.php";
		}

                function f_error(obj){
	 		window.alert('Объекта с кодом '+ obj + ' не существует!');
	     		document.location = "/index.php";
		}
		
		//-->
	</script>
    </head>
    <body>
	<font size="5"><it><b>История</b></it></font>
	
        <?php
		$cookieType = trim($_COOKIE['type']);
		$cookieId = trim($_COOKIE['id']);
		$cookieSerialNumber = trim($_COOKIE['serialNumber']);
		setrawcookie("id",""); 
		function f_winToUTF($str){
			return iconv(mb_detect_encoding($str),"UTF-8",$str);
		}	
		if ($db=mysqli_connect("localhost","mysql_boards","75020141551q1619w","boardsDataBase")) #подключение к бд: хост,логин,пароль, название бд
			{
			mb_regex_encoding('UTF-8'); 
			mysqli_query($db,"SET NAMES utf8");
			mb_internal_encoding('UTF-8'); 
			if (!mysqli_set_charset($db,'utf8'))
				echo 'Charset setting fail';
			if (trim($cookieId)===""){
				$sql = 'SELECT `objId` FROM (SELECT * FROM `objects` WHERE `type`="'.$cookieType.'") AS a WHERE `serialNumber`="'.$cookieSerialNumber.'"';
				$rs = mysqli_query($db,$sql);
				$rightId = mysqli_fetch_array($rs);
				mysqli_free_result($rs);
				$cookieId = $rightId[0];
				#setrawcookie("id",$cookieId); 
			}
			$sql = 'SELECT `type`,`isFree`,`serialNumber`,`isVerified`,`objComment` FROM (SELECT * FROM `objects` WHERE `type`="'.$cookieType.'") AS tab1  WHERE `objId`="'.trim($cookieId).'"';
			$rs = mysqli_query($db,$sql);
			$pole = mysqli_fetch_array($rs);
			echo '<input type="button" name="regButt" value="Страница регистрации" onclick="f_open1();">
		<input type="button" name="objListButt" value="Просмотр объектов" onclick="f_open2(`'.$pole[0].'`);">
		<hr>';
			if (trim($pole[0])===""){
				echo "<script type='text/javascript'>\n";
				#echo "window.alert('Объекта с кодом ".f_winToUTF($cookieSerialNumber)." не существует!')\n";
				echo "window.alert('Объекта с запрашиваемым номером не существует!')\n";
				echo "document.location = '/index.php';\n";
				echo "</script>";
			}
			echo 'Тип объекта - '.$pole[0];

			if ($pole[3]==="1")
			echo '<p>Серийный номер - '.$pole[2].'</p>';
			else 
				echo '<br>Серийный номер - '. $pole[2].'<br>';

			echo '<textarea disabled>'.$pole[4].'</textarea><br>';
			echo 'Статус:';
			if ($pole[1]==="1")
				echo 'Доступен';
			else 
				echo 'Недоступен';
			echo '<br>';
			mysqli_free_result($rs);
			$sql = 'SELECT `recordId`,`name`,`location`,`takingDate`,`returnDate`,`comments` FROM `records` WHERE `objId`="'.trim($cookieId).'" ORDER BY `records`.`recordId` DESC';
			$rs = mysqli_query($db,$sql); 
			echo '<table border="1" width="500">';
			echo	'<thead>';
			echo		'<tr>';
			echo		'<th>№</th>';
			echo		'<th>ФИО</th>';
			echo		'<th>Куда</th>';
			echo		'<th>Дата взятия</th>';
			echo		'<th>Дата возвращения</th>';
			echo		'<th>Примечание</th>';
			echo		'</tr>';
			echo	'</thead>';
			echo	'<tbody>';
			while ($pole = mysqli_fetch_array($rs)){
						echo '<tr>';
						echo '<td>'.$pole[0].'</td>'; 
						echo '<td>'.$pole[1].'</td>';
						echo '<td>'.$pole[2].'</td>';
						echo '<td>'.$pole[3].'</td>';
						echo '<td>'.$pole[4].'</td>';
						echo '<td>'.$pole[5].'</td>';
						echo '</tr>';
			}
			echo	'</tbody>';
			echo '</table>'; 
		mysqli_free_result($rs); 
		mysqli_close($db);
		}else{
			echo "fail!";
		}  
        ?>
    </body>
</html>
