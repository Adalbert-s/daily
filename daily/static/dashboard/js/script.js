let chart; // Variável para armazenar o gráfico

// Função para carregar e exibir as notas do localStorage
function displayNotes() {
    const notesList = document.getElementById('notes-list');
    notesList.innerHTML = '';

    // Carrega as notas salvas no localStorage
    const notes = JSON.parse(localStorage.getItem('notes')) || [];
    notes.forEach((note, index) => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `
            <span style="text-decoration: ${note.completed ? 'line-through' : 'none'};">${note.text}</span>
            <button onclick="toggleStatus(${index})">${note.completed ? 'Undo' : 'Complete'}</button>
            <button onclick="editNotePopup(${index}, '${note.text}')">Edit</button>
            <button onclick="deleteNote(${index})">Delete</button>
        `;
        notesList.appendChild(listItem);
    });

    updateProgress(); // Atualiza o gráfico de progresso
}

// Função para criar uma nova nota
function createNote() {
    const noteText = document.getElementById('note-text').value.trim();
    if (noteText !== '') {
        // Salva a nova nota no localStorage
        const notes = JSON.parse(localStorage.getItem('notes')) || [];
        notes.push({ text: noteText, completed: false }); // Adiciona com status "pendente"
        localStorage.setItem('notes', JSON.stringify(notes));

        closePopup();
        displayNotes();
    }
}

// Função para alternar o status de uma nota
function toggleStatus(noteIndex) {
    const notes = JSON.parse(localStorage.getItem('notes')) || [];
    notes[noteIndex].completed = !notes[noteIndex].completed; // Alterna o status
    localStorage.setItem('notes', JSON.stringify(notes));

    displayNotes();
}

// Função para atualizar o gráfico de progresso
function updateProgress() {
    const notes = JSON.parse(localStorage.getItem('notes')) || [];
    const total = notes.length;
    const completed = notes.filter(note => note.completed).length;
    const pending = total - completed;

    const ctx = document.getElementById('progressChart').getContext('2d');

    // Remove o gráfico anterior, se existir
    if (chart) {
        chart.destroy();
    }

    // Cria o gráfico
    chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Completed', 'Pending'],
            datasets: [{
                data: [completed, pending],
                backgroundColor: ['#4CAF50', '#FF9800']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                }
            }
        }
    });
}
