// Função para exibir o popup para criar uma nova nota
function popup() {
    const popupContainer = document.createElement("div");
    popupContainer.innerHTML = `
        <div id="popupContainer">
            <h1>New Note</h1>
            <textarea id="note-text" placeholder="Enter your note..."></textarea>
            <div id="btn-container">
                <button id="submitBtn" onclick="createNote()">Create Note</button>
                <button id="closeBtn" onclick="closePopup()">Close</button>
            </div>
        </div>
    `;
    document.body.appendChild(popupContainer);
}

// Função para fechar o popup
function closePopup() {
    const popupContainer = document.getElementById("popupContainer");
    if (popupContainer) {
        popupContainer.remove();
    }
}

// Função para obter o cookie CSRF necessário para enviar requisições POST
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Função para criar uma nova nota
async function createNote() {
    const noteText = document.getElementById('note-text').value.trim();
    if (noteText !== '') {
        const note = { text: noteText };
        console.log('Sending POST request to /dashboard/api/notes/create/');
        const response = await fetch('/dashboard/api/notes/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(note)
        });

        if (response.ok) {
            console.log('Note created successfully');
            closePopup();
            displayNotes();
        } else {
            console.error('Failed to create note');
        }
    }
}



// Função para carregar e exibir as notas
async function displayNotes() {
    const response = await fetch('/dashboard/api/notes/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });

    if (response.ok) {
        const notes = await response.json();
        const notesList = document.getElementById('notes-list');
        notesList.innerHTML = '';

        notes.forEach(note => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `
                <span>${note.text}</span>
                <button onclick="editNotePopup(${note.id}, '${note.text}')">Edit</button>
                <button onclick="deleteNote(${note.id})">Delete</button>
            `;
            notesList.appendChild(listItem);
        });
    } else {
        console.error('Failed to load notes');
    }
}

// Função para exibir o popup de edição
function editNotePopup(noteId, noteText) {
    const popupContainer = document.createElement("div");
    popupContainer.innerHTML = `
        <div id="editPopupContainer">
            <h1>Edit Note</h1>
            <textarea id="edit-note-text">${noteText}</textarea>
            <div id="btn-container">
                <button onclick="updateNote(${noteId})">Update Note</button>
                <button onclick="closeEditPopup()">Close</button>
            </div>
        </div>
    `;
    document.body.appendChild(popupContainer);
}

// Função para fechar o popup de edição
function closeEditPopup() {
    const editPopupContainer = document.getElementById("editPopupContainer");
    if (editPopupContainer) {
        editPopupContainer.remove();
    }
}

// Função para atualizar uma nota existente
async function updateNote(noteId) {
    const newText = document.getElementById('edit-note-text').value.trim();
    if (newText !== '') {
        const note = { text: newText };
        const response = await fetch(`/dashboard/api/notes/${noteId}/update/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(note)
        });

        if (response.ok) {
            console.log('Note updated successfully');
            closeEditPopup();
            displayNotes();
        } else {
            console.error('Failed to update note');
        }
    }
}

// Função para excluir uma nota
async function deleteNote(noteId) {
    const response = await fetch(`/dashboard/api/notes/${noteId}/delete/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        }
    });

    if (response.ok) {
        console.log('Note deleted successfully');
        displayNotes();
    } else {
        console.error('Failed to delete note');
    }
}

// Chama a função para carregar as notas ao abrir a página
displayNotes();
