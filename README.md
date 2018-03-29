# BCM Training and Consultancy
## Overview
### What is this website for?
This website is for a company that offers training and consultancy services for care agencies that provide Domiciliary Care. 
### What does it do?
Allows care agencies to learn more about BCM, sign up to book onto open group / private courses and to arrange consultancy meetings. The account functionality allows care agencies to review and amend booking through their user portal. They can also message BCM directly and leave testimonials.
### How does it work?
The site is built using the powerful Django framework to manage all of the back-end, create the models and SQL database and route the site to the different pages and views. Bootstrap and JS are used to create a responsive, modern front-end experience.
## Features
### Existing Features
- Front-End
    - Index / Template Page
    - Home Page
    - Our Services Page
    - Testimonials
    - Contact Us
    - Register / Login / Logout
    - User-Authenticated Pages
        - Booking Training Packages
        - Arranging Consultancy Meetings
        - Account
- Back-End
    - Databases
        - User
        - Packages Available
        - Testimonials
        - Order History
    - Stripe Integration
### Features Left to Implement
- Password Reset Form
## Tech Used
### The Tech Used Includes:
- [Bootstrap](http://getbootstrap.com/)
    - I use **Bootstrap** to give my project a simple, tidy and mobile friendly responsive layout.
- [Django](https://www.djangoproject.com)
    - I use **Django** as the backbone of the whole website. It manages the back-end, helps share content and database entries with the front-end and controls which views are shown depending on the current URL.
- [SQLite](https://sqlite.org)
    - I use **SQLite** which comes bundled with **Django** to store all of my data in a SQL database.
- [Stripe](https://stripe.com/gb)
    - **Stripe** is used to safely and securely handle payments from customers.
- [jQuery](http://jquery.com)
    - **jQuery** is used to simplify the use of Javascript and works in conjunction with **Bootstrap**.
- [DataTables](https://datatables.net/index)
    - I have used the **DataTables jQuery** plugin to allow powerful user control over how they view their data in the order history table in accounts.
- [django-recaptcha](https://github.com/praekelt/django-recaptcha)
    - I installed this Django Package to simplify implementing Google's noCAPTCHA reCAPTCHA mechanism for preventing bots in a modern, proven way.
- [SendGrid](https://sendgrid.com)
    - I use **SendGrid** to deliver my password reset emails to the users.
## Content Used
### Sources
- [Django Documentation](https://docs.djangoproject.com/en/1.11/)
    - I have used the **Django** documentation files to look up support when stuck with a certain aspect of the framework.
- [stack overflow](https://stackoverflow.com)
    - **stack overflow** is always invaluable at providing support when struggling to implement a new feature or fix a bug.
    - [This](https://stackoverflow.com/a/48167311/9429543) post helped me understand how to implement a Django's built-in password change form with my own website design without having to start from scratch.
    - [This](https://stackoverflow.com/a/15400806/9429543) post helped me understand how to disable dates in the datepicker that clients had already booked.
    - [This](https://stackoverflow.com/questions/3798812/how-to-compare-dates-in-django) post helped me better understand the property decorator in Django, where to use it and how to implement it to disable users changing dates that have already passed.
    - [This](https://stackoverflow.com/a/16143864/9429543) post helped me to implement tests for views where the built in messages module is used.
- [WhiteNoise Documentation](http://whitenoise.evans.io/en/stable/)
    - I used this to see how to properly implement WhiteNoise to help deliver my staticfiles.
- [Responsive Google Maps Embed](https://www.labnol.org/internet/embed-responsive-google-maps/28333/)
    - I used this trick to make the embedded Google Maps responsive to all screen sizes.
- [Responsive Recaptcha](https://geekgoddess.com/how-to-resize-the-google-nocaptcha-recaptcha/)
    - This page helped me to make the recaptcha responsive for smaller mobile devices.
- [SimpleIsBetterThanComplex](https://simpleisbetterthancomplex.com/tutorial/2016/09/19/how-to-create-password-reset-view.html)
    - This tutorial helped me understand how to use Django's built-in password reset views and urls with my own templates. It also helped me configure the settings for sending mail in Django using SMTP.
## Features Explained
- Accounts
    - A check is performed during registration to ensure that email does not already exist. Emails are also forced to lowercase as they are not case-sensitive and it makes checking the database for existing users easier.
    - Users are made aware of the password requirements when registering or altering their password.
    - Users can change date of any training or consultancies that they have previously booked and paid for as long as the date hasn't passed. This is done through simply selecting the relevant date on the order history table. Only dates not taken or in the past can be chosen.
    - Users can change their name, email and password through three separate links on the accounts page. Validation checks are performed on the entered data.
- Services
    - When purchasing a service the user is prevented from choosing dates from the past including today. They are also limited to days not already booked by themselves or other users.
- Testimonials
    - Users can add only one testimonial, which can be edited or deleted as necessary.
    - Care has been taken to only allow users to edit and delete their own testimonials (except if they are staff).
    - Users are prevented from creating more than one testimonial at any one time.
- Contact Us
    - This page shows the address and location of the business as well as a form to get in touch with the owner, including a recaptcha to prevent spam. The address and location on the map are fictional but would show accurate details in real world use. The form does not submit to anywhere at the current time but in real world use would be automatically compiled into an email to the owner using the django **send_mail** function. The form still contains validation and demonstrates to the user that it has been submitted successfully.
## Key Information
- When attempting to process a transaction from the services page to check the website funcionality please use the following details:
    - Card Number - 4242424242424242
    - CVV - Any three digit number
    - Expiry - Any date in the future
## Please view the website on the link below
<https://bcm-training.herokuapp.com>