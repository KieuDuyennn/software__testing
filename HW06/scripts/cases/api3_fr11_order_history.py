#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test-case specification for API 3 - FR-11 Order History (user).

Endpoints: GET /api/orders/my-orders   (primary)
           GET /api/orders/:id         (the detail route FR-11 also governs)
           PUT /api/orders/:id/cancel  (the transition FR-11 exposes to the user)

Pool B     Requirement FR-11, with FR-10

FR-11 as written in the requirement document:
  - "Người dùng chỉ xem được đơn hàng của chính mình" - a user may see only
    their own orders. That single sentence is what makes this collection the
    home for ownership and IDOR testing.
  - The history displays: order id, order date, total, current status.

FR-10 defines the order state machine, and history is where a user observes it:
    pending -> confirmed -> shipping -> delivered
    pending | confirmed -> canceled
  and, explicitly, cancellation is permitted only from `pending` or `confirmed`.
Every illegal transition therefore gets a case, because that is where the
defects live.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _helpers import (  # noqa: E402
    FR10_PATH, ORDER_SCHEMA, admin_login, create_order, fresh_user, is_array, js,
    json_content_type, no500, no_credentials, no_leak, order_in_state, rejected,
    set_status, st,
)

CASES = []


def add(**kw):
    CASES.append(kw)
    return kw


MY_ORDERS = "/api/orders/my-orders"

# A syntactically valid JWT whose signature was not produced by the server key.
# Payload decodes to {"id":1,"role":"admin"}.
FORGED = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
          ".eyJpZCI6MSwicm9sZSI6ImFkbWluIn0"
          ".ZmFrZXNpZ25hdHVyZV9ub3RfZnJvbV90aGVfc2VydmVy")


def hdr(value):
    return [{"key": "Authorization", "value": value}]


def own_history_ok():
    return is_array() + js("""
pm.test("Status is 200", () => pm.response.to.have.status(200));
pm.test("Every returned order belongs to the caller", function () {
    const me = Number(pm.variables.get("tok_uid"));
    pm.response.json().forEach(function (o) {
        pm.expect(Number(o.user_id), "owner of order " + o.id).to.eql(me);
    });
});""")


def status_in_history(expected):
    return js("""
pm.test("Order is listed in the caller's history", function () {
    const target = Number(pm.variables.get("orderId"));
    const found = pm.response.json().find(function (o) {
        return Number(o.id) === target;
    });
    pm.expect(found, "order " + target + " must appear in history").to.not.be.undefined;
});
pm.test("History shows the order as '%s'", function () {
    const target = Number(pm.variables.get("orderId"));
    const found = pm.response.json().find(function (o) {
        return Number(o.id) === target;
    }) || {};
    pm.expect(found.status).to.eql("%s");
});""" % (expected, expected))


# ===========================================================================
# STEP 2 - DOMAIN PARTITIONS
# ===========================================================================

# --- authentication partitions on GET /api/orders/my-orders ----------------

add(id="A3-DP-001", dim="Domain", param="authorization", rule="FR-11",
    partition="valid: a genuine bearer token",
    title="An authenticated user receives their own order list",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(fresh_user()), expected="200 with an array of the caller's orders",
    tests=own_history_ok())

add(id="A3-DP-002", dim="Domain", param="authorization", rule="SEC-02",
    partition="invalid: no Authorization header",
    title="A request with no token is rejected",
    method="GET", path=MY_ORDERS,
    expected="401 - SEC-02 requires a valid JWT",
    tests=st(401))

add(id="A3-DP-003", dim="Domain", param="authorization", rule="SEC-02",
    partition="invalid: Bearer with an empty token",
    title="An empty bearer token is rejected",
    method="GET", path=MY_ORDERS, extra_headers=hdr("Bearer "),
    expected="401", tests=rejected("empty token", 401, 403))

add(id="A3-DP-004", dim="Domain", param="authorization", rule="SEC-02",
    partition="invalid: malformed token",
    title="A malformed token is rejected",
    method="GET", path=MY_ORDERS, extra_headers=hdr("Bearer not.a.real.token"),
    expected="403 - the token cannot be verified",
    tests=rejected("malformed token", 401, 403))

add(id="A3-DP-005", dim="Domain", param="authorization", rule="SEC-02",
    partition="invalid: token without the Bearer scheme",
    title="A bare token with no scheme is rejected",
    method="GET", path=MY_ORDERS, extra_headers=hdr("{{tok}}"),
    pre=js(fresh_user()),
    expected="401 - the spec documents `Authorization: Bearer <token>`",
    tests=rejected("missing Bearer scheme", 401, 403))

add(id="A3-DP-006", dim="Domain", param="authorization", rule="SEC-02",
    partition="invalid: wrong authentication scheme",
    title="Basic authentication is rejected",
    method="GET", path=MY_ORDERS,
    extra_headers=hdr("Basic dXNlcjpwYXNzd29yZA=="),
    expected="401", tests=rejected("wrong scheme", 401, 403))

add(id="A3-DP-007", dim="Domain", param="authorization", rule="SEC-02",
    partition="invalid: signature from another key",
    title="A token signed with a different key is rejected",
    method="GET", path=MY_ORDERS, extra_headers=hdr("Bearer " + FORGED),
    expected="403 - signature verification must fail",
    tests=rejected("bad signature", 401, 403))

add(id="A3-DP-008", dim="Domain", param="authorization", rule="SEC-02",
    partition="edge: lowercase scheme keyword",
    title="A lowercase 'bearer' scheme is handled without a server error",
    method="GET", path=MY_ORDERS, extra_headers=hdr("bearer {{tok}}"),
    pre=js(fresh_user()),
    expected="200 or 401 - RFC 7235 makes the scheme case-insensitive; never a 5xx",
    tests=no500(),
    gap="The spec does not state whether the scheme keyword is case-sensitive.")

