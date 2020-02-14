<?php 
//Проверяем, пришел ли файл
if( !empty($_FILES['image']['name'])){
	//Проверяем, что при загрузке не произошло ошибоу
	if($_FILES['image']['error'] == 0){
	//Если файл загружен успешно, проверяем - графический ли он
		if( substr($_FILES['image']['type'], 0,5) =='image')
			{
			if ($db=mysqli_connect("localhost","mysql_boards","75020141551q1619w","boardsDataBase"))
			{
			//mb_regax_encoding('UTF-8');
			//mysqli_query($db,"SET NAMES utf8");
			//mb_internal_encoding('UTF-8');
			//if (!mysqli_set_charset($db,'utf8'))
			//	echo 'Charset setting fail';
			//Читаем содержимое файла
			$image = file_get_contents( $_FILES['image']['tmp_name']);
			//экранируем специальные символы изображения
			$image = mysqli_escape_string($image);
			//формируем запрос на добавление файла в базу данных
			$somePost = $_POST["hiddenTypeName"];
			//$query= 'UPDATE `boardsDataBase`.`objects` SET `objComment`="'.$somePost.'" WHERE `objId`="859"'; //Строка для проверки работоспособности скрипта 
			$query= 'UPDATE `boardsDataBase`.`objectTypes` SET `typeImage`="'.$image.'" WHERE `type`="'.$somePost.'"'; //Рабочий скрипт загрузки картинк в базу данных
			//После чего остается только выполнить данный запрос к базе данных
			mysqli_query($db, $query);
			mysqli_close($db);
			
			}
		}
	}
}

?>
