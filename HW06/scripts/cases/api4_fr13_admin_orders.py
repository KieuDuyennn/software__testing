#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test-case specification for API 4 - FR-13 Admin Dashboard.

Endpoint: GET /api/admin/orders     Pool C     Requirement FR-13 (with FR-12)

FR-13 as written in the requirement document:
  - "Hiển thị tổng doanh thu: Chỉ tính tổng `total_amount` của các đơn có
    `status = 'delivered'`" - total revenue sums delivered orders only.
  - "Hiển thị tổng số đơn hàng" - and the total order count.

The dashboard has no endpoint of its own; both figures are derived from
`GET /api/admin/orders`, so that endpoint is the API under test. The revenue
rule is what makes this collection an FR-10 test too: the aggregate is a
projection of the order state machine, and it must move only when an order
actually reaches `delivered`.

FR-12 / SEC-03 bind the route as well: admin APIs must verify `role = 'admin'`
in the token, not merely that a token exists.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _helpers import (  # noqa: E402
    ADMIN_ORDER_SCHEMA, admin_login, create_order, fresh_user, is_array, js,
    json_content_type, no500, no_credentials, no_leak, order_in_state, rejected,
    st,
)

CASES = []


def add(**kw):
    CASES.append(kw)
    return kw


ADMIN_ORDERS = "/api/admin/orders"

FORGED = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
          ".eyJpZCI6MSwicm9sZSI6ImFkbWluIn0"
          ".ZmFrZXNpZ25hdHVyZV9ub3RfZnJvbV90aGVfc2VydmVy")


def hdr(value):
    return [{"key": "Authorization", "value": value}]


def revenue_js():
    """Compute the dashboard's two figures from the payload, FR-13's way."""
    return """
const rows = pm.response.json();
const delivered = rows.filter(function (o) { return o.status === "delivered"; });
const revenue = delivered.reduce(function (s, o) {
    return s + Number(o.total_amount || 0);
}, 0);
pm.variables.set("computedRevenue", revenue);
pm.variables.set("computedCount", rows.length);
console.log("[HW06] orders=" + rows.length + " delivered=" + delivered.length +
            " revenue=" + revenue);
"""


def admin_ok():
    return is_array() + js("""
pm.test("Status is 200", () => pm.response.to.have.status(200));""")


# ===========================================================================
# STEP 2 - DOMAIN PARTITIONS
# ===========================================================================

# --- authorisation partitions ----------------------------------------------

add(id="A4-DP-001", dim="Domain", param="authorization", rule="FR-13",
    partition="valid: an admin token",
    title="An admin receives the full order list",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(admin_login()), expected="200 with an array of every order",
    tests=admin_ok())

add(id="A4-DP-002", dim="Domain", param="authorization", rule="SEC-02",
    partition="invalid: no Authorization header",
    title="An unauthenticated request is rejected",
    method="GET", path=ADMIN_ORDERS, expected="401", tests=st(401))

add(id="A4-DP-003", dim="Domain", param="authorization", rule="SEC-02",
    partition="invalid: empty bearer token",
    title="An empty bearer token is rejected",
    method="GET", path=ADMIN_ORDERS, extra_headers=hdr("Bearer "),
    expected="401", tests=rejected("empty token", 401, 403))

add(id="A4-DP-004", dim="Domain", param="authorization", rule="SEC-02",
    partition="invalid: malformed token",
    title="A malformed token is rejected",
    method="GET", path=ADMIN_ORDERS,
    extra_headers=hdr("Bearer not.a.real.token"),
    expected="403", tests=rejected("malformed token", 401, 403))

add(id="A4-DP-005", dim="Domain", param="authorization", rule="SEC-02",
    partition="invalid: signature from another key",
    title="A token signed with a different key is rejected",
    method="GET", path=ADMIN_ORDERS, extra_headers=hdr("Bearer " + FORGED),
    expected="403", tests=rejected("bad signature", 401, 403))

add(id="A4-DP-006", dim="Domain", param="authorization", rule="SEC-02",
    partition="invalid: wrong authentication scheme",
    title="Basic authentication is rejected",
    method="GET", path=ADMIN_ORDERS,
    extra_headers=hdr("Basic YWRtaW46QWRtaW4xMjMh"),
    expected="401", tests=rejected("wrong scheme", 401, 403))

add(id="A4-DP-007", dim="Domain", param="authorization", rule="SEC-02",
    partition="invalid: token with no Bearer scheme",
    title="A bare token with no scheme is rejected",
    method="GET", path=ADMIN_ORDERS, extra_headers=hdr("{{adminTok}}"),
    pre=js(admin_login()), expected="401",
    tests=rejected("missing Bearer scheme", 401, 403))

add(id="A4-DP-008", dim="Domain", param="authorization", rule="SEC-03 / FR-12",
    partition="invalid: a valid NON-admin token",
    title="An ordinary user's token is rejected",
    method="GET", path=ADMIN_ORDERS, auth_var="tok",
    pre=js(fresh_user()),
    expected="403 - SEC-03 requires role='admin', not merely a valid token",
    tests=rejected("caller is not an admin", 401, 403))

# --- content partitions ----------------------------------------------------

add(id="A4-DP-009", dim="Domain", param="-", rule="FR-13",
    partition="content: every order in the system is listed",
    title="The admin list includes orders belonging to other users",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(fresh_user(on_done=create_order(amount=131000,
                                           on_done=admin_login()))),
    expected="the order created by an unrelated user appears in the list",
    tests=admin_ok() + js("""
pm.test("Another user's order is visible to the admin", function () {
    const target = Number(pm.variables.get("orderId"));
    const found = pm.response.json().some(function (o) {
        return Number(o.id) === target;
    });
    pm.expect(found, "order " + target + " must be in the admin list").to.be.true;
});"""))