add(id="A3-DP-009", dim="Domain", param="authorization", rule="SEC-02",
    partition="invalid: token belonging to a deleted account",
    title="A token whose account no longer exists is rejected",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(fresh_user(on_done=admin_login("""
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/admin/users/" +
         pm.variables.get("tok_uid"),
    method: "DELETE",
    header: { "X-Student-Id": pm.environment.get("student_id"),
              "Authorization": "Bearer " + pm.variables.get("adminTok") }
}, function () {});"""))),
    expected="401 - a session must not outlive its account",
    tests=rejected("account no longer exists", 401, 403))

# --- content partitions ----------------------------------------------------

add(id="A3-DP-010", dim="Domain", param="-", rule="FR-11",
    partition="boundary: a user with no orders",
    title="A user with no orders receives an empty array",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(fresh_user()),
    expected="200 with [] - not null, not 404",
    tests=is_array() + js("""
pm.test("A brand-new account has an empty history", function () {
    pm.expect(pm.response.json()).to.be.empty;
});"""))

add(id="A3-DP-011", dim="Domain", param="-", rule="FR-11",
    partition="boundary: exactly one order",
    title="A user with one order sees exactly that order",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(fresh_user(on_done=create_order())),
    expected="200 with a single entry",
    tests=js("""
pm.test("Exactly one order is listed", function () {
    pm.expect(pm.response.json()).to.have.lengthOf(1);
});"""))

add(id="A3-DP-012", dim="Domain", param="-", rule="FR-11",
    partition="multiple orders",
    title="A user with three orders sees all three",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(fresh_user(on_done=create_order(
        amount=100000, on_done=create_order(
            amount=200000, var="orderId2", on_done=create_order(
                amount=300000, var="orderId3"))))),
    expected="200 with three entries",
    tests=js("""
pm.test("All three orders are listed", function () {
    pm.expect(pm.response.json()).to.have.lengthOf(3);
});"""))

add(id="A3-DP-013", dim="Domain", param="-", rule="FR-11",
    partition="ordering is stable and deterministic",
    title="Order history returns the same order on two consecutive reads",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(fresh_user(on_done=create_order(
        amount=100000, on_done=create_order(
            amount=200000, var="orderId2", on_done="""
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/orders/my-orders",
    method: "GET",
    header: { "X-Student-Id": pm.environment.get("student_id"),
              "Authorization": "Bearer " + pm.variables.get("tok") }
}, function (err, res) {
    if (res) {
        pm.variables.set("firstOrder",
            JSON.stringify(res.json().map(function (o) { return o.id; })));
    }
});""")))),
    expected="the id sequence is identical between calls",
    tests=js("""
pm.test("Ordering is deterministic across calls", function () {
    const now = JSON.stringify(pm.response.json().map(function (o) { return o.id; }));
    pm.expect(now).to.eql(pm.variables.get("firstOrder"));
});"""),
    gap="FR-11 does not mandate a sort order, only that it be usable.")

add(id="A3-DP-014", dim="Domain", param="query string", rule="FR-11",
    partition="parameter tampering: user_id in the query string",
    title="A user_id query parameter must not widen the caller's scope",
    method="GET", path=MY_ORDERS, raw_query="?user_id=1", auth_var="tok",
    pre=js(fresh_user()),
    expected="still only the caller's own orders - here, none",
    tests=own_history_ok() + js("""
pm.test("Scope is not widened by an unexpected query parameter", function () {
    pm.expect(pm.response.json(),
        "a fresh account must still see zero orders").to.be.empty;
});"""))

add(id="A3-DP-015", dim="Domain", param="query string", rule="FR-11",
    partition="undocumented query parameters are ignored",
    title="Unknown query parameters do not change the result",
    method="GET", path=MY_ORDERS, raw_query="?limit=1&status=delivered&sort=asc",
    auth_var="tok",
    pre=js(fresh_user(on_done=create_order(
        amount=100000, on_done=create_order(amount=200000, var="orderId2")))),
    expected="200 with both orders - the spec defines no query parameters",
    tests=js("""
pm.test("Undocumented parameters are ignored, not honoured", function () {
    pm.expect(pm.response.json()).to.have.lengthOf(2);
});"""))

# --- HTTP methods ----------------------------------------------------------

for _i, _method in enumerate(["POST", "PUT", "DELETE", "PATCH"]):
    add(id="A3-DP-%03d" % (16 + _i), dim="Domain", param="http method",
        rule="spec conformance",
        partition="invalid: %s on the history route" % _method,
        title="%s /api/orders/my-orders is not routed" % _method,
        method=_method, path=MY_ORDERS, auth_var="tok", body=None,
        pre=js(fresh_user()),
        expected="404 or 405 - the spec documents GET only",
        tests=st(404, 405))

# --- the order detail route ------------------------------------------------

add(id="A3-DP-020", dim="Domain", param="id", rule="FR-11",
    partition="valid: the caller's own order",
    title="A user can read their own order by id",
    method="GET", path="/api/orders/{{orderId}}", auth_var="tok",
    pre=js(fresh_user(on_done=create_order())),
    expected="200 with that order",
    tests=js("""
pm.test("Status is 200", () => pm.response.to.have.status(200));
pm.test("The order returned is the one requested", function () {
    pm.expect(String(pm.response.json().id))
      .to.eql(String(pm.variables.get("orderId")));
});"""))

add(id="A3-DP-021", dim="Domain", param="id", rule="FR-11",
    partition="invalid: order that does not exist",
    title="A non-existent order id returns 404",
    method="GET", path="/api/orders/987654", auth_var="tok",
    pre=js(fresh_user()), expected="404", tests=st(404))

