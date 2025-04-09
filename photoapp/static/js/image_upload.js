const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const preview = document.getElementById('preview');
const uploadForm = document.getElementById('uploadForm');

// Handle file selection
dropZone.addEventListener('click', () => fileInput.click());

// Handle drag and drop
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#007bff';
});

dropZone.addEventListener('dragleave', () => {
    dropZone.style.borderColor = '#ccc';
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#ccc';
    const files = e.dataTransfer.files;
    if (files.length) {
        fileInput.files = files;
        handleFile(files[0]);
    }
});

// Handle file input change
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length) {
        handleFile(e.target.files[0]);
    }
});

// Preview image
function handleFile(file) {
    if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
            preview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
        };
        reader.readAsDataURL(file);
    }
}

// Handle form submission
uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('title', document.getElementById('photoTitle').value);
    formData.append('description', document.getElementById('description').value);
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('http://your-api-endpoint/upload', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            alert('Photo uploaded successfully!');
            uploadForm.reset();
            preview.innerHTML = '';
        } else {
            alert('Error uploading photo');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to upload photo');
    }
});
