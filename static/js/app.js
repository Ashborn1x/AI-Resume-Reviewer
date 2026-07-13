document.addEventListener('DOMContentLoaded', () => {
  // Loading state for forms
  const forms = document.querySelectorAll("form");
  
  forms.forEach((form) => {
    form.addEventListener("submit", () => {
      const button = form.querySelector("button[type='submit']");
      if (button) {
        button.disabled = true;
        const btnText = button.querySelector('.btn-text');
        const loader = button.querySelector('.loader-wrapper');
        
        if (btnText && loader) {
          btnText.classList.add('hidden');
          loader.classList.add('visible');
        } else {
          button.textContent = "Analyzing...";
        }
      }
    });
  });

  // Dropzone interactivity
  const dropzone = document.querySelector('.dropzone');
  const fileInput = document.querySelector('.dropzone-input');
  const fileNameDisplay = document.querySelector('.file-name-display');

  if (dropzone && fileInput) {
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      dropzone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
      e.preventDefault();
      e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
      dropzone.addEventListener(eventName, () => {
        dropzone.classList.add('dragover');
      }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropzone.addEventListener(eventName, () => {
        dropzone.classList.remove('dragover');
      }, false);
    });

    fileInput.addEventListener('change', (e) => {
      if (fileInput.files.length > 0) {
        const fileName = fileInput.files[0].name;
        if (fileNameDisplay) {
          fileNameDisplay.textContent = `Selected: ${fileName}`;
        }
      } else {
        if (fileNameDisplay) {
          fileNameDisplay.textContent = '';
        }
      }
    });
  }
});