add(id="A3-DP-022", dim="Domain", param="id", rule="FR-11",
    partition="boundary: id zero",
    title="Order id 0 returns 404",
    method="GET", path="/api/orders/0", auth_var="tok",
    pre=js(fresh_user()), expected="404", tests=st(404))

add(id="A3-DP-023", dim="Domain", param="id", rule="FR-11",
    partition="invalid: negative id",
    title="A negative order id is rejected",
    method="GET", path="/api/orders/-1", auth_var="tok",
    pre=js(fresh_user()), expected="400 or 404, never 200",
    tests=rejected("ids cannot be negative"))

add(id="A3-DP-024", dim="Domain", param="id", rule="FR-11",
    partition="invalid: non-numeric id",
    title="A non-numeric order id is rejected",
    method="GET", path="/api/orders/abc", auth_var="tok",
    pre=js(fresh_user()), expected="400 or 404, never 200",
    tests=rejected("ids are numeric") + "\n" + no500())

add(id="A3-DP-025", dim="Domain", param="id", rule="FR-11",
    partition="invalid: decimal id",
    title="A decimal order id is rejected",
    method="GET", path="/api/orders/1.5", auth_var="tok",
    pre=js(fresh_user()), expected="400 or 404",
    tests=rejected("ids are integers"))

add(id="A3-DP-026", dim="Domain", param="id", rule="FR-11",
    partition="boundary: id beyond 2^31",
    title="An out-of-range order id returns 404 without erroring",
    method="GET", path="/api/orders/2147483648", auth_var="tok",
    pre=js(fresh_user()), expected="404, never a 5xx",
    tests=st(404) + "\n" + no500())

add(id="A3-DP-027", dim="Domain", param="id", rule="spec conformance",
    partition="invalid: extra path segment",
    title="An extra path segment is not routed to order detail",
    method="GET", path="/api/orders/1/2", auth_var="tok",
    pre=js(fresh_user()), expected="404 or 405", tests=st(404, 405))

add(id="A3-DP-028", dim="Domain", param="-", rule="FR-11 / FR-10",
    partition="valid: cancel route accepts the owner",
    title="The owner can cancel their own pending order",
    method="PUT", path="/api/orders/{{orderId}}/cancel", auth_var="tok",
    pre=js(fresh_user(on_done=create_order())),
    expected="200 - FR-10 permits cancellation from pending",
    tests=st(200))

add(id="A3-DP-029", dim="Domain", param="-", rule="FR-11",
    partition="invalid: cancel a non-existent order",
    title="Cancelling an order that does not exist returns 404",
    method="PUT", path="/api/orders/987654/cancel", auth_var="tok",
    pre=js(fresh_user()), expected="404", tests=st(404))

add(id="A3-DP-030", dim="Domain", param="-", rule="FR-11",
    partition="invalid: cancel without a token",
    title="Cancelling without a token is rejected",
    method="PUT", path="/api/orders/{{orderId}}/cancel",
    pre=js(fresh_user(on_done=create_order())),
    expected="401", tests=rejected("no token supplied", 401, 403))


# ===========================================================================
# STEP 3 - STATE TRANSITIONS (FR-10, observed through order history)
# ===========================================================================

add(id="A3-ST-001", dim="State", param="-", rule="FR-10",
    partition="initial state: a new order is pending",
    title="A newly created order appears in history as 'pending'",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(order_in_state("pending")),
    expected="the order is listed with status 'pending'",
    tests=status_in_history("pending"))

for _i, _state in enumerate(["confirmed", "shipping", "delivered", "canceled"]):
    add(id="A3-ST-%03d" % (2 + _i), dim="State", param="-", rule="FR-10 / FR-11",
        partition="legal transition observed in history: -> %s" % _state,
        title="History reflects an order driven to '%s'" % _state,
        method="GET", path=MY_ORDERS, auth_var="tok",
        pre=js(order_in_state(_state, prefix=_state[:2])),
        expected="the order is listed with status '%s'" % _state,
        tests=status_in_history(_state))

# --- cancellation rules ----------------------------------------------------
# FR-10: "Chỉ được hủy khi pending hoặc confirmed."

add(id="A3-ST-006", dim="State", param="-", rule="FR-10",
    partition="legal cancellation: from pending",
    title="Cancelling a pending order is accepted",
    method="PUT", path="/api/orders/{{orderId}}/cancel", auth_var="tok",
    pre=js(order_in_state("pending")),
    expected="200 - pending is a cancellable state",
    tests=st(200))

add(id="A3-ST-007", dim="State", param="-", rule="FR-10",
    partition="legal cancellation: from confirmed",
    title="Cancelling a confirmed order is accepted",
    method="PUT", path="/api/orders/{{orderId}}/cancel", auth_var="tok",
    pre=js(order_in_state("confirmed", prefix="cf")),
    expected="200 - confirmed is a cancellable state",
    tests=st(200))

add(id="A3-ST-008", dim="State", param="-", rule="FR-10",
    partition="ILLEGAL cancellation: from shipping",
    title="Cancelling a shipping order must be refused",
    method="PUT", path="/api/orders/{{orderId}}/cancel", auth_var="tok",
    pre=js(order_in_state("shipping", prefix="sh")),
    expected='400 - FR-10 permits cancellation only from pending or confirmed',
    tests=rejected("shipping is not a cancellable state"))

add(id="A3-ST-009", dim="State", param="-", rule="FR-10",
    partition="ILLEGAL cancellation: from delivered",
    title="Cancelling a delivered order must be refused",
    method="PUT", path="/api/orders/{{orderId}}/cancel", auth_var="tok",
    pre=js(order_in_state("delivered", prefix="dl")),
    expected="400 - delivered is terminal",
    tests=rejected("delivered is terminal"))

