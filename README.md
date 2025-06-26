# FastAPI Product Management API

A secure REST API built with FastAPI for user authentication and product management. Users can register, authenticate, and manage their own products with full CRUD operations.

## Features

- **User Authentication**: JWT-based authentication with username/password
- **User Registration**: Secure user account creation
- **Product Management**: Full CRUD operations for products
- **Bulk Operations**: Create multiple products at once
- **User Isolation**: Users can only access their own products
- **Database Integration**: SQLAlchemy with SQLite database
- **Automatic API Documentation**: Interactive API docs with Swagger UI

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM)
- **Pydantic**: Data validation using Python type annotations
- **JWT**: JSON Web Tokens for authentication
- **SQLite**: Lightweight database (can be easily changed to PostgreSQL/MySQL)

## Project Structure

```
FASTAPI/
├── app/
│   ├── main.py          # FastAPI application and routes
│   ├── models.py        # SQLAlchemy database models
│   ├── schemas.py       # Pydantic models for request/response
│   ├── crud.py          # Database operations
│   ├── auth.py          # JWT authentication utilities
│   ├── database.py      # Database configuration
│   └── deps.py          # Dependency injection utilities
├── venv/                # Virtual environment
└── README.md           # This file
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd FASTAPI
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic python-multipart python-jose[cryptography] passlib[bcrypt]
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### Authentication

#### Register User
```http
POST /register
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securepassword123"
}
```

#### Login
```http
POST /token
Content-Type: application/x-www-form-urlencoded

username=john_doe&password=securepassword123
```

#### Get Current User
```http
GET /me
Authorization: Bearer <access_token>
```

### Product Management

#### Create Product
```http
POST /products/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Sample Product",
  "description": "A sample product description",
  "image_url": "https://example.com/image.jpg"
}
```

#### List My Products
```http
GET /products/
Authorization: Bearer <access_token>
```

#### Update Product
```http
PUT /products/{product_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Updated Product Name",
  "description": "Updated description",
  "image_url": "https://example.com/new-image.jpg"
}
```

#### Delete Product
```http
DELETE /products/{product_id}
Authorization: Bearer <access_token>
```

#### Bulk Create Products
```http
POST /products/bulk
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "products": [
    {
      "name": "Product 1",
      "description": "Description 1",
      "image_url": "https://example.com/image1.jpg"
    },
    {
      "name": "Product 2",
      "description": "Description 2",
      "image_url": "https://example.com/image2.jpg"
    }
  ]
}
```

## Data Models

### User
- `id`: Primary key (auto-generated)
- `username`: Unique username (max 50 characters)
- `hashed_password`: Securely hashed password

### Product
- `id`: Primary key (auto-generated)
- `name`: Product name (max 100 characters)
- `description`: Optional product description (max 255 characters)
- `user_id`: Foreign key to User (required)
- `image_url`: Optional image URL (max 255 characters)

## Security Features

- **Password Hashing**: Passwords are hashed using bcrypt
- **JWT Authentication**: Secure token-based authentication
- **User Isolation**: Users can only access their own products
- **Input Validation**: All inputs are validated using Pydantic models

## Usage Examples

### Using curl

1. **Register a new user**
   ```bash
   curl -X POST "http://localhost:8000/register" \
        -H "Content-Type: application/json" \
        -d '{"username": "testuser", "password": "testpass123"}'
   ```

2. **Login and get token**
   ```bash
   curl -X POST "http://localhost:8000/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=testuser&password=testpass123"
   ```

3. **Create a product**
   ```bash
   curl -X POST "http://localhost:8000/products/" \
        -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"name": "My Product", "description": "A great product"}'
   ```

4. **List user's products**
   ```bash
   curl -X GET "http://localhost:8000/products/" \
        -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
   ```

### Using Python requests

```python
import requests

# Base URL
base_url = "http://localhost:8000"

# Register user
response = requests.post(f"{base_url}/register", json={
    "username": "testuser",
    "password": "testpass123"
})
print("Registration:", response.json())

# Login
response = requests.post(f"{base_url}/token", data={
    "username": "testuser",
    "password": "testpass123"
})
token = response.json()["access_token"]

# Create product
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(f"{base_url}/products/", 
                        headers=headers,
                        json={
                            "name": "Sample Product",
                            "description": "A sample product"
                        })
print("Product created:", response.json())

# List products
response = requests.get(f"{base_url}/products/", headers=headers)
print("My products:", response.json())
```

## Development

### Running in Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database

The application uses SQLite by default. The database file will be created automatically when you first run the application.

To use a different database (PostgreSQL, MySQL), modify the database URL in `app/database.py`.

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid input data
- **401 Unauthorized**: Invalid or missing authentication
- **404 Not Found**: Resource not found or not owned by user
- **422 Unprocessable Entity**: Validation errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For questions or issues, please open an issue on the GitHub repository. 