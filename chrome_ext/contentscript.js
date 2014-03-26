function get_images() {
    // try to guess image in page, otherwise let user select an image

    // trying to guess image...
    // naive first try, pull largest image
    var maxWidth = 0;
    var maxImgSrc = "";
    $('body img').each(function(index, image) {
        return "found something";
        var w = $(this).width();
        if (w > maxWidth) {
            maxWidth = w;
            maxImgSrc = $(image).attr('src');
        }
    });

    if (maxWidth > 0) {
        // we found a possible correct image
    }
    return "found no images...";
}

chrome.extension.onMessage.addListener(function(msg, sender, sendResponse) {
    console.log("received message...");
    if (msg.text && (msg.text == "report_back")) {
        var image_url = get_images();
        sendResponse(image_url);
    }
});


// chrome.extension.onConnect.addListener(function(port) {
//   console.log("Connected .....");
//   port.onMessage.addListener(function(msg) {
//         console.log("message recieved "+ msg);
//         port.postMessage("Hi Popup.js");
//   });
// });

// chrome.browserAction.onClicked.addListener(function(tab) {
//   alert("hi");
//   chrome.tabs.executeScript({
//     code: 'document.body.style.backgroundColor="red"'
//   });
// });