add(id="A3-ST-010", dim="State", param="-", rule="FR-10",
    partition="ILLEGAL cancellation: from canceled",
    title="Cancelling an already-cancelled order must be refused",
    method="PUT", path="/api/orders/{{orderId}}/cancel", auth_var="tok",
    pre=js(order_in_state("canceled", prefix="cx")),
    expected="400 - canceled is terminal",
    tests=rejected("canceled is terminal"))

add(id="A3-ST-011", dim="State", param="-", rule="FR-10 / FR-11",
    partition="post-condition: cancellation is visible in history",
    title="A cancelled order shows as 'canceled' in history",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(order_in_state("pending", on_done="""
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/orders/" +
         pm.variables.get("orderId") + "/cancel",
    method: "PUT",
    header: { "X-Student-Id": pm.environment.get("student_id"),
              "Authorization": "Bearer " + pm.variables.get("tok") }
}, function () {});""")),
    expected="status 'canceled'", tests=status_in_history("canceled"))

# --- illegal admin transitions, observed through history -------------------

_ILLEGAL = [
    ("pending", "shipping", "pending may only go to confirmed or canceled"),
    ("pending", "delivered", "pending may only go to confirmed or canceled"),
    ("confirmed", "delivered", "confirmed may only go to shipping or canceled"),
    ("confirmed", "pending", "the machine does not move backwards"),
    ("shipping", "confirmed", "the machine does not move backwards"),
    ("shipping", "canceled", "shipping is not a cancellable state"),
    ("delivered", "shipping", "delivered is terminal"),
    ("delivered", "canceled", "delivered is terminal"),
    ("canceled", "delivered", "canceled is terminal"),
    ("canceled", "pending", "canceled is terminal"),
]

for _i, (_from, _to, _why) in enumerate(_ILLEGAL):
    add(id="A3-ST-%03d" % (12 + _i), dim="State", param="-", rule="FR-10",
        partition="ILLEGAL transition: %s -> %s" % (_from, _to),
        title="Transition %s -> %s must be refused" % (_from, _to),
        method="PUT", path="/api/admin/orders/{{orderId}}/status",
        auth_var="adminTok", body={"status": _to},
        pre=js(order_in_state(_from, prefix=_from[:2] + _to[:2])),
        expected="400 - %s" % _why,
        tests=rejected("%s -> %s is not a legal transition" % (_from, _to)))

add(id="A3-ST-022", dim="State", param="-", rule="FR-10",
    partition="invalid status value",
    title="An unrecognised status value is refused",
    method="PUT", path="/api/admin/orders/{{orderId}}/status",
    auth_var="adminTok", body={"status": "teleported"},
    pre=js(order_in_state("pending", prefix="iv")),
    expected="400 - the status set is closed",
    tests=rejected("unknown status value"))

add(id="A3-ST-023", dim="State", param="-", rule="FR-10",
    partition="data preservation across transitions",
    title="An order's total and address survive the full lifecycle",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(order_in_state("delivered", amount=777000, prefix="pv")),
    expected="total_amount is still 777000 after pending->confirmed->shipping->delivered",
    tests=js("""
pm.test("Order data is preserved through every transition", function () {
    const target = Number(pm.variables.get("orderId"));
    const found = pm.response.json().find(function (o) {
        return Number(o.id) === target;
    }) || {};
    pm.expect(Number(found.total_amount)).to.eql(777000);
    pm.expect(found.shipping_address).to.eql("123 Le Loi, Q1, TP.HCM");
});"""))

add(id="A3-ST-024", dim="State", param="-", rule="FR-10 / FR-11",
    partition="ownership: cancelling another user's order",
    title="A user must not be able to cancel someone else's order",
    method="PUT", path="/api/orders/{{victimOrder}}/cancel", auth_var="tok",
    pre=js(fresh_user(var="victimTok", prefix="vic", on_done=create_order(
        token_var="victimTok", var="victimOrder",
        on_done=fresh_user(prefix="atk")))),
    expected="403 or 404 - FR-11 scopes orders to their owner",
    tests=rejected("caller does not own this order", 401, 404))


# ===========================================================================
# STEP 4 - SECURITY (SEC-01 .. SEC-07)
# ===========================================================================

add(id="A3-SEC-001", dim="Security", param="-", rule="SEC-02 / FR-11",
    partition="IDOR: anonymous read of an arbitrary order",
    title="Reading an order with no token at all must be refused",
    method="GET", path="/api/orders/{{orderId}}",
    pre=js(fresh_user(on_done=create_order())),
    expected="401 - SEC-02 requires a valid JWT on order data",
    tests=rejected("no token supplied", 401, 404))

add(id="A3-SEC-002", dim="Security", param="-", rule="FR-11",
    partition="IDOR: cross-user read with a valid token",
    title="User A must not be able to read user B's order",
    method="GET", path="/api/orders/{{victimOrder}}", auth_var="tok",
    pre=js(fresh_user(var="victimTok", prefix="vc2", on_done=create_order(
        token_var="victimTok", var="victimOrder", amount=999000,
        on_done=fresh_user(prefix="at2")))),
    expected="403 or 404 - FR-11 scopes orders to their owner",
    tests=rejected("caller does not own this order", 401, 404))

add(id="A3-SEC-003", dim="Security", param="-", rule="FR-11 / SEC-02",
    partition="IDOR: enumeration of the id space",
    title="Sequential order ids must not be enumerable anonymously",
    method="GET", path="/api/orders/1",
    expected="401 - walking ids from 1 must not disclose other customers' orders",
    tests=rejected("anonymous enumeration must be refused", 401, 404))

add(id="A3-SEC-004", dim="Security", param="-", rule="FR-11",
    partition="privacy: shipping address disclosure",
    title="An anonymous caller must not learn a customer's shipping address",
    method="GET", path="/api/orders/{{orderId}}",
    pre=js(fresh_user(on_done=create_order(
        address="99 Secret Lane, District 1"))),
    expected="the response must not contain the address",
    tests=js("""
pm.test("No shipping address is disclosed to an anonymous caller", function () {
    pm.expect(pm.response.text()).to.not.include("99 Secret Lane");
});"""))

