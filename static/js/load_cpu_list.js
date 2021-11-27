$(document).ready(function () {
    $("#id_cpu").html("<option>---Please Select---</option>")

    $("#id_cpu_family").change(function () {
        var url = $("#id-code-submission").attr("cpu_data_url");
        var familyId = $(this).val();

        $.ajax({
            url: url,
            data: {'cpu_family': familyId},
            success: function (data) {
                console.log(url)
                $("#id_cpu").html(data);
            }
        });
    })
})