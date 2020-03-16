$(document).ready(function() {

    $('#authselect').click(function() {
        //make sure value updates before retrieving
        setTimeout(update_form_auth, 5);

    });

    function update_form_auth() {
        var value = $("input[name='numauth']:checked").val();
        var input = "<div class=\"row\">\n" +
                "                <div class=\"input-field col autocomplete\">\n" +
                "                    <input type=\"text\" class=\"validate authors\" name =\"author\" required/>\n" +
                "                    <label for=\"author-input\">Author</label>\n" +
                "                    <span class=\"helper-text\" data-error=\"Enter the author's name here.\" data-success=\"\"></span>\n" +
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
                "                    <input type=\"text\" class=\"validate authors\" name =\"author\" required disabled value='VARIOUS'/>\n" +
                "                </div>\n" +
                "            </div>";
        } else if (value == 'N/A') {
            document.getElementById("authors").innerHTML = "<div class=\"row\">\n" +
                "                <div class=\"input-field col autocomplete\">\n" +
                "                    <input type=\"text\" class=\"validate authors\" name =\"author\" required disabled value='N/A'/>\n" +

                "                    <span class=\"helper-text\" data-error=\"Enter the author's name here.\" data-success=\"\"></span>\n" +
                "                </div>\n" +
                "            </div>";
        }

        elements = document.getElementsByClassName("authors");
        for (var i = 0; i < elements.length; i++) {
            autocomplete(elements[i], authors);
        }
    }

    $('#edselect').click(function() {
        //make sure value updates before retrieving
        setTimeout(update_form_edit, 5);

    });

    function update_form_edit() {
        var value = $("input[name='numedit']:checked").val();
        var input = "<div class=\"row\">\n" +
                "                <div class=\"input-field col autocomplete\">\n" +
                "                    <input type=\"text\" class=\"validate editors\" name =\"editor\" required/>\n" +
                "                    <label for=\"editor-input\">Editor</label>\n" +
                "                    <span class=\"helper-text\" data-error=\"Enter the editor's name here.\" data-success=\"\"></span>\n" +
                "                </div>\n" +
                "            </div>";
        if (value == '1') {
            document.getElementById("editors").innerHTML = input;
        } else if (value == '2') {
            document.getElementById("editors").innerHTML = input+input;
        } else if (value == '3') {
            document.getElementById("editors").innerHTML = input+input+input;
        } else if (value == 'VARIOUS') {
            document.getElementById("editors").innerHTML = "<div class=\"row\">\n" +
                "                <div class=\"input-field col autocomplete\">\n" +
                "                    <input type=\"text\" class=\"validate editors\" name =\"editor\" required disabled value='VARIOUS'/>\n" +
                "                </div>\n" +
                "            </div>";
        } else if (value == '0') {
            document.getElementById("editors").innerHTML = "";
        }

        elements = document.getElementsByClassName("editors");
        for (var i = 0; i < elements.length; i++) {
            autocomplete(elements[i], editors);
        }
    }

    $('#genre').change(function() {

        var dot = document.getElementById("sticker");
        var selector = document.getElementById("genre");
        var label = document.getElementById("label");

        dot.style = "background-color:" + colors[genres[selector.value][0]];
        label.innerHTML = genres[selector.value][1]

    });

});