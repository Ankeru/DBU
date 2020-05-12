// Устанавливает куки при изменении типа
function manage_view_type_cookies()
{
    var type_ = $('#select_type').prop('selected', 'true').val();
    document.cookie = "chosen_type="+type_;
    // Спускаемся на два уровня и заходим на страницу нового типа
    window.location.replace('../../'+type_ + "/view_type/");
}
const type_element = $('#select_type');
type_element.change(manage_view_type_cookies);

// Устанавливает куки типа при нажатии submit Анкеты
function manage_edit_profile_cookies()
{
    var type_ = $('#select_type').prop('selected', 'true').val();
    document.cookie = "chosen_type="+type_;
}
type_element.change(manage_edit_profile_cookies);

//Показывает панель редактирования при выборе одного из кружков "править" и заполняет её соответсвующими данными
//Скрывает п.р. при нажатии "Сохранить изменения в истории"
// function change_sb_visibility()
// {
//     block = $('div#stelth_block');
//     if (block.prop('hidden')){
//         block.prop('hidden', false);
//     }else{

//         block.prop('hidden', true);
//     }  
// }
const his_radio_element = $('input[name="his_radio"]');
his_radio_element.change(
        function show_block(){
            $('div#stelth_block').prop('hidden', false);
        }
    );
const his_button_submit_element = $('input[type="submit"]#submit_history_change');
his_button_submit_element.click(
    function hide_block_and_copy_data(){
        $('div#stelth_block').prop('hidden', true);
        const o_table =  $("table#open_table tr").slice(2);
        const s_table =  $("table#stelth_table tr").slice(2);
        const number_in_o_table = o_table.length - parseInt($('input[name="his_radio"]:checked').val())
        
        s_table.eq(1).text(o_table.eq(number_in_o_table));
        

        // td.eq(1).find('a').eq(0).text($(sorted_table).eq(index).attr("serial_num"));
        // td.eq(1).find('a').eq(0).attr('href', $(sorted_table).eq(index).attr("serial_num_href"));
        // td.eq(2).text($(sorted_table).eq(index).attr("status"));
        // td.eq(3).text($(sorted_table).eq(index).attr("spec_check"));
        // td.eq(4).find('input[type="date"]').val($(sorted_table).eq(index).attr("date_made"));
        // td.eq(5).find('input[type="date"]').val($(sorted_table).eq(index).attr("date_delivered"));
        // td.eq(6).find('a').eq(0).text($(sorted_table).eq(index).attr("doc_delivered"));
        // td.eq(7).find('a').eq(0).text($(sorted_table).eq(index).attr("label"));
        // td.eq(8).find('a').eq(0).text($(sorted_table).eq(index).attr("soft_link"));



    }
);



