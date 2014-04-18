chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    var popupWindows = chrome.extension.getViews({type:'popup'});
    if (popupWindows.length) { // A popup has been found
        popupWindows[0].process_undistortion(message, sendResponse);
    }
});


// Called when the user clicks on the browser action.
// chrome.browserAction.onClicked.addListener(function(tab) {
//    chrome.tabs.create({
//                url: chrome.extension.getURL('popup.html'),
//                active: false
//            }, function(tab) {
//                // After the tab has been created, open a window to inject the tab
//                chrome.windows.create({
//                    tabId: tab.id,
//                    type: 'popup',
//                    focused: true
//                    // incognito, top, left, ...
//                });
//            });
// });
