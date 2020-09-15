// Переключает поля ввода типа (выпадающее меню/текстовое поле) в зав-ти от состояния чек-бокса
function manage_type_cb_change()
{
    if ($('#new_type_cb').is(':checked'))
    {
        $('#new_type').prop("hidden", false);
        $('#chosen_type').prop("hidden", true);
    } else {
        $('#new_type').prop("hidden", true);
        $('#chosen_type').prop("hidden", false);        
    }          
}
$('#new_type_cb').change(manage_type_cb_change);


// Добавляет строку в конец таблицы
function add_new_entity_block(){
    window.onbeforeunload = onbeforun; 
    var last_record_num = (Number($('input[type="text"]#hidden_counter').val())+ 1);
    var record_count = (Number($('input[type="text"]#hidden_string_count').val())+ 1);
    $('input[type="text"]#hidden_string_count').val(record_count)
    $('#hidden_counter').val(last_record_num);
    $('table.relative_container').append(`
                    <tr class="new_entity_line"  name="new_entity_block_`+ last_record_num +`" >
                    <td name="object_num_`+ last_record_num +`">`+ record_count+`</td>
                    <td><input type="text" name="select_serial_num_`+ last_record_num +`" title='Серийный №'/></td>                    
                    <td><input type="date" name="production_date_`+ last_record_num +`" class='large_date'/></td>
                    <td>
                        <label class="custom-file-upload">
                            <input type="file" name="label_ref_`+ last_record_num +`" class="link_content"/>
                        </label>
                    </td>
                    <td><textarea class="textarea_standart_size_content" name="loc_of_storage_original_label_`+ last_record_num +`" class="loc_content" ></textarea></td> 
                    <td><input type="date" name="date_of_delivery_`+ last_record_num +`" class='large_date'/></td>                                                                               
                    <td><input type="file" name="delivery_document_`+ last_record_num +`"class="link_content"/></td>
                    <td><textarea class="textarea_standart_size_content" name="loc_of_storage_original_delivery_document_`+ last_record_num +`" class="loc_content" ></textarea></td>                                                                               
                    <td><textarea class="textarea_standart_size_content" name="note_`+ last_record_num +`"></textarea></td>
                    <td>
                    <div class="profile_property">
                        <input type="checkbox" class="checkbox" name='special_check_`+ last_record_num +`' id='special_check_`+ last_record_num +`' />
                        <label for="special_check_`+ last_record_num +`"></label>
                    </div>
                    </td> 
                    <td>
                        <div class="num_n_delete_block"><img class="delete" src="" title="Удалить" alt='Удалить' onclick="deleteBlock(`+ last_record_num +`)" name="img_`+ last_record_num +`">                      
                        <div class="num_n_delete_block"><img class="delete" src="" title="Копировать" alt='Копировать' onclick="toogle_modal(`+ last_record_num +`)" name="img_`+ last_record_num +`1">  
                        <div class="num_n_delete_block"><img class="delete" src="" title="Добавить после текущей строки" alt='Добавить после текущей строки' onclick="add_new_entity_block_after(`+ last_record_num +`, 1)" name="img_`+ last_record_num +`2">  
                    </td>                                                                               
                </tr>`
        );
        // Копируем картинки из скрытого источника, так как нет возможность отрендерить url
        $('img[name="img_' + last_record_num + '"]').attr('src', $('img[name="img_0"]').attr('src'));
        $('img[name="img_' + last_record_num + '2"]').attr('src', $('img[name="img_01"]').attr('src'));
        $('img[name="img_' + last_record_num + '1"]').attr('src', $('img[name="img_02"]').attr('src'));    
}
$('#more_block').click(add_new_entity_block);


