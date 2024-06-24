document.addEventListener('DOMContentLoaded', function() {
    // Quota Text Logic
    var quotaText = document.querySelector('.quota-text');
    if (quotaText) {
        var percentageFull = quotaText.textContent.match(/(\d+)%/)[1];
        var leftPosition = Math.min(Math.max(parseInt(percentageFull), 0), 100);
        quotaText.style.left = `${leftPosition}vw`;
    }

    // Modal Logic Functions
    function openModal(modalId) {
        document.getElementById(modalId).style.display = "block";
    }

    function closeModal(modalId) {
        const modal = document.getElementById(modalId);
        modal.classList.add('hide');
        setTimeout(() => {
            modal.classList.remove('hide');
            modal.style.display = "none";
        }, 500);
    }

    // Modal Open/Close Events
    document.getElementById('create-folder-btn').addEventListener('click', function() {
        openModal('create-folder-modal');
    });

    document.getElementById('upload-folder-btn').addEventListener('click', function() {
        openModal('upload-folder-modal');
    });

    document.getElementById('upload-file-btn').addEventListener('click', function() {
        openModal('upload-file-modal');
    });

    // Close modal when clicking on span (x)
    document.querySelectorAll('.close').forEach(function(closeBtn) {
        closeBtn.addEventListener('click', function() {
            closeModal(this.closest('.modal').id);
        });
    });

    // Close modal when clicking outside of it
    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            closeModal(event.target.id);
        }
    };

    // Toggle Visibility Logic
    function toggleVisibility(divId) {
        var x = document.getElementById(divId);
        x.style.display = (x.style.display === 'none' || !x.style.display) ? 'block' : 'none';
    }

    // Attach Toggle Functionality to SVG Icons
    document.querySelectorAll('.icon-settings').forEach(function(icon) {
        icon.addEventListener('click', function() {
            const folderHash = this.getAttribute('data-folder-hash');
            const targetPrefix = this.getAttribute('data-toggle-target'); // Ensure your SVG has this attribute
            toggleVisibility(targetPrefix + folderHash);
        });
    });

    // Folder rename modal
    document.querySelectorAll('[data-toggle-target="renameFolderModal"]').forEach(function(icon) {
        icon.addEventListener('click', function() {
            const folderHash = this.getAttribute('data-folder-hash');
            const form = document.getElementById('renameFolderForm');
            form.action = `/drive/rename-folder/${folderHash}/`;
            openModal('renameFolderModal');
        });
    });

    // Folder move modal
    document.querySelectorAll('[data-toggle-target="moveFolderModal"]').forEach(function(icon) {
        icon.addEventListener('click', function() {
            const folderHash = this.getAttribute('data-folder-hash');
            const form = document.getElementById('moveFolderForm');
            form.action = `/drive/move-folder/${folderHash}/`;
            openModal('moveFolderModal');
        });
    });

    // File rename modal
    document.querySelectorAll('.rename-file-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const fileHash = this.getAttribute('data-file-hash');
            const form = document.getElementById('renameFileForm');
            form.action = `/drive/rename-file/${fileHash}/`;
            openModal('renameFileModal');
        });
    });
});
