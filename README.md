# Project Documentation

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
   1. [Login](#login)
   2. [Authorization](#authorization)
3. [Data Operations](#operations)
   1. [Add Data](#add)
4. [Technology Stack](#technology)

## The API can be accessed [here](https://backend-cdp-407c9642e80d.herokuapp.com/)

## Overview<a name="overview"></a>

This document provides information about the RESTful API implementation, including authentication and data operations. The API utilizes Flask, a micro web framework for Python, and is integrated with MySQL for data storage. Deployment is handled through Heroku. The Flask extensions used include Flask-RESTX, Flask-SQLAlchemy, Flask-Bcrypt, and Flask-JWT-Extended.

## Authentication<a name="authentication"></a>

### Login<a name="login"></a>

To access protected operations, users must authenticate via the Auth operation. A user logs in with a POST request to /auth/login:

```json
{
  "username": "example",
  "password": "example"
}
```

If successful, the API responds with a JSON Web Token (JWT) for subsequent authorization:

```json
{
  "status": 200,
  "message": "Login successful",
  "data": {
    "token": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...."
  }
}
```

### Authorization<a name="authorization"></a>

The token obtained during login must be included in the Authorization header for protected data operations. For example:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9....
```

## Data Operations<a name="operations"></a>

### Add Data<a name="add"></a>

To add data, users send a POST request to /data with the required fields:

```json
{
  "source": "example",
  "sentiment": "example",
  "text": "example"
}
```

If successful, the API responds with details about the created data, including user information who owns the data:

```json
{
  "status": 201,
  "message": "Data created successful",
  "data": {
    "id": 1,
    "source": "example",
    "sentiment": "example",
    "text": "example",
    "created_date": "2023-12-14T00:37:26.199567",
    "user": {
      "id": 1,
      "username": "example"
    }
  }
}
```

## Technology Stack<a name="technology"></a>

- **Flask**: Micro web framework for Python.
- **Flask-RESTX**: Extension for quickly building REST APIs.
- **Flask-SQLAlchemy**: Flask extension for SQLAlchemy, a SQL toolkit and Object-Relational Mapping (ORM) library.
- **Flask-Bcrypt**: Flask extension for Bcrypt hashing.
- **Flask-JWT-Extended**: Flask extension for JSON Web Token (JWT) support.
- **MySQL**: Relational database management system.
- **Heroku**: Cloud platform for deployment.

This API provides secure access to data operations through token-based authentication. The combination of Flask, MySQL, and associated extensions facilitates the implementation of a robust and scalable RESTful API. Deployment on Heroku ensures accessibility and reliability.
