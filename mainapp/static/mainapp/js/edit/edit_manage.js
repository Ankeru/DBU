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

function add_new_entity_block(){
    var last_record_num = (Number($('input[type="text"]#hidden_counter').val())+ 1);
    $('#hidden_counter').val(last_record_num);
    $('form.relative_container').append(`
        <div class="new_entity_block" name="new_entity_block_` + last_record_num + `">
        <div class="num_n_delete_block"><img class="delete" src="{% static 'mainapp/images/edit/delete.png' %}" title="Удалить" alt='Удалить' onclick="deleteBlock(` + last_record_num + `)" name="img_` + last_record_num + `"/></div>
                    <div id="view_serial_num">
                      <div class="one_line_blocks">
                      <div>Серийный №</div>
                      <input type="text" name="select_serial_num_` + last_record_num + `" title='Серийный №'/>                                                            
                      </div>
                      <div class="one_line_blocks">
                          <div class="profile_property">
                              <input type="checkbox" class="checkbox" name='special_check_` + last_record_num + `'>
                              <label for="special_check"> Спецпроверка</label></div>                                                       
                      </div>                    
                    </div>    
                    <div id="view_profile">
                      <div>                                                                        
                          <div class="profile_property">                                                              
                            <input type="date" name="production_date_` + last_record_num + `"/><label for="production_date"> Дата изготовления</label> 
                          </div>
                          <div class="profile_property">
                            <label for="label_ref">Этикетка: </label>                                                          
                            <input type="file" name="label_ref_` + last_record_num + `">                            
                          </div>                        
                          <div class="profile_property">
                            <label for="loc_of_storage_original_label">Место хранения оригинала этикетки: </label>
                            <input type="text" name="loc_of_storage_original_label_` + last_record_num + `">
                          </div>                        
                          <div class="profile_property"><label>
                              <input type="date" name="date_of_delivery_` + last_record_num + `"/>Дата поставки</label for="date_of_delivery">
                          </div>
                          <div class="profile_property">
                              <label for="delivery_document">Документ поставки: </label>                            
                              <input type="file" name="delivery_document_` + last_record_num + `">
                          </div>
                          <div class="profile_property">
                              <label for="loc_of_storage_original_delivery_document">Место хранения оригинала документа поставки: </label>
                              <input type="text" name="loc_of_storage_original_delivery_document_` + last_record_num + `">
                          </div>
                          <div class="profile_property">
                              <label for="note">Примечание: </label>
                              <textarea class="textarea_standart_size1" name="note_` + last_record_num + `"></textarea>
                          </div>
                      </div>
                  </div>
                </div> `        
        );
        $('img[name="img_' + last_record_num + '"]').attr('src', $('img[name="img_1"]').attr('src'));

}
$('#more_block').click(add_new_entity_block);

function deleteBlock(x){
    $('div[name="new_entity_block_' + x + '"]').remove();
    

}