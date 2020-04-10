
function submitForm() {
    var form = $('#book-form');
    var form_id = 'book-form';
    var url = "/submitbook";
    var type = form.prop('method');
    var formData = getBookFormData(form_id);

    console.log(formData);

    // submit form via AJAX
    send_form(form, form_id, url, type, modular_ajax, formData);
}

function getBookFormData(form) {
    // creates a FormData object and adds chips text
    var formData = new FormData(document.getElementById(form));
    for (var [key, value] of formData.entries()) { console.log('formData', key, value);}
    return formData
}

function send_form(form, form_id, url, type, inner_ajax, formData) {
    // form validation and sending of form items

    if ( form[0].checkValidity() && isFormDataEmpty(formData) == false ) { // checks if form is empty
        event.preventDefault();

        // inner AJAX call
        inner_ajax(url, type, formData);

    }
    else {
        // first, scan the page for labels, and assign a reference to the label from the actual form element:
        var labels = document.getElementsByTagName('LABEL');
        for (var i = 0; i < labels.length; i++) {
            if (labels[i].htmlFor != '') {
                 var elem = document.getElementById(labels[i].htmlFor);
                 if (elem)
                    elem.label = labels[i];
            }
        }

        // then find all invalid input elements (form fields)
        var Form = document.getElementById(form_id);
        var invalidList = Form.querySelectorAll(':invalid');

        if ( typeof invalidList !== 'undefined' && invalidList.length > 0 ) {
            // errors were found in the form (required fields not filled out)

            // for each invalid input element (form field) return error
            for (var item of invalidList) {
                M.toast({html: "Please fill the "+item.label.innerHTML+"", classes: 'bg-danger text-white'});
            }
        }
        else {
            M.toast({html: "Another error occurred, please try again.", classes: 'bg-danger text-white'});
        }
    }
}


function isFormDataEmpty(formData) {
    // checks for all values in formData object if they are empty
    for (var [key, value] of formData.entries()) {
        if (key != 'csrf_token') {
            if (value != '' && value != []) {
                return false;
            }
        }
    }
    return true;
}

function modular_ajax(url, type, formData) {
    // Most simple modular AJAX building block
    $.ajax({
        url: url,
        type: type,
        data: formData,
        processData: false,
        contentType: false,
        beforeSend: function() {
            // show the preloader (progress bar)
            $('#form-response').html("<div class='progress'><div class='indeterminate'></div></div>");
        },
        complete: function () {
            // hide the preloader (progress bar)
            $('#form-response').html("");
        },
        success: function ( data ){
            if ( !$.trim( data.feedback )) { // response from Flask is empty
                toast_error_msg = "An empty response was returned.";
                toast_category = "danger";
            }
            else { // response from Flask contains elements
                toast_error_msg = data.feedback;
                toast_category = data.category;
                setTimeout(function(){window.location.reload();},5);
            }
        },
        error: function(xhr) {console.log("error. see details below.");
            console.log(xhr.status + ": " + xhr.responseText);
            toast_error_msg = "An error occured";
            toast_category = "danger";
        },
    }).done(function() {
        M.toast({html: toast_error_msg, classes: 'bg-' +toast_category+ ' text-white'});
    });
};

var csrf_token = "{{ csrf_token() }}";

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});