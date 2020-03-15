$(document).ready(function() {
    console.log($("input[name='numauth']:checked").val());

    $('#authselect').click(function() {
        //make sure value updates before retrieving
         setTimeout(update_form, 5);
    });

    function update_form() {
        var value = $("input[name='numauth']:checked").val();
        var input = "<div class=\"row\">\n" +
                "                <div class=\"input-field col autocomplete\">\n" +
                "                    <input type=\"text\" class=\"validate\" name =\"title\" id=\"author-input\" required/>\n" +
                "                    <label for=\"author-input\">Author</label>\n" +
                "                    <span class=\"helper-text\" data-error=\"Enter the book author here.\" data-success=\"\"></span>\n" +
                "                </div>\n" +
                "            </div>";
        if (value == '1') {
            document.getElementById("authors").innerHTML = input;
        } else if (value == '2') {
            document.getElementById("authors").innerHTML = input+input;
        } else if (value == '3') {
            document.getElementById("authors").innerHTML = input+input+input;
        } else if (value == 'VARIOUS') {
            document.getElementById("authors").innerHTML = "<div class=\"row\">\n" +
                "                <div class=\"input-field col autocomplete\">\n" +
                "                    <input type=\"text\" class=\"validate\" name =\"title\" id=\"author-input\" required disabled value='VARIOUS'/>\n" +

                "                    <span class=\"helper-text\" data-error=\"Enter the book author here.\" data-success=\"\"></span>\n" +
                "                </div>\n" +
                "            </div>";
        } else if (value == 'N/A') {
            document.getElementById("authors").innerHTML = "<div class=\"row\">\n" +
                "                <div class=\"input-field col autocomplete\">\n" +
                "                    <input type=\"text\" class=\"validate\" name =\"title\" id=\"author-input\" required disabled value='N/A'/>\n" +

                "                    <span class=\"helper-text\" data-error=\"Enter the book author here.\" data-success=\"\"></span>\n" +
                "                </div>\n" +
                "            </div>";
        }
    }

});