function manage_cookies()
{
    var type_ = $('#select_type').prop('selected', 'true').val();
    var serial_num_ = $('#select_serial_num').prop('selected', 'true').val();
    document.cookie = "chosen_type="+type_;
    document.cookie = "chosen_serial_num="+serial_num_;
    location.reload();
}

const type_element = $('#select_type');
const serial_num_element = $('#select_serial_num');
type_element.change(manage_cookies);
serial_num_element.change(manage_cookies);