add(id="A4-DP-010", dim="Domain", param="-", rule="FR-13",
    partition="content: the ordering user's name is joined in",
    title="Each row carries the ordering user's name",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(fresh_user(on_done=create_order(on_done=admin_login()))),
    expected="every row has a user_name field",
    tests=js("""
pm.test("Every row carries user_name", function () {
    pm.response.json().forEach(function (o) {
        pm.expect(o, "order " + o.id).to.have.property("user_name");
    });
});"""))

add(id="A4-DP-011", dim="Domain", param="-", rule="FR-13",
    partition="content: order count is the row count",
    title="The dashboard's order count equals the number of rows returned",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(fresh_user(on_done=create_order(on_done=admin_login()))),
    expected="at least one order exists and the count is well defined",
    tests=revenue_js() + js("""
pm.test("Order count is a non-negative integer", function () {
    pm.expect(Number.isInteger(rows.length)).to.be.true;
    pm.expect(rows.length).to.be.at.least(1);
});"""))

add(id="A4-DP-012", dim="Domain", param="-", rule="FR-13",
    partition="content: an order whose user was deleted",
    title="An order whose user was deleted still appears, with a null user_name",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(fresh_user(on_done=create_order(on_done=admin_login("""
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/admin/users/" +
         pm.variables.get("tok_uid"),
    method: "DELETE",
    header: { "X-Student-Id": pm.environment.get("student_id"),
              "Authorization": "Bearer " + pm.variables.get("adminTok") }
}, function () {});""")))),
    expected="the LEFT JOIN keeps the order; user_name is null rather than missing",
    tests=admin_ok() + js("""
pm.test("The orphaned order is still listed", function () {
    const target = Number(pm.variables.get("orderId"));
    const found = pm.response.json().find(function (o) {
        return Number(o.id) === target;
    });
    pm.expect(found, "order " + target).to.not.be.undefined;
    pm.expect(found).to.have.property("user_name");
});"""),
    gap="The spec does not define how orphaned orders are presented.")

add(id="A4-DP-013", dim="Domain", param="query string", rule="FR-13",
    partition="undocumented query parameters are ignored",
    title="Unknown query parameters do not filter the admin list",
    method="GET", path=ADMIN_ORDERS,
    raw_query="?status=delivered&limit=1&user_id=999", auth_var="adminTok",
    pre=js(fresh_user(on_done=create_order(on_done=admin_login()))),
    expected="the full list is still returned - the spec defines no parameters",
    tests=admin_ok() + js("""
pm.test("The list is not filtered by undocumented parameters", function () {
    const target = Number(pm.variables.get("orderId"));
    pm.expect(pm.response.json().some(function (o) {
        return Number(o.id) === target;
    }), "a pending order must still be listed").to.be.true;
});"""))

add(id="A4-DP-014", dim="Domain", param="-", rule="FR-13",
    partition="ordering is stable across calls",
    title="The admin list returns a deterministic order",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(admin_login("""
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/admin/orders",
    method: "GET",
    header: { "X-Student-Id": pm.environment.get("student_id"),
              "Authorization": "Bearer " + pm.variables.get("adminTok") }
}, function (err, res) {
    if (res) {
        pm.variables.set("firstIds",
            JSON.stringify(res.json().map(function (o) { return o.id; })));
    }
});""")),
    expected="the id sequence is identical between two consecutive calls",
    tests=js("""
pm.test("Ordering is deterministic", function () {
    const now = JSON.stringify(pm.response.json().map(function (o) { return o.id; }));
    pm.expect(now).to.eql(pm.variables.get("firstIds"));
});"""))

# --- HTTP methods ----------------------------------------------------------

for _i, _method in enumerate(["POST", "PUT", "DELETE", "PATCH"]):
    add(id="A4-DP-%03d" % (15 + _i), dim="Domain", param="http method",
        rule="spec conformance",
        partition="invalid: %s on the admin order list" % _method,
        title="%s /api/admin/orders is not routed" % _method,
        method=_method, path=ADMIN_ORDERS, auth_var="adminTok", body=None,
        pre=js(admin_login()),
        expected="404 or 405 - the spec documents GET only",
        tests=st(404, 405))


# ===========================================================================
# STEP 3 - STATE TRANSITIONS (FR-10, projected into the dashboard aggregate)
# ===========================================================================
# FR-13's revenue figure must move only when an order actually reaches
# `delivered`. Each case builds an order in a known state and checks whether the
# aggregate counts it.

def revenue_excludes(state, amount):
    return revenue_js() + js("""
pm.test("An order in '%s' is NOT counted toward revenue", function () {
    const target = Number(pm.variables.get("orderId"));
    const row = rows.find(function (o) { return Number(o.id) === target; });
    pm.expect(row, "order " + target + " must be listed").to.not.be.undefined;
    pm.expect(row.status).to.eql("%s");
    const counted = delivered.some(function (o) { return Number(o.id) === target; });
    pm.expect(counted,
        "FR-13 counts only delivered orders toward revenue").to.be.false;
});
pm.test("An order in '%s' IS counted toward the order total", function () {
    pm.expect(rows.length, "every order counts toward the count").to.be.at.least(1);
});""" % (state, state, state))


