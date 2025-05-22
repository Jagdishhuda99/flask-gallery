// zoom.js

const zoomImage = document.getElementById('lightbox-img');

let isDragging = false;
let startX, startY;
let offsetX = 0, offsetY = 0;
let scale = 1;

zoomImage.addEventListener('mousedown', (e) => {
    e.preventDefault();
    isDragging = true;
    startX = e.clientX - offsetX;
    startY = e.clientY - offsetY;
    zoomImage.style.cursor = 'grabbing';
});

document.addEventListener('mouseup', () => {
    isDragging = false;
    zoomImage.style.cursor = 'grab';
});

document.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    offsetX = e.clientX - startX;
    offsetY = e.clientY - startY;
    zoomImage.style.transform = `translate(${offsetX}px, ${offsetY}px) scale(${scale})`;
});

zoomImage.addEventListener('wheel', (e) => {
    e.preventDefault();
    const delta = e.deltaY > 0 ? -0.1 : 0.1;
    const newScale = scale + delta;
    scale = Math.max(1, newScale);
    zoomImage.style.transform = `translate(${offsetX}px, ${offsetY}px) scale(${scale})`;

    if (scale === 1 && delta < 0) {
        document.getElementById("lightbox").style.display = "none";
    }
});