// Добавляет строку после элемента
function add_new_entity_block_after(record_num){
    //Теперь при закрытии окна будет выдаваться предупреждение
    window.onbeforeunload = onbeforun;
    // 
    //Перебиваем номера на строках, которые должны оказаться под вставкой. Начинаем с конца, чтобы дважды не менять одну строку.
    var block_num = $("body").find(`td[name="object_num_`+ record_num +`"]`).eq(0).text();           
    for (var i = Number($('input[type="text"]#hidden_string_count').val()); i > Number(block_num) + 1 - 1; i--) {                      
            $("body").find(`td[name="object_num_`+ get_inner_num_by_outer_position(i) +`"]`).eq(0).text(i + 1);
        }

    //Берём последний внутренний номер + 1
    let new_last_record_num = Number($('#hidden_counter').val()) + 1 
    $('#hidden_counter').val(new_last_record_num)

    // Получаем количество строк на странице + 1 
    var record_count = (Number($('input[type="text"]#hidden_string_count').val())+ 1);
    $('input[type="text"]#hidden_string_count').val(record_count);

    // Получаем номер нового блока
    var new_block_num = Number($("body").find(`td[name="object_num_`+ record_num +`"]`).eq(0).text()) + 1;

    // Вставляем новую строку
    $('tr[name="new_entity_block_' + record_num + '"]').after(`
                    <tr class="new_entity_line"  name="new_entity_block_`+ new_last_record_num +`" >
                        <td name="object_num_`+ new_last_record_num +`">` + new_block_num + `</td>
                        <td><input type="text" name="select_serial_num_`+ new_last_record_num +`" title='Серийный №'/></td>                    
                        <td><input type="date" name="production_date_`+ new_last_record_num +`" class='large_date'/></td>
                        <td>
                            <label class="custom-file-upload">
                                <input type="file" name="label_ref_`+ new_last_record_num +`" class="link_content"/>
                            </label>
                        </td>
                        <td><textarea class="textarea_standart_size_content" name="loc_of_storage_original_label_`+ new_last_record_num +`" class="loc_content" ></textarea></td> 
                        <td><input type="date" name="date_of_delivery_`+ new_last_record_num +`" class='large_date'/></td>                                                                               
                        <td><input type="file" name="delivery_document_`+ new_last_record_num +`"class="link_content"/></td>
                        <td><textarea class="textarea_standart_size_content" name="loc_of_storage_original_delivery_document_`+ new_last_record_num +`" class="loc_content" ></textarea></td>                                                                               
                        <td><textarea class="textarea_standart_size_content" name="note_`+ new_last_record_num +`"></textarea></td>
                        <td>
                        <div class="profile_property">
                            <input type="checkbox" class="checkbox" name='special_check_`+ new_last_record_num +`' id='special_check_`+ new_last_record_num +`' />
                            <label for="special_check_`+ new_last_record_num +`"></label>
                        </div>
                        </td> 
                        <td>
                            <div class="num_n_delete_block"><img class="delete" src="" title="Удалить" alt='Удалить' onclick="deleteBlock(`+ new_last_record_num +`)" name="img_`+ new_last_record_num +`">                      
                            <div class="num_n_delete_block"><img class="delete" src="" title="Копировать" alt='Копировать' onclick="toogle_modal(`+ new_last_record_num +`)" name="img_`+ new_last_record_num +`1">  
                            <div class="num_n_delete_block"><img class="delete" src="" title="Добавить после текущей строки" alt='Добавить после текущей строки' onclick="add_new_entity_block_after(`+ new_last_record_num +`)" name="img_`+ new_last_record_num +`2">  
                        </td>                                                                               
                    </tr>`
        );
        // Копируем картинки из скрытого источника, так как нет возможность отрендерить url
        $('img[name="img_' + new_last_record_num + '"]').attr('src', $('img[name="img_0"]').attr('src'));
        $('img[name="img_' + new_last_record_num + '2"]').attr('src', $('img[name="img_01"]').attr('src'));
        $('img[name="img_' + new_last_record_num + '1"]').attr('src', $('img[name="img_02"]').attr('src'));    
}

