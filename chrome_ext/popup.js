
// display a new image in the pop up html
function display_image(src) {
    var img = document.createElement('img');
    img.src = src;
    document.body.appendChild(img);
}

// send message to content script:
function send_message() {
    // currently just for testing purposes

}