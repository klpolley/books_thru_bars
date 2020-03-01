$(document).ready(function(){
	$("#search-box").keyup(function(){
		value = $(this).val()

		$.ajax({
		type: "POST",
		url: "/ajaxautocomplete",
		data: {
			'query': value
		},
		success: function(data){
			$("#suggesstion-box").show();
			$("#suggesstion-box").html(data);
			$("#search-box").css("background","#FFF");
		}
		});
	});
});

function selectCountry(val) {
$("#search-box").val(val);
$("#suggesstion-box").hide();
}