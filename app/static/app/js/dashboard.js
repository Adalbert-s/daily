/* globals Chart:false */

(() => {
    'use strict'

    // Função para atualizar o gráfico de notas criadas por dia
    function updateNotesByDay() {
        const notes = JSON.parse(localStorage.getItem('notes')) || [];

        // Inicializa um array de contagem de notas por dia (7 dias)
        const notesPerDay = [0, 0, 0, 0, 0, 0, 0];  // Domingo a Sábado

        // Preenche o array com a contagem de notas para cada dia
        notes.forEach(note => {
            const dayOfWeek = new Date(note.createdAt).getDay();  // Obtém o dia da semana (0-6)
            notesPerDay[dayOfWeek]++;
        });

        // Cria o gráfico com os dados de notas por dia
        const ctx = document.getElementById('myChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: [
                    'Sunday',  // Domingo
                    'Monday',  // Segunda-feira
                    'Tuesday', // Terça-feira
                    'Wednesday', // Quarta-feira
                    'Thursday', // Quinta-feira
                    'Friday',   // Sexta-feira
                    'Saturday'  // Sábado
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

    // Chama a função para exibir o gráfico assim que o script for carregado
    updateNotesByDay();
})();
