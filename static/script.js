// ===== Dark Mode Toggle =====
const darkModeBtn = document.querySelector('.dark-mode-btn');
darkModeBtn?.addEventListener('click', () => {
  document.body.classList.toggle('dark-mode');
});

// ===== Drag & Drop Upload =====
const uploadForm = document.querySelector('.upload-form');
if (uploadForm) {
  uploadForm.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadForm.classList.add('dragover');
  });

  uploadForm.addEventListener('dragleave', () => {
    uploadForm.classList.remove('dragover');
  });

  uploadForm.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadForm.classList.remove('dragover');
    const files = e.dataTransfer.files;
    document.querySelector('input[type="file"]').files = files;
  });
}

// ===== Lightbox Preview =====
document.querySelectorAll('.media-item img').forEach(img => {
  img.addEventListener('click', () => {
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.createElement('img');
    lightboxImg.src = img.src;
    lightbox.innerHTML = '';
    lightbox.appendChild(lightboxImg);
    lightbox.style.display = 'flex';
  });
});

document.getElementById('lightbox')?.addEventListener('click', () => {
  document.getElementById('lightbox').style.display = 'none';
});

// ===== Loader Control =====
function showLoader() {
  document.querySelector('.loader')?.classList.remove('hidden');
}

function hideLoader() {
  document.querySelector('.loader')?.classList.add('hidden');
}

// ===== Mobile Drawer Navigation (Optional Placeholder) =====
const mobileNavBtn = document.querySelector('.mobile-nav');
mobileNavBtn?.addEventListener('click', () => {
  alert('Drawer navigation will appear here.');
});


function addDownloadEmoji(viewer) {
  viewer.viewer.addEventListener('shown', () => {
    const buttons = document.querySelectorAll('.viewer-toolbar > li');
    buttons.forEach(btn => {
      if (btn.getAttribute('data-action') === 'download') {
        btn.innerHTML = '⬇️ Download';  // या '⬇️ डाउनलोड'
      }
    });
  });
}
