/**
 * script.js - Gerenciamento completo de notas
 * Funcionalidades:
 * - Criar/editar/excluir notas
 * - Popup interativo
 * - Integração com API Django
 */

document.addEventListener('DOMContentLoaded', function () {
    // ==================== CONSTANTES ====================
    const API_URL = '/api/todonotas/';
    const CSRF_TOKEN = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // ==================== ELEMENTOS DO DOM ====================
    const addNoteBtn = document.getElementById('addNoteDiv');
    const notesList = document.getElementById('notes-list');

    function getCookie(name) {
        let cookieArr = document.cookie.split(';');

        for (let i = 0; i < cookieArr.length; i++) {
            let cookie = cookieArr[i].trim();
            if (cookie.startsWith(name + '=')) {
                return cookie.substring(name.length + 1);
            }
        }
        return ''; // Retorna uma string vazia caso o cookie não seja encontrado
    }


    // ==================== FUNÇÕES PRINCIPAIS ====================

    // 1. Gerencia o popup de notas
    function showPopup(note = null) {
        const isEditMode = note !== null;

        const popupHTML = `
        <div class="popup-overlay">
            <div class="popup-content">
                <h2>${isEditMode ? 'Editar Nota' : 'Nova Nota'}</h2>
                <textarea id="note-text">${isEditMode ? note.text : ''}</textarea>
                <div class="popup-actions">
                    <button id="saveNoteBtn">${isEditMode ? 'Atualizar' : 'Salvar'}</button>
                    <button id="cancelNoteBtn">Cancelar</button>
                </div>
            </div>
        </div>
        `;

        document.body.insertAdjacentHTML('beforeend', popupHTML);

        // Event listeners para os botões do popup
        document.getElementById('saveNoteBtn').addEventListener('click', () => {
            const text = document.getElementById('note-text').value.trim();
            if (text) {
                if (isEditMode) {
                    updateNote(note.id, text);
                } else {
                    createNote(text);
                }
            }
        });

        document.getElementById('cancelNoteBtn').addEventListener('click', closePopup);
    }

    // 2. Fecha o popup
    function closePopup() {
        const popup = document.querySelector('.popup-overlay');
        if (popup) popup.remove();
    }

    // 3. Cria uma nova nota
    async function createNote() {
        const text = document.getElementById('note-text').value.trim();
        if (!text) return showError('Texto não pode estar vazio');

        try {
            console.log("Enviando:", { text });  // Debug

            const response = await fetch('/api/notes/', {
                method: 'POST',             
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Authorization': `Token ${localStorage.getItem('token') || ''}`
                },
                body: JSON.stringify({ text })
            });

            const data = await response.json();
            console.log("Resposta:", data);  // Debug

            if (!response.ok) {
                throw new Error(data.error || JSON.stringify(data));
            }

            closePopup();
            loadNotes();
        } catch (error) {
            console.error("Erro completo:", {
                error: error,
                message: error.message,
                stack: error.stack
            });
            showError(`Erro: ${error.message}`);
        }
    }
    // 4. Atualiza uma nota existente
    async function updateNote(id, text) {
        try {
            const response = await fetch(`${API_URL}${id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': CSRF_TOKEN,
                },
                body: JSON.stringify({ text })
            });

            if (response.ok) {
                closePopup();
                loadNotes();
            } else {
                showError('Erro ao atualizar nota');
            }
        } catch (error) {
            console.error('Error:', error);
            showError('Falha na conexão');
        }
    }

    // 5. Carrega todas as notas
    async function loadNotes() {
        try {
            const response = await fetch(API_URL);
            if (response.ok) {
                const notes = await response.json();
                renderNotes(notes);
                updateChart(notes);
            } else {
                showError('Erro ao carregar notas');
            }
        } catch (error) {
            console.error('Error:', error);
            showError('Falha ao carregar notas');
        }
    }

    // 6. Exclui uma nota
    async function deleteNote(id) {
        if (confirm('Tem certeza que deseja excluir esta nota?')) {
            try {
                const response = await fetch(`${API_URL}${id}/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': CSRF_TOKEN,
                    }
                });

                if (response.ok) {
                    loadNotes();
                } else {
                    showError('Erro ao excluir nota');
                }
            } catch (error) {
                console.error('Error:', error);
                showError('Falha na conexão');
            }
        }
    }

    // ==================== FUNÇÕES AUXILIARES ====================

    // Renderiza a lista de notas
    function renderNotes(notes) {
        notesList.innerHTML = notes.map(note => `
            <li class="note-item" data-id="${note.id}">
                <div class="note-content">${note.text}</div>
                <div class="note-actions">
                    <button class="edit-btn" data-id="${note.id}">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="delete-btn" data-id="${note.id}">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </li>
        `).join('');

        // Adiciona eventos aos botões
        document.querySelectorAll('.edit-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const noteId = e.currentTarget.getAttribute('data-id');
                const noteText = e.currentTarget.closest('.note-item').querySelector('.note-content').textContent;
                showPopup({ id: noteId, text: noteText });
            });
        });

        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const noteId = e.currentTarget.getAttribute('data-id');
                deleteNote(noteId);
            });
        });
    }

    // Atualiza o gráfico (implementação básica)
    function updateChart(notes) {
        console.log('Atualizando gráfico com:', notes);
        // Implemente sua lógica de gráfico aqui
    }

    // Mostra mensagens de erro
    function showError(message) {
        alert(message);
    }

    // ==================== INICIALIZAÇÃO ====================
    if (addNoteBtn) {
        addNoteBtn.addEventListener('click', () => showPopup());
    }

    // Delegation para eventos dinâmicos
    notesList.addEventListener('click', (e) => {
        if (e.target.classList.contains('fa-edit')) {
            const noteId = e.target.closest('.edit-btn').getAttribute('data-id');
            const noteText = e.target.closest('.note-item').querySelector('.note-content').textContent;
            showPopup({ id: noteId, text: noteText });
        } else if (e.target.classList.contains('fa-trash')) {
            const noteId = e.target.closest('.delete-btn').getAttribute('data-id');
            deleteNote(noteId);
        }
    });

    // Carrega as notas ao iniciar
    loadNotes();

    // Debug
    console.log('Aplicação inicializada com sucesso!');
});