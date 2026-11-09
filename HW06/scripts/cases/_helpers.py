#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared building blocks for the HW06 case specifications.

Every expected result written with these helpers must come from
`refs/spec/api_specification.md` or from the FR / SEC rules in
`refs/spec/eshop_requirements_README.md` - never from the SUT's observed
behaviour. An oracle read off the implementation produces a test that passes by
construction and can never find a defect.
"""

from __future__ import annotations

OMIT = object()          # distinct from None, which means an explicit JSON null


# ---------------------------------------------------------------------------
# Assertion fragments
# ---------------------------------------------------------------------------

def st(*codes):
    """Assert the status code is one of `codes`."""
    if len(codes) == 1:
        return ('pm.test("Status is %d", function () {\n'
                '    pm.response.to.have.status(%d);\n});' % (codes[0], codes[0]))
    lst = ", ".join(str(c) for c in codes)
    return ('pm.test("Status is one of [%s]", function () {\n'
            '    pm.expect(pm.response.code).to.be.oneOf([%s]);\n});' % (lst, lst))


def rejected(reason, lo=400, hi=499):
    """The specification says this request is invalid: it must be refused."""
    return (
        'pm.test("Rejected with a %d-%d (%s)", function () {\n'
        '    pm.expect(pm.response.code, "status code").to.be.within(%d, %d);\n'
        '});' % (lo, hi, reason, lo, hi)
    )


def no500():
    return (
        'pm.test("Server does not fail with a 5xx", function () {\n'
        '    pm.expect(pm.response.code, "status code").to.be.below(500);\n'
        '});'
    )


def no_leak():
    return (
        'pm.test("No database internals leak to the client", function () {\n'
        '    const t = pm.response.text().toLowerCase();\n'
        '    ["sqlite", "sql error", "syntax error", "at object."]\n'
        '        .forEach(function (needle) {\n'
        '            pm.expect(t, "response must not contain \\"" + needle + "\\"")\n'
        '                .to.not.include(needle);\n'
        '        });\n'
        '});'
    )


def no_credentials():
    return (
        'pm.test("No credential material in the response", function () {\n'
        '    const t = pm.response.text();\n'
        '    pm.expect(t.toLowerCase()).to.not.include(\'"password"\');\n'
        '    pm.expect(t).to.not.include("Admin123!");\n'
        '    pm.expect(t).to.not.include("Test1234!");\n'
        '});'
    )


def json_content_type():
    return (
        'pm.test("Content-Type is application/json", function () {\n'
        '    pm.expect(pm.response.headers.get("Content-Type") || "")\n'
        '        .to.include("application/json");\n'
        '});'
    )


def is_array():
    return (
        'pm.test("Response is a JSON array", function () {\n'
        '    pm.expect(pm.response.json()).to.be.an("array");\n'
        '});'
    )


def js(raw):
    return raw.strip()


# ---------------------------------------------------------------------------
# Shared JSON schemas, transcribed from api_specification.md
# ---------------------------------------------------------------------------

PRODUCT_SCHEMA = """
const productSchema = {
    type: "object",
    required: ["id", "name", "price", "description", "imageUrl", "category_id"],
    additionalProperties: false,
    properties: {
        id:          { type: "integer" },
        name:        { type: "string" },
        price:       { type: "number" },
        description: { type: ["string", "null"] },
        imageUrl:    { type: ["string", "null"] },
        category_id: { type: ["integer", "null"] }
    }
};
"""

ORDER_STATUSES = '["pending", "confirmed", "shipping", "delivered", "canceled"]'

ORDER_SCHEMA = """
const orderSchema = {
    type: "object",
    required: ["id", "user_id", "total_amount", "status", "shipping_address", "created_at"],
    properties: {
        id:               { type: "integer" },
        user_id:          { type: "integer" },
        total_amount:     { type: "number" },
        status:           { type: "string", enum: %s },
        shipping_address: { type: ["string", "null"] },
        created_at:       { type: "string" }
    }
};
""" % ORDER_STATUSES

ADMIN_ORDER_SCHEMA = """
const adminOrderSchema = {
    type: "object",
    required: ["id", "user_id", "total_amount", "status", "user_name"],
    properties: {
        id:               { type: "integer" },
        user_id:          { type: ["integer", "null"] },
        total_amount:     { type: "number" },
        status:           { type: "string", enum: %s },
        shipping_address: { type: ["string", "null"] },
        created_at:       { type: "string" },
        user_name:        { type: ["string", "null"] }
    }
};
""" % ORDER_STATUSES


# ---------------------------------------------------------------------------
# Pre-request fixture snippets
# ---------------------------------------------------------------------------

def login_fixture(email_expr, password_expr, var):
    """Log in and stash the JWT in a request-scoped variable."""
    return """
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/login",
    method: "POST",
    header: { "Content-Type": "application/json",
              "X-Student-Id": pm.environment.get("student_id") },
    body: { mode: "raw", raw: JSON.stringify({
        email: %s, password: %s }) }
}, function (err, res) {
    if (res && res.json() && res.json().token) {
        pm.variables.set("%s", res.json().token);
        pm.variables.set("%s_uid", res.json().user.id);
    }
});
""" % (email_expr, password_expr, var, var)


# --- fixture chain builder -------------------------------------------------
#
# Fixtures are built as an explicitly nested chain of pm.sendRequest callbacks.
# Nesting matters: each step needs the previous step's result (a token, an
# order id), and Postman/Newman completes the pre-request script - callbacks
# included - before the request under test is sent.


def _step(url_js, method, body_js=None, auth_var=None, on_done=""):
    """One pm.sendRequest, with `on_done` nested inside its callback."""
    header = ['"Content-Type": "application/json"',
              '"X-Student-Id": pm.environment.get("student_id")']
    if auth_var:
        header.append('"Authorization": "Bearer " + pm.variables.get("%s")' % auth_var)
    body = ""
    if body_js is not None:
        body = ",\n    body: { mode: \"raw\", raw: JSON.stringify(%s) }" % body_js
    return (
        "pm.sendRequest({\n"
        "    url: %s,\n"
        "    method: \"%s\",\n"
        "    header: { %s }%s\n"
        "}, function (err, res) {\n%s\n});"
        % (url_js, method, ", ".join(header), body, _indent(on_done))
    )


def _indent(src, spaces=4):
    if not src.strip():
        return ""
    pad = " " * spaces
    return "\n".join(pad + line if line.strip() else line
                     for line in src.split("\n"))


BASE = 'pm.environment.get("base_url")'


def _capture_token(var):
    return ('if (res && res.json() && res.json().token) {\n'
            '    pm.variables.set("%s", res.json().token);\n'
            '    pm.variables.set("%s_uid", res.json().user.id);\n'
            '}' % (var, var))


def login_step(email_js, password_js, var, on_done=""):
    return _step(BASE + ' + "/api/login"', "POST",
                 "{ email: %s, password: %s }" % (email_js, password_js),
                 on_done=_capture_token(var) + "\n" + on_done)


def admin_login(on_done=""):
    return login_step('pm.environment.get("admin_email")',
                      'pm.environment.get("admin_password")', "adminTok", on_done)


def seeded_user_login(on_done=""):
    return login_step('pm.environment.get("user_email")',
                      'pm.environment.get("user_password")', "tok", on_done)


def fresh_user(var="tok", prefix="u", on_done=""):
    """Register a throwaway account and log it in. Leaves `<var>` and
    `<var>_uid` set, plus freshEmail / freshPassword."""
    return (
        'const %sEmail = "%s" + pm.variables.get("uniq") + "@domain.com";\n'
        'const %sPassword = "Password123!";\n'
        'pm.variables.set("freshEmail", %sEmail);\n'
        'pm.variables.set("freshPassword", %sPassword);\n'
        % (var, prefix, var, var, var)
    ) + _step(
        BASE + ' + "/api/register"', "POST",
        ('{ name: "Fresh User", email: %sEmail, password: %sPassword, '
         'confirmPassword: %sPassword }') % (var, var, var),
        on_done=login_step("%sEmail" % var, "%sPassword" % var, var, on_done),
    )


def create_order(token_var="tok", amount=250000, var="orderId",
                 address="123 Le Loi, Q1, TP.HCM", on_done=""):
    """Create an order owned by whoever holds `token_var`; store its id."""
    capture = ('if (res && res.json()) { pm.variables.set("%s", res.json().orderId); }'
               % var)
    return _step(
        BASE + ' + "/api/checkout"', "POST",
        '{ total_amount: %d, shipping_address: "%s" }' % (amount, address),
        auth_var=token_var, on_done=capture + "\n" + on_done,
    )


def set_status(status, order_var="orderId", on_done=""):
    """Drive an order to `status` as the seeded admin (adminTok must be set)."""
    return _step(
        BASE + ' + "/api/admin/orders/" + pm.variables.get("%s") + "/status"' % order_var,
        "PUT", '{ status: "%s" }' % status, auth_var="adminTok", on_done=on_done,
    )


# FR-10 legal path to each state, used to build orders in a known status.
FR10_PATH = {
    "pending":   [],
    "confirmed": ["confirmed"],
    "shipping":  ["confirmed", "shipping"],
    "delivered": ["confirmed", "shipping", "delivered"],
    "canceled":  ["canceled"],
}


def create_product(name_js='"HW06 fixture product"', price=123000, var="prodId",
                   token_var="adminTok", category_id=1, on_done=""):
    """Create a product as admin and store its id in `var`.

    Fixtures always work on their own throwaway products - never on the five
    seeded ones - so that a case which updates or deletes cannot disturb the
    cases that run after it.
    """
    capture = ('if (res && res.json()) { pm.variables.set("%s", res.json().id); }'
               % var)
    return _step(
        BASE + ' + "/api/products"', "POST",
        '{ name: %s, price: %d, description: "fixture", imageUrl: "", '
        'category_id: %d }' % (name_js, price, category_id),
        auth_var=token_var, on_done=capture + "\n" + on_done,
    )


def delete_product(var="prodId", token_var="adminTok", on_done=""):
    return _step(
        BASE + ' + "/api/products/" + pm.variables.get("%s")' % var,
        "DELETE", auth_var=token_var, on_done=on_done,
    )


def update_product(fields_js, var="prodId", token_var="adminTok", on_done=""):
    return _step(
        BASE + ' + "/api/products/" + pm.variables.get("%s")' % var,
        "PUT", fields_js, auth_var=token_var, on_done=on_done,
    )


def admin_with_product(name_js='"HW06 fixture product"', price=123000,
                       var="prodId", category_id=1, on_done=""):
    """Log in as admin, then create a throwaway product."""
    return admin_login(create_product(name_js, price, var,
                                      category_id=category_id, on_done=on_done))


def order_in_state(status, amount=250000, order_var="orderId", prefix="o",
                   on_done=""):
    """Fixture: fresh user -> order -> walked to `status` along the legal
    FR-10 path. Leaves `tok`, `adminTok` and `<order_var>` set."""
    chain = on_done
    for step in reversed(FR10_PATH[status]):
        chain = set_status(step, order_var, chain)
    return fresh_user(
        prefix=prefix,
        on_done=create_order(
            amount=amount, var=order_var,
            on_done=admin_login(chain),
        ),
    )
