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

function get_images_on_page() {
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

    return return_urls;
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


function undistort_image(image_url) {
    var post_url = "https://scoring-distortion.herokuapp.com/post/";
    //var image_url = encodeURIComponent(image_url)
    var encoded_post_url = post_url + image_url;

    var xhr = new XMLHttpRequest();
    xhr.open("GET", encoded_post_url, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            // JSON.parse does not evaluate the attacker's scripts.
            var resp = jQuery.parseJSON(xhr.responseText);
            var undist_url = resp.url;
            console.log("undistorted url: ");
            console.log(undist_url);
            send_undistorted_image_to_popup(undist_url);
      }
    }
    xhr.send();
}


function send_undistorted_image_to_popup(undist_url) {
    console.log("attempting to send undistorted url back to popup");
    // send message to popup.js with undistorted image url
    chrome.runtime.sendMessage(undist_url, function() { /*response*/ });
}


chrome.extension.onMessage.addListener(function(msg, sender, sendResponse) {
    console.log("received message...");
    if (msg.text && (msg.text == "report_back")) {
        var return_urls = get_images_on_page();
        console.log("sending: ");
        console.log(return_urls);

        // send response back to popup window
        sendResponse(return_urls);
    } else if (msg.text) {
        undistort_image(msg.text);
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