// Fun��o para exibir o popup para criar uma nova nota

document.addEventListener('DOMContentLoaded', displayNotes);
function popup() {
    const popupContainer = document.createElement("div");
    popupContainer.id = "popupContainer";
    popupContainer.innerHTML = `
        <h1>Novo</h1>
        <textarea id="note-text" placeholder="Enter your note..."></textarea>
        <div id="btn-container">
            <button id="submitBtn" onclick="createNote()">Create Note</button>
            <button id="closeBtn" onclick="closePopup()">Close</button>
        </div>
    `;
    document.body.appendChild(popupContainer);
}

// Fun��o para fechar o popup
function closePopup() {
    const popupContainer = document.getElementById("popupContainer");
    if (popupContainer) {
        popupContainer.remove();
    }
}

// Fun��o para carregar e exibir as notas do localStorage
// Fun��o para carregar e exibir as notas do localStorage
function displayNotes() {
    const notesList = document.getElementById('notes-list');
    notesList.innerHTML = '';

    // Carrega as notas salvas no localStorage
    const notes = JSON.parse(localStorage.getItem('notes')) || [];
    notes.forEach((note, index) => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `
            <span>${note.text}</span> <!-- Exibe o texto da nota -->
            <button onclick="editNotePopup(${index}, '${note.text}')">Edit</button>
            <button onclick="deleteNote(${index})">Delete</button>
        `;
        notesList.appendChild(listItem);
    });

    // Atualiza o gr�fico com base nas notas salvas
    updateChart(notes);
}


// Fun��o para criar uma nova nota
// Fun��o para criar uma nova nota
function createNote() {
    const noteText = document.getElementById('note-text').value.trim();
    if (noteText !== '') {
        const notes = JSON.parse(localStorage.getItem('notes')) || [];

        // Cria um objeto de nota com o texto e a data de cria��o
        const newNote = {
            text: noteText,
            createdAt: new Date().toISOString()  // Adiciona a data de cria��o
        };

        // Adiciona a nova nota ao array
        notes.push(newNote);
        localStorage.setItem('notes', JSON.stringify(notes));  // Atualiza o localStorage

        closePopup();  // Fecha o popup
        displayNotes();  // Exibe as notas atualizadas
    }
}


// Fun��o para exibir o popup de edi��o
function editNotePopup(noteIndex, noteText) {
    const popupContainer = document.createElement("div");
    popupContainer.id = "editPopupContainer";
    popupContainer.innerHTML = `
        <h1>Edit Note</h1>
        <textarea id="edit-note-text">${noteText}</textarea>
        <div id="btn-container">
            <button onclick="updateNote(${noteIndex})">Update Note</button>
            <button onclick="closeEditPopup()">Close</button>
        </div>
    `;
    document.body.appendChild(popupContainer);
}

// Fun��o para fechar o popup de edi��o
function closeEditPopup() {
    const editPopupContainer = document.getElementById("editPopupContainer");
    if (editPopupContainer) {
        editPopupContainer.remove();
    }
}

// Fun��o para atualizar uma nota existente
function updateNote(noteIndex) {
    const newText = document.getElementById('edit-note-text').value.trim();
    if (newText !== '') {
        const notes = JSON.parse(localStorage.getItem('notes')) || [];
        notes[noteIndex] = newText; // Atualiza a nota no �ndice especificado
        localStorage.setItem('notes', JSON.stringify(notes)); // Atualiza o localStorage

        closeEditPopup(); // Fecha o popup de edi��o
        displayNotes(); // Exibe as notas atualizadas
    }
}

// Fun��o para excluir uma nota
function deleteNote(noteIndex) {
    const notes = JSON.parse(localStorage.getItem('notes')) || [];
    notes.splice(noteIndex, 1); // Remove a nota do �ndice especificado
    localStorage.setItem('notes', JSON.stringify(notes)); // Atualiza o localStorage

    displayNotes(); // Exibe as notas atualizadas
}

//* globals Chart:false */

