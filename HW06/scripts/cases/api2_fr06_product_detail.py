#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test-case specification for API 2 - FR-06 Product Detail.

Endpoint: GET /api/products/:id     Pool A     Requirement FR-06

FR-06 as written in the requirement document:
  - the detail view shows the image, name, price, description and category, so
    all five must be present in the payload and correctly typed;
  - the quantity input accepts positive integers only (a UI concern, but it
    means `price` has to be arithmetic-safe on the client).

Beyond FR-06 the endpoint is bound by the REST contract the specification
implies: a resource that does not exist is `404`, not `200` with an empty body.

This is the collection that carries the schema-validation evidence. The same
strict assertions are run across **every** seeded product id rather than one
representative, because type drift can be data-dependent.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _helpers import (  # noqa: E402
    PRODUCT_SCHEMA, admin_login, admin_with_product, create_product,
    delete_product, is_array, js, json_content_type, no500, no_credentials,
    no_leak, rejected, st, update_product,
)

CASES = []


def add(**kw):
    CASES.append(kw)
    return kw


PATH = "/api/products/{id}"

# The five products database.js seeds, with the price each one is created with.
SEEDED = [
    (1, "iPhone 15 Pro Max", 30000000),
    (2, "Samsung Galaxy S24 Ultra", 28000000),
    (3, "MacBook Pro M3", 45000000),
    (4, "Tai nghe AirPods Pro 2", 6000000),
    (5, "Bàn phím cơ Keychron Q1", 4000000),
]


def get(id_segment):
    return {"method": "GET", "path": "/api/products/%s" % id_segment}


def found(product_id=None):
    """The resource exists: 200 plus the product that was asked for."""
    check_id = ""
    if product_id is not None:
        check_id = (
            '\npm.test("Returned product is the one requested", function () {\n'
            '    pm.expect(Number(pm.response.json().id)).to.eql(%d);\n});' % product_id
        )
    return (
        'pm.test("Status is 200", function () {\n'
        '    pm.response.to.have.status(200);\n});\n'
        'pm.test("A product object is returned", function () {\n'
        '    const b = pm.response.json();\n'
        '    pm.expect(b).to.be.an("object");\n'
        '    pm.expect(Object.keys(b).length, "product must not be empty")'
        '.to.be.above(0);\n});' + check_id
    )


def not_found():
    """The resource does not exist: 404, and never 200 with an empty object."""
    return (
        'pm.test("Unknown product returns 404", function () {\n'
        '    pm.response.to.have.status(404);\n'
        '});\n'
        'pm.test("Response is not an empty object served as success", function () {\n'
        '    const b = pm.response.json();\n'
        '    const isEmptyObject = b && typeof b === "object" &&\n'
        '                          !Array.isArray(b) && Object.keys(b).length === 0;\n'
        '    pm.expect(isEmptyObject,\n'
        '        "200 with {} makes \\"missing\\" indistinguishable from \\"blank\\""\n'
        '    ).to.be.false;\n'
        '});'
    )


# ===========================================================================
# STEP 2 - DOMAIN PARTITIONS on the :id path parameter
# ===========================================================================

# --- valid ids: every seeded product ---------------------------------------

for _i, (_pid, _name, _price) in enumerate(SEEDED):
    add(id="A2-DP-%03d" % (1 + _i), dim="Domain", param="id", rule="FR-06",
        partition="valid: seeded product id %d (%s)" % (_pid, "odd" if _pid % 2 else "even"),
        title="Product %d (%s) is retrievable" % (_pid, _name),
        expected="200 with product %d" % _pid,
        tests=found(_pid), **get(_pid))

add(id="A2-DP-006", dim="Domain", param="id", rule="FR-06",
    partition="encoding boundary: percent-encoded decimal digit",
    title="A percent-encoded digit resolves to the same product id",
    expected="200 with product 5 after URL decoding",
    tests=found(5), **get("%35"))

add(id="A2-DP-007", dim="Domain", param="id", rule="FR-06",
    partition="boundary: first id beyond the seeded range",
    title="Id 6, one past the seeded range, returns 404",
    expected="404 - no such product", tests=not_found(), **get(6))

# --- non-existent and out-of-range -----------------------------------------

add(id="A2-DP-008", dim="Domain", param="id", rule="FR-06",
    partition="invalid: far out of range",
    title="A far out-of-range id returns 404",
    expected="404", tests=not_found(), **get(999999))

add(id="A2-DP-009", dim="Domain", param="id", rule="FR-06",
    partition="boundary: zero",
    title="Id 0 returns 404",
    expected="404 - ids are AUTOINCREMENT and start at 1",
    tests=not_found(), **get(0))

