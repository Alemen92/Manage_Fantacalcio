document.addEventListener("DOMContentLoaded", function () {
    const exportButton = document.querySelector('a[href*="export"]');

    if (exportButton) {
        exportButton.addEventListener("click", function (e) {
            const confirmation = confirm("Vuoi davvero esportare la lista dei giocatori?");
            if (!confirmation) {
                e.preventDefault();
            }
        });
    }

    // Example: Dynamically update remaining budget (in role_page.html)
    const costInput = document.querySelector('input[name="cost"]');
    const remainingCredits = document.getElementById('remaining_credits');
    
    if (costInput && remainingCredits) {
        costInput.addEventListener('input', function () {
            const budgetLeft = parseInt(remainingCredits.dataset.remaining) - parseInt(costInput.value || 0);
            remainingCredits.textContent = `Budget rimanente: ${budgetLeft}`;
        });
    }
});