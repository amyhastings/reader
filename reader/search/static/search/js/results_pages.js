function show(item) {
    item.classList.remove("inactive");
}

function hide(item) {
    item.classList.add("inactive");
}

// Event listener for showing and hiding pages
document.addEventListener('click', function (e) {
    const c = e.target.classList;
    if (c.contains("show-all-pages-btn")) {
        show(document.getElementById("all-pages"));
        hide(document.getElementById("fewer-pages"));
    } else if (c.contains("show-fewer-pages-btn")) {
        hide(document.getElementById("all-pages"));
        show(document.getElementById("fewer-pages"));
    } else if (c.contains("author-show-all-pages-btn")) {
        show(document.getElementById("author-all-pages"));
        hide(document.getElementById("author-fewer-pages"));
    } else if (c.contains("author-show-fewer-pages-btn")) {
        hide(document.getElementById("author-all-pages"));
        show(document.getElementById("author-fewer-pages"));
    }
});