for _i, _state in enumerate(["pending", "confirmed", "shipping", "canceled"]):
    add(id="A4-ST-%03d" % (1 + _i), dim="State", param="-", rule="FR-13 / FR-10",
        partition="revenue excludes orders in '%s'" % _state,
        title="An order in '%s' does not contribute to revenue" % _state,
        method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
        pre=js(order_in_state(_state, amount=500000, prefix="r" + _state[:2])),
        expected="the order is listed but excluded from the revenue sum",
        tests=revenue_excludes(_state, 500000))

add(id="A4-ST-005", dim="State", param="-", rule="FR-13 / FR-10",
    partition="revenue includes orders in 'delivered'",
    title="A delivered order contributes its total to revenue",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(order_in_state("delivered", amount=500000, prefix="rdl")),
    expected="the order appears in the delivered set and its 500000 is summed",
    tests=revenue_js() + js("""
pm.test("The delivered order is counted toward revenue", function () {
    const target = Number(pm.variables.get("orderId"));
    const counted = delivered.some(function (o) { return Number(o.id) === target; });
    pm.expect(counted, "order " + target + " is delivered").to.be.true;
});
pm.test("Revenue is at least this order's total", function () {
    pm.expect(revenue).to.be.at.least(500000);
});"""))

add(id="A4-ST-006", dim="State", param="-", rule="FR-13 / FR-10",
    partition="revenue moves only on reaching delivered",
    title="Revenue increases by exactly the order's total when it is delivered",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(order_in_state("shipping", amount=400000, prefix="rmv", on_done="""
// Snapshot revenue while the order is still 'shipping', then deliver it.
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/admin/orders",
    method: "GET",
    header: { "X-Student-Id": pm.environment.get("student_id"),
              "Authorization": "Bearer " + pm.variables.get("adminTok") }
}, function (err, res) {
    let before = 0;
    if (res) {
        before = res.json()
            .filter(function (o) { return o.status === "delivered"; })
            .reduce(function (s, o) { return s + Number(o.total_amount || 0); }, 0);
    }
    pm.variables.set("revenueBefore", before);
    pm.sendRequest({
        url: pm.environment.get("base_url") + "/api/admin/orders/" +
             pm.variables.get("orderId") + "/status",
        method: "PUT",
        header: { "Content-Type": "application/json",
                  "X-Student-Id": pm.environment.get("student_id"),
                  "Authorization": "Bearer " + pm.variables.get("adminTok") },
        body: { mode: "raw", raw: JSON.stringify({ status: "delivered" }) }
    }, function () {});
});""")),
    expected="revenue after - revenue before === 400000, exactly",
    tests=revenue_js() + js("""
pm.test("Revenue rose by exactly the delivered order's total", function () {
    const before = Number(pm.variables.get("revenueBefore"));
    pm.expect(revenue - before,
        "delivering a 400000 order must add exactly 400000").to.eql(400000);
});"""))

add(id="A4-ST-007", dim="State", param="-", rule="FR-13 / FR-10",
    partition="cancellation does not remove an order from the count",
    title="A cancelled order still counts toward the total order number",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(order_in_state("canceled", amount=300000, prefix="ccx")),
    expected="the order is still listed - FR-13 counts orders, not sales",
    tests=js("""
pm.test("A cancelled order remains in the order list", function () {
    const target = Number(pm.variables.get("orderId"));
    pm.expect(pm.response.json().some(function (o) {
        return Number(o.id) === target;
    })).to.be.true;
});"""))

_ILLEGAL = [
    ("pending", "shipping"),
    ("pending", "delivered"),
    ("confirmed", "delivered"),
    ("confirmed", "pending"),
    ("shipping", "pending"),
    ("delivered", "shipping"),
    ("delivered", "pending"),
    ("delivered", "canceled"),
    ("canceled", "delivered"),
    ("canceled", "confirmed"),
]

for _i, (_from, _to) in enumerate(_ILLEGAL):
    add(id="A4-ST-%03d" % (8 + _i), dim="State", param="-", rule="FR-10",
        partition="ILLEGAL transition through the admin route: %s -> %s"
                  % (_from, _to),
        title="Admin transition %s -> %s must be refused" % (_from, _to),
        method="PUT", path="/api/admin/orders/{{orderId}}/status",
        auth_var="adminTok", body={"status": _to},
        pre=js(order_in_state(_from, prefix="a" + _from[:2] + _to[:2])),
        expected="400 - FR-10 does not permit %s -> %s" % (_from, _to),
        tests=rejected("%s -> %s is not a legal transition" % (_from, _to)))

add(id="A4-ST-018", dim="State", param="-", rule="FR-10",
    partition="legal transition through the admin route",
    title="Admin transition pending -> confirmed is accepted",
    method="PUT", path="/api/admin/orders/{{orderId}}/status",
    auth_var="adminTok", body={"status": "confirmed"},
    pre=js(order_in_state("pending", prefix="lg")),
    expected="200 - the positive control for the illegal-transition cases",
    tests=st(200))

add(id="A4-ST-019", dim="State", param="-", rule="FR-10",
    partition="status value outside the closed set",
    title="An unrecognised status value is refused",
    method="PUT", path="/api/admin/orders/{{orderId}}/status",
    auth_var="adminTok", body={"status": "refunded"},
    pre=js(order_in_state("pending", prefix="uk")),
    expected="400 - the FR-10 status set is closed",
    tests=rejected("unknown status value"))

