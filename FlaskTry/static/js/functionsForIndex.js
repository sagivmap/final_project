var modal = document.getElementById("myModal");
var showLoggerBtn = document.getElementById("showlogger");
var crawlFacebookBtn = document.getElementById("crawlFBBtn");
var span = document.getElementById("closeFBLogger");

span.onclick = function () {
    modal.style.display = "none";
}

function showFloatingWindow() {
    modal.style.display = "block";
    showLoggerBtn.style.display = "block";
    crawlFacebookBtn.style.display = "none";
}


function showLogger() {
    modal.style.display = "block";
}


var scrolled = false;
function updateScroll() {
    if (!scrolled) {
        var element = document.getElementById("output");
        element.scrollTop = element.scrollHeight;
    }
}

setInterval(updateScroll, 1000);

$("#output").on('scroll', function () {
    scrolled = true;
});
