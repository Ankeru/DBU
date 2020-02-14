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
			 //$uploaddir = '';
			$uploaddir = 'typeImages/';
			
			$uploadfile = $uploaddir.basename($_FILES['image']['name']);
			echo $uploadfile;
			echo '<pre>';
			if (move_uploaded_file( $_FILES['image']['tmp_name'], $uploadfile)){
			echo 'succes';
			 //формируем запрос на добавление имени файла в базу данных
                        $imageName = $_FILES['image']['name'];
                        $somePost = $_POST["hiddenTypeName"];
                        //$query= 'UPDATE `boardsDataBase`.`objects` SET `objComment`="'.$somePost.'" WHERE `objId`="859"'; //Строка для проверки работоспособности скрипта
                        $query= 'UPDATE `boardsDataBase`.`objectTypes` SET `typeImage`="'.$imageName.'" WHERE `type`="'.$somePost.'"'; //Рабочий скрипт загрузки картинк в базу данных
                        //После чего остается только выполнить данный запрос к базе данных
                        mysqli_query($db, $query);
                        mysqli_close($db);
			}else{
			echo 'fail';}
			print_r($_FILES);
			print "</pre>";
			
			//Читаем содержимое файла
			//$image = file_get_contents( $_FILES['image']['tmp_name']);
			//экранируем специальные символы изображения
			//$image = mysqli_escape_string($image);
			}
		}
	}
}

?>
