const form = document.getElementById('uploadForm');
const fileInput = document.getElementById('imageFile');
const dropZone = document.getElementById('dropZone');
const fileName = document.getElementById('fileName');
const uploadButton = document.getElementById('uploadButton');
const statusMessage = document.getElementById('statusMessage');
const previewSection = document.getElementById('previewSection');
const resultsSection = document.getElementById('resultsSection');
const imageContainer = document.getElementById('imageContainer');
const previewMeta = document.getElementById('previewMeta');
const copyButton = document.getElementById('copyButton');

const MAX_SIZE = 8 * 1024 * 1024;
const ALLOWED_TYPES = new Set(['image/png', 'image/jpeg', 'image/webp']);

function setStatus(message, type = '') {
    statusMessage.textContent = message;
    statusMessage.className = `status ${type}`.trim();
}

function resetResults() {
    resultsSection.classList.add('hidden');
    document.getElementById('outputContainer').textContent = '';
    document.getElementById('confidenceContainer').textContent = '';
    document.getElementById('keywordsContainer').textContent = '';
    document.getElementById('ratingContainer').textContent = '';
    document.getElementById('searchContainer').textContent = '';
}

function validateFile(file) {
    if (!file) return 'Choose an image before processing.';
    if (!ALLOWED_TYPES.has(file.type)) return 'Unsupported file type. Use PNG, JPG, JPEG or WEBP.';
    if (file.size > MAX_SIZE) return 'The selected file is larger than 8 MB.';
    return null;
}

function showPreview(file) {
    const error = validateFile(file);
    resetResults();

    if (error) {
        previewSection.classList.add('hidden');
        setStatus(error, 'error');
        return false;
    }

    const image = document.createElement('img');
    image.src = URL.createObjectURL(file);
    image.alt = 'Selected document preview';
    image.onload = () => URL.revokeObjectURL(image.src);

    imageContainer.replaceChildren(image);
    fileName.textContent = file.name;
    previewMeta.textContent = `${(file.size / (1024 * 1024)).toFixed(2)} MB`;
    previewSection.classList.remove('hidden');
    setStatus('Ready to process.', 'success');
    return true;
}

fileInput.addEventListener('change', () => showPreview(fileInput.files[0]));

['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, event => {
        event.preventDefault();
        dropZone.classList.add('drag-active');
    });
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, event => {
        event.preventDefault();
        dropZone.classList.remove('drag-active');
    });
});

dropZone.addEventListener('drop', event => {
    const file = event.dataTransfer.files[0];
    if (!file) return;
    const transfer = new DataTransfer();
    transfer.items.add(file);
    fileInput.files = transfer.files;
    showPreview(file);
});

form.addEventListener('submit', async event => {
    event.preventDefault();

    const file = fileInput.files[0];
    const error = validateFile(file);
    if (error) {
        setStatus(error, 'error');
        return;
    }

    uploadButton.disabled = true;
    uploadButton.textContent = 'Processing…';
    setStatus('Running OCR and extracting keywords…', 'loading');
    resetResults();

    const formData = new FormData();
    formData.append('imageFile', file);

    try {
        const response = await fetch('/image_text_recognition', {
            method: 'POST',
            body: formData,
        });

        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
            throw new Error(data.error || 'The document could not be processed.');
        }

        renderResults(data);
        resultsSection.classList.remove('hidden');
        setStatus('Document processed successfully.', 'success');
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (error) {
        setStatus(error.message || 'Something went wrong. Please try again.', 'error');
    } finally {
        uploadButton.disabled = false;
        uploadButton.textContent = 'Process document';
    }
});

function renderResults(data) {
    document.getElementById('outputContainer').textContent = data.text || '';

    const confidenceContainer = document.getElementById('confidenceContainer');
    confidenceContainer.replaceChildren(
        metric('Block confidence', `${data.avg_block_confidence ?? 0}%`),
        metric('Paragraph confidence', `${data.avg_paragraph_confidence ?? 0}%`),
    );

    renderList('keywordsContainer', data.keywords || [], 'No keywords detected.');
    renderList('ratingContainer', data.rating || [], 'No scores available.');

    const searchContainer = document.getElementById('searchContainer');
    searchContainer.replaceChildren();
    const links = (data.search || []).flat().filter(Boolean);
    if (!links.length) {
        searchContainer.textContent = 'No related links returned.';
    } else {
        const list = document.createElement('ul');
        list.className = 'link-list';
        links.forEach(url => {
            const item = document.createElement('li');
            const anchor = document.createElement('a');
            anchor.href = url;
            anchor.target = '_blank';
            anchor.rel = 'noopener noreferrer';
            anchor.textContent = url;
            item.appendChild(anchor);
            list.appendChild(item);
        });
        searchContainer.appendChild(list);
    }
}

function metric(label, value) {
    const wrapper = document.createElement('div');
    wrapper.className = 'metric';
    const valueNode = document.createElement('strong');
    valueNode.textContent = value;
    const labelNode = document.createElement('span');
    labelNode.textContent = label;
    wrapper.append(valueNode, labelNode);
    return wrapper;
}

function renderList(containerId, values, emptyMessage) {
    const container = document.getElementById(containerId);
    container.replaceChildren();
    if (!values.length) {
        container.textContent = emptyMessage;
        return;
    }
    const list = document.createElement('ul');
    list.className = 'tag-list';
    values.forEach(value => {
        const item = document.createElement('li');
        item.textContent = value;
        list.appendChild(item);
    });
    container.appendChild(list);
}

copyButton.addEventListener('click', async () => {
    const text = document.getElementById('outputContainer').textContent;
    if (!text) return;
    await navigator.clipboard.writeText(text);
    const original = copyButton.textContent;
    copyButton.textContent = 'Copied';
    setTimeout(() => { copyButton.textContent = original; }, 1400);
});