add(id="A2-DP-010", dim="Domain", param="id", rule="FR-06",
    partition="invalid: negative",
    title="A negative id is rejected",
    expected="400 or 404 - never 200", tests=rejected("ids cannot be negative"),
    **get(-1))

add(id="A2-DP-011", dim="Domain", param="id", rule="FR-06",
    partition="invalid: negative zero",
    title="Id '-0' is rejected",
    expected="400 or 404", tests=rejected("'-0' is not a valid id"), **get("-0"))

add(id="A2-DP-012", dim="Domain", param="id", rule="FR-06",
    partition="boundary: 32-bit integer overflow",
    title="An id beyond 2^31 returns 404 rather than erroring",
    expected="404, never a 5xx",
    tests=not_found() + "\n" + no500(), **get(2147483648))

add(id="A2-DP-013", dim="Domain", param="id", rule="FR-06",
    partition="boundary: beyond 64-bit range",
    title="A 22-digit id is handled without a server error",
    expected="404 or 400, never a 5xx",
    tests=no500() + "\n" + no_leak(), **get("9999999999999999999999"))

# --- wrong type / malformed ------------------------------------------------

_MALFORMED = [
    ("abc", "alphabetic", "an id must be numeric"),
    ("1.5", "decimal", "ids are integers"),
    ("1e0", "scientific notation", "ids are plain integers"),
    ("0x1", "hexadecimal literal", "ids are decimal integers"),
    ("+1", "explicit plus sign", "ids carry no sign"),
    ("null", "the literal string 'null'", "not a numeric id"),
    ("undefined", "the literal string 'undefined'", "not a numeric id"),
    ("true", "a boolean literal", "not a numeric id"),
    ("NaN", "NaN", "not a numeric id"),
    ("Infinity", "Infinity", "not a numeric id"),
    ("1abc", "digits followed by letters", "not a well-formed integer"),
    ("abc1", "letters followed by digits", "not a well-formed integer"),
]

for _i, (_seg, _label, _why) in enumerate(_MALFORMED):
    add(id="A2-DP-%03d" % (14 + _i), dim="Domain", param="id", rule="FR-06",
        partition="invalid: %s" % _label,
        title="Id '%s' (%s) is rejected" % (_seg, _label),
        expected="400 - %s" % _why,
        tests=rejected(_why) + "\n" + no500(), **get(_seg))

# --- formatting edges ------------------------------------------------------

add(id="A2-DP-026", dim="Domain", param="id", rule="FR-06",
    partition="edge: leading zeros",
    title="Id '01' resolves to product 1 or is rejected, but never 404s silently",
    expected="200 for product 1, or a 400; not a 404 for a product that exists",
    tests=no500(),
    gap="The spec does not say whether ids are normalised before lookup.",
    **get("01"))

add(id="A2-DP-027", dim="Domain", param="id", rule="FR-06",
    partition="edge: leading whitespace",
    title="Id ' 1' with a leading space is rejected or trimmed",
    expected="400, or 200 for product 1 - never a 5xx",
    tests=no500(), gap="Trimming behaviour is unspecified.", **get("%201"))

add(id="A2-DP-028", dim="Domain", param="id", rule="FR-06",
    partition="edge: percent-encoded space only",
    title="An id consisting solely of an encoded space is rejected",
    expected="400 or 404", tests=no500() + "\n" + no_leak(), **get("%20"))

add(id="A2-DP-029", dim="Domain", param="id", rule="FR-06",
    partition="edge: very long numeric id",
    title="A 300-digit id does not crash the server",
    expected="404 or 400, never a 5xx",
    tests=no500() + "\n" + no_leak(), **get("1" * 300))

add(id="A2-DP-030", dim="Domain", param="id", rule="FR-06",
    partition="edge: extra path segment",
    title="An extra path segment is not routed to product detail",
    expected="404 - /api/products/1/2 is not a documented route",
    tests=st(404, 405), **get("1/2"))

add(id="A2-DP-031", dim="Domain", param="id", rule="FR-06",
    partition="edge: empty id (trailing slash)",
    title="A trailing slash falls through to the product list, not to detail",
    expected="200 with an ARRAY - this is the list route, not a product",
    tests=js("""
pm.test("Status is 200", () => pm.response.to.have.status(200));
pm.test("An empty id lands on the list route, returning an array", function () {
    pm.expect(pm.response.json()).to.be.an("array");
});"""),
    gap="Documents routing behaviour the spec does not describe.",
    **get(""))

# --- HTTP methods on the detail route --------------------------------------