add(id="A4-ST-020", dim="State", param="-", rule="FR-10",
    partition="status omitted from the request",
    title="A status update with no status field is refused",
    method="PUT", path="/api/admin/orders/{{orderId}}/status",
    auth_var="adminTok", body={},
    pre=js(order_in_state("pending", prefix="ns")),
    expected="400", tests=rejected("no status supplied"))

add(id="A4-ST-021", dim="State", param="-", rule="FR-10",
    partition="transition on an order that does not exist",
    title="Updating the status of a non-existent order returns 404",
    method="PUT", path="/api/admin/orders/987654/status",
    auth_var="adminTok", body={"status": "confirmed"},
    pre=js(admin_login()), expected="404", tests=st(404))

add(id="A4-ST-022", dim="State", param="-", rule="FR-13 / FR-10",
    partition="aggregate consistency after a full lifecycle",
    title="Revenue and count stay consistent after a complete lifecycle",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(order_in_state("delivered", amount=250000, prefix="fl")),
    expected="revenue equals the sum over exactly the delivered rows",
    tests=revenue_js() + js("""
pm.test("Revenue is exactly the sum over the delivered rows", function () {
    const recomputed = rows
        .filter(function (o) { return o.status === "delivered"; })
        .reduce(function (s, o) { return s + Number(o.total_amount || 0); }, 0);
    pm.expect(revenue).to.eql(recomputed);
});
pm.test("No non-delivered order leaks into the revenue set", function () {
    const wrong = delivered.filter(function (o) { return o.status !== "delivered"; });
    pm.expect(wrong).to.eql([]);
});"""))


# ===========================================================================
# STEP 4 - SECURITY (SEC-01 .. SEC-07)
# ===========================================================================

add(id="A4-SEC-001", dim="Security", param="-", rule="SEC-03 / FR-12",
    partition="privilege escalation: ordinary user reads the admin list",
    title="A non-admin token must not reach GET /api/admin/orders",
    method="GET", path=ADMIN_ORDERS, auth_var="tok",
    pre=js(fresh_user()),
    expected="403 - the token's role claim is 'user'",
    tests=rejected("caller is not an admin", 401, 403))

add(id="A4-SEC-002", dim="Security", param="-", rule="SEC-03 / FR-12",
    partition="privilege escalation: the seeded ordinary account",
    title="The seeded test user must not reach the admin order list",
    method="GET", path=ADMIN_ORDERS, auth_var="tok",
    pre=js(js("""
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/login",
    method: "POST",
    header: { "Content-Type": "application/json",
              "X-Student-Id": pm.environment.get("student_id") },
    body: { mode: "raw", raw: JSON.stringify({
        email: pm.environment.get("user_email"),
        password: pm.environment.get("user_password") }) }
}, function (err, res) {
    if (res && res.json() && res.json().token) {
        pm.variables.set("tok", res.json().token);
    }
});""")),
    expected="403", tests=rejected("caller is not an admin", 401, 403))

add(id="A4-SEC-003", dim="Security", param="-", rule="SEC-03",
    partition="privilege escalation: forged admin token",
    title="A forged token claiming role=admin is rejected",
    method="GET", path=ADMIN_ORDERS, extra_headers=hdr("Bearer " + FORGED),
    expected="403 - the signature is not the server's",
    tests=rejected("forged token", 401, 403))

add(id="A4-SEC-004", dim="Security", param="-", rule="SEC-03 / SEC-06",
    partition="privilege escalation: tampered role claim",
    title="A real user token with role edited to admin is rejected",
    method="GET", path=ADMIN_ORDERS, extra_headers=hdr("Bearer {{tamperedTok}}"),
    pre=js(fresh_user(on_done="""
const parts = String(pm.variables.get("tok")).split(".");
if (parts.length === 3) {
    const payload = JSON.parse(Buffer.from(parts[1], "base64").toString());
    payload.role = "admin";
    const forged = Buffer.from(JSON.stringify(payload))
        .toString("base64").replace(/=+$/, "");
    pm.variables.set("tamperedTok", parts[0] + "." + forged + "." + parts[2]);
}""")),
    expected="403 - the signature no longer matches the payload",
    tests=rejected("tampered role claim", 401, 403))

add(id="A4-SEC-005", dim="Security", param="-", rule="SEC-03 / FR-12",
    partition="privilege escalation: user driving the state machine",
    title="A non-admin must not perform a legal status transition",
    method="PUT", path="/api/admin/orders/{{orderId}}/status", auth_var="tok",
    # A LEGAL transition, so a 400 cannot be mistaken for authorisation working.
    body={"status": "confirmed"},
    pre=js(order_in_state("pending", prefix="ue", on_done=fresh_user(prefix="uz"))),
    expected="403 - authorisation must be checked before the transition rules",
    tests=rejected("caller is not an admin", 401, 403))

add(id="A4-SEC-006", dim="Security", param="-", rule="SEC-03 / FR-12",
    partition="privilege escalation: user listing all accounts",
    title="A non-admin must not reach the admin user list",
    method="GET", path="/api/admin/users", auth_var="tok",
    pre=js(fresh_user()), expected="403",
    tests=rejected("caller is not an admin", 401, 403))

add(id="A4-SEC-007", dim="Security", param="-", rule="SEC-03 / FR-12",
    partition="privilege escalation: user deleting an account",
    title="A non-admin must not be able to delete a user",
    method="DELETE", path="/api/admin/users/{{victimUid}}", auth_var="tok",
    pre=js(fresh_user(var="victimTok", prefix="vd", on_done="""
pm.variables.set("victimUid", pm.variables.get("victimTok_uid"));
""" + fresh_user(prefix="ad"))),
    expected="403 - destructive admin operations need role='admin'",
    tests=rejected("caller is not an admin", 401, 403))

