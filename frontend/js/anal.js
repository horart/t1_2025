// Обработка гамбургер-меню
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.getElementById('hamburger');
    const nav = document.getElementById('nav');
    
    hamburger.addEventListener('click', function() {
        hamburger.classList.toggle('active');
        nav.classList.toggle('active');
    });
    
    // Закрытие меню при клике вне его области
    document.addEventListener('click', function(event) {
        const isClickInsideNav = nav.contains(event.target);
        const isClickInsideHamburger = hamburger.contains(event.target);
        
        if (!isClickInsideNav && !isClickInsideHamburger && nav.classList.contains('active')) {
            hamburger.classList.remove('active');
            nav.classList.remove('active');
        }
    });
    
    // Предотвращение изменения состояния чекбоксов
    document.querySelectorAll('.career-checkbox').forEach(checkbox => {
        checkbox.addEventListener('click', (e) => {
            e.preventDefault();
        });
    });
    
    // Анимация прогрессбара
    setTimeout(() => {
        document.querySelector('.progress-bar').style.width = '60%';
    }, 500);
});