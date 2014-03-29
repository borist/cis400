
// display a new image in the pop up html
function display_main_image(src) {
    var img = document.createElement('img');
    img.src = src;
    img.setAttribute('alt', "Select an image");
    img.setAttribute('class', "main_img");

    $("#image_tbc").empty();
    $("#image_tbc").append(img);
}

function display_image_options(urls) {
    var len = urls.length;
    for (var i = 0; i < len; i++) {
        var url = urls[i];

        // check if image exists
        var image = new Image();
        image.src = url;

        image.onerror = function() {
            // doesn't exist or error loading
            console.log("no image.");
        };

        // if image exists, add image to popup
        var img = document.createElement('img');
        img.src = url;
        img.setAttribute('class', "scroll_img");

        $("#hor_container").append(img);
    }
}

function display_images(urls_str) {
    urls = urls_str.split("$_$");
    display_main_image(urls[0]);
    display_image_options(urls);
}

function display_text(text) {
    if (text === undefined) {
        $("#image_tbc").append("undefined text...");
    } else {
        $("#image_tbc").append(text);
    }
}

function process_response(response) {
    //display_text(response);

    // display images if any were found
    if (response === "") {
        display_text("unable to detect an image in the current tab");
    } else {
        display_images(response);

        // add onclick listeners for the images
        $('.scroll_img').click(function () {
            var img = this;
            var url = img.getAttribute('src');
            display_main_image(url);
        });
    }
}

// send message to contentscript.js
chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {text: "report_back"}, process_response);
    });