for _i, _method in enumerate(["POST", "PATCH"]):
    add(id="A2-DP-%03d" % (32 + _i), dim="Domain", param="http method",
        rule="spec conformance",
        partition="invalid: %s on the detail route" % _method,
        title="%s /api/products/:id is not routed" % _method,
        method=_method, path="/api/products/1", body=None,
        expected="404 or 405 - the spec documents GET, PUT and DELETE only",
        tests=st(404, 405))

add(id="A2-DP-034", dim="Domain", param="http method", rule="spec conformance",
    partition="valid: HEAD mirrors GET",
    title="HEAD /api/products/1 succeeds without a body",
    method="HEAD", path="/api/products/1",
    expected="200 - HEAD is GET without the payload",
    tests=st(200))

add(id="A2-DP-035", dim="Domain", param="id", rule="FR-06",
    partition="valid: repeated read is stable",
    title="Reading the same product twice returns an identical payload",
    expected="the second read is byte-identical to the first",
    pre=js("""
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/products/3",
    method: "GET",
    header: { "X-Student-Id": pm.environment.get("student_id") }
}, function (err, res) {
    if (res) { pm.variables.set("firstRead", res.text()); }
});"""),
    tests=js("""
pm.test("GET is idempotent for an unchanged product", function () {
    pm.expect(pm.response.text()).to.eql(pm.variables.get("firstRead"));
});"""),
    **get(3))


# ===========================================================================
# STEP 3 - STATE TRANSITIONS
# ===========================================================================
# Product existence lifecycle: absent -> created -> updated -> deleted -> absent.
# Every fixture works on its own throwaway product, never on the seeded five,
# so a case that deletes cannot disturb the cases that follow it.

add(id="A2-ST-001", dim="State", param="-", rule="FR-06",
    partition="transition: absent -> created",
    title="A newly created product is immediately retrievable by id",
    method="GET", path="/api/products/{{prodId}}",
    pre=js(admin_with_product('"HW06 ST-001 " + pm.variables.get("uniq")', 111000)),
    expected="200 with the product just created",
    tests=js("""
pm.test("Status is 200", () => pm.response.to.have.status(200));
pm.test("The created product is returned", function () {
    pm.expect(String(pm.response.json().id))
      .to.eql(String(pm.variables.get("prodId")));
});"""))

add(id="A2-ST-002", dim="State", param="-", rule="FR-06",
    partition="transition: created -> renamed",
    title="A renamed product's detail reflects the new name",
    method="GET", path="/api/products/{{prodId}}",
    pre=js(admin_with_product(
        '"HW06 ST-002 " + pm.variables.get("uniq")', 111000,
        on_done=update_product(
            '{ name: "Renamed " + pm.variables.get("uniq"), price: 111000, '
            'description: "fixture", imageUrl: "", category_id: 1 }'))),
    expected="the detail payload carries the updated name",
    tests=js("""
pm.test("Detail reflects the rename", function () {
    pm.expect(String(pm.response.json().name))
      .to.include("Renamed " + pm.variables.get("uniq"));
});"""))

add(id="A2-ST-003", dim="State", param="-", rule="FR-06",
    partition="transition: created -> repriced",
    title="A repriced product's detail reflects the new price, still as a number",
    method="GET", path="/api/products/{{prodId}}",
    pre=js(admin_with_product(
        '"HW06 ST-003 " + pm.variables.get("uniq")', 111000,
        on_done=update_product(
            '{ name: "Repriced", price: 222000, description: "fixture", '
            'imageUrl: "", category_id: 1 }'))),
    expected="price === 222000 as a JSON number",
    tests=js("""
pm.test("Detail reflects the new price", function () {
    pm.expect(Number(pm.response.json().price)).to.eql(222000);
});
pm.test("price is still a number after an update", function () {
    pm.expect(pm.response.json().price).to.be.a("number");
});"""))

add(id="A2-ST-004", dim="State", param="-", rule="FR-06",
    partition="transition: created -> deleted",
    title="A deleted product is no longer retrievable",
    method="GET", path="/api/products/{{prodId}}",
    pre=js(admin_with_product('"HW06 ST-004 " + pm.variables.get("uniq")', 111000,
                              on_done=delete_product())),
    expected="404 - the product no longer exists",
    tests=not_found())

add(id="A2-ST-005", dim="State", param="-", rule="FR-06",
    partition="transition: deleted -> recreated gets a fresh identity",
    title="Recreating a deleted product yields a different id",
    method="GET", path="/api/products/{{prodId2}}",
    pre=js(admin_with_product(
        '"HW06 ST-005a " + pm.variables.get("uniq")', 111000,
        on_done=delete_product(on_done=create_product(
            '"HW06 ST-005b " + pm.variables.get("uniq")', 111000, var="prodId2")))),
    expected="200, and the new id differs from the deleted one",
    tests=js("""
pm.test("Status is 200", () => pm.response.to.have.status(200));
pm.test("The recreated product has a new identity", function () {
    pm.expect(String(pm.response.json().id))
      .to.not.eql(String(pm.variables.get("prodId")));
});"""))

