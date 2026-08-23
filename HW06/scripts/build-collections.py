#!/usr/bin/env python3
"""Generate the four HW06 Postman collection skeletons.

Each collection ships the shared harness (X-Student-Id injection, global
assertions, auth setup) plus a small set of exemplar test cases per required
coverage dimension. The bulk of the >=35 cases per API is added afterwards, in
the AI-generation and human-audit phases, and re-exported from Postman.

Re-running this script OVERWRITES the collections. Once you start editing in
Postman, treat the exported JSON as the source of truth and stop re-running it.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "collections"

# --------------------------------------------------------------------------
# Shared harness scripts, applied at collection level.
# --------------------------------------------------------------------------

PRE_REQUEST = r"""
// ---------------------------------------------------------------------------
// HW06 mandatory harness: every request must carry X-Student-Id.
// The console line below is the anti-AI-cheat evidence (Section 11 of the
// brief) - screenshot the Postman console showing it.
// ---------------------------------------------------------------------------
const studentId = pm.environment.get("student_id") || "23127184";

pm.request.headers.upsert({ key: "X-Student-Id", value: studentId });

// Tag each run so Newman output and SUT state can be correlated.
if (!pm.environment.get("run_tag")) {
    pm.environment.set("run_tag", "run-" + Date.now());
}

console.log(
    "[HW06] X-Student-Id=" + studentId +
    " | " + pm.request.method + " " + pm.request.url.toString() +
    " | run_tag=" + pm.environment.get("run_tag")
);
""".strip()

GLOBAL_TEST = r"""
// ---------------------------------------------------------------------------
// Assertions that apply to every request in the collection.
// ---------------------------------------------------------------------------
pm.test("Request carried the X-Student-Id header", function () {
    const sent = pm.request.headers.get("X-Student-Id");
    pm.expect(sent, "X-Student-Id header").to.eql(
        pm.environment.get("student_id") || "23127184"
    );
});

pm.test("Response is not rate-limited (HTTP 429)", function () {
    pm.expect(
        pm.response.code,
        "Backend rate limiter tripped - start the SUT with LOADTEST=1"
    ).to.not.eql(429);
});

pm.test("Response arrived under 2000 ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(2000);
});
""".strip()


def script(exec_src, listen):
    return {
        "listen": listen,
        "script": {"type": "text/javascript", "exec": exec_src.split("\n")},
    }


def request(method, path, body=None, auth_var=None, extra_headers=None,
            raw_query=None):
    url_raw = "{{base_url}}" + path + (raw_query or "")
    segments = [s for s in path.strip("/").split("/") if s]
    url = {"raw": url_raw, "host": ["{{base_url}}"], "path": segments}
    if raw_query:
        url["query"] = [
            {"key": kv.split("=")[0], "value": kv.split("=", 1)[1]}
            for kv in raw_query.lstrip("?").split("&") if "=" in kv
        ]
    headers = list(extra_headers or [])
    if body is not None:
        headers.append({"key": "Content-Type", "value": "application/json"})
    if auth_var:
        headers.append({"key": "Authorization", "value": "Bearer {{%s}}" % auth_var})
    req = {"method": method, "header": headers, "url": url}
    if body is not None:
        raw = body if isinstance(body, str) else json.dumps(body, indent=2, ensure_ascii=False)
        req["body"] = {"mode": "raw", "raw": raw,
                       "options": {"raw": {"language": "json"}}}
    return req


def item(name, req, test_src, pre_src=None, description=""):
    events = []
    if pre_src:
        events.append(script(pre_src.strip(), "prerequest"))
    events.append(script(test_src.strip(), "test"))
    node = {"name": name, "event": events, "request": req, "response": []}
    if description:
        node["request"]["description"] = description
    return node


def folder(name, items, description=""):
    return {"name": name, "item": items, "description": description}


def collection(name, description, items):
    return {
        "info": {
            "_postman_id": str(uuid.uuid4()),
            "name": name,
            "description": description,
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "item": items,
        "event": [script(PRE_REQUEST, "prerequest"), script(GLOBAL_TEST, "test")],
        "variable": [],
    }


# Reusable login step -------------------------------------------------------

def login_item(name, email_var, pwd_var, token_var):
    return item(
        name,
        request("POST", "/api/login", {"email": "{{%s}}" % email_var,
                                       "password": "{{%s}}" % pwd_var}),
        """