add(id="A4-SEC-008", dim="Security", param="-", rule="SEC-01",
    partition="information disclosure: credentials in the admin payload",
    title="The admin order list exposes no password material",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(admin_login()),
    expected="no password field and no seeded plaintext anywhere in the body",
    tests=no_credentials())

add(id="A4-SEC-009", dim="Security", param="-", rule="SEC-01",
    partition="information disclosure: session material in the payload",
    title="The admin order list exposes no tokens or reset codes",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(admin_login()),
    expected="no token, reset_token or role key on an order row",
    tests=js("""
const text = pm.response.text().toLowerCase();
["\\"token\\"", "\\"reset_token\\"", "\\"role\\""].forEach(function (key) {
    pm.test("Admin order payload contains no " + key + " field", function () {
        pm.expect(text).to.not.include(key);
    });
});"""))

_INJECTIONS = [
    ("1 OR 1=1", "tautology"),
    ("1; DROP TABLE orders;--", "statement termination"),
    ("1 UNION SELECT id,email,password,role FROM users--", "UNION SELECT against users"),
]

for _i, (_payload, _label) in enumerate(_INJECTIONS):
    add(id="A4-SEC-%03d" % (10 + _i), dim="Security", param="id", rule="SEC-05",
        partition="SQL injection through the status route id: %s" % _label,
        title="Injection via the admin status route (%s) is neutralised" % _label,
        method="PUT", path="/api/admin/orders/%s/status" % _payload,
        auth_var="adminTok", body={"status": "confirmed"},
        pre=js(admin_login()),
        expected="no 5xx, no SQL error, no credential leak",
        tests=no500() + "\n" + no_leak() + "\n" + no_credentials())

add(id="A4-SEC-013", dim="Security", param="status", rule="SEC-05",
    partition="SQL injection through the status value",
    title="Injection in the status field is neutralised",
    method="PUT", path="/api/admin/orders/{{orderId}}/status",
    auth_var="adminTok", body={"status": "confirmed'; DROP TABLE orders;--"},
    pre=js(order_in_state("pending", prefix="si")),
    expected="4xx (not a legal status) with no SQL error and no 5xx",
    tests=no500() + "\n" + no_leak())

add(id="A4-SEC-014", dim="Security", param="-", rule="SEC-05",
    partition="data integrity after the injection attempts",
    title="The orders table survives the injection attempts intact",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(order_in_state("pending", prefix="ig", on_done="""
const base = pm.environment.get("base_url");
const sid = pm.environment.get("student_id");
["1; DROP TABLE orders;--", "1 OR 1=1"].forEach(function (payload) {
    pm.sendRequest({
        url: base + "/api/admin/orders/" + encodeURIComponent(payload) + "/status",
        method: "PUT",
        header: { "Content-Type": "application/json", "X-Student-Id": sid,
                  "Authorization": "Bearer " + pm.variables.get("adminTok") },
        body: { mode: "raw", raw: JSON.stringify({ status: "confirmed" }) }
    }, function () {});
});""")),
    expected="the fixture order is still listed",
    tests=admin_ok() + js("""
pm.test("The order survived the injection attempts", function () {
    const target = Number(pm.variables.get("orderId"));
    pm.expect(pm.response.json().some(function (o) {
        return Number(o.id) === target;
    })).to.be.true;
});"""))

add(id="A4-SEC-015", dim="Security", param="-", rule="SEC-05",
    partition="information disclosure on error",
    title="An invalid admin request must not leak database internals",
    method="PUT", path="/api/admin/orders/';--/status",
    auth_var="adminTok", body={"status": "confirmed"},
    pre=js(admin_login()),
    expected="a clean 4xx with no driver, table or stack detail",
    tests=no_leak() + "\n" + no500())

add(id="A4-SEC-016", dim="Security", param="-", rule="SEC-02",
    partition="unauthenticated state change",
    title="Changing an order's status without a token must be refused",
    method="PUT", path="/api/admin/orders/{{orderId}}/status",
    body={"status": "delivered"},
    pre=js(order_in_state("pending", prefix="na")),
    expected="401", tests=rejected("no token supplied", 401, 403))

add(id="A4-SEC-017", dim="Security", param="-", rule="FR-13",
    partition="revenue cannot be inflated by an unauthorised transition",
    title="A non-admin cannot inflate revenue by delivering their own order",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(order_in_state("shipping", amount=900000, prefix="inf", on_done="""
// The order's owner tries to mark it delivered using their own token.
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/admin/orders/" +
         pm.variables.get("orderId") + "/status",
    method: "PUT",
    header: { "Content-Type": "application/json",
              "X-Student-Id": pm.environment.get("student_id"),
              "Authorization": "Bearer " + pm.variables.get("tok") },
    body: { mode: "raw", raw: JSON.stringify({ status: "delivered" }) }
}, function () {});""")),
    expected="the order is still 'shipping' and contributes nothing to revenue",
    tests=revenue_js() + js("""
pm.test("The self-service delivery did not take effect", function () {
    const target = Number(pm.variables.get("orderId"));
    const row = rows.find(function (o) { return Number(o.id) === target; });
    pm.expect(row, "order " + target).to.not.be.undefined;
    pm.expect(row.status,
        "a customer must not be able to mark their own order delivered")
        .to.eql("shipping");
});"""))

