document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const photoInput = document.getElementById('photoInput');
    const preview = document.getElementById('preview');
    const form = document.getElementById('uploadForm');

    // Drag and drop handlers
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.background = '#eee';
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.style.background = '';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.style.background = '';
        const files = e.dataTransfer.files;
        if (files.length) {
            photoInput.files = files;
            showPreview(files[0]);
        }
    });

    // File input change handler
    photoInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            showPreview(e.target.files[0]);
        }
    });

    // Form submit handler
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('photo', photoInput.files[0]);
        formData.append('title', form.title.value);
        formData.append('description', form.description.value);

        fetch('/upload', {
            method: 'POST',
            body: formData
        }).then(response => {
            if (response.ok) {
                alert('Upload successful!');
                form.reset();
                preview.style.display = 'none';
            } else {
                alert('Upload failed');
            }
        });
    });

    function showPreview(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            preview.src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
});