add(id="A3-SEC-005", dim="Security", param="-", rule="FR-11",
    partition="scope: history never leaks another user's orders",
    title="Order history contains only the caller's orders",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(fresh_user(var="victimTok", prefix="vc3", on_done=create_order(
        token_var="victimTok", var="victimOrder", amount=888000,
        on_done=fresh_user(prefix="at3", on_done=create_order(amount=111000))))),
    expected="the other user's order is absent from the caller's history",
    tests=own_history_ok() + js("""
pm.test("Another user's order does not appear", function () {
    const victim = Number(pm.variables.get("victimOrder"));
    const leaked = pm.response.json().some(function (o) {
        return Number(o.id) === victim;
    });
    pm.expect(leaked, "order " + victim + " belongs to someone else").to.be.false;
});"""))

add(id="A3-SEC-006", dim="Security", param="authorization", rule="SEC-02",
    partition="token tampering: payload edited, signature kept",
    title="A token with an edited payload is rejected",
    method="GET", path=MY_ORDERS, extra_headers=hdr("Bearer {{tamperedTok}}"),
    pre=js(fresh_user(on_done="""
// Re-encode the payload with role=admin but leave the original signature.
const parts = String(pm.variables.get("tok")).split(".");
if (parts.length === 3) {
    const payload = JSON.parse(Buffer.from(parts[1], "base64").toString());
    payload.role = "admin";
    payload.id = 1;
    const forgedPayload = Buffer.from(JSON.stringify(payload))
        .toString("base64").replace(/=+$/, "");
    pm.variables.set("tamperedTok", parts[0] + "." + forgedPayload + "." + parts[2]);
}""")),
    expected="403 - the signature no longer matches the payload",
    tests=rejected("tampered payload", 401, 403))

add(id="A3-SEC-007", dim="Security", param="authorization", rule="SEC-03",
    partition="privilege escalation via a forged admin token",
    title="A forged admin token must not reach the admin order API",
    method="GET", path="/api/admin/orders",
    extra_headers=hdr("Bearer " + FORGED),
    expected="403 - the signature is not the server's",
    tests=rejected("forged token", 401, 403))

add(id="A3-SEC-008", dim="Security", param="-", rule="SEC-03 / FR-12",
    partition="privilege escalation: a real user token on an admin route",
    title="An ordinary user must not reach the admin order list",
    method="GET", path="/api/admin/orders", auth_var="tok",
    pre=js(fresh_user()),
    expected="403 - SEC-03 requires role='admin'",
    tests=rejected("caller is not an admin", 401, 403))

add(id="A3-SEC-009", dim="Security", param="-", rule="SEC-03 / FR-12",
    partition="privilege escalation: a user driving the state machine",
    title="An ordinary user must not change an order's status",
    method="PUT", path="/api/admin/orders/{{orderId}}/status", auth_var="tok",
    # The transition itself must be LEGAL (pending -> confirmed). If the case
    # asked for an illegal one, a 400 "invalid transition" would be
    # indistinguishable from a 403 "not an admin", and the case could not tell
    # whether authorisation was checked at all.
    body={"status": "confirmed"},
    pre=js(order_in_state("pending", prefix="pe")),
    expected="403 - only an admin may drive FR-10 transitions, even legal ones",
    tests=rejected("caller is not an admin", 401, 403) + js("""
pm.test("The transition did not take effect", function () {
    pm.expect(pm.response.code,
        "a 200 here means the role claim was never checked").to.not.eql(200);
});"""))

_ORDER_INJECTIONS = [
    ("1 OR 1=1", "tautology"),
    ("1' OR '1'='1", "quoted tautology"),
    ("1; DROP TABLE orders;--", "statement termination"),
    ("1 UNION SELECT id,email,password,role FROM users--", "UNION SELECT against users"),
]

for _i, (_payload, _label) in enumerate(_ORDER_INJECTIONS):
    add(id="A3-SEC-%03d" % (10 + _i), dim="Security", param="id", rule="SEC-05",
        partition="SQL injection: %s" % _label,
        title="Injection via the order id (%s) is neutralised" % _label,
        method="GET", path="/api/orders/%s" % _payload, auth_var="tok",
        pre=js(fresh_user()),
        expected="no 5xx, no SQL error, no credential leak, never an array",
        tests=no500() + "\n" + no_leak() + "\n" + no_credentials() + js("""
pm.test("A single-resource route never returns a list", function () {
    pm.expect(Array.isArray(pm.response.json())).to.be.false;
});"""))

add(id="A3-SEC-014", dim="Security", param="-", rule="SEC-05",
    partition="SQL injection: data integrity afterwards",
    title="The orders table survives the injection attempts intact",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(fresh_user(on_done=create_order(on_done="""
const base = pm.environment.get("base_url");
const sid = pm.environment.get("student_id");
["1; DROP TABLE orders;--", "1' OR '1'='1"].forEach(function (payload) {
    pm.sendRequest({
        url: base + "/api/orders/" + encodeURIComponent(payload),
        method: "GET",
        header: { "X-Student-Id": sid,
                  "Authorization": "Bearer " + pm.variables.get("tok") }
    }, function () {});
});"""))),
    expected="the caller's order is still there",
    tests=js("""
pm.test("The order survived the injection attempts", function () {
    pm.expect(pm.response.json()).to.have.lengthOf(1);
});"""))

add(id="A3-SEC-015", dim="Security", param="-", rule="SEC-01",
    partition="information disclosure in order payloads",
    title="Order history exposes no credential fields",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(fresh_user(on_done=create_order())),
    expected="no password, token or role key in any order",
    tests=no_credentials() + js("""
const text = pm.response.text().toLowerCase();
["token", "role"].forEach(function (key) {
    pm.test('History contains no "' + key + '" field', function () {
        pm.expect(text).to.not.include('"' + key + '"');
    });
});"""))

