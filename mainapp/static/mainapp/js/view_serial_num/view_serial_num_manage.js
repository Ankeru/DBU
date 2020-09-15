// Устанавливает куки при изменении типа и перезагружает страницу
function manage_view_type_cookies()
{
    var type_ = $('#select_type').val();
    document.cookie = "chosen_type1="+type_;
    // Спускаемся на два уровня и заходим на страницу нового типа
    window.location.replace('../../../'+type_ + "/view_type/");
}
const type_element = $('#select_type');
type_element.change(manage_view_type_cookies);

// Устанавливает куки при изменении cерийного номера и перезагружает страницу
function manage_view_type_serial_num_cookies()
{
    var type_ = $('#select_type').val();
    document.cookie = "chosen_type1="+type_;
    var serial_num = $('#select_serial_num').prop('selected', 'true').val();
    document.cookie = "serial_num="+serial_num;
    // Спускаемся на два уровня и заходим на страницу нового типа
    window.location.replace('../../../'+type_ + "/"+ serial_num + "/view_serial_num/");
}
const serial_num_element = $('#select_serial_num');
serial_num_element.change(manage_view_type_serial_num_cookies);

// Устанавливает куки типа при нажатии submit Анкеты
function manage_edit_profile_cookies()
{
    var type_ = $('#select_type').val();
    document.cookie = "chosen_type1="+type_;
}
type_element.change(manage_edit_profile_cookies);

const his_radio_element = $('input[name="his_radio"]');
his_radio_element.change(
        function show_block(){
            $('div#stelth_block').prop('hidden', false);
        }
    );
his_radio_element.change(
        function change_data(){
            const o_table =  $("table#open_table tr").slice(2);
            const s_table_first_row_td_list =  $("table#stelth_table tr").slice(2).eq(0).find('td');
            const number_in_o_table = o_table.length - parseInt($('input[name="his_radio"]:checked').val())            
            s_table_first_row_td_list.eq(0).find("textarea").eq(0).val(o_table.eq(number_in_o_table).find('td').eq(0).text());        
            s_table_first_row_td_list.eq(1).find("input[type='date']").eq(0).val(o_table.eq(number_in_o_table).find('td').eq(1).find('input').val());       
            s_table_first_row_td_list.eq(2).find("input[type='date']").eq(0).val(o_table.eq(number_in_o_table).find('td').eq(2).find('input').val());  
            s_table_first_row_td_list.eq(3).find('select').val(
                o_table.eq(number_in_o_table).find('td').eq(3).text());               
            s_table_first_row_td_list.eq(4).find('textarea').val(
                o_table.eq(number_in_o_table).find('td').eq(4).text());              
            s_table_first_row_td_list.eq(5).find('textarea').val(
                o_table.eq(number_in_o_table).find('td').eq(5).text());
            s_table_first_row_td_list.eq(6).find('select').val(
                o_table.eq(number_in_o_table).find('td').eq(6).text());
            s_table_first_row_td_list.eq(7).find('select').val(
                o_table.eq(number_in_o_table).find('td').eq(7).text());                    
        }
    );