add(id="A2-ST-006", dim="State", param="-", rule="FR-06 / FR-05",
    partition="consistency: detail agrees with the list",
    title="The detail payload matches the product's entry in the list",
    method="GET", path="/api/products/2",
    pre=js("""
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/products",
    method: "GET",
    header: { "X-Student-Id": pm.environment.get("student_id") }
}, function (err, res) {
    if (res && Array.isArray(res.json())) {
        const match = res.json().find(function (p) { return Number(p.id) === 2; });
        if (match) { pm.variables.set("listEntry", JSON.stringify(match)); }
    }
});"""),
    expected="every field, and every field's type, matches the list entry",
    tests=js("""
const fromList = JSON.parse(pm.variables.get("listEntry"));
const fromDetail = pm.response.json();
pm.test("Detail and list agree on the product's fields", function () {
    pm.expect(fromDetail).to.eql(fromList);
});
pm.test("price has the same JSON type in both views", function () {
    pm.expect(typeof fromDetail.price, "detail price type")
      .to.eql(typeof fromList.price);
});"""))

add(id="A2-ST-007", dim="State", param="-", rule="FR-06",
    partition="transition: category reassigned",
    title="Reassigning a product's category is reflected in its detail",
    method="GET", path="/api/products/{{prodId}}",
    pre=js(admin_with_product(
        '"HW06 ST-007 " + pm.variables.get("uniq")', 111000, category_id=1,
        on_done=update_product(
            '{ name: "Recategorised", price: 111000, description: "fixture", '
            'imageUrl: "", category_id: 2 }'))),
    expected="category_id === 2",
    tests=js("""
pm.test("Detail reflects the new category", function () {
    pm.expect(Number(pm.response.json().category_id)).to.eql(2);
});"""))

add(id="A2-ST-008", dim="State", param="-", rule="FR-06",
    partition="transition: category deleted underneath the product",
    title="Deleting a product's category does not break its detail view",
    method="GET", path="/api/products/{{prodId}}",
    pre=js(admin_login(
        _cat := """
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/categories",
    method: "POST",
    header: { "Content-Type": "application/json",
              "X-Student-Id": pm.environment.get("student_id"),
              "Authorization": "Bearer " + pm.variables.get("adminTok") },
    body: { mode: "raw", raw: JSON.stringify({
        name: "HW06 temp " + pm.variables.get("uniq") }) }
}, function (err, res) {
    const catId = res && res.json() ? res.json().id : 1;
    pm.variables.set("tempCat", catId);
    pm.sendRequest({
        url: pm.environment.get("base_url") + "/api/products",
        method: "POST",
        header: { "Content-Type": "application/json",
                  "X-Student-Id": pm.environment.get("student_id"),
                  "Authorization": "Bearer " + pm.variables.get("adminTok") },
        body: { mode: "raw", raw: JSON.stringify({
            name: "Orphan " + pm.variables.get("uniq"), price: 111000,
            description: "fixture", imageUrl: "", category_id: catId }) }
    }, function (err, res2) {
        if (res2 && res2.json()) { pm.variables.set("prodId", res2.json().id); }
        pm.sendRequest({
            url: pm.environment.get("base_url") + "/api/categories/" + catId,
            method: "DELETE",
            header: { "X-Student-Id": pm.environment.get("student_id"),
                      "Authorization": "Bearer " + pm.variables.get("adminTok") }
        }, function () {});
    });
});""")),
    expected="200 - the product is still readable even with a dangling category_id",
    tests=js("""
pm.test("Product detail survives its category being deleted", function () {
    pm.response.to.have.status(200);
});""") + "\n" + no500(),
    gap="The spec does not define referential behaviour when a category is removed.")

add(id="A2-ST-009", dim="State", param="-", rule="FR-06",
    partition="isolation: reads do not mutate",
    title="Reading a product does not change it",
    method="GET", path="/api/products/4",
    pre=js("""
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/products/4",
    method: "GET",
    header: { "X-Student-Id": pm.environment.get("student_id") }
}, function (err, res) {
    if (res) { pm.variables.set("beforeRead", res.text()); }
});"""),
    expected="the payload is unchanged after a prior read",
    tests=js("""
pm.test("A GET has no side effect on the resource", function () {
    pm.expect(pm.response.text()).to.eql(pm.variables.get("beforeRead"));
});"""))

