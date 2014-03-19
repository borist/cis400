$(document).ready(function(){
    // try to guess image in page, otherwise let user select an image

    // trying to guess image...
    // naive first try, pull largest image
    var maxWidth = 0;
    var maxImgSrc = "";
    $('body img').each(function(index, image) {
        var w = $(this).width();
        if (w > maxWidth) {
            maxWidth = w;
            maxImgSrc = $(image).attr('src');
        }
    });

    if (maxWidth > 0) {
        // we found a possible correct image
    }
});