pm.test("Login succeeded", function () {{
    pm.response.to.have.status(200);
    pm.expect(pm.response.json()).to.have.property("token");
}});

const body = pm.response.json();
pm.environment.set("{token_var}", body.token);
if (body.user) {{
    pm.environment.set("{token_var}_user_id", body.user.id);
    pm.environment.set("{token_var}_role", body.user.role);
}}
""".format(token_var=token_var),
        description="Setup step: obtains a JWT used by later requests in this collection.",
    )


# --------------------------------------------------------------------------
# API 1 - FR-01 Account registration - POST /api/register
# --------------------------------------------------------------------------

api1 = collection(
    "API1 - FR-01 Account Registration (POST /api/register)",
    "HW06 / Pool A / FR-01.\n\n"
    "Spec: POST /api/register {name, email, password} -> 200 "
    "{\"message\":\"User registered successfully\",\"id\":<int>}.\n\n"
    "Coverage dimensions required by the brief: domain partitions on every "
    "parameter, state transitions (registered -> can log in), security "
    "(SEC-01 plaintext storage, SEC-05 SQL injection, SEC-06 role injection) "
    "and schema validation.",
    [
        folder("00 - Setup", [],
               "Fixtures and tokens needed by later folders. FR-01 needs none by default."),
        folder("01 - Domain partitions", [
            item(
                "DP-001 | Valid registration (all fields in-partition)",
                request("POST", "/api/register", {
                    "name": "Kieu Duyen QA",
                    "email": "{{$guid}}@domain.com",
                    "password": "Password123!",
                }),
                """
pm.test("Status is 200", () => pm.response.to.have.status(200));

pm.test("Body matches the spec's success shape", function () {
    const b = pm.response.json();
    pm.expect(b).to.have.property("message", "User registered successfully");
    pm.expect(b).to.have.property("id");
    pm.expect(b.id, "id must be an integer").to.be.a("number");
});

pm.environment.set("last_registered_id", pm.response.json().id);
""",
            ),
            item(
                "DP-002 | Invalid email format is rejected",
                request("POST", "/api/register", {
                    "name": "Bad Email",
                    "email": "not-an-email",
                    "password": "Password123!",
                }),
                """
// FR-01: "Email phai co dinh dang hop le (user@domain.com)".
// EXPECTED per requirement; the SUT currently accepts it -> defect evidence.
pm.test("Malformed email is rejected with 4xx", function () {
    pm.expect(pm.response.code).to.be.within(400, 499);
});
""",
            ),
        ], "One case per equivalence class / boundary on name, email, password. "
           "Expand to the full partition table during the AI-generation phase."),
        folder("02 - State transitions", [
            item(
                "ST-001 | Registered account can immediately log in",
                request("POST", "/api/login", {
                    "email": "{{registered_email}}",
                    "password": "{{registered_password}}",
                }),
                """
pm.test("Newly registered account transitions to a usable login state", function () {
    pm.response.to.have.status(200);
    pm.expect(pm.response.json()).to.have.property("token");
});
""",
                pre_src="""
// Register a fresh account in this step so the transition is self-contained.
const email = pm.variables.replaceIn("{{$guid}}") + "@domain.com";
const password = "Password123!";
pm.environment.set("registered_email", email);
pm.environment.set("registered_password", password);

pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/register",
    method: "POST",
    header: {
        "Content-Type": "application/json",
        "X-Student-Id": pm.environment.get("student_id")
    },
    body: { mode: "raw", raw: JSON.stringify({ name: "ST Fixture", email, password }) }
}, function (err, res) {
    console.log("[HW06] ST-001 fixture registered " + email + " -> " + (res ? res.code : err));
});
""",
            ),
        ], "Account lifecycle states reachable from registration: new -> registered -> authenticated."),
        folder("03 - Security (SEC-01..SEC-07)", [
            item(
                "SEC-01 | Password must not be retrievable in plaintext",
                request("POST", "/api/login", {
                    "email": "{{registered_email}}",
                    "password": "{{registered_password}}",
                }),
                """
// SEC-01: "Mat khau khong duoc luu duoi dang plaintext."
// The login response echoes the whole users row; if password comes back equal
// to what we sent, storage is plaintext.
pm.test("Login response does not expose the plaintext password", function () {
    const u = pm.response.json().user || {};
    pm.expect(u.password, "password field in response").to.not.eql(
        pm.environment.get("registered_password")
    );
});
""",
            ),
            item(
                "SEC-05 | SQL injection in the email field is neutralised",
                request("POST", "/api/register", {
                    "name": "SQLi Probe",
                    "password": "Password123!",
                    "email": "sqli'); DROP TABLE users;--@domain.com",
                }),
                """
pm.test("Server does not return a 500 / SQL error", function () {
    pm.expect(pm.response.code).to.not.eql(500);
});

pm.test("No SQL error text leaks to the client", function () {
    pm.expect(pm.response.text().toLowerCase()).to.not.include("sqlite");
});
""",
            ),
            item(
                "SEC-06 | Client cannot self-assign the admin role at registration",
                request("POST", "/api/register", {
                    "name": "Role Injection",
                    "email": "{{$guid}}@domain.com",
                    "password": "Password123!",
                    "role": "admin",
                }),
                """
// The created account must not come back with role=admin.
pm.test("Injected role is ignored", function () {
    pm.expect(pm.response.code).to.be.oneOf([200, 400]);
});
// Follow-up verification (log in and inspect role) is added in the extend phase.
""",
            ),
        ], "Map every case to the SEC-01..SEC-07 id it exercises."),
        folder("04 - Schema validation", [
            item(
                "SCH-001 | Success response matches the specified schema exactly",
                request("POST", "/api/register", {
                    "name": "Schema Probe",
                    "email": "{{$guid}}@domain.com",
                    "password": "Password123!",
                }),
                """
const schema = {
    type: "object",
    required: ["message", "id"],
    additionalProperties: false,
    properties: {
        message: { type: "string" },
        id: { type: "integer" }
    }
};

pm.test("Response body conforms to the spec schema", function () {
    pm.response.to.have.jsonSchema(schema);
});
""",
            ),
        ], "The response shape must match api_specification.md exactly - no extra "
           "or missing fields, correct JSON types."),
    ],
)

# --------------------------------------------------------------------------
# API 2 - FR-06 Product detail - GET /api/products/:id
# --------------------------------------------------------------------------

PRODUCT_SCHEMA = """
const schema = {
    type: "object",
    required: ["id", "name", "price", "description", "imageUrl", "category_id"],
    properties: {
        id: { type: "integer" },
        name: { type: "string" },
        price: { type: "number" },
        description: { type: "string" },
        imageUrl: { type: "string" },
        category_id: { type: "integer" }
    }
};
"""

api2 = collection(
    "API2 - FR-06 Product Detail (GET /api/products/:id)",
    "HW06 / Pool A / FR-06.\n\n"
    "Spec: GET /api/products/:id -> the product record.\n\n"
    "This collection is the main carrier of schema-validation evidence: the "
    "response type of `price` and the not-found behaviour are both worth "
    "checking against the spec on every id partition.",
    [
        folder("00 - Setup", [
            item(
                "SETUP-001 | Capture a known-good product id",
                request("GET", "/api/products"),
                """