add(id="A2-ST-010", dim="State", param="-", rule="FR-06",
    partition="consistency: a freshly created product is well typed",
    title="A product created through the API has a numeric price on read-back",
    method="GET", path="/api/products/{{prodId}}",
    pre=js(admin_with_product('"HW06 ST-010 " + pm.variables.get("uniq")', 999000)),
    expected="price === 999000 as a JSON number, whatever the id turns out to be",
    tests=js("""
pm.test("price of a newly created product is a JSON number", function () {
    pm.expect(pm.response.json().price,
        "id " + pm.variables.get("prodId") + " returned price as " +
        typeof pm.response.json().price).to.be.a("number");
});"""))


# ===========================================================================
# STEP 4 - SECURITY (SEC-01 .. SEC-07)
# ===========================================================================

_INJECTIONS = [
    ("1 OR 1=1", "tautology", "must not widen the result set"),
    ("1' OR '1'='1", "quoted tautology", "must not widen the result set"),
    ("1; DROP TABLE products;--", "statement termination", "must not execute a second statement"),
    ("1 UNION SELECT id,email,password,role,id,id FROM users--", "UNION SELECT against users",
     "must not return credential data"),
    ("1--", "comment sequence", "must not truncate the query"),
]

for _i, (_payload, _label, _why) in enumerate(_INJECTIONS):
    add(id="A2-SEC-%03d" % (1 + _i), dim="Security", param="id", rule="SEC-05",
        partition="SQL injection: %s" % _label,
        title="Injection via :id (%s) is neutralised" % _label,
        expected="no 5xx, no SQL error text, no extra rows, no credential leak",
        tests=no500() + "\n" + no_leak() + "\n" + no_credentials() + js("""
pm.test("Injection does not turn the detail route into a list", function () {
    pm.expect(Array.isArray(pm.response.json()),
        "a single-resource route must never return an array").to.be.false;
});"""),
        **get(_payload))

add(id="A2-SEC-006", dim="Security", param="id", rule="SEC-05",
    partition="SQL injection: data integrity afterwards",
    title="The products table survives the injection attempts intact",
    method="GET", path="/api/products",
    pre=js("""
const base = pm.environment.get("base_url");
const sid = pm.environment.get("student_id");
["1; DROP TABLE products;--", "1' OR '1'='1"].forEach(function (payload) {
    pm.sendRequest({
        url: base + "/api/products/" + encodeURIComponent(payload),
        method: "GET",
        header: { "X-Student-Id": sid }
    }, function () {});
});"""),
    expected="the five seeded products are still listed",
    tests=is_array() + js("""
pm.test("Seeded products survived the injection attempts", function () {
    pm.expect(pm.response.json().length,
        "at least the five seeded products").to.be.at.least(5);
});"""))

add(id="A2-SEC-007", dim="Security", param="id", rule="SEC-05",
    partition="path traversal",
    title="A path-traversal payload does not escape the route",
    expected="404 or 400 - no file content, no directory listing",
    tests=no500() + "\n" + no_leak() + js("""
pm.test("No filesystem content is returned", function () {
    pm.expect(pm.response.text()).to.not.include("root:");
});"""),
    **get("..%2F..%2Fetc%2Fpasswd"))

add(id="A2-SEC-008", dim="Security", param="name", rule="SEC-04",
    partition="stored XSS returned through the detail view",
    title="A script payload in a product name is returned as inert JSON data",
    method="GET", path="/api/products/{{prodId}}",
    pre=js(admin_with_product(
        '"<script>alert(1)</script>" + pm.variables.get("uniq")', 111000)),
    expected="Content-Type is application/json and the payload is a string field",
    tests=json_content_type() + js("""
pm.test("Payload is preserved as data, not rendered as markup", function () {
    pm.expect(pm.response.json().name).to.be.a("string");
});"""))

add(id="A2-SEC-009", dim="Security", param="-", rule="SEC-01",
    partition="information disclosure in the detail payload",
    title="Product detail exposes no credential or internal fields",
    expected="no password, token, role or reset_token key",
    tests=no_credentials() + js("""
const text = pm.response.text().toLowerCase();
["token", "role", "reset_token"].forEach(function (key) {
    pm.test('Detail payload contains no "' + key + '" field', function () {
        pm.expect(text).to.not.include('"' + key + '"');
    });
});"""),
    **get(1))

add(id="A2-SEC-010", dim="Security", param="-", rule="SEC-02 (not applicable)",
    partition="authentication requirement: browsing is public by design",
    title="Product detail is readable without any Authorization header",
    expected="200 - SEC-02 does not apply to public product browsing",
    tests=found(1),
    gap="Documents why SEC-02 is not applicable to this endpoint.",
    **get(1))

