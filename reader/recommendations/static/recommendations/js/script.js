function show(item) {
    item.classList.remove("inactive");
}

function hide(item) {
    item.classList.add("inactive");
}

function handleLike(e) {
    // Show/hide appropriate icon
    hide(e.target);
    const fields = e.target.id.split('-');
    const recommendation_id = fields[1];
    const unlike = document.getElementById("unlike-" + recommendation_id);
    show(unlike);

    // Make call to back end
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            // Update like counter
            const response = JSON.parse(this.responseText);
            document.getElementById("like_count-" + recommendation_id).innerHTML = response.likes_count;
        }
    };
    xhttp.open("POST", `/recommendation/${recommendation_id}/like/`, true);
    xhttp.setRequestHeader("X-CSRFToken", getCSRFToken()); // Include CSRF token for Django
    xhttp.send();
}

function handleUnlike(e) {
    // Show/hide appropriate icon
    hide(e.target);
    const fields = e.target.id.split('-');
    const recommendation_id = fields[1];
    const like = document.getElementById("like-" + recommendation_id);
    show(like);

    // Make call to back end
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            // Update like counter
            const response = JSON.parse(this.responseText);
            document.getElementById("like_count-" + recommendation_id).innerHTML = response.likes_count;
        }
    };
    xhttp.open("POST", `/recommendation/${recommendation_id}/like/`, true);
    xhttp.setRequestHeader("X-CSRFToken", getCSRFToken()); // Include CSRF token for Django
    xhttp.send();
}

// Utility function to get CSRF token from cookies
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith("csrftoken=")) {
            return cookie.substring("csrftoken=".length, cookie.length);
        }
    }
    return "";
}

// Event listener for like/unlike buttons
document.addEventListener('click', function (e) {
    const c = e.target.classList;
    if (c.contains("like-button")) {
        handleLike(e);
    } else if (c.contains("unlike-button")) {
        handleUnlike(e);
    }
});