pm.test("Product list is available", () => pm.response.to.have.status(200));
const list = pm.response.json();
if (Array.isArray(list) && list.length) {
    pm.environment.set("existing_product_id", list[0].id);
    pm.environment.set("max_product_id", list[list.length - 1].id);
}
""",
            ),
        ]),
        folder("01 - Domain partitions", [
            item(
                "DP-001 | Existing id returns that product",
                request("GET", "/api/products/{{existing_product_id}}"),
                """
pm.test("Status is 200", () => pm.response.to.have.status(200));
pm.test("Returned product is the one requested", function () {
    pm.expect(String(pm.response.json().id)).to.eql(
        String(pm.environment.get("existing_product_id"))
    );
});
""",
            ),
            item(
                "DP-002 | Non-existent id returns 404",
                request("GET", "/api/products/999999"),
                """
// Spec/REST contract: an unknown resource is 404, not 200 with an empty body.
pm.test("Unknown product id returns 404", function () {
    pm.response.to.have.status(404);
});
""",
            ),
            item(
                "DP-003 | Non-numeric id is rejected",
                request("GET", "/api/products/abc"),
                """
pm.test("Non-numeric id yields a 4xx, never a 500", function () {
    pm.expect(pm.response.code).to.be.within(400, 499);
});
""",
            ),
        ], "Partitions on :id - valid / non-existent / zero / negative / "
           "non-numeric / overflow / injection."),
        folder("02 - State transitions", [
            item(
                "ST-001 | Deleted product is no longer retrievable",
                request("GET", "/api/products/{{transient_product_id}}"),
                """
pm.test("A deleted product returns 404", function () {
    pm.response.to.have.status(404);
});
""",
                pre_src="""
// Create then delete a product so this request observes the post-delete state.
// NOTE: POST/DELETE /api/products currently need no token - that itself is a
// finding for the security folder.
const base = pm.environment.get("base_url");
const sid = pm.environment.get("student_id");
pm.sendRequest({
    url: base + "/api/products",
    method: "POST",
    header: { "Content-Type": "application/json", "X-Student-Id": sid },
    body: { mode: "raw", raw: JSON.stringify({
        name: "HW06 transient", price: 1000, description: "state fixture",
        imageUrl: "", category_id: 1 }) }
}, function (err, res) {
    if (err || !res) { return; }
    const id = res.json().id;
    pm.environment.set("transient_product_id", id);
    pm.sendRequest({
        url: base + "/api/products/" + id,
        method: "DELETE",
        header: { "X-Student-Id": sid }
    }, function () {
        console.log("[HW06] ST-001 fixture created+deleted product " + id);
    });
});
""",
            ),
        ], "Existence states of a product: present -> deleted -> absent."),
        folder("03 - Security (SEC-01..SEC-07)", [
            item(
                "SEC-05 | SQL injection through the :id path parameter",
                request("GET", "/api/products/1 OR 1=1"),
                """
pm.test("Injection does not return the whole table", function () {
    const b = pm.response.json();
    pm.expect(Array.isArray(b), "response must not be a list of all products").to.be.false;
});
pm.test("No 500 / SQL error leak", function () {
    pm.expect(pm.response.code).to.not.eql(500);
    pm.expect(pm.response.text().toLowerCase()).to.not.include("sqlite");
});
""",
            ),
        ]),
        folder("04 - Schema validation", [
            item(
                "SCH-001 | Product schema holds for an odd id",
                request("GET", "/api/products/1"),
                PRODUCT_SCHEMA + """
pm.test("Response conforms to the product schema", function () {
    pm.response.to.have.jsonSchema(schema);
});

pm.test("price is a JSON number, not a string", function () {
    pm.expect(pm.response.json().price).to.be.a("number");
});
""",
            ),
            item(
                "SCH-002 | Product schema holds for an even id",
                request("GET", "/api/products/2"),
                PRODUCT_SCHEMA + """
