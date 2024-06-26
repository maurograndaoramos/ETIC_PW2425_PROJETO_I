document.addEventListener('DOMContentLoaded', function() {

    // Esta função é responsável por ajustar a posição do texto de quota no dashboard e garantir que segue o tamanho da barra de progresso
    var quotaText = document.querySelector('.quota-text');
    if (quotaText) {
        var percentageFull = parseInt(quotaText.textContent.split('%')[0]);
        var leftPosition = Math.min(Math.max(parseInt(percentageFull), 0), 100);
        quotaText.style.left = `${leftPosition}vw`;
    }

    // Função simplex para mudar a visibilidade do elemento modal
    function openModal(modalId) {
        document.getElementById(modalId).style.display = "block";
    }

    // Same as above, mas para fechar o modal
    function closeModal(modalId) {
        const modal = document.getElementById(modalId);
        modal.classList.add('hide');
        setTimeout(() => {
            modal.classList.remove('hide');
            modal.style.display = "none";
        }, 500);
    }

    // Modal event listeners, same-old-same-old
    document.getElementById('create-folder-btn').addEventListener('click', function() {
        openModal('create-folder-modal');
    });
    
    document.getElementById('upload-folder-btn').addEventListener('click', function() {
        openModal('upload-folder-modal');
    });

    document.getElementById('upload-file-btn').addEventListener('click', function() {
        openModal('upload-file-modal');
    });

    document.querySelectorAll('.close').forEach(function(closeBtn) {
        closeBtn.addEventListener('click', function() {
            closeModal(this.closest('.modal').id);
        });
    });

    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            closeModal(event.target.id);
        }
    };

    // Parecido com o de cima mas para os modals dentro dos cards
    document.querySelectorAll('[data-toggle-target="renameFolderModal"]').forEach(function(icon) {
        icon.addEventListener('click', function() {
            const folderHash = this.getAttribute('data-folder-hash');
            const form = document.getElementById('renameFolderForm');
            form.action = `/drive/rename-folder/${folderHash}/`;
            openModal('renameFolderModal');
        });
    });

    document.querySelectorAll('[data-toggle-target="moveFolderModal"]').forEach(function(icon) {
        icon.addEventListener('click', function() {
            const folderHash = this.getAttribute('data-folder-hash');
            const form = document.getElementById('moveFolderForm');
            form.action = `/drive/move-folder/${folderHash}/`;
            openModal('moveFolderModal');
        });
    });

    document.querySelectorAll('.rename-file-btn').forEach(function(icon) {
        icon.addEventListener('click', function() {
            const fileHash = this.getAttribute('data-file-hash');
            const form = document.getElementById('renameFileForm');
            form.action = `/drive/rename-file/${fileHash}/`;
            openModal('renameFileModal');
        });
    });

    document.querySelectorAll('[data-toggle-target="moveFileModal"]').forEach(function(icon) {
        icon.addEventListener('click', function() {
            const fileHash = this.getAttribute('data-file-hash');
            const form = document.getElementById('moveFileForm');
            form.action = `/drive/move-file/${fileHash}/`;
            openModal('moveFileModal');
        });
    });

    // Honestamente, só queria que o código fosse mais limpo no HTML e não ter um botão por cima do delete svg
    document.querySelectorAll('.trash-btn').forEach(function(icon) {
        icon.addEventListener('click', function(e) {
            e.preventDefault();
            const action = this.getAttribute('data-action');
            const itemType = this.hasAttribute('data-folder-hash') ? 'folder' : 'file';
            if (confirm(`Are you sure you want to delete this ${itemType}?`)) {
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = action;
                
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                const csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = 'csrfmiddlewaretoken';
                csrfInput.value = csrfToken;
                
                form.appendChild(csrfInput);
                document.body.appendChild(form);
                form.submit();
            }
        });
    });

    // Isto é um hack para permitir que o input de ficheiros funcione com pastas - não é suportado nativamente e francamente é uma dor de cabeça. Tive que fazer isto para permitir uploads de pastas mas não é perfeito e nem deve funcionar em todos os browsers
    document.getElementById('upload-folder-form').addEventListener('submit', function(e) {
        e.preventDefault();
        var formData = new FormData(this);
        var files = document.getElementById('folder-input').files;
        
        for (var i = 0; i < files.length; i++) {
            formData.append('file_paths', files[i].webkitRelativePath);
        }
    
        fetch(this.action, {
            method: 'POST',
            body: formData,
            credentials: 'same-origin'
        }).then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                console.error('Upload failed');
            }
        });
    });

    // Assigna a classe fade-out a todas as mensagens de sucesso, erro, info e aviso após 5 segundos - Yay dynamic messages!
    var messages = document.querySelectorAll('.messages .success, .messages .error, .messages .info, .messages .warning');
    messages.forEach(function(message) {
        setTimeout(function() {
            message.classList.add('fade-out');
            message.addEventListener('animationend', function() {
                message.remove();
            });
        }, 5000);
    });

    // É um toggle switch para mudar o tema da página
    const toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');
    const currentTheme = localStorage.getItem('theme');
  
    if (currentTheme) {
      document.documentElement.setAttribute('data-theme', currentTheme);
      if (currentTheme === 'light') {
        toggleSwitch.checked = true;
      }
    }
  
    function switchTheme(e) {
      if (e.target.checked) {
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
      } else {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
      }    
    }
  
    toggleSwitch.addEventListener('change', switchTheme, false);
  
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    toggleSwitch.checked = savedTheme === 'light';

    // Isto foi feito para permitir que o utilizador veja o nome da extensão do ficheiro mesmo que o nome seja muito longo.
    function truncateFileName(element, maxLength) {
        const fileName = element.textContent;
        const lastDotIndex = fileName.lastIndexOf('.');
        
        if (lastDotIndex === -1 || fileName.length <= maxLength) {
          return;
        }
      
        const name = fileName.slice(0, lastDotIndex);
        const extension = fileName.slice(lastDotIndex);
        
        const availableLength = maxLength - extension.length - 3;
        if (availableLength < 5) {
          return;
        }
        
        const start = name.slice(0, Math.ceil(availableLength / 2));
        const end = name.slice(-Math.floor(availableLength / 2));
        
        element.textContent = start + '...' + end + extension;
    }
      
    document.querySelectorAll('.file-body p').forEach(element => {
        truncateFileName(element, 20);
    });

});