(() => {
    'use strict'

    // Fun��o para atualizar o gr�fico de notas criadas por dia
    function updateNotesByDay() {
        const notes = JSON.parse(localStorage.getItem('notes')) || [];

        // Inicializa um array de contagem de notas por dia (7 dias)
        const notesPerDay = [0, 0, 0, 0, 0, 0, 0];  // Domingo a S�bado

        // Preenche o array com a contagem de notas para cada dia
        notes.forEach(note => {
            const dayOfWeek = new Date(note.createdAt).getDay();  // Obt�m o dia da semana (0-6)
            notesPerDay[dayOfWeek]++;
        });

        // Cria o gr�fico com os dados de notas por dia
        const ctx = document.getElementById('myChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: [
                    'Sunday',  // Domingo
                    'Monday',  // Segunda-feira
                    'Tuesday', // Ter�a-feira
                    'Wednesday', // Quarta-feira
                    'Thursday', // Quinta-feira
                    'Friday',   // Sexta-feira
                    'Saturday'  // S�bado
                ],
                datasets: [{
                    data: notesPerDay,  // Usando a contagem de notas por dia
                    lineTension: 0,
                    backgroundColor: 'transparent',
                    borderColor: '#007bff',
                    borderWidth: 4,
                    pointBackgroundColor: '#007bff'
                }]
            },
            options: {
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        boxPadding: 3
                    }
                }
            }
        });
    }

    // Chama a fun��o para exibir o gr�fico assim que o script for carregado
    updateNotesByDay();
})();
document.addEventListener('DOMContentLoaded', displayNotes);

document.addEventListener('DOMContentLoaded', function () {
    let activateComplete = false; // Controla a exibi��o do bot�o "Complete"
    let activateDelete = false;   // Controla a exibi��o do bot�o "Delete"

    // Fun��o para adicionar uma nova meta
    function addReport() {
        const reportText = prompt('Enter your new report:');
        if (reportText && reportText.trim() !== '') {
            const reports = JSON.parse(localStorage.getItem('reports')) || [];
            reports.push({ text: reportText.trim(), completed: false });
            localStorage.setItem('reports', JSON.stringify(reports));
            displayReports();
        } else {
            alert('Please enter a valid report!');
        }
    }

    // Fun��o para exibir as metas salvas no localStorage
    function displayReports() {
        const reportList = document.getElementById('report-list');
        reportList.innerHTML = '';

        const reports = JSON.parse(localStorage.getItem('reports')) || [];
        reports.forEach((report, index) => {
            const listItem = document.createElement('li');
            listItem.classList.add('py-2');

            const buttonGroup = document.createElement('div');
            buttonGroup.classList.add('button-group');

            const completeBtn = document.createElement('button');
            completeBtn.classList.add('btn', 'btn-success', 'btn-sm', 'hidden');
            completeBtn.textContent = 'Complete';
            completeBtn.addEventListener('click', function () {
                completeReport(index);
            });

            const deleteBtn = document.createElement('button');
            deleteBtn.classList.add('btn', 'btn-danger', 'btn-sm', 'hidden');
            deleteBtn.textContent = 'Delete';
            deleteBtn.addEventListener('click', function () {
                deleteReport(index);
            });

            buttonGroup.appendChild(completeBtn);
            buttonGroup.appendChild(deleteBtn);

            listItem.textContent = report.text;
            listItem.appendChild(buttonGroup);

            reportList.appendChild(listItem);
        });
    }


    // Fun��o para excluir uma meta individual
    function deleteReport(index) {
        const reports = JSON.parse(localStorage.getItem('reports')) || [];
        reports.splice(index, 1);
        localStorage.setItem('reports', JSON.stringify(reports));
        displayReports();
    }

    // Fun��o para concluir (remover) uma meta individual
    function completeReport(index) {
        const reports = JSON.parse(localStorage.getItem('reports')) || [];
        reports.splice(index, 1); // Remove a meta conclu�da
        localStorage.setItem('reports', JSON.stringify(reports));
        displayReports();
    }

    // Fun��o para ativar/desativar os bot�es "Complete"
    function toggleCompleteActivation() {
        activateComplete = !activateComplete;
        const completeButtons = document.querySelectorAll('.btn-success');
        completeButtons.forEach(button => {
            button.classList.toggle('hidden', !activateComplete);
        });
    }

    // Fun��o para ativar/desativar os bot�es "Delete"
    function toggleDeleteActivation() {
        activateDelete = !activateDelete;
        const deleteButtons = document.querySelectorAll('.btn-danger');
        deleteButtons.forEach(button => {
            button.classList.toggle('hidden', !activateDelete);
        });
    }

    // Exibe as metas ao carregar a p�gina
    displayReports();

    // Configura os bot�es principais
    const addReportBtn = document.getElementById('addReportBtn');
    if (addReportBtn) {
        addReportBtn.addEventListener('click', addReport);
    } else {
        console.error('Button for adding reports not found!');
    }

    const activateCompleteBtn = document.getElementById('activateCompleteBtn');
    if (activateCompleteBtn) {
        activateCompleteBtn.addEventListener('click', toggleCompleteActivation);
    }

    const activateDeleteBtn = document.getElementById('activateDeleteBtn');
    if (activateDeleteBtn) {
        activateDeleteBtn.addEventListener('click', toggleDeleteActivation);
    }
});