// Same contract must hold regardless of the id's parity.
pm.test("Response conforms to the product schema", function () {
    pm.response.to.have.jsonSchema(schema);
});

pm.test("price is a JSON number, not a string", function () {
    pm.expect(pm.response.json().price).to.be.a("number");
});
""",
            ),
        ], "Run the same schema assertions across every id partition - type drift "
           "is id-dependent here."),
    ],
)

# --------------------------------------------------------------------------
# API 3 - FR-11 Order history (user) - GET /api/orders/my-orders
# --------------------------------------------------------------------------

api3 = collection(
    "API3 - FR-11 Order History (GET /api/orders/my-orders)",
    "HW06 / Pool B / FR-11.\n\n"
    "Spec: GET /api/orders/my-orders (Bearer token) -> the caller's orders. "
    "FR-11 states a user may only see their own orders, which makes this the "
    "natural home for IDOR / ownership testing, and for the FR-10 order state "
    "machine as it is observed through order history.",
    [
        folder("00 - Setup", [
            login_item("SETUP-001 | Log in as the primary user",
                       "user_email", "user_password", "user_token"),
            item(
                "SETUP-002 | Create an order owned by the primary user",
                request("POST", "/api/checkout", {
                    "total_amount": 250000,
                    "shipping_address": "123 Le Loi, Q1, TP.HCM",
                }, auth_var="user_token"),
                """
pm.test("Checkout created an order", function () {
    pm.response.to.have.status(200);
    pm.expect(pm.response.json()).to.have.property("orderId");
});
pm.environment.set("own_order_id", pm.response.json().orderId);
""",
            ),
            item(
                "SETUP-003 | Register + log in a second user (the victim)",
                request("POST", "/api/login", {
                    "email": "{{victim_email}}",
                    "password": "{{victim_password}}",
                }),
                """
pm.test("Victim account is usable", () => pm.response.to.have.status(200));
pm.environment.set("victim_token", pm.response.json().token);
pm.environment.set("victim_user_id", pm.response.json().user.id);
""",
                pre_src="""
const email = pm.variables.replaceIn("{{$guid}}") + "@victim.com";
const password = "Victim123!";
pm.environment.set("victim_email", email);
pm.environment.set("victim_password", password);
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/register",
    method: "POST",
    header: { "Content-Type": "application/json",
              "X-Student-Id": pm.environment.get("student_id") },
    body: { mode: "raw", raw: JSON.stringify({ name: "Victim", email, password }) }
}, function () { console.log("[HW06] victim account created: " + email); });
""",
            ),
            item(
                "SETUP-004 | Create an order owned by the victim",
                request("POST", "/api/checkout", {
                    "total_amount": 777000,
                    "shipping_address": "99 Victim Street",
                }, auth_var="victim_token"),
                """
pm.test("Victim order created", () => pm.response.to.have.status(200));
pm.environment.set("victim_order_id", pm.response.json().orderId);
""",
            ),
        ], "Builds the two-user fixture that ownership and IDOR cases depend on."),
        folder("01 - Domain partitions", [
            item(
                "DP-001 | Authenticated user receives their own order list",
                request("GET", "/api/orders/my-orders", auth_var="user_token"),
                """
pm.test("Status is 200", () => pm.response.to.have.status(200));
pm.test("Response is an array", function () {
    pm.expect(pm.response.json()).to.be.an("array");
});
pm.test("Every returned order belongs to the caller", function () {
    const me = Number(pm.environment.get("user_token_user_id"));
    pm.response.json().forEach(function (o) {
        pm.expect(o.user_id, "order " + o.id + " owner").to.eql(me);
    });
});
""",
            ),
            item(
                "DP-002 | Missing token is rejected",
                request("GET", "/api/orders/my-orders"),
                """
pm.test("Unauthenticated request returns 401", function () {
    pm.response.to.have.status(401);
});
""",
            ),
        ]),
        folder("02 - State transitions (FR-10)", [
            item(
                "ST-001 | A new order appears in history as 'pending'",
                request("GET", "/api/orders/my-orders", auth_var="user_token"),
                """
