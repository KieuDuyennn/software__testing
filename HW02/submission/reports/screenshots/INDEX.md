# Screenshot index - captured behavior on the live EShop SUT (2026-07-07)

Factual screenshots of the SUT's actual behavior, captured with a headless browser against
the running apps (web `:5173`, admin `:5174`, backend `:3000`). Visual raw evidence only -
which behavior is a *bug*, and all bug wording, is the student's to decide. Only non-`OK`
(non-Khớp) cases with a meaningful UI state are captured; cases with no UI (or no distinct
screen) are listed with their reason in `../TC_Checklist.md`.

| File | Feature / TC | What it shows |
|---|---|---|
| `fr01_TC01a_valid_pw_rejected.png` | FR-01 TC-01a | Valid strong pw `Password123!` rejected with "Mật khẩu quá yếu". |
| `fr01_BVA02_valid_pw8_rejected.png` | FR-01 BVA-02 | Valid 8-char pw `Pa1!abcd` also rejected. |
| `fr01_weak_pw_with_space_accepted.png` | FR-01 (regex) | Weak pw `Test 1234` (no special char, has a space; violates FR) accepted → navigated to Login. |
| `fr06_TC10_empty_name.png` | FR-06 TC-10 | Product with empty name. |
| `fr06_TC09_empty_image.png` | FR-06 TC-09 | Product with empty imageUrl (broken image area). |
| `fr06_TC12_empty_description.png` | FR-06 TC-12 | Product with empty description. |
| `fr06_TC13_null_category.png` | FR-06 TC-13 | Product with null category (no category rendered - CF-01). |
| `fr06_TC02_edge_fixture.png` | FR-06 TC-02 | Edge product: 200-char name, price 0, broken image. |
| `fr06_TC11_null_price_oddid.png` | FR-06 TC-11 | Null price, odd id (no crash): screen shows "0 ₫" for a null price. |
| `fr06_TC11_null_price_evenid_crash.png` | FR-06 TC-11 | Null price, even id: GET crashes backend, page stuck on "Đang tải…". |
| `fr06_TC05_quantity_negative.png` | FR-06 TC-05 | Quantity field accepts `-5` with no validation. |
| `fr06_nonexistent_product.png` | FR-06 | `/product/9999` nonexistent (API 200+`{}`) empty-data screen. |
| `fr06_product_2_even_id.png` | FR-06 | `/product/2` (even id) reference render. |
| `fr11_order_by_id_no_auth.png` | FR-11 TC-03 | `GET /api/orders/1` in a browser with no login returns the order JSON. |
| `fr13_TC05_dashboard_revenue_doubled.png` | FR-13 TC-05 | Dashboard revenue 200,000 ₫ for one 100,000 ₫ delivered order. |
| `fr13_orders_table_context.png` | FR-13 | Admin orders table: delivered = 100,000, canceled = 50,000. |

Reproduction: backend seeded fresh, atypical products seeded via `POST /api/products`, one
delivered order 100,000 ₫ + one canceled 50,000 ₫ created. Admin login `admin@eshop.com` / `Admin123!`.
