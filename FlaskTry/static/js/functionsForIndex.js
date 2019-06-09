var modal = document.getElementById("myModal");
var showLoggerBtn = document.getElementById("showlogger");
var crawlFacebookBtn = document.getElementById("crawlFBBtn");
var closeFBLogger = document.getElementById("closeFBLogger");

closeFBLogger.onclick = function () {
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
        var element = document.getElementById("loggerModal");
        element.scrollTop = element.scrollHeight;
    }
}

setInterval(updateScroll, 500);

$("#loggerModal").on('scroll', function () {
    scrolled = true;
});

/*
// Get the modal
var modal1 = document.getElementById("myModal1");

// Get the button that opens the modal
var btn = document.getElementById("myBtn1");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal1.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal1.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal1) {
    modal1.style.display = "none";
  }
}
*/