# --- FR-12 / SEC-03: the mutating siblings of this route -------------------
# FR-12 names POST/PUT/DELETE /api/products explicitly as routes that must
# require a valid token AND role='admin'. They share the detail route's path,
# so they belong in this collection's security folder.

add(id="A2-SEC-011", dim="Security", param="-", rule="FR-12 / SEC-02",
    partition="unauthenticated write: create",
    title="Creating a product without a token must be refused",
    method="POST", path="/api/products",
    body={"name": "Anonymous product {{uniq}}", "price": 1000,
          "description": "should not exist", "imageUrl": "", "category_id": 1},
    expected="401 - FR-12 requires a valid JWT on POST /api/products",
    tests=rejected("no token supplied", 401, 403))

add(id="A2-SEC-012", dim="Security", param="-", rule="FR-12 / SEC-02",
    partition="unauthenticated write: update",
    title="Updating a product without a token must be refused",
    method="PUT", path="/api/products/{{prodId}}",
    body={"name": "Hijacked", "price": 1, "description": "", "imageUrl": "",
          "category_id": 1},
    pre=js(admin_with_product('"HW06 SEC-012 " + pm.variables.get("uniq")', 111000)),
    expected="401 - FR-12 requires a valid JWT on PUT /api/products/:id",
    tests=rejected("no token supplied", 401, 403))

add(id="A2-SEC-013", dim="Security", param="-", rule="FR-12 / SEC-02",
    partition="unauthenticated write: delete",
    title="Deleting a product without a token must be refused",
    method="DELETE", path="/api/products/{{prodId}}",
    pre=js(admin_with_product('"HW06 SEC-013 " + pm.variables.get("uniq")', 111000)),
    expected="401 - FR-12 requires a valid JWT on DELETE /api/products/:id",
    tests=rejected("no token supplied", 401, 403))

