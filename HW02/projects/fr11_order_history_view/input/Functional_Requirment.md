# FR-11: Order History View (User)

> Pool B — Shopping Cart and Checkout.
> Source of truth: EShop System Requirements Specification (README.md, section 5, FR-11).

## 1. Overview

A logged-in user can view the history of their own orders. Each order shows summary information, and the status is displayed in Vietnamese with color coding.

## 2. API Reference (from api_specification.md)

- **List own orders:** `GET /api/orders/my-orders`
- **Get one order detail:** `GET /api/orders/:id`
- **Authentication:** required — header `Authorization: Bearer <token>`.

## 3. Functional Requirements

### 3.1 Ownership restriction
- A user MUST be able to view **only their own orders**.
- A user MUST NOT be able to view another user's orders.

### 3.2 Displayed fields
Each order in the history MUST display:
- **Order ID**
- **Order date**
- **Total amount**
- **Current status**

### 3.3 Status presentation
- The order status MUST be translated into clear **Vietnamese**.
- Statuses MUST be visually distinguished by **color**.
- The five possible statuses (from FR-10 state machine) are: `pending`, `confirmed`, `shipping`, `delivered`, `canceled`.

## 4. Inputs Summary (for test design)

| Input | Type | Constraint |
| --- | --- | --- |
| Authenticated user (JWT token) | token | Required; identifies whose orders are returned |
| Order id (for detail view, `GET /api/orders/:id`) | integer | Must belong to the requesting user |
| Order status (value being displayed) | enum | One of: pending / confirmed / shipping / delivered / canceled |

## 5. Expected Outputs

- **Authenticated user, own orders:** list of that user's orders with id, date, total, status (status shown in Vietnamese + color).
- **Request another user's order id:** MUST be denied / not returned (ownership rule).
- **No token / invalid token:** request rejected (unauthorized).
- **User with no orders:** an appropriate empty state.