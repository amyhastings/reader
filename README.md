# reader. A Community for Book Lovers

## Overview
**reader.** is a web application designed for book lovers to discover, review, and discuss their favourite reads. **reader.** is an application for people who read for fun to allow them to journal their reading experience and engage with like-minded people. The emphasis of the app is on reading for pleasure not obligation. Unlike other apps focussing on achievement of targets and progress tracking, **reader.** allows users to keep private notes on books they have read or want to read. 

This web application comprises my project for Module 6: Final Project of UCD's 24-03 Full-Stack Software Development Course. The objective of the project is as follows:

> Develop a full-featured web application using Django ... The key is to ensure proper integration between frontend and backend, manage the database effectively, and deploy the application while demonstrating strong communication and teamwork skills.

Please NOTE: the gitHub repository for this application at https://github.com/amyhastings/reader includes the python library, which allows for integration of the Open Library API. While this does not form part of the project submission, it was included in the submission for simplicity and in the interests of completeness. 

## Features
- **Personal Book Journal** - Users can privately track books that they have read, are reading or want to read, as well as making notes on books.
- **Search & Discover** - Search millions of books through the Open Library API.
- **Recommendations** - Users can recommend the books that they loved.
- **Discussion Forums** - Engage in book discussions, themed chats, and genre-based conversations.

## Tech Stack
- **Backend**: Django 
- **Frontend**: HTML, CSS, Javascript
- **Database**: PostgreSQL

## APIs Used in the Web Application
- Open Library API
- Cloudinary

## Installation & Setup
A version of the website is deployed here: https://reader.ie/. To view this website off-line and/or make changes:
- clone the gitHub repository at https://github.com/amyhastings/reader;
- pip install -r requirements.txt;
- go to https://cloudinary.com; generate a cloud name, API key and API secret key; edit the .env file;
- source the .env file;
- run the following commands: python manage.py migrate ; python manage.py collectstatic ; python manage.py ensure_adminuser;
- in the terminal, launch the application python manage.py runserver;
- to test the reset password functionality, generate a Google email application password and edit the corresponding fields in the .env file.

### Licensing
This web application is the copyright of Amy Hastings. The Open Library API is integrated into the website to allow for book searches. The photographs for profile pictures were sourced from https://www.pexels.com. The default image used when the user has not uploaded their own profile picture was sourced from	https://www.freepik.com. Special thanks to Christian Kelly for information on how to go about creating a python library.
