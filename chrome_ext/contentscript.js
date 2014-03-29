// TODO: add error handling (when image not found)

function get_images() {
    // try to guess image in page, otherwise let user select an image

    // trying to guess image...
    // naive first try, pull largest image
    var maxWidth = 0;
    var maxImgSrc = "";
    var urls = new Array();

    $("img").each(function(index, image) {
        console.log("found image...");

        // add image url to return result
        var src = $(image).attr('src');
        urls.push(src);

        // check if this is our max image
        var w = $(this).width();
        if (w > maxWidth) {
            maxWidth = w;
            maxImgSrc = src;
        }
    });

    return [maxImgSrc, urls];
    // return "found no images";
}

function dedupe(urls) {
    var set = {};
    for (var i = 0; i < urls.length; i++) {
        set[urls] = true;
    }
    urls = [];
    for (var url in set) {
        urls.push(url);
    }
   return urls;
}

chrome.extension.onMessage.addListener(function(msg, sender, sendResponse) {
    console.log("received message...");
    if (msg.text && (msg.text == "report_back")) {
        var urls = get_images();
        //urls[1] = dedupe(urls[1]);

        // get the url of the largest image
        var return_urls = urls[0];
        return_urls = return_urls.concat("$_$");

        // get the rest of the urls
        var len = urls[1].length;
        for (var i = 0; i < len; i++) {
            var str = urls[1][i];
            return_urls = return_urls.concat(str);
            return_urls = return_urls.concat("$_$");
        }

        console.log("sending: ");
        console.log(return_urls);

        // send a semicolon-delineated response
        sendResponse(return_urls);
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