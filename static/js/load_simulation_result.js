$(document).ready(function(){
    var submission = document.getElementById('submission').value;
    $(".id-code-line").click(function(){
        var url = $("#result-card").attr("result-data-url");
        var line = $(this).attr("value")
        console.log(submission)

        $.ajax({
            url:url,
            data:{'line_number':line, 'submission':submission},
            success: function(data){
                console.log(data)
                $("#result-text").html(data)
            }
        })
    })
})