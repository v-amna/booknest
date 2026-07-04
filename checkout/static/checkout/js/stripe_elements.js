/*
    Core Stripe logic based on:
    https://stripe.com/docs/payments/accept-a-payment
*/

var stripePublicKey = JSON.parse(document.getElementById('id_stripe_public_key').textContent);
var clientSecret = JSON.parse(document.getElementById('id_client_secret').textContent);

var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();

var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

var card = elements.create('card', { style: style });
card.mount('#card-element');

/* =========================
   Real-time validation
========================= */
card.addEventListener('change', function(event) {
    var errorDiv = document.getElementById('card-errors');

    if (event.error) {
        errorDiv.innerHTML = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
    } else {
        errorDiv.textContent = '';
    }
});

/* =========================
   Handle form submit
========================= */
var form = document.getElementById('payment-form');
var submitButton = document.getElementById('submit-button');

if (form) {
    form.addEventListener('submit', function(ev) {

        ev.preventDefault();

    card.update({ disabled: true });
    submitButton.disabled = true;

    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    var postData = {
        csrfmiddlewaretoken: csrfToken,
        client_secret: clientSecret,
        save_info: false,
    };

    $.post('/checkout/cache_checkout_data/', postData)
        .done(function() {

            stripe.confirmCardPayment(clientSecret, {

                payment_method: {
                    card: card,
                    billing_details: {
                        name: $.trim(form.full_name.value),
                        phone: $.trim(form.phone_number.value),
                        email: $.trim(form.email.value),
                        address: {
                            line1: $.trim(form.street_address1.value),
                            line2: $.trim(form.street_address2.value),
                            city: $.trim(form.town_or_city.value),
                            postal_code: $.trim(form.postcode.value),
                            country: $.trim(form.country.value),
                        }
                    }
                },

                shipping: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    address: {
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        city: $.trim(form.town_or_city.value),
                        postal_code: $.trim(form.postcode.value),
                        country: $.trim(form.country.value),
                    }
                }

            }).then(function(result) {

                if (result.error) {

                    var errorDiv = document.getElementById('card-errors');
                    errorDiv.textContent = result.error.message;

                    card.update({ disabled: false });
                    submitButton.disabled = false;

                } else {

                    if (result.paymentIntent.status === 'succeeded') {
                        form.submit();
                    }
                }

            });

        })
        .fail(function() {
            location.reload();
        });

});}