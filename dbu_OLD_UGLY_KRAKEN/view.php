<html>
    <head>
	<title>Просмотр объектов</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <script type="text/javascript"> //js функции
		<!--

		function f_radio(password,radio){
		//document.cookie = "type="+ document.getElementById("objType").value;
		document.cookie = "password="+document.getElementById("password").value; 
		document.cookie = "radio="+radio;
		//window.alert(document.cookie);
		document.location = "/view.php";
		}
		function f_open1(){// Переход на страницу "Учет системных плат и комплектующих" для кнопки "назад"
			document.cookie = "password=";
			//document.cookie = "type="+ document.getElementById("objType").value;
			document.location = "/index.php";
		}
		function f_update(password){// Фактически переход на ту же самую страницу с новыми параметрами (для кнопки "Обновить"; при изменении значения выпадающего списка objType)
			document.cookie = "type="+ document.getElementById("objType").value;
			//document.cookie = "password="+password;
			document.cookie = "password="+document.getElementById("password").value;
			document.location = "/view.php";
		}
		function f_openRegParam1(objId){//Для кнопки "Страница регистрации"
			document.cookie = "type="+ document.getElementById("objType").value;
			document.cookie = "id="+ objId;
			document.cookie = "password=";
			document.location = "/index.php";
		} 
                function f_changeSerialNumber(objId){// Фактически переход на ту же самую страницу с новыми параметрами (для кнопок  "Изменить")
                        document.cookie = "type="+ document.getElementById("objType").value;
                        document.cookie = "id="+ objId;
                        document.cookie = "newSerialNum="+document.getElementById("serial"+objId).value;
			document.cookie = "password="+ document.getElementById("password").value;
              		document.location = "/view.php";
                }
		 function f_delete(objId){// Фактически переход на ту же самую страницу с новыми параметрами (для кнопок  "Изменить")
                        document.cookie = "type="+ document.getElementById("objType").value;
                        document.cookie = "deletionId="+ objId;
                        document.cookie = "password="+ document.getElementById("password").value;
                        document.location = "/view.php";
                }
		function f_deleteType(TypeName){//Для кнопки удаления типа
                        document.cookie = "deletionTypeName="+ TypeName;
                        document.cookie = "password="+ document.getElementById("password").value;
                        document.location = "/view.php";
                }
		function f_changeTypeName(TypeName){//Для кнопки изменения имени типа
                        document.cookie = "changingTypeName=" + TypeName;
                        document.cookie = "password=" + document.getElementById("password").value;
			document.cookie = "newTypeName=" + document.getElementById("type"+TypeName).value;
                        document.location = "/view.php";
                }

		function f_openHistory(objId){//Для кнопки "История".
			document.cookie = "type="+ document.getElementById("objType").value;
			document.cookie = "id="+ objId;
			document.cookie = "password=";
			document.location = "/history.php";
		}
		function f_changeVerified(objId,index){//Для изменения статуса спецпроверенности.
			document.cookie = "verifiedIndex=" + index;
			document.cookie = "type="+ document.getElementById("objType").value;
                        document.cookie = "id="+ objId;
			document.cookie = "password="+ document.getElementById("password").value;
                        document.location = "/view.php";
                }
		function f_deleteAllCookie(){
			document.cookie = "type=";
                        document.cookie = "deletionId=";
                        document.cookie = "deletionTypeName=";
                        document.cookie = "newTypeName=";
                        document.cookie = "changingTypeName=";
                        document.cookie = "verifiedIndex=";
                        document.cookie = "id=";
                        document.cookie = "newSerialNum=";
                        document.cookie = "password=";
			document.cookie = "comment=";
                        //document.cookie = "radio=";

		}
		function f_changeComment(objId){
		document.cookie = "id="+objId;
		document.cookie = "comment="+ document.getElementById(objId+"Comment").value; 
		document.cookie = "type="+ document.getElementById("objType").value;
		document.cookie = "password="+ document.getElementById("password").value;
		document.location = "/view.php";
		}

                        

		//-->
	</script>
    </head>
    <body>
	<font size="5"><it><b>Просмотр объектов</b></it></font>
	<input type="button" name="back" value="Страница учета" onclick="f_open1();">
	<hr>  
		<?php
			$AdminPassword= "whiterabbit";//Здесь задается пароль доступа
			$cookieType = trim($_COOKIE['type']);
                        $IdCookie = trim($_COOKIE['id']);
			$SerialNumCookie = trim($_COOKIE['newSerialNum']);
			$DeletionIdCookie = trim($_COOKIE['deletionId']);
                        $PasswordCookie = trim($_COOKIE['password']);
			$RadioCookie = trim($_COOKIE['radio']);
			$DelitionTypeNameCookie =  trim($_COOKIE['deletionTypeName']);
			$NewTypeName = trim($_COOKIE['newTypeName']);
			$ChangingTypeNameCookie =  trim($_COOKIE['changingTypeName']);
			$VerifiedIndexCookie = trim($_COOKIE['verifiedIndex']);
			$CommentCookie = trim($_COOKIE['comment']);
			echo "<script type='text/javascript'>\n";
			echo 'f_deleteAllCookie();';
			//echo 'window.alert(document.cookie)';
			echo "</script>";

                       	function f_winToUTF($str){
				return iconv(mb_detect_encoding($str),'UTF-8',$str);
			}

			if ($db=mysqli_connect("localhost","mysql_boards","75020141551q1619w","boardsDataBase")) #подключение к бд: хост,логин,пароль, название бд
				{
////////////////////////////////////Шаманство с кодировками
				mb_regex_encoding('UTF-8'); 
				mysqli_query($db,"SET NAMES utf8");
				mb_internal_encoding('UTF-8'); 
				if (!mysqli_set_charset($db,'utf8'))
			       		echo 'Charset setting fail';
///////////////////////////////////Шаманство закончилось

			        if (!(trim($IdCookie)===""))//Для кнопки "Изменить (объект)"
                                	if(!(trim($SerialNumCookie)===""))
						 if($PasswordCookie===$AdminPassword)
						{
						$sql = 'update `objects` SET `serialNumber` = "'.$SerialNumCookie.'" WHERE `objId`='.$IdCookie;
						mysqli_query($db,$sql);
	                			setrawcookie("type",$cookieType);
						
 		               		        echo "<script type='text/javascript'>\n";
						echo 'f_deleteAllCookie();';
                                                echo 'document.cookie = "type='.$cookieType.'";'; 
						echo "document.location = '/view.php'";
                                                echo "</script>";
						} else {
                                               	echo "<script type='text/javascript'>\n";
						echo 'f_deleteAllCookie();';
                                                echo "window.alert('Пароль введен неверно!')";
						echo "</script>";
						}
						

                                if (!(trim($DeletionIdCookie)===""))//Для кнопки "Удалить (объект)"
                                        if(trim($PasswordCookie)===$AdminPassword)
                                                {
						$sql = 'DELETE FROM `objects` WHERE `objId`='.$DeletionIdCookie;
                                        	mysqli_query($db,$sql);
                                                echo "<script type='text/javascript'>\n";
						echo 'f_deleteAllCookie();';
					        echo "document.cookie = 'type='".$cookieType ;
                                                echo "document.location = '/view.php'";
                                                echo "</script>";
                                                } else {	
                                                echo "<script type='text/javascript'>\n";
						echo 'f_deleteAllCookie();';
                                                echo "window.alert('Пароль введен неверно!')";
                                                echo "</script>";
                                                }

				if (!(trim($DelitionTypeNameCookie)===""))//Для кнопки "Удалить (Тип)"
                                        if(trim($PasswordCookie)===$AdminPassword)
                                                {
                                                $sql = 'DELETE FROM objectTypes WHERE `type`="'.$DelitionTypeNameCookie.'"';
                                                mysqli_query($db,$sql);
                                                echo "<script type='text/javascript'>\n";
                                                echo 'f_deleteAllCookie();';
                                                //echo "document.location = '/view.php'";
                                                echo "</script>";
                                                } else {
						setrawcookie("deletionTypeName","");
                                                echo "<script type='text/javascript'>\n";
						echo 'f_deleteAllCookie();';
                                                echo "window.alert('Пароль введен неверно!')";
                                                echo "</script>";
                                                }
				
				if (!(trim($ChangingTypeNameCookie)===""))//Для кнопки "Изменить (Тип)"
					if(!(trim($NewTypeName)===""))      
                                  		if(trim($PasswordCookie)===$AdminPassword)
					        {
                                                $sql = 'UPDATE `objectTypes` SET `type` = "'.$NewTypeName.'"  WHERE `type`="'.$ChangingTypeNameCookie.'"';
                                                
                                                mysqli_query($db,$sql);
                                                echo "<script type='text/javascript'>\n";
 						echo 'f_deleteAllCookie();';                                   
                                                ///view.phpecho "document.location = '/view.php'";
                                                echo "</script>";
                                                } else {
                                                echo "<script type='text/javascript'>\n";
                                                echo 'f_deleteAllCookie();';
						echo "window.alert('Пароль введен неверно!')";
                                                echo "</script>";
                                                }

				if (!(trim($VerifiedIndexCookie)===""))//Для чекбокса спецпроверки
                                        if(!(trim($IdCookie)===""))
                                                if(trim($PasswordCookie)===$AdminPassword)
                                                {
						if (trim($VerifiedIndexCookie)==="1")
							 $sql = 'UPDATE `objects` SET `isVerified` = "0" WHERE `objId`="'.$IdCookie.'"';
						else 
							 $sql = 'UPDATE `objects` SET `isVerified` = "1" WHERE `objId`="'.$IdCookie.'"';
                                                mysqli_query($db,$sql);
                                                echo "<script type='text/javascript'>\n";
                                                echo 'f_deleteAllCookie();';
                                                // echo "document.location = '/view.php'";
                                                echo "</script>";
                                                } else {
						echo "<script type='text/javascript'>\n";
                                                echo 'f_deleteAllCookie();';
						echo "window.alert('Пароль введен неверно!')";
                                                echo "</script>";
                                                }

				if (!(trim($CommentCookie)===""))//Для изменения комментария к типу
					if(!(trim($IdCookie)===""))
						if(trim($PasswordCookie)===$AdminPassword)
						{
						$sql = 'UPDATE `objects` SET `objComment` = "'.trim($CommentCookie).'" WHERE `objId`="'.$IdCookie.'"';
						mysqli_query($db,$sql);

						echo "<script type='text/javascript'>\n";
                                                echo 'f_deleteAllCookie();';
						echo "</script>";
						}else {
                                        	        echo "<script type='text/javascript'>\n";
                                                	echo 'f_deleteAllCookie();';
                                                	echo "window.alert('Пароль введен неверно!')";
                                                	echo "</script>";
                                                       }




					$sql = 'SELECT `type` FROM `objectTypes` ORDER BY `objectTypes`.`type` ASC';
					$rs = mysqli_query($db,$sql);
					$pole = mysqli_fetch_array($rs);

					if (trim($RadioCookie)==="")
					$RadioCookie = "choice";

                                        switch($RadioCookie) {
					case 'choice'://Режим "Выбор"
					{
					echo 'Тип  <select id="objType"  name="objType" onchange="f_update('.$PasswordCookie.');" >';
                                       	if (trim($cookieType)==="")
                                               $cookieType = $pole[0];

                                        echo '<option value="'.$pole[0];

					if ($pole[0] === $cookieType )
                                        	echo '" selected>';
                                	else 
                                        	echo '">';

                                	echo $pole[0];
                                	echo '</option>';
                                	while ($pole = mysqli_fetch_array($rs)){
                                        	echo '<option value="'.$pole[0];
                                        	if ($pole[0]===$cookieType ) 
                                                	echo '" selected>';
                                        	else 
                                               		echo '">';
                                        	echo $pole[0].'</option>';
                               	 	}
                                	echo '</select>';

					echo '<input id="radChoice" type="radio" name="typeRadio" onclick="f_radio(`'.$PasswordCookie.'`,`choice`);" checked> Выбор
        	                        <input id="radEdit" type="radio" name="typeRadio" onclick="f_radio(`'.$PasswordCookie.'`,`edit`);"> Редактирование';
					 mysqli_free_result($rs);

                                	echo '<br>Свободно:';
                                	$sql = 'SELECT COUNT(*) FROM (SELECT * FROM `objects` WHERE `type`="'.$cookieType .'") AS tab1  WHERE `isFree`="1"';
                                	$rs = mysqli_query($db,$sql);
                                	$pole = mysqli_fetch_array($rs);
                                	echo $pole[0];
                             		mysqli_free_result($rs);

                              	  	echo ' из ';
                                	$sql = 'SELECT COUNT(*) FROM (SELECT * FROM `objects` WHERE `type`="'.$cookieType .'") AS tab1';
                                	$rs = mysqli_query($db,$sql);
                                	$pole = mysqli_fetch_array($rs);
                                	echo $pole[0];
                                	mysqli_free_result($rs);

                                	echo '. Пароль для изменений:';
                                	echo '<input id="password" type="password" name="password" value="'.$PasswordCookie.'">';
                               	 	
					echo '   <table border="1" width="1400">
               					 <thead>
                        			   <tr>
                        			 	<th>Серийный номер</th>
                        			 	<th>Статус</th>
                        			 	<th>Действие</th>
							<th>Комментарий</th>
                       				   </tr>
                				 </thead>';
	               			echo '  <tbody>';
					$GlobalColorStyle = 'style="color:green;"';
                                        $sql = 'SELECT `objId`,`isFree`,`serialNumber`, `isVerified`, `objComment` FROM `objects` WHERE `type`="'.$cookieType .'" ORDER BY `objects`.`serialNumber` ASC';
                                	$rs = mysqli_query($db,$sql);
                                		while ($pole = mysqli_fetch_array($rs))
							{
                                        		echo '<tr>';
                                        		echo '<td><input ';
							if ($pole[3]==="1")
								echo  $GlobalColorStyle;
							echo ' id="serial'.$pole[0].'" type="text" name="serial'.$pole[0].'" value="'.$pole[2].'">
                                               		<input type="button" name="'.$pole[0].'ChangeButton" value="Изменить" onclick="f_changeSerialNumber(`'.$pole[0].'`);"></td>';
                                        		if  ($pole[1]==="1")
                                               			echo '<td>'."Доступен".'</td>';
                                        		else 
								{  $sql = 'SELECT `location` FROM `records`  WHERE `objId`="'.$pole[0].'" ORDER BY `records`.`recordId` DESC';
                                               			$reque = mysqli_query($db,$sql);
                                               			$prec = mysqli_fetch_array($reque);
                                               			mysqli_free_result($reque);
                                               			echo '<td>Взят '.$prec[0].'</td>';
                                               			}
                                        		echo '<td>'.'<input type="button" name="'.$pole[0].'RegButton" value="Страница регистрации" onclick="f_openRegParam1(`'.$pole[0].'`);">';
                                        		echo '<input type="button" name="'.$pole[0].'HistoryButton" value="История" onclick="f_openHistory(`'.$pole[0].'`);">';
                                        		echo '<input type="button" name="'.$pole[0].'DeleteButton" value="Удалить" onclick="f_delete(`'.$pole[0].'`);">';
							echo '<input type="checkbox" id="'.$pole[0].'verifiedCheckboxId" name="'.$pole[0].'verifiedCheckbox" value="Удалить" onclick="f_changeVerified(`'.$pole[0].'`,`'.trim($pole[3]).' `);"';
							if ($pole[3]==="1")
								echo ' checked>';
							else 
								echo '>';
							echo '<label for="'.$pole[0].'verifiedCheckboxId">Спецпроверенная</label></td>';
							echo '<td><input size="40" id="'.$pole[0].'Comment" type="text" value="'.$pole[4].'" >
							<input type="button" value="Изменить" onclick="f_changeComment(`'.$pole[0].'`);"></td>';
                                        		echo '</tr>';
                                			}
                                		mysqli_free_result($rs);
                             	 	  echo  ' </tbody>
        					   </table>';
						};
						break;

                                        case 'edit':{//Режим "Редактирование"
					echo '<input id="radChoice" type="radio" name="typeRadio" onchange="f_radio(`'.$PasswordCookie.'`,`choice`);"> Выбор
                                        <input id="radEdit" type="radio" name="typeRadio" onchange="f_radio(`'.$PasswordCookie.'`,`edit`);" checked> Редактирование';
					echo '<br> Пароль для изменений: <input id="password" type="password" name="password" value="'.$PasswordCookie.'"><br>';

                                        echo '   <table border="1" width="481">
                                                 <thead>
                                                   <tr>
                                                   <th>Тип</th>
						   <th>Картинка</th>
                                                   </tr>
                                                 </thead>';
                                        echo '  <tbody>';
					$sql = 'SELECT `type` FROM `objectTypes` ORDER BY `objectTypes`.`type` ASC';
					$rs = mysqli_query($db,$sql);
					
					while ($pole = mysqli_fetch_array($rs))
                                        	{
						echo '<tr>';
						echo '<td><input  size="42" id="type'.$pole[0].'" type="text" name="type'.$pole[0].'" value="'.$pole[0].'">';
						echo '<input type="button" name="'.$pole[0].'ChangeButton" value="Изменить" onclick="f_changeTypeName(`'.$pole[0].'`);">';
						echo '<input type="button" name="'.$pole[0].'DeleteButton" value="Удалить" onclick="f_deleteType(`'.$pole[0].'`);">'.'</td>';
						echo '<td>';
						echo '<form enctype="multipart/form-data" method="post" action="saveImg.php">
						<fieldset>
						<input type="hidden" name="hiddenTypeName" value="'.$pole[0].'">
						Изображение: <input type="file" name="image" />
						<input type="submit" value="Загрузить" />
						</fieldset>
						</form>';
						echo '</td>';
						echo '</tr>';
						}
				         echo  ' </tbody>
                                                   </table>';
					};
					break;
					}
			}else{echo "fail!";}
		?>
    </body>
</html>
