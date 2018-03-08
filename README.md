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
- Front-End
    - Contact Us
    
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
## Content Used
### Sources
- [Django Documentation](https://docs.djangoproject.com/en/1.11/)
    - I have used the **Django** documentation files to look up support when stuck with a certain aspect of the framework.
- [stack overflow](https://stackoverflow.com)
    - **stack overflow** is always invaluable at providing support when struggling to implement a new feature or fix a bug.
    - [This](https://stackoverflow.com/a/48167311/9429543) post helped me understand how to implement a Django's built-in password change form with my own website design without having to start from scratch.
    - [This](https://stackoverflow.com/a/15400806/9429543) post helped me understand how to disable dates in the datepicker that clients had already booked.
    - [This](https://stackoverflow.com/questions/3798812/how-to-compare-dates-in-django) post helped me better understand the property decorator in Django, where to use it and how to implement it to disable users changing dates that have already passed.
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

## Key Information
- When attempting to process a transaction from the services page to check the website funcionality please use the following details:
    - Card Number - 4242424242424242
    - CVV - Any three digit number
    - Expiry - Any date in the future
## Please view the website on the link below
Link will be provided on project completion.