function add_several_new_entity_blocks_after(record_num, n){
    //Теперь при закрытии окна будет выдаваться предупреждение
    window.onbeforeunload = onbeforun;

    //Берём последний внутренний номер + 1
    let new_last_record_num = Number($('#hidden_counter').val()) + 1 
    $('#hidden_counter').val(new_last_record_num)

    // Получаем количество строк на странице + 1 
    var record_count = (Number($('input[type="text"]#hidden_string_count').val())+ 1);
    $('input[type="text"]#hidden_string_count').val(record_count);

    // Получаем номер нового блока
    var new_block_num = Number($("body").find(`td[name="object_num_`+ record_num +`"]`).eq(0).text())+n;

    // Вставляем новую строку
    $('tr[name="new_entity_block_' + record_num + '"]').after(`
                    <tr class="new_entity_line"  name="new_entity_block_`+ new_last_record_num +`" >
                        <td name="object_num_`+ new_last_record_num +`">` + new_block_num + `</td>
                        <td><input type="text" name="select_serial_num_`+ new_last_record_num +`" title='Серийный №'/></td>                    
                        <td><input type="date" name="production_date_`+ new_last_record_num +`" class='large_date'/></td>
                        <td>
                            <label class="custom-file-upload">
                                <input type="file" name="label_ref_`+ new_last_record_num +`" class="link_content"/>
                            </label>
                        </td>
                        <td><textarea class="textarea_standart_size_content" name="loc_of_storage_original_label_`+ new_last_record_num +`" class="loc_content" ></textarea></td> 
                        <td><input type="date" name="date_of_delivery_`+ new_last_record_num +`" class='large_date'/></td>                                                                               
                        <td><input type="file" name="delivery_document_`+ new_last_record_num +`"class="link_content"/></td>
                        <td><textarea class="textarea_standart_size_content" name="loc_of_storage_original_delivery_document_`+ new_last_record_num +`" class="loc_content" ></textarea></td>                                                                               
                        <td><textarea class="textarea_standart_size_content" name="note_`+ new_last_record_num +`"></textarea></td>
                        <td>
                        <div class="profile_property">
                            <input type="checkbox" class="checkbox" name='special_check_`+ new_last_record_num +`' id='special_check_`+ new_last_record_num +`' />
                            <label for="special_check_`+ new_last_record_num +`"></label>
                        </div>
                        </td> 
                        <td>
                            <div class="num_n_delete_block"><img class="delete" src="" title="Удалить" alt='Удалить' onclick="deleteBlock(`+ new_last_record_num +`)" name="img_`+ new_last_record_num +`">                      
                            <div class="num_n_delete_block"><img class="delete" src="" title="Копировать" alt='Копировать' onclick="toogle_modal(`+ new_last_record_num +`)" name="img_`+ new_last_record_num +`1">  
                            <div class="num_n_delete_block"><img class="delete" src="" title="Добавить после текущей строки" alt='Добавить после текущей строки' onclick="add_new_entity_block_after(`+ new_last_record_num +`)" name="img_`+ new_last_record_num +`2">  
                        </td>                                                                               
                    </tr>`
        );
        // Копируем картинки из скрытого источника, так как нет возможность отрендерить url
        $('img[name="img_' + new_last_record_num + '"]').attr('src', $('img[name="img_0"]').attr('src'));
        $('img[name="img_' + new_last_record_num + '2"]').attr('src', $('img[name="img_01"]').attr('src'));
        $('img[name="img_' + new_last_record_num + '1"]').attr('src', $('img[name="img_02"]').attr('src'));    
}

// Переключаем видимость модального окна
function toogle_modal(x){
    window.onbeforeunload = onbeforun; 
    $('#hidden_string_number').val(x);
    var modal = document.querySelector("#modal");
    var modalOverlay = document.querySelector("#modal-overlay");
    modal.classList.toggle("closed");
    modalOverlay.classList.toggle("closed")     
}