add(id="A3-SEC-016", dim="Security", param="-", rule="SEC-05",
    partition="information disclosure on error",
    title="An invalid order id must not leak database internals",
    method="GET", path="/api/orders/';--", auth_var="tok",
    pre=js(fresh_user()),
    expected="a clean 4xx with no driver or stack detail",
    tests=no_leak() + "\n" + no500())

add(id="A3-SEC-017", dim="Security", param="-", rule="FR-11",
    partition="ownership on the detail route with the owner's token",
    title="The owner reading their own order is allowed",
    method="GET", path="/api/orders/{{orderId}}", auth_var="tok",
    pre=js(fresh_user(on_done=create_order())),
    expected="200 - this is the positive control for the IDOR cases",
    tests=st(200))

add(id="A3-SEC-018", dim="Security", param="-", rule="SEC-02",
    partition="cancel route: forged token",
    title="Cancelling with a forged token must be refused",
    method="PUT", path="/api/orders/{{orderId}}/cancel",
    extra_headers=hdr("Bearer " + FORGED),
    pre=js(fresh_user(on_done=create_order())),
    expected="403", tests=rejected("forged token", 401, 403))

add(id="A3-SEC-019", dim="Security", param="-", rule="FR-11",
    partition="scope: an admin's own history is still only their own",
    title="Admin order history returns only the admin's own orders",
    method="GET", path=MY_ORDERS, auth_var="adminTok",
    pre=js(admin_login()),
    expected="only orders whose user_id is the admin's - my-orders is not an admin view",
    tests=is_array() + js("""
pm.test("Even an admin sees only their own orders here", function () {
    const me = Number(pm.variables.get("adminTok_uid"));
    pm.response.json().forEach(function (o) {
        pm.expect(Number(o.user_id), "owner of order " + o.id).to.eql(me);
    });
});"""))

add(id="A3-SEC-020", dim="Security", param="-", rule="SEC-02",
    partition="replay after cancellation",
    title="A cancelled order cannot be cancelled again by replaying the request",
    method="PUT", path="/api/orders/{{orderId}}/cancel", auth_var="tok",
    pre=js(order_in_state("pending", prefix="rp", on_done="""
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/orders/" +
         pm.variables.get("orderId") + "/cancel",
    method: "PUT",
    header: { "X-Student-Id": pm.environment.get("student_id"),
              "Authorization": "Bearer " + pm.variables.get("tok") }
}, function () {});""")),
    expected="400 - the order is already in a terminal state",
    tests=rejected("already cancelled"))


# ===========================================================================
# STEP 5 - SCHEMA VALIDATION
# ===========================================================================

add(id="A3-SCH-001", dim="Schema", param="-", rule="spec conformance",
    partition="history: array schema",
    title="Order history validates against the order schema",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(fresh_user(on_done=create_order())),
    expected="every entry validates against the orders schema",
    tests=ORDER_SCHEMA + js("""
pm.test("Every history entry conforms to the order schema", function () {
    pm.response.to.have.jsonSchema({ type: "array", items: orderSchema });
});"""))

add(id="A3-SCH-002", dim="Schema", param="status", rule="FR-10",
    partition="status is drawn from the closed FR-10 set",
    title="Every order's status is one of the five FR-10 states",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(fresh_user(on_done=create_order())),
    expected="status in [pending, confirmed, shipping, delivered, canceled]",
    tests=js("""
const allowed = ["pending", "confirmed", "shipping", "delivered", "canceled"];
pm.test("All statuses come from the FR-10 state set", function () {
    pm.response.json().forEach(function (o) {
        pm.expect(allowed, "status of order " + o.id).to.include(o.status);
    });
});"""))

add(id="A3-SCH-003", dim="Schema", param="total_amount", rule="FR-11",
    partition="total_amount type",
    title="total_amount is a JSON number, not a string",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(fresh_user(on_done=create_order(amount=250000))),
    expected="FR-11 displays the total, so it must be arithmetic-safe",
    tests=js("""
pm.test("total_amount is a number in every entry", function () {
    pm.response.json().forEach(function (o) {
        pm.expect(o.total_amount, "order " + o.id).to.be.a("number");
    });
});"""))

add(id="A3-SCH-004", dim="Schema", param="id", rule="FR-11",
    partition="order id type",
    title="Every order id is a JSON integer",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(fresh_user(on_done=create_order())),
    expected="FR-11 displays 'Mã đơn', so the id must be present and integral",
    tests=js("""
pm.test("Every order id is an integer", function () {
    pm.response.json().forEach(function (o) {
        pm.expect(Number.isInteger(o.id), "order id " + o.id).to.be.true;
    });
});"""))

add(id="A3-SCH-005", dim="Schema", param="created_at", rule="FR-11",
    partition="created_at presence and parseability",
    title="created_at is present and parseable as a date",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(fresh_user(on_done=create_order())),
    expected="FR-11 displays 'Ngày đặt', so the date must be usable",
    tests=js("""
pm.test("created_at is present and parseable", function () {
    pm.response.json().forEach(function (o) {
        pm.expect(o.created_at, "order " + o.id).to.be.a("string");
        pm.expect(isNaN(Date.parse(o.created_at)),
            "created_at must parse as a date: " + o.created_at).to.be.false;
    });
});"""))

