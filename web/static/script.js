function domReady(fn) {
    if (
        document.readyState === "complete" ||
        document.readyState === "interactive"
    ) {
        setTimeout(fn, 1000);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}

domReady(function () {
    // If found your QR code
    function onScanSuccess(decodeText, decodeResult) {
        // Send the decoded text to Flask backend
        sendDataToBackend(decodeText);
    }

    // Function to send data to Flask backend
    function sendDataToBackend(data) {
        // Make an AJAX request
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/process_qr_code", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    // Parse the response JSON
                    var response = JSON.parse(xhr.responseText);
                    if (response.redirect_url) {
                        // Redirect to the provided URL
                        window.location.href = response.redirect_url;
                    } else if (response.error) {
                        // Handle error
                        alert(response.error);
                    }
                } else {
                    // Handle non-200 responses
                    alert("An error occurred: " + xhr.statusText);
                }
            }
        };
        xhr.send(JSON.stringify({ qr_data: data }));
    }

    let htmlscanner = new Html5QrcodeScanner(
        "my-qr-reader",
        { fps: 10, qrbos: 250 }
    );
    htmlscanner.render(onScanSuccess);
});
