document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.add-to-cart-btn').forEach(function (button) {
        button.addEventListener('click', function () {
            let url = button.dataset.url;

            button.disabled = true;

            fetch(url)
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    showToast(
                        data.message || 'Something went wrong.',
                        data.success
                    );
                })
                .catch(function () {
                    showToast('Something went wrong. Please try again.', false);
                })
                .finally(function () {
                    button.disabled = false;
                });
        });
    });
});