add(id="A3-SCH-006", dim="Schema", param="-", rule="FR-11",
    partition="all four display fields present",
    title="Every entry carries the four fields FR-11 requires displaying",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(fresh_user(on_done=create_order())),
    expected="id, created_at, total_amount and status present on every entry",
    tests=js("""
pm.test("FR-11's four display fields are present", function () {
    pm.response.json().forEach(function (o) {
        ["id", "created_at", "total_amount", "status"].forEach(function (f) {
            pm.expect(o, "order " + o.id + " field " + f).to.have.property(f);
        });
    });
});"""))

add(id="A3-SCH-007", dim="Schema", param="-", rule="spec conformance",
    partition="empty history is an array, not null",
    title="An empty history is rendered as [] rather than null or an object",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(fresh_user()),
    expected="the body is exactly []",
    tests=js("""
pm.test("Empty history is an empty array", function () {
    pm.expect(pm.response.json()).to.be.an("array").that.is.empty;
});"""))

add(id="A3-SCH-008", dim="Schema", param="-", rule="spec conformance",
    partition="detail route: order schema",
    title="A single order validates against the order schema",
    method="GET", path="/api/orders/{{orderId}}", auth_var="tok",
    pre=js(fresh_user(on_done=create_order())),
    expected="validates against the orders schema",
    tests=ORDER_SCHEMA + js("""
pm.test("Order detail conforms to the order schema", function () {
    pm.response.to.have.jsonSchema(orderSchema);
});"""))

add(id="A3-SCH-009", dim="Schema", param="-", rule="spec conformance",
    partition="error body: not-found shape",
    title="A not-found order returns a structured error body",
    method="GET", path="/api/orders/987654", auth_var="tok",
    pre=js(fresh_user()),
    expected='404 with {"error": "<string>"}',
    tests=js("""
pm.test("Status is 404", () => pm.response.to.have.status(404));
pm.test("Error body is structured JSON", function () {
    const b = pm.response.json();
    pm.expect(b).to.have.property("error");
    pm.expect(b.error).to.be.a("string");
});"""))

add(id="A3-SCH-010", dim="Schema", param="-", rule="spec conformance",
    partition="error body: unauthorised shape",
    title="An unauthorised request returns a structured error body",
    method="GET", path=MY_ORDERS,
    expected='401 with {"error": "<string>"}',
    tests=js("""
pm.test("Status is 401", () => pm.response.to.have.status(401));
pm.test("Error body is structured JSON", function () {
    pm.expect(pm.response.json()).to.have.property("error");
});"""))

add(id="A3-SCH-011", dim="Schema", param="-", rule="spec conformance",
    partition="response headers",
    title="Order history is served as application/json",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(fresh_user()), expected="Content-Type includes application/json",
    tests=json_content_type())

add(id="A3-SCH-012", dim="Schema", param="user_id", rule="FR-11",
    partition="user_id type and value",
    title="Every entry's user_id is an integer equal to the caller's id",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(fresh_user(on_done=create_order())),
    expected="user_id is an integer and matches the token's subject",
    tests=js("""
pm.test("user_id is an integer matching the caller", function () {
    const me = Number(pm.variables.get("tok_uid"));
    pm.response.json().forEach(function (o) {
        pm.expect(Number.isInteger(o.user_id), "order " + o.id).to.be.true;
        pm.expect(Number(o.user_id)).to.eql(me);
    });
});"""))

add(id="A3-SCH-013", dim="Schema", param="-", rule="spec conformance",
    partition="no undocumented fields on an order",
    title="An order entry carries no fields beyond the documented set",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(fresh_user(on_done=create_order())),
    expected="keys are a subset of the six documented order fields",
    tests=js("""
const documented = ["id", "user_id", "total_amount", "status",
                    "shipping_address", "created_at"];
pm.test("No undocumented fields appear on an order", function () {
    pm.response.json().forEach(function (o) {
        const extra = Object.keys(o).filter(function (k) {
            return documented.indexOf(k) === -1;
        });
        pm.expect(extra, "undocumented fields on order " + o.id).to.eql([]);
    });
});"""))

add(id="A3-SCH-014", dim="Schema", param="total_amount", rule="FR-11",
    partition="total_amount value fidelity",
    title="total_amount round-trips the value supplied at checkout",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(fresh_user(on_done=create_order(amount=654321))),
    expected="total_amount === 654321 exactly",
    tests=js("""
pm.test("The stored total matches what was submitted", function () {
    const target = Number(pm.variables.get("orderId"));
    const found = pm.response.json().find(function (o) {
        return Number(o.id) === target;
    }) || {};
    pm.expect(Number(found.total_amount)).to.eql(654321);
});"""))

add(id="A3-SCH-015", dim="Schema", param="-", rule="spec conformance",
    partition="error body: not an HTML page",
    title="Errors on this route are JSON, never an HTML page",
    method="GET", path=MY_ORDERS, extra_headers=hdr("Bearer broken.token.here"),
    expected="Content-Type is not text/html",
    tests=js("""
pm.test("Error response is not an HTML page", function () {
    pm.expect((pm.response.headers.get("Content-Type") || "").toLowerCase())
      .to.not.include("text/html");
});"""))


# ===========================================================================
# PHASE 3 - STUDENT-DESIGNED EXTENSIONS
# ===========================================================================

add(id="A3-HR-001", dim="State", param="-", rule="FR-10 / FR-11",
    partition="post-condition after refused shipping cancellation",
    title="A refused shipping cancellation leaves the order in shipping",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(order_in_state("shipping", prefix="hrsh", on_done="""
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/orders/" +
         pm.variables.get("orderId") + "/cancel",
    method: "PUT",
    header: { "X-Student-Id": pm.environment.get("student_id"),
              "Authorization": "Bearer " + pm.variables.get("tok") }
}, function () {});""")),
    expected="the order remains shipping after the forbidden request",
    tests=status_in_history("shipping"), origin="Student-designed",
    rationale="The AI checked the rejection status but did not verify that a failed transition is atomic and leaves state unchanged.")