// Добавляет строки после данной
function add_strings(){
    window.onbeforeunload = onbeforun; 
    // Количество элементов для вставки
    let n = Number($('#copy_count').val())
    // Внутренний номер элемента после которого вставляем новые элементы
    let num = Number($('#hidden_string_number').val())
    // Крайний задействованный внутренний номер
    let last_number = Number($('#hidden_counter').val())          

    //Перебиваем номера на строках, которые должны оказаться под вставкой. Начинаем с конца, чтобы дважды не менять одну строку.
    var block_num = $("body").find(`td[name="object_num_`+ num +`"]`).eq(0).text();           
    for (var i = Number($('input[type="text"]#hidden_string_count').val()); i >= Number(block_num) + 1; i--) {                    
            $("body").find(`td[name="object_num_`+ get_inner_num_by_outer_position(i) +`"]`).eq(0).text(i + n);
        }

    for (let i = n; i > 0 ; i--){ 
        // Добавление новой строки после num cо сдвигом номера i
        add_several_new_entity_blocks_after(
            num, i);
      }
    var position = last_number+1;  
    for  (let i = position; i < position+n+1; i++){
        // Копирование значений исходной строки

        $(`input[name="production_date_`+ i +`"]`).val(
            $(`input[name="production_date_`+ num +`"]`).val()
            );
        $(`textarea[name="loc_of_storage_original_label_`+ i +`"]`).val(
            $(`textarea[name="loc_of_storage_original_label_`+ num +`"]`).val()
            );
        $(`input[name="date_of_delivery_`+ i +`"]`).val(
            $(`input[name="date_of_delivery_`+ num +`"]`).val()
            );
        $(`textarea[name="loc_of_storage_original_delivery_document_`+ i +`"]`).val(
            $(`textarea[name="loc_of_storage_original_delivery_document_`+ num +`"]`).val()
            );
        $(`textarea[name="note_`+ i +`"]`).val(
            $(`textarea[name="note_`+ num +`"]`).val()
            );
        $(`input[name="special_check_`+ i +`"]`).prop(
            'checked', $(`input[name="special_check_`+ num +`"]`).prop('checked')
            );
    }
    
    // Скрываем модальное окно
    toogle_modal(0);    
}


// Удаляет строку в таблице
function deleteBlock(x){
    var block_num = $("body").find(`td[name="object_num_`+ x +`"]`).eq(0).text();
    var record_count = Number($('input[type="text"]#hidden_string_count').val());
    $('tr[name="new_entity_block_' + x + '"]').remove();
    record_count = record_count - 1;
    $('input[type="text"]#hidden_string_count').val(record_count)
    //Убавляем значение всех последующих строк на единицу
    if (record_count + 1 - block_num > 0) 
    {    
        for (var i = Number(block_num) + 1; i < record_count + 2; i++) {                     
            $("body").find(`td[name="object_num_`+ get_inner_num_by_outer_position(i) +`"]`).eq(0).text(i-1);
        }
    }
}
// Принимает на вход №(позиция в списке), отдает внутренний номер элемента с этим №, по которому уже можно получать значения пармаетров
function get_inner_num_by_outer_position(N){
    var num = $('#hidden_counter').val()
    for (var i = 1; i < num+1; i++){
        if (N == $("body").find(`td[name="object_num_`+ i +`"]`).eq(0).text()){
            return i;
        }
    }
}

//Вывводит модальноe окно, запрашивающее подтверждение ухода со страницы

function onbeforun(evt) {
	var message = "Докумиент не сохранен. При уходе со странцы все данные будут утеряны";
	if (typeof evt == "undefined") {
		evt = window.event;
	}
	if (evt) {
		evt.returnValue = message;
	}
	return message;
}
function remove_onbeforunload(){
    window.onbeforeunload = null;
}
$('#submit_edit').click(remove_onbeforunload);

