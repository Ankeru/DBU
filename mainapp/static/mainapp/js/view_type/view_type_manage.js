
function manage_view_type_cookies()
{
    var type_ = $('#select_type').prop('selected', 'true').val();
    document.cookie = "chosen_type="+type_;
    // Спускаемся на два уровня и заходим на страницу нового типа
    window.location.replace('../../'+type_ + "/view_type/");

}

const type_element = $('#select_type');
type_element.change(manage_view_type_cookies);