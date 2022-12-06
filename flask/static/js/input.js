$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();
        var age = $("#age").val();
        $.ajax({
            url:"/get_input?age="+String(age),
            method:"GET",
            success: function (result) {
                console.log(result);
                if (result["prediction"]) {
                    alert("Congratulations! \rYour approval possibility is " + result["possibility"]);
                }
            },
            fail: function (error) {
                console.log(error);
                alert("Your input is incomplete, please check again.");
            }
        })
    })
})