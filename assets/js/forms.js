(function($) {

    /* Function to submit the contact form contents to API */

    $.fn.submitContactForm = function(e) {

        e.preventDefault();

        // The submit URL
        targetURL = 'https://rx9pusw9le.execute-api.ap-southeast-1.amazonaws.com/contact_form'

        // Ensure name is not empty
        var name_re = /[A-Za-z]{1}[A-Za-z]/;
        if (!name_re.test($("#namefield").val())) {
                     alert ("Have you entered a valid name?");
            return;
        }

        // Ensure email address is valid
        var email_re = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,6})?$/;
        if (!email_re.test($("#emailfield").val())) {
            alert ("Check that the email address is valid");
            return;
        }

        //Gather data
        var name = $("#namefield").val();
        var email = $("#emailfield").val();
        var message = $("#messagefield").val();
        var data = {
           name : name,
           email : email,
           message : message
         };

        $.ajax({
          type: "POST",
          url : targetURL,
          dataType: "json",
          crossDomain: "true",
          contentType: "application/json; charset=utf-8",
          data: JSON.stringify(data),

          success: function () {
            // clear form and show a success message
            alert("Thank you for your message!");
            document.getElementById("contactform").reset();
            location.reload();
          },
          error: function () {
            // show an error message
            alert("Sorry, unable to send message");
          }});
    }
}
)(jQuery)
