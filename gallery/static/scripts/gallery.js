imageNumber = 0;
$(document).ready(function() {
    if (($(window).width() > 501) || ($(window).height() > 501)) {
        desktopSetup();
    } else {
        mobileSetup();
    }
});

function mobileSetup() {
    getThumbs();
}

function desktopSetup() {
    var overlay = $('<div id="overlay"><div id="overlay_left" class="overlay_pannel"></div><div id="overlay_center" class="overlay_pannel"></div><div id="overlay_right" class="overlay_pannel"><img src="/static/images/close.png" id="close_overlay" /></div></div>');
    overlay.appendTo(document.body);
    var wWidth = $(window).width();
    var wHeight = $(window).height();
    $('.overlay_pannel').css('height', '100%');
    var overlayWidth = wWidth * 0.2;
    overlay.css('left', overlayWidth);
    overlay.css('width', '60%');
    $('#overlay_center').css('width', '90%');
    $('#overlay_left').css('width', '5%');
    $('#overlay_right').css('width', '5%');
    var overlayHeight = wHeight * 0.1;
    overlay.css('top', overlayHeight);
    overlay.css('height', '80%');
    overlay.attr('hidden', true);

    $('#overlay_right').click(function() {
        nextImage();
        setOverlayImage();
    });
    $('#overlay_left').click(function() {
        previousImage();
        setOverlayImage();
    });

    $('#close_overlay').click(function () {
        overlay.attr('hidden', true);
    });

    getThumbs();
}

function getThumbs() {
    for (var i = 0; i < imageList.length; i++) {
        var filepath = thumbPath + 'thumb_' + imageList[i];
        var image = $('.gallery_image').eq(i);
        image.css('background-size', 'auto');
        image.css('background-image', 'url("' + filepath + '")');
        //$('#gallery').append('<div class="gallery_image"><img class="gallery_image" class="gallery_image" src="' + filepath + '" />');
        image.click(imageClickGenerator(i));
    }
}

function imageClickGenerator(i) {
    if (($(window).width() > 501) || ($(window).height() > 501)) {
        return function() {
            imageNumber = i;
            setOverlayImage();
            $('#overlay').attr('hidden', false);
        };
    } else {
        return function() {
            window.location.href = '/media/gallery/images/' + imageList[i];
        };
    }
}

function nextImage() {
    imageNumber ++;
    if (imageNumber > imageList.length) {
        imageNumber = 0;
    }
}

function previousImage() {
    imageNumber ++;
    if (imageNumber < 0) {
        imageNumber = imageList.length -1;
    }
}

function setOverlayImage() {
    var filename = imageList[imageNumber];
    var url = "/media/gallery/images/" + filename;
    $('#overlay_center').css('background-image', 'url("' +  url + '")');

}