add(id="A4-SEC-018", dim="Security", param="-", rule="SEC-02",
    partition="positive control: a genuine admin is allowed",
    title="A genuine admin token is accepted",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(admin_login()),
    expected="200 - the positive control for every rejection case above",
    tests=admin_ok())


# ===========================================================================
# STEP 5 - SCHEMA VALIDATION
# ===========================================================================

add(id="A4-SCH-001", dim="Schema", param="-", rule="spec conformance",
    partition="admin order rows: array schema",
    title="The admin order list validates against the joined order schema",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(fresh_user(on_done=create_order(on_done=admin_login()))),
    expected="every row validates against the admin order schema",
    tests=ADMIN_ORDER_SCHEMA + js("""
pm.test("Every row conforms to the admin order schema", function () {
    pm.response.to.have.jsonSchema({ type: "array", items: adminOrderSchema });
});"""))

add(id="A4-SCH-002", dim="Schema", param="status", rule="FR-10",
    partition="status drawn from the closed FR-10 set",
    title="Every row's status is one of the five FR-10 states",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(admin_login()),
    expected="status in [pending, confirmed, shipping, delivered, canceled]",
    tests=js("""
const allowed = ["pending", "confirmed", "shipping", "delivered", "canceled"];
pm.test("All statuses come from the FR-10 state set", function () {
    pm.response.json().forEach(function (o) {
        pm.expect(allowed, "status of order " + o.id).to.include(o.status);
    });
});"""))

add(id="A4-SCH-003", dim="Schema", param="total_amount", rule="FR-13",
    partition="total_amount type",
    title="total_amount is a JSON number in every row",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(fresh_user(on_done=create_order(on_done=admin_login()))),
    expected="revenue is summed from this field, so it must be arithmetic-safe",
    tests=js("""
const offenders = pm.response.json()
    .filter(function (o) { return typeof o.total_amount !== "number"; })
    .map(function (o) { return o.id; });
pm.test("No row types total_amount as a string", function () {
    pm.expect(offenders,
        "a string total would make the revenue sum concatenate").to.eql([]);
});"""))

add(id="A4-SCH-004", dim="Schema", param="id", rule="FR-13",
    partition="order id type",
    title="Every row's id is a JSON integer",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(admin_login()), expected="Number.isInteger(id) for every row",
    tests=js("""
pm.test("Every order id is an integer", function () {
    pm.response.json().forEach(function (o) {
        pm.expect(Number.isInteger(o.id), "order id " + o.id).to.be.true;
    });
});"""))

add(id="A4-SCH-005", dim="Schema", param="user_name", rule="FR-13",
    partition="user_name type",
    title="user_name is a string or null, never missing",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(fresh_user(on_done=create_order(on_done=admin_login()))),
    expected="the joined field is present on every row",
    tests=js("""
pm.test("user_name is present and correctly typed on every row", function () {
    pm.response.json().forEach(function (o) {
        pm.expect(o, "order " + o.id).to.have.property("user_name");
        const t = typeof o.user_name;
        pm.expect(t === "string" || o.user_name === null,
            "user_name of order " + o.id + " was a " + t).to.be.true;
    });
});"""))

add(id="A4-SCH-006", dim="Schema", param="created_at", rule="FR-13",
    partition="created_at parseability",
    title="created_at is present and parseable on every row",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(fresh_user(on_done=create_order(on_done=admin_login()))),
    expected="the dashboard displays order dates, so they must parse",
    tests=js("""
pm.test("created_at parses as a date on every row", function () {
    pm.response.json().forEach(function (o) {
        pm.expect(isNaN(Date.parse(o.created_at)),
            "created_at of order " + o.id + ": " + o.created_at).to.be.false;
    });
});"""))

add(id="A4-SCH-007", dim="Schema", param="user_id", rule="FR-13",
    partition="user_id type",
    title="user_id is an integer or null on every row",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(admin_login()), expected="integer, or null for an orphaned order",
    tests=js("""
pm.test("user_id is an integer or null", function () {
    pm.response.json().forEach(function (o) {
        pm.expect(Number.isInteger(o.user_id) || o.user_id === null,
            "user_id of order " + o.id).to.be.true;
    });
});"""))

add(id="A4-SCH-008", dim="Schema", param="-", rule="spec conformance",
    partition="response headers",
    title="The admin order list is served as application/json",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(admin_login()), expected="Content-Type includes application/json",
    tests=json_content_type())

add(id="A4-SCH-009", dim="Schema", param="-", rule="spec conformance",
    partition="error body: unauthorised shape",
    title="An unauthorised request returns a structured error body",
    method="GET", path=ADMIN_ORDERS,
    expected='401 with {"error": "<string>"}',
    tests=js("""
pm.test("Status is 401", () => pm.response.to.have.status(401));
pm.test("Error body is structured JSON", function () {
    const b = pm.response.json();
    pm.expect(b).to.have.property("error");
    pm.expect(b.error).to.be.a("string");
});"""))

add(id="A4-SCH-010", dim="Schema", param="-", rule="spec conformance",
    partition="error body: forbidden shape",
    title="A forbidden request returns a structured error body",
    method="GET", path=ADMIN_ORDERS, auth_var="tok",
    pre=js(fresh_user()),
    expected='403 with {"error": "<string>"}',
    tests=js("""
pm.test("Status is 403", function () {
    pm.expect(pm.response.code).to.be.oneOf([401, 403]);
});
pm.test("Error body is structured JSON", function () {
    pm.expect(pm.response.json()).to.have.property("error");
});"""))

