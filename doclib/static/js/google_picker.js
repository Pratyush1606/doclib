// The Browser API key obtained from the Google API Console.
// Replace with your own Browser API key, or your own key.
var developerKey = "";
// The Client ID obtained from the Google API Console. Replace with your own Client ID.
var clientId = ""
// Replace with your own project number from console.developers.google.com.
// See "Project number" under "IAM & Admin" > "Settings"
var appId = "";
// Scope to use to access user's Drive items.
var scope = ['https://www.googleapis.com/auth/drive.file'];
var pickerApiLoaded = false;
var oauthToken;

// For getting parameters from backend

fetch("fetch_cred_gcs",{
    method: "POST",
    credentials: 'same-origin',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfcookie('csrftoken'),
    },
    body: JSON.stringify("Just Send the creds"),
}).then(function(response){
    return response.json();
}).then(function(data){
    // setting the parameters
    developerKey = data["developerKey"];
    clientId = data["clientId"];
    appId = data["appId"];
})

// Use the Google API Loader script to load the google.picker script.

function loadPicker() {
    gapi.load('auth', {'callback': onAuthApiLoad});
    gapi.load('picker', {'callback': onPickerApiLoad});
}
function onAuthApiLoad() {
    window.gapi.auth.authorize(
        {
        'client_id': clientId,
        'scope': scope,
        'immediate': false,
        'response_type': 'id_token permission code'
        },
        handleAuthResult);
}
function onPickerApiLoad() {
    pickerApiLoaded = true;
    createPicker();
}
function handleAuthResult(authResult) {
    if (authResult && !authResult.error) {
    oauthToken = authResult.access_token;
    createPicker();
    }
}
// Create and render a Picker object for searching images.
function createPicker() {
    if (pickerApiLoaded && oauthToken) {
    var view = new google.picker.View(google.picker.ViewId.DOCS);
    view.setMimeTypes("image/png,image/jpeg,image/jpg,application/pdf");
    var picker = new google.picker.PickerBuilder()
        .enableFeature(google.picker.Feature.NAV_HIDDEN)
        .enableFeature(google.picker.Feature.MULTISELECT_ENABLED)
        .setAppId(appId)
        .setOAuthToken(oauthToken)
        .addView(view)
        .addView(new google.picker.DocsUploadView())
        .setDeveloperKey(developerKey)
        .setCallback(pickerCallback)
        .build();
        picker.setVisible(true);
    }
}
function csrfcookie(name){
    var cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};
// A simple callback implementation.

function pickerCallback(data) {
    if (data.action == google.picker.Action.PICKED) {
        var array = [];
        for(let i=0;i<data.docs.length;i++){
            var obj={};
            obj['file_id']=(data.docs[i].id);
            obj['name']=(data.docs[i].name);
            obj['size']=(data.docs[i].sizeBytes);
            obj['url']=(data.docs[i].url);
            array.push(obj);
        }
        var csrftoken = csrfcookie('csrftoken');

        fetch("google_api",{
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(array),
        }).then(function(response){
          location.href="/doclib/files_display";
        })
    }
}
