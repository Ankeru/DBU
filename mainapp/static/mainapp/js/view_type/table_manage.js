const filtrating_list_queue = [ "serial_num", "status", "spec_check", "date_made", "date_delivered", "doc_delivered", "label", "soft_link"];
const filtrating_list_direction = ["desc", "desc", "desc", "desc", "desc", "desc", "desc", "desc"];

function manage_par_sequence()
{   
    const table =  $("div#entity_table table tr").slice(1);
    //Представляем список в виде массива для фильтрации
    const mapped_table = table.map(function(index, element){
        const td = $(element).find("td");
        return {
            serial_num: td.eq(1).text(),
            serial_num_href: td.eq(1).children('a').eq(0).attr('href'),
            status: td.eq(2).text(),
            spec_check: td.eq(3).text(),
            date_made: td.eq(4).find('input[type="date"]').val(),
            date_delivered: td.eq(5).find('input[type="date"]').val(),
            doc_delivered: td.eq(6).text(),
            label: td.eq(7).text(),
            soft_link: td.eq(8).text()
        };
      }); 
      //Производим фильтрацию по всем полям - меняется только порядок признаков и направление (asc/desc)     
      const sorted_table = _.orderBy(mapped_table, filtrating_list_queue, filtrating_list_direction);
      
      //Заполняем таблицу новыми значениями
      table.each(function(index, element){
        const td = $(element).find("td");                
        td.eq(1).find('a').eq(0).text($(sorted_table).eq(index).attr("serial_num"));
        td.eq(1).find('a').eq(0).attr('href', $(sorted_table).eq(index).attr("serial_num_href"));
        td.eq(2).text($(sorted_table).eq(index).attr("status"));
        td.eq(3).text($(sorted_table).eq(index).attr("spec_check"));
        td.eq(4).find('input[type="date"]').val($(sorted_table).eq(index).attr("date_made"));
        td.eq(5).find('input[type="date"]').val($(sorted_table).eq(index).attr("date_delivered"));
        td.eq(6).find('a').eq(0).text($(sorted_table).eq(index).attr("doc_delivered"));
        td.eq(7).find('a').eq(0).text($(sorted_table).eq(index).attr("label"));
        td.eq(8).find('a').eq(0).text($(sorted_table).eq(index).attr("soft_link"));
      });



}

$('.table_manager').on("click", function(){    
    let initial_ind, new_direction, column_name;
    column_name = $(this).attr("name");
    initial_ind = filtrating_list_queue.indexOf(column_name);
    if (filtrating_list_direction[initial_ind] === "asc") 
    new_direction = "desc"
    else 
    new_direction = "asc";
    filtrating_list_queue.splice(initial_ind, 1); // начиная с позиции initial_ind, удалить 1 элемент
    filtrating_list_direction.splice(initial_ind, 1);
    filtrating_list_queue.unshift(column_name);
    filtrating_list_direction.unshift(new_direction);
    manage_par_sequence();    
});



