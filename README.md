# Book Nest
BookNest is a full-stack ecommerce web application developed using the Django framework. The platform enables users to browse, search, review, and purchase books through a secure and user-friendly online shopping experience. The application follows a Business-to-Customer (B2C) ecommerce model and provides both customer-facing features and administrative product management tools.

The primary objective of BookNest is to provide readers with an intuitive online bookstore where they can easily discover books, manage their shopping cart, securely complete purchases using Stripe, and review previously purchased books. Administrators can efficiently manage the store inventory through dedicated product management functionality.

The project was developed following Agile principles using GitHub Projects, with development organised into Epics and User Stories. Throughout the development lifecycle, emphasis was placed on clean architecture, responsive design, secure authentication, payment processing, database integrity, and an improved user experience.


## Book Nest - Buissness Model

BookNest operates as a Business-to-Customer (B2C) ecommerce platform.

### The application enables customers to:

Browse and search books
View detailed book information
Add books to a shopping cart
Securely complete purchases
View previous orders
Submit and manage book reviews

### Store administrators can:

Add new books
Edit existing books
Delete books
Manage the online catalogue
Target Audience

BookNest has been designed for users who prefer purchasing books online through a simple and secure ecommerce platform.

### The primary target audience includes:

-  Students
- General readers
- Academic readers
- Book collectors
- Parents purchasing educational books
- Individuals seeking a convenient online bookstore experience

## Project Goals

The primary goals of BookNest are:

- Deliver a modern and responsive ecommerce experience.
- Provide secure user authentication and account management.
- Allow customers to browse books efficiently using search, filtering, and pagination.
- Enable secure online payments through Stripe.
- Allow customers to review purchased books.
- Provide administrators with complete product  management functionality.
- Demonstrate full-stack web development practices using Django and PostgreSQL.
- Implement cloud-based media storage using AWS S3.
- Apply SEO and digital marketing techniques to improve visibility and customer engagement.

## Marketing Strategy

### Search Engine Optimisation (SEO)

SEO is one of the primary marketing strategies for BookNest because many customers search online before purchasing books.

The following SEO practices have been implemented:

- Unique page titles.
- Descriptive meta descriptions.
- Semantic HTML structure.
- Image alternative (alt) text.
- Sitemap.xml.
- Robots.txt.
- Keyword-focused book descriptions.
- Mobile-responsive design.

These improvements increase BookNest's visibility within search engine results and improve the user experience.

### Content Marketing

BookNest benefits from content marketing by providing useful and informative content that attracts potential customers.

Examples include:

- Detailed book descriptions.
- Author information.
- Book reviews.
- Featured books.
- New arrivals.


This content helps customers make informed purchasing decisions while also improving SEO.

### Email Marketing

BookNest includes a newsletter subscription feature that allows visitors to receive updates about:

- New book releases.
- Seasonal promotions.
- Special discounts.
- Recommended books.
- Exclusive offers.

Email marketing helps encourage repeat purchases while maintaining customer engagement.

### Social Media Marketing

The primary social media platform selected for BookNest is Facebook.

A Facebook Business Page has been created to:

![booknest_facebook_page](screenshot/Webmarketting/facebook_mockup.png)

- Promote new book releases.
- Advertise seasonal offers.
- Share reading recommendations.
- Engage with customers.
- Build brand awareness.

Future expansion may include Instagram to showcase book covers, featured collections, and promotional campaigns through visual content.

### Promotional Campaigns

BookNest plans to increase customer engagement by offering:
![add_campigns_details](screenshot/Webmarketting/add_campign.png)

![add_campigns](screenshot/Webmarketting/marketting_campign.png)
- Featured book campaigns.
- Newsletter-exclusive offers.

![current_subscribers](screenshot/Webmarketting/newsletter_subscription_detailed.png)

![newslettr_mail](screenshot/User/newsletter_subscription.jpg)

These promotions encourage repeat customers and improve conversion rates.

### Paid Advertising

As a small ecommerce business, BookNest primarily focuses on low-cost marketing strategies.

Initial marketing efforts concentrate on:

- SEO.
- Organic social media.
- Email marketing.
- Customer reviews.

As the business grows, paid Facebook and Google advertising campaigns may be introduced to increase website traffic and sales.

### Why These Marketing Types?

The selected marketing strategies were chosen because they align with BookNest's target audience and business objectives.

Marketing Type	Benefit to BookNest
- SEO	Increases organic search visibility and website traffic.
- Content Marketing	Helps customers discover and - evaluate books before purchasing.
- Email Marketing	Encourages repeat customers through newsletters and promotions.
- Facebook Business Page	Builds brand awareness and customer engagement.
- Promotions & Discounts	Increases sales during seasonal campaigns.
- Customer Reviews	Builds trust and improves purchasing confidence.

### Marketing Goals

The primary marketing objectives for BookNest are:

- Increase organic website traffic.
- Improve search engine rankings.
- Encourage repeat purchases.
- Build customer trust through reviews.
- Grow the newsletter subscriber list.
- Increase customer engagement through social media.
- Establish BookNest as a trusted online bookstore.

### User Goals

BookNest has been designed to provide customers with a simple, secure, and enjoyable online shopping experience. The application enables users to discover books easily, make informed purchasing decisions, and manage their accounts through an intuitive interface.

- Browse available books by category.

![book_search_category](screenshot/User/search_isbn.png)
- Search for specific books quickly.
- View detailed book information before purchasing.