add(id="A4-SCH-011", dim="Schema", param="-", rule="spec conformance",
    partition="status update: success body shape",
    title="A successful status update returns a structured message",
    method="PUT", path="/api/admin/orders/{{orderId}}/status",
    auth_var="adminTok", body={"status": "confirmed"},
    pre=js(order_in_state("pending", prefix="sb")),
    expected='200 with {"message": "<string>"}',
    tests=js("""
pm.test("Status is 200", () => pm.response.to.have.status(200));
pm.test("Body carries a message", function () {
    const b = pm.response.json();
    pm.expect(b).to.have.property("message");
    pm.expect(b.message).to.be.a("string");
});"""))

add(id="A4-SCH-012", dim="Schema", param="-", rule="spec conformance",
    partition="status update: error body shape",
    title="A refused transition returns a structured error body",
    method="PUT", path="/api/admin/orders/{{orderId}}/status",
    auth_var="adminTok", body={"status": "delivered"},
    pre=js(order_in_state("pending", prefix="eb")),
    expected='400 with {"error": "<string>"}',
    tests=js("""
pm.test("Illegal transition is refused", function () {
    pm.expect(pm.response.code).to.be.within(400, 499);
});
pm.test("Error body is structured JSON", function () {
    const b = pm.response.json();
    pm.expect(b).to.have.property("error");
    pm.expect(b.error).to.be.a("string");
});"""))

add(id="A4-SCH-013", dim="Schema", param="-", rule="FR-13",
    partition="aggregate is computable from the payload alone",
    title="Both dashboard figures are derivable from the response",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(order_in_state("delivered", amount=123000, prefix="ag")),
    expected="revenue and count are both finite numbers",
    tests=revenue_js() + js("""
pm.test("Revenue is a finite number", function () {
    pm.expect(Number.isFinite(revenue),
        "a string total_amount would make this NaN or a concatenation").to.be.true;
});
pm.test("Order count is a finite number", function () {
    pm.expect(Number.isFinite(rows.length)).to.be.true;
});"""))

add(id="A4-SCH-014", dim="Schema", param="-", rule="spec conformance",
    partition="no undocumented fields on an admin row",
    title="Admin rows carry no fields beyond the documented set",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(fresh_user(on_done=create_order(on_done=admin_login()))),
    expected="keys are a subset of the seven documented fields",
    tests=js("""
const documented = ["id", "user_id", "total_amount", "status",
                    "shipping_address", "created_at", "user_name"];
pm.test("No undocumented fields appear on an admin order row", function () {
    pm.response.json().forEach(function (o) {
        const extra = Object.keys(o).filter(function (k) {
            return documented.indexOf(k) === -1;
        });
        pm.expect(extra, "undocumented fields on order " + o.id).to.eql([]);
    });
});"""))

add(id="A4-SCH-015", dim="Schema", param="-", rule="spec conformance",
    partition="error body: not an HTML page",
    title="Errors on this route are JSON, never an HTML page",
    method="GET", path=ADMIN_ORDERS,
    extra_headers=hdr("Bearer broken.token.here"),
    expected="Content-Type is not text/html",
    tests=js("""
pm.test("Error response is not an HTML page", function () {
    pm.expect((pm.response.headers.get("Content-Type") || "").toLowerCase())
      .to.not.include("text/html");
});"""))


# ===========================================================================
# PHASE 3 - STUDENT-DESIGNED EXTENSIONS
# ===========================================================================

add(id="A4-HR-001", dim="State", param="-", rule="FR-13 / FR-10",
    partition="aggregate additivity across two delivered orders",
    title="Two delivered orders contribute the exact sum of their totals",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(order_in_state("delivered", amount=111000, order_var="orderOne", prefix="hr1",
        on_done=order_in_state("delivered", amount=222000, order_var="orderTwo", prefix="hr2"))),
    expected="both rows are delivered and contribute 333000 in total",
    tests=revenue_js() + js("""
pm.test("Both fixture orders contribute exactly 333000", function () {
    const ids = [Number(pm.variables.get("orderOne")), Number(pm.variables.get("orderTwo"))];
    const fixtures = rows.filter(function (o) { return ids.indexOf(Number(o.id)) !== -1; });
    pm.expect(fixtures).to.have.lengthOf(2);
    pm.expect(fixtures.every(function (o) { return o.status === "delivered"; })).to.be.true;
    pm.expect(fixtures.reduce(function (s, o) { return s + Number(o.total_amount); }, 0)).to.eql(333000);
});"""), origin="Student-designed",
    rationale="The AI tested one delivered order but not additivity across multiple rows, where aggregation bugs commonly appear.")

add(id="A4-HR-002", dim="Schema", param="id", rule="FR-13",
    partition="identity uniqueness across the admin payload",
    title="The admin order list contains no duplicate order ids",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok", pre=js(admin_login()),
    expected="every id occurs exactly once",
    tests=js("""
pm.test("Order ids are unique in the dashboard payload", function () {
    const ids = pm.response.json().map(function (o) { return String(o.id); });
    pm.expect(new Set(ids).size).to.eql(ids.length);
});"""), origin="Student-designed",
    rationale="The AI checked id types and list count but omitted uniqueness, which protects both count and revenue from join duplication.")

