let open_profile = document.querySelector(".open");
let reveal = document.querySelector(".profile-section-1");
let close = document.querySelector(".close");

open_profile.addEventListener("click", function () {
  reveal.classList.toggle("open-profile");
});

close.addEventListener("click", function () {
  reveal.classList.remove("open-profile");
});
document.addEventListener("scroll", function () {
  reveal.classList.remove("open-profile");
});
