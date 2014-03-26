function get_images() {
    // try to guess image in page, otherwise let user select an image

    // trying to guess image...
    // naive first try, pull largest image
    var maxWidth = 0;
    var maxImgSrc = "";

    if ($("body").length > 0) {
        console.log("found body");
    }

    $("img").each(function(index, image) {
        console.log("found images...");
        var w = $(this).width();
        if (w > maxWidth) {
            maxWidth = w;
            maxImgSrc = $(image).attr('src');
        }
    });

    if (maxWidth > 0 && maxImgSrc.length > 0) {
        // we found a possible correct image
        return maxImgSrc;
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