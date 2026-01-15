$(document).ready(function(){
    console.log("We are in MenuIte_Ajax");
    
    $('#menuItem_register_btn').click(function(event){
        event.preventDefault();
        let restaurant_id = $('#restaurant_id').val();
        let menuItems_id = $('#menuItems_id').val();
        let menuItems_name = $('#menuItems_name').val();
        let menuItems_desc = $('#menuItems_desc').val();
        let menuItems_price = $('#menuItems_price').val();
        let menuItems_img = $('#menuItems_img')[0].files[0];
        let csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();

        if (!restaurant_id || !menuItems_name || !menuItems_desc || !menuItems_price) {
            $("#acknowledge").text('All fields are required').css('color','red');
            return;
        }

        if (!menuItems_id && !menuItems_img) {
            $("#acknowledge").text('Image is required for new items').css('color','red');
            return;
        }

        let formData = new FormData();

        formData.append('restaurant_id', restaurant_id);
        formData.append('name', menuItems_name);
        formData.append('description', menuItems_desc);
        formData.append('price', menuItems_price);
        if (menuItems_img) formData.append('image', menuItems_img);  // append only if a file was selected
        formData.append('csrfmiddlewaretoken', csrfmiddlewaretoken);

        console.log(`Sending: restaurant_id=${restaurant_id}, name=${menuItems_name}, description=${menuItems_desc}, price=${menuItems_price}, has_image=${!!menuItems_img}`);
        

        $.ajax({
            url: menuItems_id ? `/menuItems-temp/edit/${menuItems_id}/`:`/menuItems-temp/add/`,
            type: "POST",
            data: formData,
            processData: false,   // jQuery MUST NOT convert FormData into a string  
            contentType: false,   // jQuery MUST NOT set content-type (browser will set multipart/form-data) 
            success: function(response){
                $("#acknowledge").text(response.message).css('color','green').fadeIn().delay(2000).fadeOut();
                $("#menuItems_List").html(response.menuItems)
                $("#subjectForm")[0].reset();
                $('#menuItem_register_btn').text("ADD")
                $('#heading').text("Add a menu item")
            },
            error: function(error){
                const errMsg = error.responseJSON?.message || 'An error occure';
                console.error('AJAX Error:', error);
                $("#acknowledge").text(errMsg).css('color','red').fadeIn().delay(2000).fadeOut();
            }
        });
    });
    
    $(document).on('click', '.edit-menuItem-btn', function(event){
        event.preventDefault();

        const menu_id = $(this).data('id');
        const name = $(this).data('name');
        const description = $(this).data('description');
        const price = $(this).data('price');
        const restaurant = $(this).data('restaurant');

        $('#menuItems_id').val(menu_id);
        $('#menuItems_name').val(name);
        $('#menuItems_desc').val(description);
        $('#menuItems_price').val(price);
        $('#restaurant_id').val(restaurant);
        $('#menuItem_register_btn').text('Update');
        $('#heading').text("Edit menu item")
    });


    $(document).on('click', '.delete-menuItem-btn', function(event){
        event.preventDefault();
        const menu_id = $(this).data('id');
        const csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();

        if(!confirm("Are you sure you want to delete this menu item?"))
            return;

        $.ajax({
            url: `/menuItems-temp/delete/${menu_id}/`,
            method: 'POST',
            data: {
                csrfmiddlewaretoken: csrfmiddlewaretoken
            },
            success: function(response){
                $('#acknowledge').text(response.message)
                                 .css('color','green').fadeIn().delay(2000).fadeOut();
                $('#menuItems_List').html(response.menuItems);
            },
            error: function(error){
                const errMsg = error.responseJSON?.message || 'Failed to delete menu item';
                $('#acknowledge').text(errMsg).css('color','red').fadeIn().delay(2000).fadeOut();
            }
        })
    });

});
