function manage_select_change()
{
    var uname = $('#select_uname').prop('selected', 'true').val();
    window.location.replace('../../'+uname + "/profiles/");
}
        
$('#select_uname').change(manage_select_change);
