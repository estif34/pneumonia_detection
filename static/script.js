document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('upload-area');
    const imageInput = document.getElementById('image-input');
    const previewImg = document.getElementById('preview-img');
    const uploadPlaceholder = document.getElementById('upload-placeholder');
    const uploadForm = document.getElementById('upload-form');
    const analyzeBtn = document.getElementById('analyze-btn');
    const btnText = analyzeBtn.querySelector('.btn-text');
    const btnLoading = analyzeBtn.querySelector('.btn-loading');
    
    // Theme selector
    const themeButtons = document.querySelectorAll('.theme-btn');
    const html = document.documentElement;
    
    // Load saved theme or default to dark
    const savedTheme = localStorage.getItem('theme') || 'dark';
    applyTheme(savedTheme);
    
    themeButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const theme = this.getAttribute('data-theme');
            applyTheme(theme);
            localStorage.setItem('theme', theme);
        });
    });
    
    function applyTheme(theme) {
        themeButtons.forEach(btn => btn.classList.remove('active'));
        document.querySelector(`[data-theme="${theme}"]`).classList.add('active');
        
        if (theme === 'system') {
            const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
            html.setAttribute('data-theme', systemTheme);
        } else {
            html.setAttribute('data-theme', theme);
        }
    }
    
    // Listen for system theme changes if system is selected
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        const currentTheme = localStorage.getItem('theme');
        if (currentTheme === 'system') {
            html.setAttribute('data-theme', e.matches ? 'dark' : 'light');
        }
    });

    // Preview image on file select
    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            displayPreview(file);
        }
    });

    // Drag and drop functionality
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            imageInput.files = e.dataTransfer.files;
            displayPreview(file);
        }
    });

    // Display image preview
    function displayPreview(file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImg.src = e.target.result;
            previewImg.classList.remove('hidden');
            uploadPlaceholder.classList.add('hidden');
        };
        reader.readAsDataURL(file);
    }

    // Form submission - show loading state
    uploadForm.addEventListener('submit', function(e) {
        if (!imageInput.files.length) {
            e.preventDefault();
            alert('Please select an image first');
            return;
        }

        analyzeBtn.disabled = true;
        btnText.classList.add('hidden');
        btnLoading.classList.remove('hidden');
    });

    // Animate confidence bar on page load (if results exist)
    const confidenceFill = document.querySelector('.confidence-fill');
    if (confidenceFill) {
        const targetWidth = confidenceFill.style.width;
        confidenceFill.style.width = '0%';
        setTimeout(() => {
            confidenceFill.style.width = targetWidth;
        }, 100);
    }
});