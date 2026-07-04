# FR-14: Category Management (CRUD)

> Pool C — Web Admin.
> Source of truth: EShop System Requirements Specification (README.md, section 6, FR-14). Access is governed by FR-12 (admin-only).

## 1. Overview

An admin can manage product categories: add a new category, view the list of categories, and delete a category. Category name is mandatory.

## 2. API Reference (from api_specification.md)

- **List categories:** `GET /api/categories`
- **Create category:** `POST /api/categories` — body `{ "name": "Category name" }`
- **Update category:** `PUT /api/categories/:id`
- **Delete category:** `DELETE /api/categories/:id`
- **Authentication/authorization:** category-mutating endpoints (`POST/PUT/DELETE /api/categories`) require a valid JWT with `role = 'admin'` (see FR-12).

## 3. Functional Requirements

### 3.1 Operations
- The admin MUST be able to **Add**, **View (list)**, and **Delete** categories.
  - Note: the README specifies Add / View / Delete. The API also exposes `PUT /api/categories/:id` (update); treat update as an available operation but flag any discrepancy between the README (which does not list "edit") and the API (which exposes it) as an Open Question.

### 3.2 Category name validation
- Category **name is required** and MUST NOT be empty.
- A create/update request with an empty or whitespace-only name MUST be rejected.

### 3.3 Access control (per FR-12)
- Only accounts with `role = 'admin'` may create, update, or delete categories.
- A valid JWT alone is not sufficient; the token MUST carry `role = 'admin'`.

## 4. Inputs Summary (for test design)

| Field / Input | Type | Constraint |
| --- | --- | --- |
| Category `name` (create/update) | string | Required; must not be empty or whitespace-only |
| Category `id` (update/delete path param) | integer | Must refer to an existing category |
| Requesting account role (in JWT) | enum | Must be `admin`; `user`/absent → denied |

## 5. Expected Outputs

- **Create with valid non-empty name (admin):** category created; appears in `GET /api/categories`.
- **Create with empty / whitespace-only name:** rejected with a validation error.
- **Delete existing category (admin):** category removed from the list.
- **Delete non-existent category id:** appropriate error / no-op (behavior not fully specified — flag as Open Question).
- **Non-admin or unauthenticated request to mutate:** access denied.