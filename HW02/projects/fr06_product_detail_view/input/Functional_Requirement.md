# FR-06: Product Detail View

> Pool A — Authentication, Categories, and Products.
> Source of truth: EShop System Requirements Specification (README.md, section 3, FR-06).

## 1. Overview

When a user opens a single product, the system displays the full product detail, allows the user to choose a quantity, and provides an "Add to Cart" action with visual feedback.

## 2. API Reference (from api_specification.md)

- **Endpoint:** `GET /api/products/:id`
- **Path parameter:** `id` — the product identifier.
- **Success response (200 OK):** a product object, e.g.
  ```json
  {
    "id": 1,
    "name": "Product name",
    "price": 100000,
    "description": "Description",
    "imageUrl": "http://...",
    "category_id": 1
  }
  ```
- Related "Add to Cart" endpoint: `POST /api/cart` with body `{ id, name, price, quantity }`.

## 3. Functional Requirements

### 3.1 Detail display
The product detail page MUST display all of the following:
- Large product **image**
- Product **name**
- **Price**
- **Description**
- **Category**

### 3.2 Quantity input
- There MUST be a **Quantity** input field.
- Quantity MUST accept only **positive integers**.
- The **minimum** accepted quantity is **1**.

### 3.3 Add to Cart
- There MUST be an **Add to Cart** button.
- After clicking Add to Cart, the system MUST show visual feedback (a toast notification or an updated cart badge).

## 4. Inputs Summary (for test design)

| Field | Type | Constraint |
| --- | --- | --- |
| Product id (path param) | integer | Identifies which product to display; must refer to an existing product |
| Quantity | integer | Positive integer; minimum 1 (no explicit maximum stated in the specification) |

## 5. Expected Outputs

- **Valid product id:** full product detail rendered (image, name, price, description, category).
- **Add to cart with valid quantity:** item added to cart and visual feedback shown.
- **Invalid quantity (0, negative, non-integer, empty):** input rejected / add-to-cart prevented (exact behavior not specified — flag as Open Question).
- **Non-existent product id:** behavior not fully specified in the requirement — flag as Open Question.