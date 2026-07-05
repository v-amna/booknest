document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.add-to-cart-btn').forEach(function (button) {
        button.addEventListener('click', function () {
            let url = button.dataset.url;
            let originalText = button.textContent;

            button.disabled = true;

            fetch(url)
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    // TODO move to bootstrap toast instead this
                    button.textContent = data.success ? 'Added!' : 'Error';

                    setTimeout(function () {
                        button.textContent = originalText;
                        button.disabled = false;
                    }, 1200);
                })
                .catch(function () {
                    // TODO move to bootstrap toast instead this
                    button.textContent = 'Error';

                    setTimeout(function () {
                        button.textContent = originalText;
                        button.disabled = false;
                    }, 1200);
                });
        });
    });
});
