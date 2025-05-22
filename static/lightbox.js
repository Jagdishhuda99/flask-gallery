// lightbox.js
window.openLightbox = function (src) {
    const lightbox = document.getElementById("lightbox");
    const lightboxImg = document.getElementById("lightbox-img");
    lightboxImg.src = src;
    lightbox.style.display = "flex";

    // Reset zoom
    lightboxImg.style.transform = "translate(0px, 0px) scale(1)";
    offsetX = offsetY = 0;
    scale = 1;
};

window.closeLightbox = function () {
    const lightbox = document.getElementById("lightbox");
    lightbox.style.display = "none";
};
