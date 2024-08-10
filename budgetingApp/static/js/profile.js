$(document).ready(function(){
    $("#submitBTN").click(function(){
        let index = $('#pictureCarousel .active').index();
        
        $('#num').val(index);
        $('#pictureForm').submit();
    });
});