add(id="A4-HR-003", dim="State", param="-", rule="FR-10 / FR-13",
    partition="terminal-state idempotence: delivered -> delivered",
    title="Repeating delivered on a delivered order is refused and non-mutating",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(order_in_state("delivered", amount=345000, prefix="hrdd", on_done="""
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/admin/orders/" +
         pm.variables.get("orderId") + "/status",
    method: "PUT",
    header: { "Content-Type": "application/json",
              "X-Student-Id": pm.environment.get("student_id"),
              "Authorization": "Bearer " + pm.variables.get("adminTok") },
    body: { mode: "raw", raw: JSON.stringify({ status: "delivered" }) }
}, function (err, res) {
    if (res) { pm.variables.set("repeatDeliveredStatus", res.code); }
});""")),
    expected="4xx and the order remains delivered exactly once",
    tests=js("""
pm.test("The repeated terminal transition was refused", function () {
    pm.expect(Number(pm.variables.get("repeatDeliveredStatus"))).to.be.within(400, 499);
});
pm.test("The terminal order remains delivered", function () {
    const target = Number(pm.variables.get("orderId"));
    const row = pm.response.json().find(function (o) { return Number(o.id) === target; }) || {};
    pm.expect(row.status).to.eql("delivered");
});"""), origin="Student-designed",
    rationale="The generated transition matrix covered different-state edges but omitted same-state replay on a terminal state.")

add(id="A4-HR-004", dim="Security", param="authorization", rule="SEC-03 / FR-10",
    partition="atomicity after a non-admin legal transition attempt",
    title="A non-admin transition attempt is refused without changing status",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(order_in_state("confirmed", amount=456000, prefix="hrna", on_done="""
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/admin/orders/" +
         pm.variables.get("orderId") + "/status",
    method: "PUT",
    header: { "Content-Type": "application/json",
              "X-Student-Id": pm.environment.get("student_id"),
              "Authorization": "Bearer " + pm.variables.get("tok") },
    body: { mode: "raw", raw: JSON.stringify({ status: "shipping" }) }
}, function (err, res) {
    if (res) { pm.variables.set("nonAdminTransitionStatus", res.code); }
});""")),
    expected="401/403 and the order remains confirmed",
    tests=js("""
pm.test("The non-admin request was refused", function () {
    pm.expect(Number(pm.variables.get("nonAdminTransitionStatus"))).to.be.oneOf([401, 403]);
});
pm.test("The refused request did not mutate the order", function () {
    const target = Number(pm.variables.get("orderId"));
    const row = pm.response.json().find(function (o) { return Number(o.id) === target; }) || {};
    pm.expect(row.status).to.eql("confirmed");
});"""), origin="Student-designed",
    rationale="The AI proved the authorization defect and one revenue impact; this case adds an explicit atomicity post-condition for another legal edge.")

add(id="A4-HR-005", dim="State", param="-", rule="FR-13",
    partition="count integrity after one checkout",
    title="A newly created order appears exactly once in the admin count source",
    method="GET", path=ADMIN_ORDERS, auth_var="adminTok",
    pre=js(fresh_user(prefix="hrct", on_done=create_order(amount=567000, on_done=admin_login()))),
    expected="the new order id occurs exactly once",
    tests=js("""
pm.test("The checkout contributes exactly one row", function () {
    const target = Number(pm.variables.get("orderId"));
    const matches = pm.response.json().filter(function (o) { return Number(o.id) === target; });
    pm.expect(matches).to.have.lengthOf(1);
});"""), origin="Student-designed",
    rationale="The AI asserted aggregate count but did not test that a single checkout cannot be duplicated by the admin join.")


# ---------------------------------------------------------------------------

META = {
    "api": 4,
    "slug": "api4-fr13-admin-orders",
    "collection_name": "API4 - FR-13 Admin Dashboard (GET /api/admin/orders)",
    "sheet": "API4 FR-13 Admin Dashboard",
    "endpoint": "GET /api/admin/orders",
    "pool": "C",
    "requirement": "FR-13 (with FR-12)",
    "description": (
        "HW06 / Pool C / FR-13 - Admin dashboard.\n\n"
        "The dashboard has no endpoint of its own: total revenue (the sum of "
        "total_amount over orders with status='delivered') and the total order "
        "count are both derived from GET /api/admin/orders, so that endpoint is "
        "the API under test.\n\n"
        "Generated from scripts/cases/api4_fr13_admin_orders.py. The revenue "
        "rule makes the aggregate a projection of the FR-10 state machine, so "
        "the state folder drives orders into each status and checks whether the "
        "figure moves when - and only when - it should. FR-12 / SEC-03 access "
        "control is exercised with genuine, forged and tampered tokens.\n\n"
        "Escalation cases deliberately use LEGAL transitions, so that a refusal "
        "can only mean authorisation was checked."
    ),
    "folders": [
        ("01 - Domain partitions", "Domain",
         "Authorisation partitions on the route, content partitions on what it "
         "returns, and the HTTP methods it does not accept."),
        ("02 - State transitions (FR-10)", "State",
         "The revenue aggregate as a projection of the order state machine, "
         "plus every illegal transition through the admin status route."),
        ("03 - Security (SEC-01..SEC-07)", "Security",
         "SEC-03 role enforcement with real, forged and tampered tokens, "
         "SEC-01 disclosure, and SEC-05 injection."),
        ("04 - Schema validation", "Schema",
         "The joined admin order schema, the closed status enum, and the "
         "arithmetic safety the revenue figure depends on."),
    ],
    "subfolders": {
        "01 - Domain partitions": [
            ("authorization", "authorization"),
            ("query string", "query string"),
            ("http method", "http method"),
        ],
    },
}
