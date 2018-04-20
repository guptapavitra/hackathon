console.log("We can show recommendations!")

var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        var listOfUrls = JSON.parse(xhttp.responseText);
        
        var container = createContainer();
        listOfUrls.forEach(function(url) {
            var childContainer = createChildContainer(url);
            container.appendChild(childContainer);
        });

        document.getElementById("hackathon-recommendations").appendChild(container);
    }
};

function createContainer() {
    var container = document.createElement('div');
    container.classList.add('parent');
    return container;
}

function createChildContainer(details) {
    var container = document.createElement('div');
    container.classList.add('child');
    container.innerHTML = details;
    return container;
}

xhttp.open("GET", "http://localhost:5000/recommend?url=" + encodeURIComponent(document.location.href), true);
xhttp.send();