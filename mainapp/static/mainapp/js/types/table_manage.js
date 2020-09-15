const filtrating_list_queue = [ "type", "note", "soft"];
const filtrating_list_direction = ["desc", "desc", "desc" ];

function manage_par_sequence()
{   
    const table =  $("div#entity_table table tr").slice(1);
    //Представляем список в виде массива для фильтрации
    const mapped_table = table.map(function(index, element){
        const td = $(element).find("td");        
        return {
            type: td.eq(0).text() ,
            type_href: td.eq(0).children('a').eq(0).attr('href') ,
            note: td.eq(1).text(),
            soft: td.eq(2).html(),            
        };  
      }); 
      //Производим фильтрацию по всем полям - меняется только порядок признаков и направление (asc/desc)     
      const sorted_table = _.orderBy(mapped_table, filtrating_list_queue, filtrating_list_direction);
    
      //Заполняем таблицу новыми значениями
      table.each(function(index, element){
        const td = $(element).find("td");
        td.eq(0).find('a').eq(0).text($(sorted_table).eq(index).attr("type"));
        td.eq(0).find('a').eq(0).attr('href', $(sorted_table).eq(index).attr("type_href"));
        td.eq(1).eq(0).text($(sorted_table).eq(index).attr("note"));
        td.eq(2).html($(sorted_table).eq(index).attr("soft"))
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

//Копирование пути к папке по нажатию кнопки
function copytext(el) {
  var $tmp = $("<textarea>");
  $("body").append($tmp);
  $tmp.val(el).select();
  document.execCommand("copy");
  $tmp.remove();
  window.alert("Путь скопирован!")
} 