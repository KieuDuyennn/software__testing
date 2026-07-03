# FR-13: Admin Dashboard

> Pool C — Web Admin.
> Source of truth: EShop System Requirements Specification (README.md, section 6, FR-13). Access is governed by FR-12 (admin-only).

## 1. Overview

The Admin Dashboard displays aggregate business metrics: total revenue and total number of orders.

## 2. API Reference (from api_specification.md)

- Admin order data source: `GET /api/admin/orders` (requires admin JWT).
- Order status is updated via `PUT /api/admin/orders/:id/status` with body `{ "status": "confirmed" }` (allowed statuses: `pending`, `confirmed`, `shipping`, `delivered`, `canceled`).
- **Authentication/authorization:** all `/api/admin/*` endpoints require a valid JWT with `role = 'admin'` (see FR-12).

## 3. Functional Requirements

### 3.1 Total revenue
- The dashboard MUST display **total revenue**.
- Total revenue MUST be computed as the **sum of `total_amount` of orders whose `status = 'delivered'`** — and ONLY those orders.
- Orders in any other status (`pending`, `confirmed`, `shipping`, `canceled`) MUST NOT contribute to total revenue.

### 3.2 Total number of orders
- The dashboard MUST display the **total number of orders**.

### 3.3 Access control (per FR-12)
- The dashboard and its underlying admin APIs MUST be accessible only to accounts with `role = 'admin'`.
- A valid JWT alone is not sufficient; the token MUST carry `role = 'admin'`.

## 4. Inputs Summary (for test design)

| Input | Type | Constraint |
| --- | --- | --- |
| Requesting account role (in JWT) | enum | Must be `admin` to access; `user`/absent → denied |
| Order status (per order, drives revenue calculation) | enum | pending / confirmed / shipping / delivered / canceled — only `delivered` counts toward revenue |
| `total_amount` per delivered order | number | Summed into total revenue |

## 5. Expected Outputs

- **Admin token:** dashboard shows total revenue (sum of `total_amount` where status = delivered) and total order count.
- **Order status = delivered:** included in revenue sum.
- **Order status ≠ delivered:** excluded from revenue sum, but may still count in "total number of orders".
- **Non-admin token (`role = 'user'`):** access denied.
- **No token / invalid token:** access denied.