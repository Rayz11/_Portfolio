const menuToggle = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");

menuToggle.addEventListener("click", () => {
    navLinks.classList.toggle("active");
});


document.querySelectorAll(".nav-links a").forEach(link => {

    link.addEventListener("click", () => {
        navLinks.classList.remove("active");
    });

});
// Tabs functionality
function opentab(tabName) {
    const tabLinks = document.querySelectorAll('.tab-links');
    const tabContents = document.querySelectorAll('.tab-contents');
    tabLinks.forEach(link => link.classList.remove('active-link'));
    tabContents.forEach(content => content.classList.remove('active-tab'));
    document.querySelector(`.tab-links[onclick*="${tabName}"]`).classList.add('active-link');
    document.getElementById(tabName).classList.add('active-tab');
}