**Forum Backend with FastAPI**

Project Description:
This project aims to create a robust Forum System backend using FastAPI, offering a modern RESTful API for various client applications.

**High-level description:**

The system allows users to create and view topics, exchange messages, and manage user-related activities, while administrators oversee users, topics, and categories.

## **Rest assured, the API meets modern standards and offers a comprehensive set of functionalities, including:**



**Register User** 
- Accepts user registration data
- Consider making at least one user property unique for login purposes.

```http
POST /users/register HTTP/1.1
Host: 127.0.0.1:8001

JSON body:

{
    "username": "name",
    "password": "password",
    "first_name": "first_name",
    "last_name": "last_name",
    "email": "samplemail@someting.com",
    "date_of_birth": "1986-02-15"
}
```


**Create Topic** 
-	Requires authentication token
-	Topic data must contain at least a title and a Category
  ```http
  POST /topics/{category_id} HTTP/1.1
  Host: 127.0.0.1:8001

JSON body:


{
    "title": "Sample title"
}
```

**Create Reply** 
- Requires authentication token
- Reply data should contain at least text and is associated with a specific Topic.

```http
POST /replies/categories/{category_id}/topics/{topic_id} HTTP/1.1
Host: 127.0.0.1:8001

JSON body:

{
    "content": "Sample content"
}
```

**View Topics** 
- Responds with a list of Topic resources.
- Consider adding search, sort, and pagination query params.

Query Parameters:

search: Allows searching for topics by keyword.
sort: Allows sorting topics by certain criteria.
page: Specifies the page number for pagination.
limit: Specifies the maximum number of topics per page.
```http
GET /topics?sort=&page=1&limit=10 HTTP/1.1
Host: 127.0.0.1:8001

Query Parameters:

search: Allows searching for topics by keyword.
sort: Allows sorting topics by certain criteria.
page: Specifies the page number for pagination.
limit: Specifies the maximum number of topics per page.

```

**View Topic** 
- Responds with a single Topic resource and a list of Reply resources.

```http
GET /topics/categories/{category_id}/{topic_id} HTTP/1.1
Host: 127.0.0.1:8001
```

**View Category**
- Responds with a list of all Topics that belong to that Category.
- Consider adding search, sort, and pagination query params.

  ```http
  GET /categories/{category_id}/topics HTTP/1.1
  Host: 127.0.0.1:8001
  Query Parameters:

    search: Allows searching for topics by keyword.
    sort: Allows sorting topics by certain criteria.
    page: Specifies the page number for pagination.
    limit: Specifies the maximum number of topics per page.

**View Categories**
- Responds with a list of all Categories.

  ```http
  GET /categories HTTP/1.1
  Host: 127.0.0.1:8001
Note:

If you are an admin, you can view all the categories, whether they are private or not.
If you are not an admin, you can view all the categories except the private ones if you do not have access.
Copy code

**Create Message**
- Requires authentication.
- Creates a Message, which should contain at least text as a property.
- Messages should be addressed to a specific user.

  ```http
  POST /messages HTTP/1.1
  Host: 127.0.0.1:8001

    JSON body:
    {
    "content": "Sample message",
    "receiver_id": 1
    }

    JSON response:
    
    {
    "Message content": "Sample message",
    "Sent at": "12/05/2024",
    "Sent to": "gosho123"
    }

**View Conversation**
- Requires authentication.
- Responds with a list of Messages exchanged between the authenticated user and another user.

  ```http
  GET /messages/{user_id} HTTP/1.1
  Host: 127.0.0.1:8001

    JSON response:
    {
        "id": 7,
        "content": "Sample message",
        "sender_id": 16,
        "receiver_id": 1,
        "created_at": "2024-05-12 13:42:25"
    }

**View Conversations**
- Requires authentication.
- Responds with a list of all Users with whom the authenticated user has exchanged messages.

  ```http
  GET /messages HTTP/1.1
  Host: 127.0.0.1:8001

    JSON response:
    [
    "Outbox:'gosho123'",
    "Inbox: []"
    ]

**Upvote/Downvote a Reply**
- Requires authentication.
- A user should be able to change their downvotes to upvotes and vice versa, but a reply can only be upvoted/downvoted once per user.

  ```http
  PUT /replies/categories/{category_id}/topics/{topic_id}/vote/{reply_id} HTTP/1.1
  Host: 127.0.0.1:8001

    Request body(Upvote):
    {
    "vote": 1
    }
    JSON response(Upvote):
    "You like this reply!"

    Request body(Downvote):
    {
    "vote": 0
    }
    JSON response(Downvote):
    "You hate this reply!"

