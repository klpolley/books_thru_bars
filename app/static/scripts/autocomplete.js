$("#autocomplete").autocomplete({

    //lookup: countries,

    serviceUrl:'autocomplete', //tell the script where to send requests
    type:'POST',
    width: 450, //set width

    //callback just to show it's working

    onSelect: function (suggestion) {

        $('#selection').html('You selected: ' + suggestion.value + ', ' + suggestion.data);

    },

    showNoSuggestionNotice: true,

    noSuggestionNotice: 'Sorry, no matching results',

});