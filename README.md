# eCommerce Project API

## Overview

This project is an API for an eCommerce system, designed to manage customers, products, orders, and authentication. It is built with **Flask**, using **SQLAlchemy** for database management, **JWT** for user authentication, and **Swagger** for documentation.

## Features

- **User Authentication**: Secure login using JWT tokens with role-based access.
- **Customers**: CRUD operations for managing customer information.
- **Products**: CRUD operations for managing product inventory.
- **Orders**: Create and retrieve customer orders.
- **Swagger Documentation**: Comprehensive API documentation using Swagger UI.
- **Caching and Rate Limiting**: Performance improvements with caching and request limiting using **Flask-Caching** and **Flask-Limiter**.

## Requirements

- **Backend**: Python with Flask and SQLAlchemy for ORM.
- **Database**: MySQL.
- **Validation**: Marshmallow for schema validation.
- **Authentication**: JWT for secure token-based authentication.
- **API Documentation**: Swagger UI.
- **Performance**: Flask-Caching for caching and Flask-Limiter for rate limiting.
- **MySQL** (Database)
- **Marshmallow** (Schema validation)
- **JWT** (Authentication)
- **Swagger UI** (API documentation)
- **Flask-Caching** and **Flask-Limiter** (Performance enhancements)

## Installation

To run the project locally, follow these steps:

### Prerequisites

- Python 3.8+
- MySQL server

### Setup

1. **Clone the Repository**

2. **Create and Activate Virtual Environment**

3. **Install Dependencies**

4. **Configure Database**

   - Update the database configuration in `application/config.py` to match your MySQL setup:

5. **Create Database Tables**
   Run the following command to create all required tables:

6. **Run the Application**

   The API will be available at `http://127.0.0.1:5000`.

## Endpoints

- **Authentication**
  - `POST /auth/login`: Authenticate and retrieve a JWT token.
- **Customers**
  - `GET /customers`: Retrieve a list of all customers (Requires JWT with admin role).
  - `POST /customers`: Create a new customer (Requires JWT with admin role).
  - `GET /customers/{id}`: Retrieve a specific customer by ID (Requires JWT with admin role).
  - `PUT /customers/{id}`: Update customer information (Requires JWT with admin role).
  - `DELETE /customers/{id}`: Delete a customer (Requires JWT with admin role).
- **Products**
  - `GET /products`: Retrieve a list of all products.
  - `POST /products`: Create a new product (Requires JWT with admin role).
  - `GET /products/{id}`: Retrieve a product by ID.
  - `PUT /products/{id}`: Update product information (Requires JWT with admin role).
  - `DELETE /products/{id}`: Delete a product (Requires JWT with admin role).
- **Orders**
  - `GET /orders`: Retrieve a list of all orders.
  - `POST /orders`: Create a new order.

## Authentication

This API uses JWT tokens for authentication. To access protected endpoints:

1. **Login** using `/auth/login` to receive a JWT token.
2. **Include the Token** in the request header for subsequent requests:

## Swagger Documentation

Swagger documentation is available for easy exploration and testing of the API endpoints. After running the app, you can visit:

## Testing

Unit tests are provided for customer and product routes. To run the tests:

## Performance Improvements

- **Caching**: `Flask-Caching` is used to cache GET requests for frequently accessed data.
- **Rate Limiting**: `Flask-Limiter` is used to limit each client to 100 requests per day per endpoint to prevent abuse.

## Project Structure

- `app.py`: Main entry point for the application.
- `application/`: Contains configuration, caching, and other utility files.
- `customers/`, `products/`, `orders/`, `customer_accounts/`: Contain blueprints, controllers, and services for each entity.
- `tests/`: Unit tests for the API.
- `static/swagger.yaml`: Swagger documentation for the API.

## Future Enhancements

- Add pagination to customer, product, and order lists.
- Improve error handling and add custom error messages.
- Implement user registration and role management.

## Author

Kelsea Conrad

