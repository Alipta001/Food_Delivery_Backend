$(document).ready(function () {
    console.log("Ajax is ready");

    $('#register_btn').click(function (event) {
        event.preventDefault();

        const restaurant_id = $('#restaurant_id').val();
        const csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
        let formData = new FormData();
        formData.append("restaurant_name", $('#restaurant_name').val());
        formData.append("restaurant_address", $('#restaurant_address').val());
        formData.append("cuisine_type", $('#cuisine_type').val());
        formData.append("restaurant_rating", $('#restaurant_rating').val());
        formData.append("csrfmiddlewaretoken", csrfmiddlewaretoken);
        const imageFile = $('#restaurant_image')[0].files[0];
        if (imageFile) {
            formData.append("image", imageFile);
        }

        const url = restaurant_id
            ? `/restaurants-temp/edit/${restaurant_id}/`
            : `/restaurants-temp/add/`;

        $.ajax({
            url: url,
            method: "POST",
            data: formData,
            processData: false,   // Very Important for Image Upload
            contentType: false,   // Very Important for Image Upload

            success: function (response) {
                // Reset fields
                $("#restaurant_form")[0].reset();
                $('#restaurant_id').val("");
                $('#register_btn').text("Add");

                $('#acknowledge').text(response.message)
                    .css("color", "green")
                    .fadeIn().delay(3000).fadeOut();

                $('#restaurant_list').html(response.restaurants);
            },

            error: function (error) {
                const errorMsg = error.responseJSON?.message || "An error occurred";
                $("#acknowledge").text(errorMsg)
                    .css("color", "red")
                    .fadeIn().delay(3000).fadeOut();
            }
        });

    });

    $(document).on('click', '.edit-btn', function (event) {
        event.preventDefault();

        const restaurant_id = $(this).data('id');
        const restaurant_name = $(this).data('name');
        const restaurant_address = $(this).data('address');
        const cuisine_type = $(this).data('cuisine_type');
        const restaurant_rating = $(this).data('rating');

        $('#restaurant_id').val(restaurant_id);
        $('#restaurant_name').val(restaurant_name);
        $('#restaurant_address').val(restaurant_address);
        $('#cuisine_type').val(cuisine_type);
        $('#restaurant_rating').val(restaurant_rating);
        $('#restaurant_image').val(""); 

        $('#register_btn').text("Update");
    });

    $(document).on('click', '.edit-delete', function (event) {
        event.preventDefault();

        const restaurant_id = $(this).data('id');
        const csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();

        if (!confirm("Are you sure you want to delete this restaurant?"))
            return;

        $.ajax({
            url: `/restaurants-temp/delete/${restaurant_id}/`,
            method: "POST",
            data: {
                csrfmiddlewaretoken: csrfmiddlewaretoken
            },

            success: function (response) {
                $('#acknowledge').text(response.message)
                    .css('color', 'green')
                    .fadeIn().delay(2000).fadeOut();

                $('#restaurant_list').html(response.restaurants);
            },

            error: function (error) {
                $("#acknowledge").text("Failed to delete the restaurant")
                    .css("color", "red")
                    .fadeIn().delay(2000).fadeOut();
            }
        });

    });

});
