function showNotification(message) {
    document.getElementById('notification-message').textContent = message;
    document.getElementById('notification-modal').classList.remove('hidden');
}
function hideNotification() {
    document.getElementById('notification-modal').classList.add('hidden');
}
document.addEventListener('DOMContentLoaded', () => {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabPanes = document.querySelectorAll('.tab-pane');
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.add('hidden'));
            button.classList.add('active');
            const tabId = button.getAttribute('data-tab');
            document.getElementById(tabId).classList.remove('hidden');
        });
    });
});