add(id="A2-SEC-014", dim="Security", param="-", rule="FR-12 / SEC-03",
    partition="non-admin write: update",
    title="A non-admin token must not be able to update a product",
    method="PUT", path="/api/products/{{prodId}}", auth_var="tok",
    body={"name": "Hijacked by user", "price": 1, "description": "",
          "imageUrl": "", "category_id": 1},
    pre=js(admin_with_product(
        '"HW06 SEC-014 " + pm.variables.get("uniq")', 111000,
        on_done="""
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
    expected="403 - SEC-03 requires role='admin', not merely a valid token",
    tests=rejected("caller is not an admin", 401, 403))

add(id="A2-SEC-015", dim="Security", param="-", rule="FR-12 / SEC-03",
    partition="non-admin write: delete",
    title="A non-admin token must not be able to delete a product",
    method="DELETE", path="/api/products/{{prodId}}", auth_var="tok",
    pre=js(admin_with_product(
        '"HW06 SEC-015 " + pm.variables.get("uniq")', 111000,
        on_done="""
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
    expected="403 - SEC-03 requires role='admin'",
    tests=rejected("caller is not an admin", 401, 403))

add(id="A2-SEC-016", dim="Security", param="-", rule="SEC-05",
    partition="information disclosure on error",
    title="An invalid id must not leak database internals",
    expected="a clean 4xx with no driver, table or stack detail",
    tests=no_leak() + "\n" + no500(), **get("';--"))


# ===========================================================================
# STEP 5 - SCHEMA VALIDATION
# ===========================================================================
# The same strict assertions across EVERY seeded id, because type drift can be
# data-dependent - checking one representative id would miss it.

for _i, (_pid, _name, _price) in enumerate(SEEDED):
    add(id="A2-SCH-%03d" % (1 + _i), dim="Schema", param="-",
        rule="spec conformance",
        partition="strict schema for product %d" % _pid,
        title="Product %d conforms to the product schema" % _pid,
        expected="validates against the schema with additionalProperties false",
        tests=PRODUCT_SCHEMA + js("""
pm.test("Response conforms to the product schema", function () {
    pm.response.to.have.jsonSchema(productSchema);
});"""),
        **get(_pid))

for _i, (_pid, _name, _price) in enumerate(SEEDED):
    add(id="A2-SCH-%03d" % (6 + _i), dim="Schema", param="price",
        rule="FR-06 / spec conformance",
        partition="price type for product %d (%s id)" % (_pid, "odd" if _pid % 2 else "even"),
        title="price of product %d is a JSON number" % _pid,
        expected="typeof price === 'number', for every id without exception",
        tests=js("""
const price = pm.response.json().price;
pm.test("price is a JSON number, not a string", function () {
    pm.expect(price, "product %d returned price as a " + typeof price)
      .to.be.a("number");
});
pm.test("price is arithmetic-safe", function () {
    pm.expect(price + 1, "adding 1 must not concatenate")
      .to.eql(Number(price) + 1);
});""" % _pid),
        **get(_pid))

add(id="A2-SCH-011", dim="Schema", param="id", rule="spec conformance",
    partition="id type",
    title="id is a JSON integer",
    expected="Number.isInteger(id)",
    tests=js("""
pm.test("id is an integer", function () {
    const id = pm.response.json().id;
    pm.expect(id).to.be.a("number");
    pm.expect(Number.isInteger(id)).to.be.true;
});"""), **get(1))

add(id="A2-SCH-012", dim="Schema", param="category_id", rule="FR-06",
    partition="category_id type",
    title="category_id is a JSON integer",
    expected="FR-06 requires the category to be displayable",
    tests=js("""
pm.test("category_id is an integer", function () {
    pm.expect(Number.isInteger(pm.response.json().category_id)).to.be.true;
});"""), **get(1))

add(id="A2-SCH-013", dim="Schema", param="name", rule="FR-06",
    partition="name presence and type",
    title="name is a non-empty string",
    expected="FR-06 requires the name to be displayed",
    tests=js("""
pm.test("name is a non-empty string", function () {
    const n = pm.response.json().name;
    pm.expect(n).to.be.a("string");
    pm.expect(n.length).to.be.above(0);
});"""), **get(1))

add(id="A2-SCH-014", dim="Schema", param="description", rule="FR-06",
    partition="description presence and type",
    title="description is a string",
    expected="FR-06 requires the description to be displayed",
    tests=js("""
pm.test("description is a string", function () {
    pm.expect(pm.response.json().description).to.be.a("string");
});"""), **get(1))

add(id="A2-SCH-015", dim="Schema", param="imageUrl", rule="FR-06",
    partition="imageUrl presence and type",
    title="imageUrl is a string",
    expected="FR-06 requires a large image to be displayed",
    tests=js("""
pm.test("imageUrl is a string", function () {
    pm.expect(pm.response.json().imageUrl).to.be.a("string");
});"""), **get(1))

add(id="A2-SCH-016", dim="Schema", param="-", rule="spec conformance",
    partition="no undocumented fields",
    title="The product payload carries exactly the six documented fields",
    expected="keys are exactly id, name, price, description, imageUrl, category_id",
    tests=js("""
pm.test("Exactly the documented keys are present", function () {
    const keys = Object.keys(pm.response.json()).sort();
    pm.expect(keys).to.eql(
        ["category_id", "description", "id", "imageUrl", "name", "price"]);
});"""), **get(1))

add(id="A2-SCH-017", dim="Schema", param="-", rule="spec conformance",
    partition="response headers",
    title="Product detail is served as application/json",
    expected="Content-Type includes application/json",
    tests=json_content_type(), **get(1))

add(id="A2-SCH-018", dim="Schema", param="-", rule="spec conformance",
    partition="error body: not-found shape",
    title="A not-found response carries a structured error body",
    expected='404 with {"error": "<string>"}',
    tests=js("""
pm.test("Missing product returns 404", function () {
    pm.response.to.have.status(404);
});
pm.test("Error body is structured JSON", function () {
    const b = pm.response.json();
    pm.expect(b).to.have.property("error");
    pm.expect(b.error).to.be.a("string");
});"""), **get(424242))

add(id="A2-SCH-019", dim="Schema", param="price", rule="FR-06",
    partition="business rule: price is positive",
    title="A product's price is greater than zero",
    expected="price > 0 - a saleable product cannot be free or negative",
    tests=js("""
pm.test("price is positive", function () {
    pm.expect(Number(pm.response.json().price)).to.be.above(0);
});"""), **get(1))

add(id="A2-SCH-020", dim="Schema", param="id", rule="spec conformance",
    partition="identity: response matches the request",
    title="The returned id equals the requested id",
    expected="response.id === 5",
    tests=js("""
pm.test("The product returned is the one requested", function () {
    pm.expect(Number(pm.response.json().id)).to.eql(5);
});"""), **get(5))

add(id="A2-SCH-021", dim="Schema", param="-", rule="spec conformance",
    partition="type stability across the whole catalogue",
    title="Every product in the catalogue has a numeric price",
    method="GET", path="/api/products",
    expected="no product in the list types price as a string",
    tests=is_array() + js("""
const offenders = pm.response.json()
    .filter(function (p) { return typeof p.price !== "number"; })
    .map(function (p) { return p.id; });
pm.test("No product types price as a string", function () {
    pm.expect(offenders, "product ids with a non-numeric price").to.eql([]);
});"""))

add(id="A2-SCH-022", dim="Schema", param="-", rule="spec conformance",
    partition="error body: not an HTML page",
    title="A not-found error is JSON, never an HTML page",
    expected="Content-Type is not text/html",
    tests=js("""
pm.test("Error response is not an HTML page", function () {
    pm.expect((pm.response.headers.get("Content-Type") || "").toLowerCase())
      .to.not.include("text/html");
});"""), **get(313131))


# ===========================================================================
# PHASE 3 - STUDENT-DESIGNED EXTENSIONS
# ===========================================================================

add(id="A2-HR-001", dim="Domain", param="id", rule="FR-06",
    partition="valid: percent-encoded digit in the path segment",
    title="A percent-encoded product id returns the same resource",
    expected="200 with product 1", tests=found(1), **get("%31"),
    origin="Student-designed",
    rationale="The AI tested whitespace encoding but not a valid id represented through URL encoding.")

add(id="A2-HR-002", dim="Security", param="query string", rule="FR-06 / SEC-04",
    partition="parameter pollution: query id must not override path id",
    title="A query-string id cannot override the product path id",
    method="GET", path="/api/products/1", raw_query="?id=2",
    expected="200 with product 1, not product 2", tests=found(1),
    origin="Student-designed",
    rationale="The generated suite did not test precedence when the same logical identifier appears in path and query.")

add(id="A2-HR-003", dim="Schema", param="Accept", rule="spec conformance",
    partition="content negotiation: explicit JSON acceptance",
    title="An explicit Accept: application/json request returns JSON",
    method="GET", path="/api/products/3",
    extra_headers=[{"key": "Accept", "value": "application/json"}],
    expected="200 with application/json", tests=found(3) + "\n" + json_content_type(),
    origin="Student-designed",
    rationale="The AI asserted the response media type but did not exercise explicit content negotiation.")

add(id="A2-HR-004", dim="Security", param="id", rule="SEC-04 / SEC-05",
    partition="invalid: double-encoded SQL metacharacters",
    title="A double-encoded SQL payload is neutralised",
    method="GET", path="/api/products/1%2520OR%25201%253D1",
    expected="clean 4xx, never a query expansion or server error",
    tests=rejected("double-encoded id is not an integer") + "\n" + no500() + "\n" + no_leak(),
    origin="Student-designed",
    rationale="The AI covered plain SQL payloads but missed a second decoding layer used to bypass filters.")

add(id="A2-HR-005", dim="Domain", param="id", rule="FR-06 / SEC-04",
    partition="invalid: full-width Unicode digit",
    title="A full-width Unicode digit is not confused with an ASCII id",
    method="GET", path="/api/products/%EF%BC%91",
    expected="400 or 404, never product 1 and never a 5xx",
    tests=rejected("ids use ASCII decimal digits") + "\n" + no500(),
    origin="Student-designed",
    rationale="The AI's malformed-id set was ASCII-only and omitted Unicode confusable characters.")


# ---------------------------------------------------------------------------

META = {
    "api": 2,
    "slug": "api2-fr06-product-detail",
    "collection_name": "API2 - FR-06 Product Detail (GET /api/products/:id)",
    "sheet": "API2 FR-06 Product Detail",
    "endpoint": "GET /api/products/:id",
    "pool": "A",
    "requirement": "FR-06",
    "description": (
        "HW06 / Pool A / FR-06 - Product detail.\n\n"
        "Spec: GET /api/products/:id -> the product record.\n\n"
        "Generated from scripts/cases/api2_fr06_product_detail.py. This is the "
        "collection carrying the schema-validation evidence: the strict schema "
        "and the price-type assertions are repeated across every seeded product "
        "id, because type drift here is data-dependent and a single "
        "representative id would miss it.\n\n"
        "Fixtures always create their own throwaway products - the five seeded "
        "products are never modified or deleted, so no case can disturb another."
    ),
    "folders": [
        ("01 - Domain partitions", "Domain",
         "Equivalence classes and boundaries on the :id path parameter, plus "
         "the HTTP methods the route does and does not accept."),
        ("02 - State transitions", "State",
         "Product existence lifecycle: absent -> created -> updated -> deleted "
         "-> absent, and read-consistency invariants."),
        ("03 - Security (SEC-01..SEC-07)", "Security",
         "SEC-05 injection through the path parameter, SEC-04 stored XSS, and "
         "the FR-12 / SEC-03 access control on the mutating siblings of this "
         "route."),
        ("04 - Schema validation", "Schema",
         "The response shape against api_specification.md, asserted strictly "
         "and repeated per product id."),
    ],
    "subfolders": {
        "01 - Domain partitions": [
            ("id", "id"),
            ("http method", "http method"),
        ],
    },
}
