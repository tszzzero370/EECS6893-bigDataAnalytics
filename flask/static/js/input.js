$(function () {
    $("#submit").click(function (event) {
        // prevent default call
        event.preventDefault();
        const birthday = $("#birthday").val();
        const gender = $("#gender").val();
        const education = $("#education").val();
        const car = $("#car").val();
        const realty = $("#realty").val();
        const housing = $("#housing").val();
        const family = $("#family").val();
        const marital = $("#marital").val();
        const children = $("#children").val();
        const income_type = $("#income_type").val();
        const occupation = $("#occupation").val();
        const income = $("#income").val();
        const employ_date = $("#employ_date").val();
        const mobile = $("#mobile").val();
        const work_phone = $("#work_phone").val();
        const fixed_line = $("#fixed_line").val();
        const email = $("#email").val();
        if (birthday === "-1" || gender == "-1" || education == "-1" || car == "-1" || realty == "-1" || housing == "-1" ||
        family == "-1" || marital == "-1" || children == "-1" || income_type == "-1" || occupation == "-1" || income == "-1" ||
        employ_date == "-1" || mobile == "-1" || work_phone == "-1" || fixed_line == "-1" || email == "-1") {
            alert("Your input is incomplete, please check again.");
        } else {
            $.ajax({
                url:"/get_input?birthday="+birthday+"&gender="+gender+"&education="+education+"&car="+car+"&realty="+realty+"\
            &housing="+housing+"&family="+family+"&marital="+marital+"&children="+children+"&income_type="+income_type+"\
            &occupation="+occupation+"&income="+income+"&employ_date="+employ_date+"&mobile="+mobile+"&work_phone="+work_phone+"\
            &fixed_line="+fixed_line+"&email="+email,
                method:"GET",
                success: function (result) {
                    console.log(result);
                    if (result["prediction"]) {
                        alert("Congratulations! \rYour approval possibility is " + result["possibility"]);
                    } else {
                        alert("We are sorry that your approval probability is +" + result["probability"]+"\
                    \rYour application might not be approved.")
                    }
                },
                fail: function (error) {
                    console.log(error);
                    alert("Your input is incomplete, please check again.");
                }
            })
        }
    })
})