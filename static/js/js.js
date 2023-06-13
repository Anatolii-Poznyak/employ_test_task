function toggleSubordinates(event, id) {
    event.stopPropagation();

    var subordinates = document.getElementById("subordinates-" + id);
    var toggleIcon = document.getElementById("toggle-icon-" + id);

    if (subordinates.style.display === "none") {
        subordinates.style.display = "block";
        toggleIcon.innerText = "-";
    } else {
        subordinates.style.display = "none";
        toggleIcon.innerText = "+";
    }
}