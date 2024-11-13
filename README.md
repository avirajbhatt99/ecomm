---

# Ecomm

Follow the steps below to set up the environment, install dependencies, and run the server locally.

## Prerequisites

- Python 3.11.6

---

## Setup & Installation

### 1. Clone the Repository

If you haven't already, clone the repository to your local machine:

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Set Up a Virtual Environment

It's recommended to use a virtual environment to manage your project's dependencies. Here's how to set it up:

- **Create a virtual environment**:

```bash
python3 -m venv .venv
```

- **Activate the virtual environment**:

  - On macOS/Linux:

    ```bash
    source .venv/bin/activate
    ```

### 3. Install Required Dependencies

Once the virtual environment is active, install the project dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Configure the `PYTHONPATH`

The `PYTHONPATH` should be set to the root directory of your project. Run the following command in the terminal to set it:

```bash
export PYTHONPATH=$(pwd)
```

This ensures that Python will correctly locate the source files.

## Running the Server

Once the environment is set up and the dependencies are installed, you can start the server with the following command:

```bash
python src/server.py
```

The server should now be running locally. You can access the API at `http://localhost:8000`.

---

## API Endpoints

This section provides an overview of the available API endpoints for your server.

### 1. Health Check

- **Endpoint**: `/v1/health`
- **Method**: `GET`
- **Description**: This endpoint is used to check the health of the server. It returns a success message if the server is up and running.

#### Request:

```http
GET /v1/health
```

#### Response:

```json
{
  "message": "Server is healthy"
}
```

- **Status Code**: `200 OK`

---

### 2. Add Items to Cart

- **Endpoint**: `/v1/cart`
- **Method**: `POST`
- **Description**: This endpoint allows users to add items to their shopping cart. It checks if the user already has a cart and adds new items that are not already in the cart.

#### Request:

```http
POST /v1/cart
Content-Type: application/json
```

**Request Body**:

```json
{
  "user_id": "user123",
  "items": [
    {
      "item_id": "item456",
      "quantity": 2,
      "price": 19.99
    },
    {
      "item_id": "item789",
      "quantity": 1,
      "price": 9.99
    }
  ]
}
```

#### Response:

```json
{
  "message": "Items added to cart"
}
```

- **Status Code**: `201 Created`

#### Description:

This endpoint checks if a cart exists for the given `user_id`. If the cart doesn't exist, a new one is created. It only adds items that are not already in the user's cart.

---

### 3. View Cart

- **Endpoint**: `/v1/cart/{user_id}`
- **Method**: `GET`
- **Description**: This endpoint allows users to view the contents of their cart. It also calculates and returns the total amount of the items in the cart.

#### Request:

```http
GET /v1/cart/{user_id}
```

**Path Parameter**:

- `user_id` (string): The unique identifier for the user whose cart is being viewed.

#### Response:

```json
{
  "user_id": "user123",
  "items": [
    {
      "item_id": "item456",
      "quantity": 2,
      "price": 19.99
    },
    {
      "item_id": "item789",
      "quantity": 1,
      "price": 9.99
    }
  ],
  "total_amount": 49.97
}
```

- **Status Code**: `200 OK`

#### Error Response (Cart not found):

```json
{
  "message": "Cart data not found"
}
```

- **Status Code**: `404 Not Found`

#### Description:

This endpoint retrieves the user's cart by their `user_id`. If the user has no cart, it returns a `404 Not Found` error. If the cart is found, the total amount of the cart is calculated and included in the response.

---

### 4. Order Details

- **Endpoint**: `/v1/order/{user_id}`
- **Method**: `GET`
- **Description**: This endpoint retrieves the details of a user's order. If the user is eligible for a discount, it will be included in the order details.

#### Request:

```http
GET /v1/order/{user_id}
```

**Path Parameter**:

- `user_id` (string): The unique identifier for the user whose order details are being retrieved.

#### Response:

```json
{
  "order_id": "ORDER-2",
  "user_id": "user123",
  "items": [
    {
      "item_id": "item456",
      "quantity": 2,
      "price": 19.99
    },
    {
      "item_id": "item789",
      "quantity": 1,
      "price": 9.99
    }
  ],
  "total_amount": 49.97,
  "discount_code": "DISCOUNT-1"
}
```

- **Status Code**: `200 OK`

#### Error Response (No order found):

```json
{
  "detail": "No order found"
}
```

- **Status Code**: `404 Not Found`

#### Description:

This endpoint retrieves the details of an order based on the provided `user_id`. It calculates the total amount of the order and includes any discount codes (if applicable). If the user does not have any order, a `404 Not Found` response will be returned.

---

### 5. Checkout

- **Endpoint**: `/v1/checkout`
- **Method**: `POST`
- **Description**: This endpoint handles the checkout process, where a user can complete their purchase by reviewing their cart, applying a discount code (if applicable), and placing an order.

#### Request:

```http
POST /v1/checkout
Content-Type: application/json
```

**Request Body**:

```json
{
  "user_id": "user123",
  "discount_code": "DISCOUNT-1"
}
```

#### Response:

```json
{
  "message": "Order placed successfully"
}
```

- **Status Code**: `200 OK`

#### Error Responses:

1. **Cart is empty**:

   ```json
   {
     "detail": "Cart is empty"
   }
   ```

   - **Status Code**: `404 Not Found`

2. **Invalid discount code**:
   ```json
   {
     "detail": "Invalid discount code"
   }
   ```
   - **Status Code**: `400 Bad Request`

#### Description:

This endpoint allows the user to complete their checkout process. If a discount code is provided, it will be validated. If the discount code is valid, the discount will be applied to the total amount. After a successful checkout, the cart is cleared and the order is saved.

---

### 6. Get Statistics

- **Endpoint**: `/v1/statistics`
- **Method**: `GET`
- **Description**: This endpoint provides various statistics related to orders and discount codes, including the total number of items purchased, total amount spent, total discount amount applied, and a summary of discount codes used.

#### Request:

```http
GET /v1/statistics
```

#### Response:

```json
{
  "items_purchsed": 100,
  "total_amount": 1500.0,
  "discount_amount": 150.0,
  "discount_codes": [
    "DISCOUNT-1"
    "DISCOUNT-2"
  ]
}
```

- **Status Code**: `200 OK`

#### Description:

This endpoint aggregates and returns statistical data based on the orders and discount codes:

- **items_purchased**: Total number of items purchased across all orders.
- **total_amount**: The total amount spent on all orders.
- **discount_amount**: The total discount amount applied to all orders.
- **discount_codes**: List of discount codess.

---
