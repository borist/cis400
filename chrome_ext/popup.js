
// display a new image in the pop up html
function display_image(src) {
    var img = document.createElement('img');
    img.src = src;
    img.setAttribute('alt', "Select an image");
    document.body.appendChild(img);
}

function display_text(text) {
    if (text === undefined) {
        $("#image_tbc").append("undefined text...");
    } else {
        $("#image_tbc").append(text);
    }
    //document.body.appendChild(dv);

}

function process_response(response) {
    //display_text(response);

    // check if response is image and display it if it is
    if (response == "found no images") {
        display_text("unable to detect an image in the current tab");
    } else {
        display_image(response);
    }

}

// document.addEventListener('DOMContentLoaded', function() {
//     console.log("me");
//     display_image(undefined);
// });

// send message to contentscript.js
chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {text: "report_back"}, process_response);
    });
