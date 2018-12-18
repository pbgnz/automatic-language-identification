$(document).ready(function () {
    $(".btn-primary").click(function () {
        $.ajax({
            url: './predict',
            type:'POST',
            data : {'sentence' : $('#sentence').val()},
        }).done(function(data) {
            res = JSON.parse(data);
            $("#results").prepend("<tr scope=\"row\"><td>" + $('#sentence').val() + "</td><td>" 
            + res.unigram +"</td><td>" + res.bigram +"</td></tr>")
        }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
            console.log(XMLHttpRequest);
            $("#result").prepend("<div> An error occured </div>")
        })
    });
});