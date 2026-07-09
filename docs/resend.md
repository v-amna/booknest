# Resend Email Provider Setup for BookNest

This guide documents the current, working Resend setup for transactional emails in this Django project.

It includes:

- why Resend was selected
- domain verification flow
- Django integration (using the Django email integration path with Anymail + Resend backend)
- API key setup for Heroku and local development

## 1. Why Resend Was Used

A Gmail-based sender flow was attempted first, but it was not used because account verification required a Google phone number step.

Resend free plan was then selected as the email provider.

To send email from the app, domain verification was required by Resend. The domain verification was completed with help from a friend.

## 2. Current Integration in This Repository

The project is configured to send email through Resend using django-anymail.

In Django settings:

- EMAIL_BACKEND is set to Anymail Resend backend
- ANYMAIL reads RESEND_API_KEY from environment variables
- DEFAULT_FROM_EMAIL uses a sender address on the verified domain

Refences:

- Resend docs: https://resend.com/docs/send-with-django

## 3. Prerequisites

1. Resend account (free plan is enough to start).
2. A domain you control in DNS.
3. Access to Heroku app config vars.
4. Local development env.py support for environment variables.

## 4. Resend Account and Domain Verification

1. Create or log in to Resend account.
2. Add your sending domain in Resend Domains dashboard.
   Here, the domain used is `amna.pattanath.com`.
3. Copy required DNS records from Resend (SPF/DKIM and related records shown in dashboard). (Manged by my friend)
4. Add those records in your DNS provider. (Manged by my friend)
5. Wait until domain status is verified in Resend. (Manged by my friend)
6. Use a sender address from that verified domain for DEFAULT_FROM_EMAIL.
   Here, `signup@amna.pattanath.com` is used.

Important:

- Resend requires a verified domain for reliable sending.
- If domain status is pending or failed, outgoing messages may not work as expected.

## 5. API Key Creation and Secret Handling

1. Create a Resend API key in Resend dashboard.
2. Store it as an environment variable named RESEND_API_KEY.
3. Do not commit API keys to Git.

## 5.1 Heroku Configuration

Set this config var in Heroku app settings:

- RESEND_API_KEY=<your_resend_api_key>

The Django app reads this value from environment variables in settings.

## 5.2 Local Development Configuration

For local testing, add the key in env.py:

- RESEND_API_KEY=<your_resend_api_key>

Then run the app locally and test an email flow.

## 6. Django Configuration Snapshot

This repo currently uses:

- EMAIL_BACKEND = anymail.backends.resend.EmailBackend
- ANYMAIL = {"RESEND_API_KEY": os.environ.get("RESEND_API_KEY")}
- DEFAULT_FROM_EMAIL = signup@amna.pattanath.com

Additional dependency used:

- django-anymail

## 7. Validation Checklist

After setup, validate with a real flow (for example signup verification or newsletter event):

1. Trigger an app path that sends email.
   Use signup or newsletter event to trigger email sending.
2. Confirm email is delivered to recipient inbox.
3. Check Resend dashboard email activity and logs.
4. If not delivered, confirm domain is verified and API key is correct.
   If API key iis invalid or missconfigured, email sending will fail and it's logged by django.
5. Confirm sender domain matches verified domain.

## 8. Troubleshooting

Domain not verified:

- Recheck DNS records in provider.
- Wait for DNS propagation and retry verification.

Invalid API key:

- Check djago logs for any Anymail/Resend errors.
- Regenerate key in Resend dashboard.
- Update Heroku config var and local env.py.

Sender mismatch:

- Ensure DEFAULT_FROM_EMAIL uses a verified domain address.
- If using a different sender, email may be rejected by resend.
  An exception raised on django.

No email sent from app:

- Ensure RESEND_API_KEY is present in runtime environment.
- Confirm EMAIL_BACKEND is set to Resend backend.

## 9. Security Notes

- Keep console and source control free from real secrets.
- Rotate API keys if exposure is suspected.
- Prefer separate API keys per environment when possible.

## 10. References (Resend Official Docs)

- Resend docs home:
  https://resend.com/docs
- Domains management and verification status:
  https://resend.com/docs/dashboard/domains/introduction
- Add a domain flow:
  https://resend.com/docs/add-a-domain
- API keys introduction and management:
  https://resend.com/docs/dashboard/api-keys/introduction
- API key create endpoint reference:
  https://resend.com/docs/api-reference/api-keys/create-api-key
- Django quickstart (useful for API-level testing):
  https://resend.com/docs/send-with-django
