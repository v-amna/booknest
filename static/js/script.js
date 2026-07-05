function showToast(message, isSuccess) {
    let toastEl = document.getElementById('toast');
    let toastBody = document.getElementById('toast-body');

    toastBody.textContent = message;

    toastEl.classList.remove('bg-success', 'bg-danger');
    toastEl.classList.add(isSuccess ? 'bg-success' : 'bg-danger');

    bootstrap.Toast.getOrCreateInstance(toastEl).show();
}
