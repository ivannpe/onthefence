$(document).ready(setup);

  function setup(){
    $(".fa-trash").click(deleteinput)
    $(".norefresh").click(saveinput)
    // fa-trash.onMouseClick

  }


function deleteinput(){
    var usertext = $(this).parent().text()
    console.log(usertext)
    var category = $(this).parent().parent().attr('class')



    var url = '/deleteinput'
    var data = {"category":category,"input":usertext }
    var settings = {"type":"POST", "data":data}



    $.ajax(url, settings)

    $(this).parent().remove()

}

function saveinput(event){
    event.preventDefault()
    var submitbutton = $(this)
    var valueofinputelement = $(submitbutton.parent().children()[0].children[0]).val()
    var category = submitbutton.parent().attr('class')

    var url = '/profile'
    var data = {"category":category,"input":valueofinputelement}
    var settings = {"type":"POST", "data":data}



    $.ajax(url, settings)
    var nuevohtml = '<li> ' + valueofinputelement + '    <i class="fa fa-trash"></i></li>'
    $("ul." + category).append(nuevohtml)

    $(submitbutton.parent().children()[0].children[0]).val("")

    var trashcans = $('ul.' + category).find('.fa-trash')
    
    $(trashcans[trashcans.length - 1]).click(deleteinput)


}