**Choose Best Reply**
-	Requires authentication
-	Topic Author can select one best reply to their Topic
    ```http
    PUT /topics/{topic_id}/replies/{reply_id} HTTP/1.1
    Host: 127.0.0.1:8001

### **SHOULD REQUIREMENTS**

**Create Category**
- Requires admin authentication.
- Category data should contain at least a name.

  ```http
  POST /categories HTTP/1.1
  Host: 127.0.0.1:8001

  Request body:

  {
    "title": "Sample title"
  }   
  
Note: Only admins can create categories. The category name must be provided in the request body.

**Make Category Private / Non-private**
- Requires admin authentication.
- Changes visibility to a category and all associated topics.
- Topics in a private category are only available to category members.

  ```http
  PUT /categories/{category_id}/visibility HTTP/1.1
  Host: 127.0.0.1:8001

  Request body(to make private):
  {
    "visibility": 1
  }

  Response(if successful):
  {
    "message": "Category is changed to private"
  }

  Request Body (to make non-private):
  {
    "visibility": 0
  }

  Response (if successful):
  {
    "message": "Category can be seen from all users"
  }

**Give User a Category Read Access**
- Requires admin authentication.
- Grants a user read access to all topics and replies in the specific private category.

  ```http
  POST /categories/{category_id}/users/{user_id}/read HTTP/1.1
  Host: 127.0.0.1:8001

  Response (if successful):
  {
    "message": "Read access granted to user 16."
  }

**Give User a Category Write Access**
-	Requires admin authentication
-	A user can now view all Topics and Replies in the specific private Category and post new Topics and Replies

  ```http
  POST /categories/{category_id}/users/{user_id}/write HTTP/1.1
  Host: 127.0.0.1:8001

  Response (if successful):
  {
    "message": "Read & write access granted to user 16."
  }

**Revoke User Access**
-	Requires admin authentication
-	A user loses their read or write access to a category

  ```http
  PUT /categories/{category_id}/users/{user_id}/revoke HTTP/1.1
  Host: 127.0.0.1:8001
  Revoke read:
  {
    "revoke_read": true,
    "revoke_write": false 
  }
  Response (if successful):
  {
    "message": "User removed completely from the category."
  }
  Revoke write:
  {
    "revoke_read": false,
    "revoke_write": true
  }
  Response (if successful):
  {
    "message": "Access rights updated successfully."
  }
  ```


**View Privileged Users**
- Requires admin authentication.
- Responds with a list of all users for a specific Private Category along with their Access Level.

  ```http
  GET /categories/{category_id}/privileged-users HTTP/1.1
  Host: 127.0.0.1:8001
  JSON Response:
  {
    "category_id": 8,
    "users": [
        {
            "username": "ikonata",
            "can_read": 1,
            "can_write": 1
        }
    ]
  }

**Lock Category**
- Requires admin authentication.
- Once locked, a Category can no longer accept new Topics.

  ```http
  PUT /topics/lock/{category_id} HTTP/1.1
  Host: 127.0.0.1:8001
  JSON Response:
  "Category has been locked!"

Note: Only admins have the authority to lock categories. Once locked, the category cannot be modified until it's unlocked.
**Lock Topics**
- Requires admin authentication.
- Once locked, a category can no longer accept new Topics.

**If Not Admin:**
  ```http
  PUT /topics/lock/{topic_id} HTTP/1.1
  Host: 127.0.0.1:8001
  JSON Response:
  "You are not authorized!"
```
**If Admin:**
```http
PUT /topics/lock/{topic_id} HTTP/1.1
Host: 127.0.0.1:8001
JSON Response:
"Topic has been locked!"
```


## **Required Packages**
To run this project, you need to install the following packages:

- `fastapi`: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- `passlib`: A password hashing library for Python 2 & 3, which provides cross-platform implementations of over 30 password hashing algorithms.
- `jose`: A JavaScript Object Signing and Encryption (JOSE) library for Python, which allows you to encode and decode JSON Web Tokens (JWT).
- `mariadb`: A Python client library for MariaDB/MySQL, which allows Python programs to connect to a MariaDB or MySQL database.
- `pydantic`: Data validation and settings management using Python type annotations.
- `starlette`: A lightweight ASGI framework/toolkit, which is ideal for building high-performance asyncio services.
- `pytest`: A framework that makes it easy to write simple tests.

You can install these packages using pip:

```bash
pip install fastapi passlib jose mariadb pydantic starlette pytest pytest-aiohttp pytest-asyncio httpx 
