$(document).ready(function () {
    $(".btn-primary").click(function () {
        if ($('#sentence').val().trim() != "") {
            $.ajax({
                url: './predict',
                type:'POST',
                data : {'sentence' : $('#sentence').val()},
            }).done(function(data) {
                res = JSON.parse(data);
                $("#results").prepend("<tr scope=\"row\"><td>" + $('#sentence').val() + "</td><td>" 
                + res.unigram +"</td><td>" + res.bigram +"</td></tr>")
                $('#sentence').val("")
            }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
                console.log(XMLHttpRequest);
                $("#result").prepend("<div> An error occured </div>")
            })
        }
    });

    $('#sentence').keypress(function(event) {
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if ($('#sentence').val().trim() != "" && keycode == '13') {
            $.ajax({
                url: './predict',
                type:'POST',
                data : {'sentence' : $('#sentence').val()},
            }).done(function(data) {
                res = JSON.parse(data);
                $("#results").prepend("<tr scope=\"row\"><td>" + $('#sentence').val() + "</td><td>" 
                + res.unigram +"</td><td>" + res.bigram +"</td></tr>")
                $('#sentence').val("")
            }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
                console.log(XMLHttpRequest);
                $("#result").prepend("<div> An error occured </div>")
            })
        }
    });
});