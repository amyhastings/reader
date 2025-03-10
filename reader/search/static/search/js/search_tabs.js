function openSearchResults(evt, resultType) {

    var i, tabcontent, tablinks;
  
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    document.getElementById(resultType).style.display = "block";
    evt.currentTarget.className += " active";
};

function submitForm(page) {
  document.getElementById("book_page").value = page;
  document.getElementById("search_form").submit();
};

function findGetParameter(parameterName) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(parameterName);
};

window.onload = function() {
  var authorId = findGetParameter("author_page");
  if (authorId) {
    document.getElementById("authorTab").click();
  } else {
    document.getElementById("titleTab").click();
  }
};