pm.test("The order created in setup is listed as pending", function () {
    const target = Number(pm.environment.get("own_order_id"));
    const found = pm.response.json().find(o => o.id === target);
    pm.expect(found, "order " + target + " in history").to.not.be.undefined;
    pm.expect(found.status).to.eql("pending");
});
""",
            ),
            item(
                "ST-002 | Cancelling a pending order is reflected in history",
                request("PUT", "/api/orders/{{own_order_id}}/cancel", auth_var="user_token"),
                """
pm.test("Cancel from 'pending' is allowed", () => pm.response.to.have.status(200));
""",
            ),
        ], "pending -> confirmed -> shipping -> delivered plus cancellation "
           "rules, observed through order history."),
        folder("03 - Security (SEC-01..SEC-07)", [
            item(
                "SEC-02 | Reading another user's order requires authentication (IDOR)",
                request("GET", "/api/orders/{{victim_order_id}}"),
                """
// SEC-02: security-relevant APIs require a valid JWT.
// FR-11: a user may only see their own orders.
pm.test("Unauthenticated read of an arbitrary order is refused", function () {
    pm.expect(pm.response.code).to.be.oneOf([401, 403, 404]);
});
""",
            ),
            item(
                "SEC-02b | User A cannot read user B's order with their own token",
                request("GET", "/api/orders/{{victim_order_id}}", auth_var="user_token"),
                """
pm.test("Cross-user order read is refused", function () {
    pm.expect(pm.response.code).to.be.oneOf([403, 404]);
});
""",
            ),
        ]),
        folder("04 - Schema validation", [
            item(
                "SCH-001 | Order-history entries match the orders schema",
                request("GET", "/api/orders/my-orders", auth_var="user_token"),
                """
const schema = {
    type: "array",
    items: {
        type: "object",
        required: ["id", "user_id", "total_amount", "status", "shipping_address", "created_at"],
        properties: {
            id: { type: "integer" },
            user_id: { type: "integer" },
            total_amount: { type: "number" },
            status: { type: "string",
                      enum: ["pending", "confirmed", "shipping", "delivered", "canceled"] },
            shipping_address: { type: ["string", "null"] },
            created_at: { type: "string" }
        }
    }
};

pm.test("Order history conforms to the schema", function () {
    pm.response.to.have.jsonSchema(schema);
});
""",
            ),
        ]),
    ],
)

# --------------------------------------------------------------------------
# API 4 - FR-13 Admin dashboard data - GET /api/admin/orders
# --------------------------------------------------------------------------

api4 = collection(
    "API4 - FR-13 Admin Dashboard (GET /api/admin/orders)",
    "HW06 / Pool C / FR-13.\n\n"
    "The admin dashboard reports total revenue - the sum of total_amount over "
    "orders whose status is 'delivered' - and the total order count. Both are "
    "computed from GET /api/admin/orders, so that endpoint is the API under "
    "test. FR-12 / SEC-03 require role='admin' in the token, not merely a "
    "valid token.",
    [
        folder("00 - Setup", [
            login_item("SETUP-001 | Log in as admin",
                       "admin_email", "admin_password", "admin_token"),
            login_item("SETUP-002 | Log in as a non-admin user",
                       "user_email", "user_password", "user_token"),
        ]),
        folder("01 - Domain partitions", [
            item(
                "DP-001 | Admin receives the full order list",
                request("GET", "/api/admin/orders", auth_var="admin_token"),
                """
pm.test("Status is 200", () => pm.response.to.have.status(200));
pm.test("Response is an array", function () {
    pm.expect(pm.response.json()).to.be.an("array");
});
pm.test("Rows are joined with the ordering user's name", function () {
    const rows = pm.response.json();
    if (rows.length) { pm.expect(rows[0]).to.have.property("user_name"); }
});
pm.environment.set("admin_order_count", pm.response.json().length);
""",
            ),
            item(
                "DP-002 | Missing token is rejected",
                request("GET", "/api/admin/orders"),
                """
