// Данные проектов
const projectsData = [
    {
        name: "Разработка HR-платформы",
        stack: ["React", "Node.js", "MongoDB"],
        creationDate: "15.03.2023",
        teamSize: 5
    },
    {
        name: "Система аналитики персонала",
        stack: ["Python", "Django", "PostgreSQL", "Chart.js"],
        creationDate: "22.05.2023",
        teamSize: 3
    },
    {
        name: "Мобильное приложение для сотрудников",
        stack: ["Flutter", "Firebase", "Dart"],
        creationDate: "10.08.2023",
        teamSize: 4
    }
];

// Функция для отображения проектов в таблице
function renderProjects() {
    const tableBody = document.getElementById('projectsTableBody');
    tableBody.innerHTML = '';

    projectsData.forEach(project => {
        const row = document.createElement('tr');

        // Название проекта
        const nameCell = document.createElement('td');
        nameCell.className = 'project-name';
        nameCell.textContent = project.name;

        // Стек технологий
        const stackCell = document.createElement('td');
        const stackContainer = document.createElement('div');
        stackContainer.className = 'project-stack';

        project.stack.forEach(tech => {
            const techTag = document.createElement('span');
            techTag.className = 'stack-tag';
            techTag.textContent = tech;
            stackContainer.appendChild(techTag);
        });

        stackCell.appendChild(stackContainer);

        // Дата создания
        const dateCell = document.createElement('td');
        dateCell.textContent = project.creationDate;

        // Команда
        const teamCell = document.createElement('td');
        const teamContainer = document.createElement('div');
        teamContainer.className = 'project-team';

        const teamCount = document.createElement('div');
        teamCount.className = 'team-count';
        teamCount.textContent = project.teamSize;

        teamContainer.appendChild(teamCount);
        teamCell.appendChild(teamContainer);

        // Действия
        const actionsCell = document.createElement('td');
        const actionsContainer = document.createElement('div');
        actionsContainer.className = 'project-actions';

        const editBtn = document.createElement('button');
        editBtn.className = 'action-btn';
        editBtn.innerHTML = '✏️';
        editBtn.title = 'Редактировать';

        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'action-btn';
        deleteBtn.innerHTML = '🗑️';
        deleteBtn.title = 'Удалить';

        actionsContainer.appendChild(editBtn);
        actionsContainer.appendChild(deleteBtn);
        actionsCell.appendChild(actionsContainer);

        // Собираем строку
        row.appendChild(nameCell);
        row.appendChild(stackCell);
        row.appendChild(dateCell);
        row.appendChild(teamCell);
        row.appendChild(actionsCell);

        tableBody.appendChild(row);
    });
}

// Функции для работы с модальным окном
function openModal() {
    document.getElementById('modalOverlay').classList.add('active');
}

function closeModal() {
    document.getElementById('modalOverlay').classList.remove('active');
    document.getElementById('projectForm').reset();
}

// Обработчики событий
document.addEventListener('DOMContentLoaded', function() {
    // Отображаем проекты при загрузке страницы
    renderProjects();

    // Обработчик для кнопки "Создать проект" в выпадающем меню
    document.getElementById('createProjectOption').addEventListener('click', function(e) {
        e.preventDefault();
        openModal();
    });

    // Обработчики для модального окна
    document.getElementById('closeModalBtn').addEventListener('click', closeModal);
    document.getElementById('cancelFormBtn').addEventListener('click', closeModal);

    // Обработчик отправки формы
    document.getElementById('projectForm').addEventListener('submit', function(e) {
        e.preventDefault();

        // Получаем данные из формы
        const projectName = document.getElementById('projectName').value;
        const projectDescription = document.getElementById('projectDescription').value;
        const projectStart = document.getElementById('projectStart').value;
        const projectEnd = document.getElementById('projectEnd').value;
        const projectStatus = document.getElementById('projectStatus').value;
        const projectPriority = document.getElementById('projectPriority').value;
        const projectTeam = document.getElementById('projectTeam').value;

        // Здесь должна быть логика сохранения проекта
        console.log('Новый проект:', {
            projectName,
            projectDescription,
            projectStart,
            projectEnd,
            projectStatus,
            projectPriority,
            projectTeam
        });

        // Закрываем модальное окно
        closeModal();

        // Показываем уведомление об успешном создании
        alert('Проект успешно создан!');
    });

    // Закрытие модального окна при клике вне его области
    document.getElementById('modalOverlay').addEventListener('click', function(e) {
        if (e.target === this) {
            closeModal();
        }
    });
});