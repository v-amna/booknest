# AWS S3 Setup for BookNest (Static + Media)

Here is the information about setting up s3 and working AWS S3 setup used by this project for static and media files in Django.
We use Amazon S3 as the storage backend for:

- static files (CSS, JS, site images)
- media files (uploaded book images)

To force Django to use S3, set `USE_AWS=True`.

## 1. AWS Account and IAM Setup

## 1.1 AWS Account

1. Sign in to AWS Console with your account.
2. Keep root user only for account-level operations.
3. Use IAM user for application access.

## 1.2 IAM User for S3 API Access

Create a dedicated IAM user for S3 access with the following properties:

- IAM username: `booknest-bucket`
- Console access: disabled
- Programmatic access: enabled (access key created)

Policies attached to this user:

- Managed policy: `AmazonS3FullAccess`
- Inline policy (bucket-scoped):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Statement1",
      "Effect": "Allow",
      "Action": [
        "s3:*"
      ],
      "Resource": [
        "arn:aws:s3:::booknest-241304351285-eu-central-1-an",
        "arn:aws:s3:::booknest-241304351285-eu-central-1-an/*"
      ]
    }
  ]
}
```

Access key operational note:

- Access key exists and is used by the Heroku app.

Reference to followed:

- AWS IAM User Guide: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html
- AWS IAM S3 Policy Guide: https://docs.aws.amazon.com/AmazonS3/latest/userguide/walkthrough1.html#walkthrough1-add-users

## 2. S3 Bucket Setup

- Regional S3 bucket name: `booknest-241304351285-eu-central-1-an`
- Region: `eu-central-1`
- Public access: allowed for the required object paths (static/media) using bucket policy.

## 2.1 Bucket Policy (Public Read for Static and Media)

This policy is applied to the S3 bucket to allow public read access for static and media files.
Using aws console, go to S3 -> bucket -> Permissions -> Bucket Policy and paste the following JSON:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadStatic",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::booknest-241304351285-eu-central-1-an/static/*"
    },
    {
      "Sid": "PublicReadMedia",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::booknest-241304351285-eu-central-1-an/media/*"
    }
  ]
}
```

This CORS configuration allows the frontend to access static and media files from the S3 bucket during development and production.
Added using aws console: S3 -> bucket -> Permissions -> CORS configuration.
## 2.2 CORS Configuration

```json
[
  {
    "AllowedHeaders": [
      "*"
    ],
    "AllowedMethods": [
      "GET",
      "HEAD"
    ],
    "AllowedOrigins": [
      "https://booknest-1-5c0fa7f9a116.herokuapp.com",
      "http://localhost:8000",
      "http://127.0.0.1:8000"
    ],
    "ExposeHeaders": [],
    "MaxAgeSeconds": 3000
  }
]
```

## 3. Heroku Environment Variables

AWS credentials and bucket settings are stored in Heroku app config vars and loaded into Django settings via environment variables.
Added using heroku web: Booknest application -> Settings -> Config Vars -> Reveal Config Vars.

Required vars:

```bash
USE_AWS=True
AWS_STORAGE_BUCKET_NAME=booknest-241304351285-eu-central-1-an
AWS_S3_REGION_NAME=eu-central-1
AWS_ACCESS_KEY_ID=<your_access_key_id>
AWS_SECRET_ACCESS_KEY=<your_secret_access_key>
```

For local testing, these can also be set in `env.py`.

## 4. Django Integration in This Repo

S3 integration is already implemented in project code.

## 4.1 Settings Toggle and S3 URL Mapping

In `booknest/settings.py`:

- `USE_AWS` controls whether S3 backends are used.
- S3 env vars are read with `os.environ.get(...)`.
- `AWS_S3_CUSTOM_DOMAIN` is built as:
  - `<bucket>.s3.<region>.amazonaws.com`
- URLs are set to:
  - `STATIC_URL = https://<custom-domain>/static/`
  - `MEDIA_URL = https://<custom-domain>/media/`

When `USE_AWS` is not `True`, local storage is used:

- static: `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- media: `MEDIA_ROOT = BASE_DIR / 'media'`


## 4.2 Storage Backends

A custom storage is created just like ADO Botique project repository.
The `storages` package is used to implement S3 storage backends for static and media files.

In `custom_storages.py`:

- `StaticStorage(S3Boto3Storage)` uses `location = settings.STATICFILES_LOCATION`
- `MediaStorage(S3Boto3Storage)` uses `location = settings.MEDIAFILES_LOCATION`

## 4.3 Media Upload Path

In `books/models.py`:

- `Book.cover_image` is `ImageField(upload_to="books/")`
- Stored object path pattern: `media/books/<filename>`

On s3 bucket this would be stored as `media/books/<filename>`.

## 5. Final Validation Flow (Manual test to confirm S3 integration)

This is the final end to end test that has already been performed successfully.

1. Added AWS environment variables in local `env.py`.
2. Ran:

```bash
python manage.py collectstatic
```

3. Opened AWS Console and confirmed static files were uploaded to the S3 bucket.
   Useing aws console: S3 -> bucket -> static/ and /media/ to verify files exist.
4. Loaded localhost pages.
5. Verified in browser DevTools that book images are served from S3 media URLs.

Example media URL observed:
- `https://booknest-241304351285-eu-central-1-an.s3.eu-central-1.amazonaws.com/media/books/pranayam.webp`

6. Confirmed IAM Access keys page last-used status to verify the correct key and region are being used.

## 6. Troubleshooting Quick Checks

- If static files are missing in S3:
  - verify `USE_AWS=True`
  - verify bucket/region vars are correct
  - run `python manage.py collectstatic` again
- If media does not load:
  - verify bucket policy includes `media/*`
  - verify CORS includes local origin during development
  - verify `Book.cover_image` object path exists in S3
- If IAM key usage is unclear:
  - check IAM -> User `booknest-bucket` -> Access keys -> Last used
  - confirm recent timestamp and `eu-central-1`

## 7. Security Notes

- Never commit real AWS secrets to Git.
- Store secrets only in Heroku config vars (or secure secret manager).
- Keep IAM user console access disabled when only API access is needed.