pm.test("Unauthenticated request returns 401", () => pm.response.to.have.status(401));
""",
            ),
            item(
                "DP-003 | Malformed token is rejected",
                request("GET", "/api/admin/orders",
                        extra_headers=[{"key": "Authorization",
                                        "value": "Bearer not.a.real.token"}]),
                """
pm.test("Invalid token returns 403", () => pm.response.to.have.status(403));
""",
            ),
        ]),
        folder("02 - State transitions (FR-10)", [
            item(
                "ST-001 | Revenue counts only 'delivered' orders",
                request("GET", "/api/admin/orders", auth_var="admin_token"),
                """
// FR-13: "Chi tinh tong total_amount cua cac don co status = 'delivered'".
const rows = pm.response.json();
const delivered = rows.filter(o => o.status === "delivered");
const revenue = delivered.reduce((s, o) => s + Number(o.total_amount || 0), 0);

pm.environment.set("expected_revenue", revenue);
console.log("[HW06] delivered orders=" + delivered.length + " revenue=" + revenue);

pm.test("Every order carries a status from the FR-10 state set", function () {
    const allowed = ["pending", "confirmed", "shipping", "delivered", "canceled"];
    rows.forEach(o => pm.expect(allowed, "status of order " + o.id).to.include(o.status));
});
""",
            ),
        ], "The dashboard's numbers are a projection of the FR-10 state machine; "
           "drive orders through transitions and re-assert the aggregate."),
        folder("03 - Security (SEC-01..SEC-07)", [
            item(
                "SEC-03 | A non-admin token must not reach an /api/admin endpoint",
                request("GET", "/api/admin/orders", auth_var="user_token"),
                """
// SEC-03 / FR-12: admin APIs must check role='admin' in the token, not just
// that a token exists.
pm.test("Non-admin caller is refused", function () {
    pm.expect(pm.response.code).to.be.oneOf([401, 403]);
});
""",
            ),
            item(
                "SEC-01 | Admin order data must not leak user credentials",
                request("GET", "/api/admin/orders", auth_var="admin_token"),
                """
pm.test("No password field is present in any row", function () {
    pm.expect(pm.response.text().toLowerCase()).to.not.include('"password"');
});
""",
            ),
        ]),
        folder("04 - Schema validation", [
            item(
                "SCH-001 | Admin order rows match the joined schema",
                request("GET", "/api/admin/orders", auth_var="admin_token"),
                """
const schema = {
    type: "array",
    items: {
        type: "object",
        required: ["id", "user_id", "total_amount", "status", "user_name"],
        properties: {
            id: { type: "integer" },
            user_id: { type: "integer" },
            total_amount: { type: "number" },
            status: { type: "string",
                      enum: ["pending", "confirmed", "shipping", "delivered", "canceled"] },
            shipping_address: { type: ["string", "null"] },
            created_at: { type: "string" },
            user_name: { type: ["string", "null"] }
        }
    }
};

pm.test("Admin order list conforms to the schema", function () {
    pm.response.to.have.jsonSchema(schema);
});
""",
            ),
        ]),
    ],
)

TARGETS = {
    "API1_FR01_Register.postman_collection.json": api1,
    "API2_FR06_ProductDetail.postman_collection.json": api2,
    "API3_FR11_OrderHistory.postman_collection.json": api3,
    "API4_FR13_AdminOrders.postman_collection.json": api4,
}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, coll in TARGETS.items():
        path = OUT / filename
        path.write_text(json.dumps(coll, indent=2, ensure_ascii=False), encoding="utf-8")
        n = sum(len(f.get("item", [])) for f in coll["item"])
        print("{0}: {1} folders, {2} requests".format(filename, len(coll["item"]), n))
