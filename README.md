# Simple Blog

A Flask-based blogging platform that makes it easy to create and share your thoughts. With features like user authentication, post management, and a commenting system.

## Table of content

- [Overview](#overview)
- [Features](#Features)
- [Built With](#built-with)
- [Getting Started](Getting-Started)
- [FutureEnhancements](#Future-Enhancements)
- [Acknowledgments](#Acknowledgments)
- [Author](#Author)


## Overview

[Simple Blog](https://simpleblog-l09c.onrender.com/) is a web application designed for creating and sharing blog posts on various topics. It provides a platform for users to express their thoughts, read content from others, and engage in discussions through comments. This project serves as a learning experience in full-stack web development, particularly focusing on Flask microframework and RESTful API design.

## Features
### Current Features

##### User Authentication

* Account creation with email verification
* Secure login and logout functionality
* Password reset capability


##### Blog Post Management

* Create, read, update, and delete blog posts

##### Commenting System

* Add comments to blog posts
* delete own comments

##### User Profiles

* Customizable user profiles

##### RESTful API

* API for data retrieval and manipulation
JWT authentication for secure API access


I developed an internal RESTful API for this web application for programmatic access to its features. All endpoints are prefixed with /api/v1. The API uses JSON for request and response bodies. 
Description of each endpoint:


* Authentication

  * POST /api/v1/login

        Authenticates a user and returns a JWT token
        Request body: { "username": "string", "password": "string" }
        Response: { "token": "string", "user_id": "integer" }


* Users

    * POST /api/v1/users

            Creates a new user
            Request body: { "username": "string", "email": "string", "password": "string" }
            Response: { "id": "integer", "username": "string", "email": "string" }


    * GET /api/v1/users/user_id

            Retrieves a specific user's information
            Response: { "id": "integer", "username": "string", "email": "string"}


    * PUT /api/v1/users/user_id

            Updates a user's information
            Request body: { "username": "string", "email": "string" }
            Response: { "id": "integer", "username": "string", "email": "string"}


    * DELETE /api/v1/users/user_id
    
            Deletes a user
            Response: {}



* Posts

    * GET /api/v1/users/<user_id>/posts

            Retrieves all posts of a particular user
            Query parameters: page (default: 1), per_page (default: 5)
            Response: { "posts": [...], "total": "integer", "pages": "integer", "current_page": "integer" }


    * POST /api/v1/users/<user_id>/posts
            
            Creates a new post for a user
            Request body: { "title": "string", "content": "string" }
            Response: { "id": "integer", "title": "string", "content": "string", "created_at": "datetime" }

    * GET /api/v1/posts
            
            Retrieves all posts (with pagination)
            Query parameters: page (default: 1), per_page (default: 10)
            Response: { "posts": [...], "total": "integer", "pages": "integer", "current_page": "integer" }



    * PUT /api/v1/posts/<post_id>
        
        Updates a post
        Request body: { "title": "string", "content": "string" }
        Response: { "id": "integer", "title": "string", "content": "string"}


    * DELETE /api/v1/posts/<post_id>
            
            Deletes a post
            Response: { "message": "Post deleted successfully" }



* Comments

    * GET /api/v1/posts/<post_id>/comments
            
            Retrieves comments for a post (with pagination)
            Query parameters: page (default: 1), per_page (default: 10)
            Response: { "comments": [...], "total": "integer", "pages": "integer", "current_page": "integer" }


    * POST /api/v1/posts/<post_id>/comments
            
            Creates a new comment on a post
            Request body: { "content": "string" }
            Response: { "id": "integer", "content": "string", "author": { "id": "integer", "username": "string" }, "created_at": "datetime" }


    * GET /api/v1/posts/<post_id>/comments/<comment_id>

            Retrieves a specific comment
            Response: { "id": "integer", "content": "string", "author": { "id": "integer", "username": "string" }, "created_at": "datetime" }


    * DELETE /api/v1/posts/<post_id>/comments/<comment_id>
        
        Deletes a comment
        Response: {}


- Note: All endpoints except /login and GET /posts require authentication. Include the JWT token in the Authorization header as `Bearer <token>`.


## Built With

### Tools
![Blog Stack](https://i.postimg.cc/T1QwnRDD/blog-stack.png)


### Architecture

[![architecture.png](https://i.postimg.cc/htnX65Sv/architecture.png)](https://postimg.cc/Vd7sb40P)


## Getting Started

To see the application in action, visit https://simpleblog-l09c.onrender.com/.

#### Local Installation

##### Clone the repository:
https://github.com/EmmanuelNiyonshuti/SimpleBlog/tree/master

##### Set up a virtual environment (optional but recommended):
`python3 -m venv venv`

`source venv/bin/activate` 
On Windows use `venv\Scripts\activate`

##### Install dependencies:
`install -r requirements.txt`

##### Set up a local database:

Install MySQL or PostgreSQL on your local machine if you haven't already.
Create a new database for the application.


##### Set up environment variables:
Create a .env file in the root directory and add the following:
`DATABASE_URL=your_local_database_url`
`SECRET_KEY=your_secret_key`
Replace your_local_database_url with your local database connection string. For example:

For MySQL: `mysql+pymysql://username:password@localhost/database_name`
For PostgreSQL: `postgresql://username:password@localhost/database_name`

Replace your_secret_key with a secure secret key for your local development.
##### Initialize the database:
db upgrade

#### Run the application:
`python3 run.py`
Alternatively, you can use `flask run` after setting the `FLASK_APP environment variable:

On Unix-based systems:

`export FLASK_APP=run.py`

`flask run`

On Windows:

`set FLASK_APP=run.py`

`flask run`

Note:
Make sure you have Python 3.x and pip installed on your system before starting the installation process.
The demo uses a database hosted on Render. For local development, you'll be using your own local database configured.

## Future Ehancement
Looking ahead, this web app has several key enhancements planned: incorporating Markdown support and a rich text editor for better content creation, implementing third-party login options and two-factor authentication, adding features like post liking, user following, and a notification system, developing an admin panel with moderation tools and msy be some analytics, optimizing performance with caching and efficient database queries, and enhancing SEO with meta tags and better URL structures. I'm always open to feedback and new ideas! If you have suggestions or would like to collaborate, please reach out.


## Acknowledgments

* Corey Schafer's Flask Tutorial Series for providing the initial inspiration and learning resources.

* The Flask and Python communities for their excellent documentation and support.


## Author
### **Emmanuel Niyonshuti**

Emmanuel is a passionate full-stack software engineering student with a keen interest in creating products that connect and empower others. Simple Blog represents his journey in learning web development and his commitment to building practical, user-centric applications.

[Github](https://github.com/EmmanuelNiyonshuti)
[LinkedIn](https://www.linkedin.com/in/niyonshuti-emmanuel-82877b285/)
[Twitter](https://x.com/NIYONSH77028058)


