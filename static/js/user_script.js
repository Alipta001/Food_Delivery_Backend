$(document).ready(function(){
    console.log('we are in jquary');
    // Register user
    $("#signup_btn").click(function (e) {
        e.preventDefault();
        console.log("Signing up...");

        $.ajax({
            url: "/users-temp/register/",
            method: "POST",
            data: {
                first_name: $("#first_name").val().trim(),
                last_name: $("#last_name").val(),
                username: $("#username").val(),
                email: $("#email").val(),
                password: $("#password").val(),
                confirm_password: $("#confirm_password").val(),
                role: $("#role").val(),
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            },
            beforeSend: function () {
                $("#spinner-overlay").show();       // Show spinner overlay before request is sent
            },
            success: function (response) {
                $("#acknowledge").text(response.message)
                    .css("color", "green")
                    .fadeIn().delay(5000).fadeOut();

                // Redirect to login page after 7 seconds
                setTimeout(() => {
                    window.location.href = response.redirect_url;
                }, 7000);
            },
            error: function (xhr) {
                const errorMsg = xhr.responseJSON?.error || "Something went wrong.";
                $("#acknowledge").html(`<div class="alert alert-danger">${errorMsg}</div>`);
            },
            complete: function () {
                // Always hide spinner overlay after request finishes (success or error)
                $("#spinner-overlay").hide();
            }
        });
    });
    
})