add(id="A3-HR-002", dim="Security", param="-", rule="FR-11 / SEC-03",
    partition="IDOR post-condition: cross-user cancellation changes nothing",
    title="A cross-user cancellation attempt cannot mutate the victim order",
    method="GET", path="/api/orders/{{victimOrder}}", auth_var="victimTok",
    pre=js(fresh_user(var="victimTok", prefix="hrvic", on_done=create_order(
        token_var="victimTok", var="victimOrder", on_done=fresh_user(
            var="attackerTok", prefix="hratk", on_done="""
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/orders/" +
         pm.variables.get("victimOrder") + "/cancel",
    method: "PUT",
    header: { "X-Student-Id": pm.environment.get("student_id"),
              "Authorization": "Bearer " + pm.variables.get("attackerTok") }
}, function () {});""")))),
    expected="200 for the owner and status remains pending",
    tests=js("""
pm.test("The owner can still read the order", () => pm.response.to.have.status(200));
pm.test("The attack did not change the victim order", function () {
    pm.expect(pm.response.json().status).to.eql("pending");
});"""), origin="Student-designed",
    rationale="The AI tested cross-user cancellation response codes but did not assert the protected resource's post-state.")

add(id="A3-HR-003", dim="Schema", param="-", rule="FR-11",
    partition="cross-route consistency: detail and history",
    title="Order detail and history expose the same values for one order",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(fresh_user(prefix="hrco", on_done=create_order(amount=432100, on_done="""
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/orders/" + pm.variables.get("orderId"),
    method: "GET",
    header: { "X-Student-Id": pm.environment.get("student_id"),
              "Authorization": "Bearer " + pm.variables.get("tok") }
}, function (err, res) {
    if (res) { pm.variables.set("detailSnapshot", JSON.stringify(res.json())); }
});"""))),
    expected="id, user_id, total_amount, status and shipping_address match",
    tests=js("""
pm.test("History and detail agree on the same order", function () {
    const detail = JSON.parse(pm.variables.get("detailSnapshot") || "{}");
    const row = pm.response.json().find(function (o) {
        return Number(o.id) === Number(pm.variables.get("orderId"));
    }) || {};
    ["id", "user_id", "total_amount", "status", "shipping_address"].forEach(function (k) {
        pm.expect(String(row[k]), k + " differs between routes").to.eql(String(detail[k]));
    });
});"""), origin="Student-designed",
    rationale="The AI validated each route independently but omitted a metamorphic consistency oracle across the two FR-11 views.")

add(id="A3-HR-004", dim="Security", param="id", rule="SEC-04 / SEC-05",
    partition="invalid: oversized id on the cancellation route",
    title="An oversized cancellation id is rejected safely",
    method="PUT", path="/api/orders/999999999999999999999999999999/cancel",
    auth_var="tok", pre=js(fresh_user(prefix="hrid")),
    expected="clean 4xx, no 5xx and no database detail",
    tests=rejected("order id is outside the supported range") + "\n" + no500() + "\n" + no_leak(),
    origin="Student-designed",
    rationale="The AI covered oversized ids on GET detail but not on the state-changing cancellation route.")

add(id="A3-HR-005", dim="Security", param="authorization", rule="SEC-02 / FR-10",
    partition="post-condition after anonymous cancellation attempt",
    title="An anonymous cancellation attempt cannot mutate an order",
    method="GET", path=MY_ORDERS, auth_var="tok",
    pre=js(fresh_user(prefix="hran", on_done=create_order(on_done="""
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/orders/" +
         pm.variables.get("orderId") + "/cancel",
    method: "PUT",
    header: { "X-Student-Id": pm.environment.get("student_id") }
}, function () {});"""))),
    expected="the order remains pending",
    tests=status_in_history("pending"), origin="Student-designed",
    rationale="The AI asserted 401 for the anonymous request but did not independently verify non-mutation.")


# ---------------------------------------------------------------------------

META = {
    "api": 3,
    "slug": "api3-fr11-order-history",
    "collection_name": "API3 - FR-11 Order History (GET /api/orders/my-orders)",
    "sheet": "API3 FR-11 Order History",
    "endpoint": "GET /api/orders/my-orders",
    "pool": "B",
    "requirement": "FR-11 (with FR-10)",
    "description": (
        "HW06 / Pool B / FR-11 - Order history.\n\n"
        "Spec: GET /api/orders/my-orders (Bearer token) -> the caller's orders. "
        "Also covers GET /api/orders/:id and PUT /api/orders/:id/cancel, the two "
        "routes FR-11 governs alongside it.\n\n"
        "Generated from scripts/cases/api3_fr11_order_history.py. FR-11's rule "
        "that a user may see only their own orders makes this the home for "
        "ownership and IDOR testing; FR-10's state machine is exercised through "
        "the history view, with a case for every ILLEGAL transition as well as "
        "every legal one.\n\n"
        "Each case builds its own users and orders in a pre-request fixture, so "
        "no case depends on another having run first."
    ),
    "folders": [
        ("01 - Domain partitions", "Domain",
         "Authentication partitions on the history route, content partitions "
         "on what it returns, and the id partitions on the detail and cancel "
         "routes."),
        ("02 - State transitions (FR-10)", "State",
         "Every legal transition, and every illegal one - the illegal ones are "
         "where the defects live."),
        ("03 - Security (SEC-01..SEC-07)", "Security",
         "IDOR and ownership across two users, token forgery and tampering, "
         "privilege escalation, and SEC-05 injection through the order id."),
        ("04 - Schema validation", "Schema",
         "The order schema, the closed status enum, and the four fields FR-11 "
         "requires the history to display."),
    ],
    "subfolders": {
        "01 - Domain partitions": [
            ("authorization", "authorization"),
            ("id", "id"),
            ("query string", "query string"),
            ("http method", "http method"),
        ],
    },
}
