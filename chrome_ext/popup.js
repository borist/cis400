var main_image_url;

// display a new image in the pop up html
function display_main_image(src) {
    var img = document.createElement('img');
    img.src = src;
    main_image_url = src;
    img.setAttribute('alt', "Select an image");
    img.setAttribute('class', "main_img");

    $("#image_tbc").empty();
    $("#image_tbc").append(img);

    // at first, display both images as undistorted
    clear_undistorted_image();
}

function clear_undistorted_image() {
    $("#images_side_by_side").removeClass();
    $("#image_con").empty();
}

function display_undistorted_image(src) {
    $("#images_side_by_side").addClass("sbs");

    var img = document.createElement('img');
    img.src = src;
    main_image_url = src;
    img.setAttribute('alt', "Select an image");
    img.setAttribute('class', "main_img");

    $("#image_con").empty();
    $("#image_con").append(img);
}

function display_distortion_scores(score) {
    $("#progress_wrapper").addClass("hide");
    $("#table_wrapper").removeClass("hide");
    // reset width of bar
    var $bar = $("#progress_bar");
    $bar.width(0);

    var scores = score.split(" ");
    console.log(scores);

    $("#radial_score").empty();
    $("#radial_score").text(scores[0]);

    $("#focal_score").empty();
    $("#focal_score").text(scores[1]);

    $("#fov_score").empty();
    $("#fov_score").text(scores[2]);

    // set overall score
    $("#overall_score").empty();
    $("#overall_score").text(scores[3]);
}


function wait_for_progress() {
    $("#table_wrapper").addClass("hide");
    $("#progress_wrapper").removeClass("hide");

    // fake the progress bar
     var progress = setInterval(function () {
         var $bar = $('#progress_bar');

         if ($bar.width() >= 500) {
             clearInterval(progress);
         } else {
             $bar.width($bar.width() + 10); //change int to increase/decrease speed
         }
     }, 100);
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
            console.log("no image found at url.");
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

function process_images_response(response) {
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

function process_response(response) {

}

function process_undistortion(response, sendResponse) {
    console.log(response);
    // display_undistorted_image(response);
    display_distortion_scores(response);
}

// send message to contentscript.js to find images
chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {text: "report_back"}, process_images_response);
    });

document.addEventListener('DOMContentLoaded', function() {
  $("#submit_image").click(function() {
        wait_for_progress();
        // send message to contentscript.js to send image and get undistorted image
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
                chrome.tabs.sendMessage(tabs[0].id, {text: main_image_url}, process_response);
            });
    });
});
