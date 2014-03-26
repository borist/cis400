
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

// // send message to content script:
// function send_message() {
//     // currently just for testing purposes

// }

// document.addEventListener('DOMContentLoaded', function() {
//     console.log("me");
//     display_image(undefined);
// });

chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {text: "report_back"}, function(response) {
            console.log(tabs[0].id);
            console.log(tabs[0].url);
            console.log("got this: " + response);
            display_text(response);
        });
    });