![book_details](screenshot/User/book_details.png)

- Add books to a shopping cart.

![cart_details](screenshot/User/user_cart.png)

- Complete purchases securely using Stripe.

![payment](screenshot/User/payment.png)

![payment_Success](screenshot/User/payment_success_oredr_details.png)

- Create an account and manage personal information.
- View previous orders.

![user_oreder_history_status](screenshot/User/user_oreder_history.png)
- Submit and manage book reviews.

![Add_book_review](screenshot/User/add_review.png)

![manage_review](screenshot/User/manage_review.png)

- Receive updates through the newsletter.

![newslettr_mail](screenshot/User/newsletter_subscription.jpg)


### Site Owner Goals

The primary objective of BookNest is to provide an efficient ecommerce platform that supports both customers and store administrators.

 The application is designed to increase book sales, improve customer engagement, and provide simple product management tools while maintaining a secure and scalable system.

- Sell books through an online ecommerce platform.

- Provide a secure checkout process.
- Increase customer engagement through reviews and newsletters.
- Promote books through digital marketing.
- Improve search engine visibility using SEO.
- Maintain the catalogue using product management features.
- Deliver a responsive shopping experience across all devices.

## Tech Stack

### Backend

- Django (Python)
- Python 3
- Gunicorn (Production WSGI Server)

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript (ES6)

### Database

- PostgreSQL
- DBeaver (Database Management Tool)

### Authentication

- Django Authentication System
- Django Allauth (Registration, Login, Logout, Email Verification)

### Payment Processing

- Stripe API
- Stripe Payment Intents
- Stripe Webhooks

### Cloud Storage

- Amazon Web Services (AWS S3)
- django-storages
- boto3

Used to store and serve static files (CSS, JavaScript, images) and media files (book cover images) in the production environment.

### Development Tools

- Visual Studio Code *(or PyCharm if you used it)*
- Git
- GitHub
- Heroku
- AWS Management Console
- Stripe Dashboard
- Chrome DevTools

## Database
The application uses PostgreSQL as the primary database in production, providing better performance, scalability, and reliability compared to SQLite.

### Development and Production
• Development: SQLite (default Django database for simplicity)

• Production: PostgreSQL (via Heroku Postgres)
Configuration

Database settings are defined in config/settings.py and are read from environment variables. This lets you keep sensitive credentials out of the repository and makes it easy to configure the application on hosting platforms like Heroku via config vars. Example database configuration from 
settings.py:

import os

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB_NAME"),
        "USER": os.environ.get("POSTGRES_DB_USERNAME"),
        "PASSWORD": os.environ.get("POSTGRES_DB_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_DB_HOST"),
        "PORT": "5432",
        'OPTIONS': {'sslmode': 'require'},
    }
}

## Django Apps

### Book
Book listing and details. Book categories and search functionality. Book reviews and ratings.
Manage book inventory and stock levels.

### cart
Online shopping cart functionality. Add, remove, and update book quantities. Cart summary and total price calculation.

### checkout
Checkout process with payment integration. Order summary and confirmation. Promo code application and discounts. Delivery address management.

### home
Home page with featured books, new arrivals, and bestsellers. Search functionality and book categories.

### marketing
Newsletter subscription, promotional banners, and special offers. Book reviews and ratings.

### profiles
User profiles and authentication. Personal information, Delivery address, order history, and account settings.





## Wireframe
### Home Page
![Homepage_and_BookCataloge_page](booknest_wireframe/Home.png)
### Cart Page and Payment Success
![payment_page](booknest_wireframe/checkout.png)
![cart_page](booknest_wireframe/add_cart.png)
### chekout Page
![checkout_page](booknest_wireframe/payment_successfull.png)
### Selected Book with Review
![review_page_and_selected_book](booknest_wireframe/selected_book_details.png)
### Newsletter subscription
![newsletter_subscription](booknest_wireframe/newsletter.png)
### User Profile
![userprofile_details](booknest_wireframe/userprofile.png)
### Signout
![signout](booknest_wireframe/signout.png)


## Agile Methodology

BookNest was developed using an Agile methodology for creating userstories, with project planning and progress managed through GitHub Projects. Development was organised into Epics, User Stories, Bugs, and Tasks, allowing features to be implemented incrementally while maintaining clear project organisation throughout the software development lifecycle.

To prioritise development, the MoSCoW prioritisation technique was used. Each User Story was assigned one of the following labels:

- Must Have – Essential functionality required for the minimum viable product (MVP).
- Should Have – Important features that significantly improve the user experience but are not critical for the initial release.
- Could Have – Desirable enhancements that add value if development time permits.

Each issue progressed through the following workflow:

- To Do
- In Progress
- Done

This structured approach enabled continuous development, frequent commits, regular testing, effective bug tracking, and incremental delivery of new features throughout the project.

## Installation

1. Clone the Repository

git clone https://github.com/your-username/booknest.git
cd booknest

2. Create Virtual Environment

python -m venv venv
source venv/bin/activate

 On Windows: venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

4. Apply Migrations

python manage.py migrate

5. Create Superuser

python manage.py createsuperuser

6. Run the Server

python manage.py runserver
Visit: http://127.0.0.1:8000/

## Testing With Validators
![sign_in](screenshot/Authentication/sign_in.png)
![sign_up](screenshot/Authentication/sign_up.png)