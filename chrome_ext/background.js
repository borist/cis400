chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    var popupWindows = chrome.extension.getViews({type:'popup'});
    if (popupWindows.length) { // A popup has been found
        popupWindows[0].process_undistortion(message, sendResponse);
    }
});