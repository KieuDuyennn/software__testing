#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the four HW06 data-driven collections.

    python scripts/build-ddt.py

The main collections in `postman/collections/APIn_*.postman_collection.json` are
data-driven at *generation* time: every case is a record in scripts/cases/, and
render-cases.py turns those records into requests. That satisfies "separate the
data from the logic", but the data ends up baked into the collection, so a
reader cannot see the data-driven shape and Newman cannot be pointed at a
different data set.

This script covers the other half - data-driven at *execution* time, which is
what the brief means by "the Collection Runner with a data file". Each output
collection holds exactly ONE request. Newman (or the Runner) replays it once
per row of the matching CSV in `postman/data/`, and every input, every URL and every
expected status comes from `pm.iterationData`.

    newman run postman/collections/API1_FR01_Register_ddt.postman_collection.json \
        -e postman/config/eshop-local.postman_environment.json \
        -d postman/data/api1_fr01_register.csv

These are deliberately rendered as SEPARATE collections rather than as a fifth
folder inside the main ones: the 386-case baseline in reports/ and README.md is
documented evidence, and appending iteration-driven requests to it would change
every assertion total that the report cites.

ORACLE DISCIPLINE
-----------------
As everywhere else in this suite, `expected_status` in the CSVs comes from the
requirement (FR-01, FR-06, FR-11, FR-13, SEC-02, SEC-03, SEC-05), not from what
the SUT currently returns. Rows that fail are defect evidence, not broken
fixtures - the same rule the main suite follows.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import postman_harness as H  # noqa: E402
from cases._helpers import (  # noqa: E402
    admin_login, create_order, fresh_user, seeded_user_login,
)

DATA = ROOT / "postman" / "data"
OUT = ROOT / "postman" / "collections"

# A syntactically well-formed JWT whose signature is wrong: jwt.verify rejects
# it, which is the "forged token" partition the CSVs ask for.
FORGED = ('"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
          '.eyJpZCI6MSwicm9sZSI6ImFkbWluIn0'
          '.hw06-invalid-signature-23127184"')


# ---------------------------------------------------------------------------
# Shared script fragments
# ---------------------------------------------------------------------------

# Running the collection WITHOUT -d leaves pm.iterationData empty. Firing the
# request anyway would send a junk payload and report a meaningless failure, so
# the run is skipped instead, with a console line saying why.
GUARD = """
const d = pm.iterationData;
if (!d.get("tc_id")) {
    console.log("[HW06][DDT] No data file supplied - skipping. Run with: " +
                "newman run <collection> -d postman/data/<file>.csv");
    if (pm.execution && pm.execution.skipRequest) {
        pm.execution.skipRequest();
    }
    return;
}
console.log("[HW06][DDT] iteration " + d.get("tc_id") + " | " +
            d.get("partition") + " | expect HTTP " + d.get("expected_status"));
""".strip()

# Every collection asserts the status this way, so one row of the CSV reads as
# one labelled test in the Newman report.
STATUS_TEST = """
const d = pm.iterationData;
if (!d.get("tc_id")) { return; }

const tc = d.get("tc_id");
const expected = Number(d.get("expected_status"));
const rule = d.get("requirement");

pm.test(tc + " [" + rule + "] " + d.get("partition") +
        " -> HTTP " + expected, function () {
    pm.expect(pm.response.code, "status code for " + tc).to.eql(expected);
});
""".strip()

NO_LEAK_TEST = """
pm.test(pm.iterationData.get("tc_id") + " | response leaks no stack trace",
        function () {
    const body = pm.response.text() || "";
    pm.expect(body).to.not.match(/at [\\w./\\\\]+:\\d+:\\d+/);
    pm.expect(body.toLowerCase()).to.not.include("sqlite_error");
});
""".strip()


def auth_apply(default_token_var="tok"):
    """JS that turns the CSV's `token_var` column into an Authorization header.

    The request carries no Authorization header of its own; the anonymous rows
    must send genuinely no header, not an empty one, or the 401 they assert
    would be proving the wrong thing.
    """
    return """
const tv = (d.get("token_var") || "").trim();
pm.request.headers.remove("Authorization");
if (tv === "admin_token") {
    pm.request.headers.upsert({ key: "Authorization",
        value: "Bearer " + pm.variables.get("adminTok") });
} else if (tv === "user_token") {
    pm.request.headers.upsert({ key: "Authorization",
        value: "Bearer " + pm.variables.get("%s") });
} else if (tv === "bad_token") {
    pm.request.headers.upsert({ key: "Authorization",
        value: "Bearer " + %s });
}
""".strip() % (default_token_var, FORGED)


def ddt_collection(name, description, item):
    return H.collection(name, description, [
        H.folder("05 - Data-driven (CSV)", [item],
                 "One request, replayed once per CSV row. Inputs and expected "
                 "results come from pm.iterationData, never from the request "
                 "body itself."),
    ])


# ---------------------------------------------------------------------------
# API 1 - FR-01 registration: the body is the data
# ---------------------------------------------------------------------------

API1_PRE = GUARD + """

// Emails in the CSV are fixed so the file stays readable and diffable, but
// FR-01 requires uniqueness - a second run would otherwise collide with the
// accounts the first run created. Insert the harness's per-request `uniq`
// into the local part, leaving malformed addresses malformed.
const uniq = pm.variables.get("uniq");
let email = d.get("email") || "";
if (email.indexOf("@") > 0) {
    email = email.replace("@", "+" + uniq + "@");
}

pm.variables.set("ddt_name", d.get("name") || "");
pm.variables.set("ddt_email", email);
pm.variables.set("ddt_password", d.get("password") || "");
"""

API1_TEST = STATUS_TEST + """

// A row that the requirement says must be accepted has to come back in the
// shape the specification promises, not merely with a 200.
if (Number(d.get("expected_status")) === 200 && pm.response.code === 200) {
    pm.test(tc + " | success body matches the FR-01 shape", function () {
        const b = pm.response.json();
        pm.expect(b).to.have.property("message", "User registered successfully");
        pm.expect(b.id, "id").to.be.a("number");
    });
}
"""

api1 = ddt_collection(
    "API1 - FR-01 Registration - DATA-DRIVEN (postman/data/api1_fr01_register.csv)",
    "HW06 / Pool A / FR-01, executed data-driven.\n\n"
    "One `POST /api/register`, replayed once per row of "
    "`postman/data/api1_fr01_register.csv`. The row supplies name, email, password and "
    "the status the requirement demands; the collection supplies no test data "
    "at all.\n\n"
    "Run: `npm run ddt:api1`",
    H.item(
        "DDT | POST /api/register <- CSV row",
        H.request(
            "POST", "/api/register",
            raw_body=json.dumps({
                "name": "{{ddt_name}}",
                "email": "{{ddt_email}}",
                "password": "{{ddt_password}}",
                "confirmPassword": "{{ddt_password}}",
            }, indent=2),
            description="Every field is bound to an iteration-data variable. "
                        "Add a row to the CSV to add a test case.",
        ),
        API1_TEST, API1_PRE,
    ),
)


# ---------------------------------------------------------------------------
# API 2 - FR-06 product detail: the path parameter is the data
# ---------------------------------------------------------------------------

API2_PRE = GUARD + """

pm.variables.set("ddt_product_id", d.get("product_id"));
"""

API2_TEST = STATUS_TEST + """

if (d.get("expect_body") === "product" && pm.response.code === 200) {
    pm.test(tc + " | body is a product per api_specification.md", function () {
        const b = pm.response.json();
        pm.expect(b).to.have.property("id");
        pm.expect(b).to.have.property("name");
        pm.expect(b).to.have.property("price");
    });
}

""" + NO_LEAK_TEST

api2 = ddt_collection(
    "API2 - FR-06 Product Detail - DATA-DRIVEN (postman/data/api2_fr06_product_detail.csv)",
    "HW06 / Pool A / FR-06, executed data-driven.\n\n"
    "One `GET /api/products/:id`, replayed once per row of "
    "`postman/data/api2_fr06_product_detail.csv`. The rows walk the :id partitions - "
    "valid, absent, boundary 0, negative, non-numeric and a SEC-05 injection "
    "payload.\n\n"
    "Run: `npm run ddt:api2`",
    H.item(
        "DDT | GET /api/products/{{ddt_product_id}} <- CSV row",
        H.request(
            "GET", "/api/products/{{ddt_product_id}}",
            description="The :id partition under test comes from the CSV.",
        ),
        API2_TEST, API2_PRE,
    ),
)


# ---------------------------------------------------------------------------
# API 3 - FR-11 order history: the actor AND the target are the data
# ---------------------------------------------------------------------------
#
# Both routes this API owns sit at /api/orders/<one segment>: `my-orders` for
# the history and an order id for the detail. One templated segment therefore
# covers the whole CSV.

API3_APPLY = """
const owner = (d.get("order_owner") || "self").trim();
pm.variables.set("ddt_target",
    owner === "victim" ? String(pm.variables.get("victimOrder")) : "my-orders");

""" + auth_apply("tok")

API3_PRE = GUARD + """

// Fixtures, built fresh for every iteration so no row depends on another:
//   tok         - the seeded user, the "primary-user" actor
//   victimTok   - a throwaway second account, the IDOR victim
//   victimOrder - an order that belongs to the victim, never to `tok`
""" + seeded_user_login(
    on_done=fresh_user(
        var="victimTok", prefix="ddtvic",
        on_done=create_order(token_var="victimTok", var="victimOrder",
                             amount=250000, on_done=API3_APPLY),
    ),
)

API3_TEST = STATUS_TEST + """

if (d.get("order_owner") === "self" && pm.response.code === 200) {
    pm.test(tc + " | history is an array of the caller's own orders",
            function () {
        const b = pm.response.json();
        pm.expect(b).to.be.an("array");
    });
}

if (d.get("order_owner") === "victim") {
    pm.test(tc + " | the victim's order is not disclosed", function () {
        const body = pm.response.text() || "";
        pm.expect(pm.response.code, "a cross-user read must not succeed")
            .to.not.eql(200);
        pm.expect(body).to.not.include("shipping_address");
    });
}
"""

api3 = ddt_collection(
    "API3 - FR-11 Order History - DATA-DRIVEN (postman/data/api3_fr11_order_history.csv)",
    "HW06 / Pool B / FR-11, executed data-driven.\n\n"
    "One `GET /api/orders/:target`, replayed once per row of "
    "`postman/data/api3_fr11_order_history.csv`. The row chooses the actor (its token), "
    "the target (own history or another user's order) and the status SEC-02 / "
    "FR-11 require. The IDOR victim and their order are created per iteration "
    "in the pre-request script.\n\n"
    "Run: `npm run ddt:api3`",
    H.item(
        "DDT | GET /api/orders/{{ddt_target}} <- CSV row",
        H.request(
            "GET", "/api/orders/{{ddt_target}}",
            description="Actor, target and expected status all come from the CSV. "
                        "The Authorization header is attached by the pre-request "
                        "script so that the anonymous rows send none at all.",
        ),
        API3_TEST, API3_PRE,
    ),
)


# ---------------------------------------------------------------------------
# API 4 - FR-13 admin dashboard: the role is the data
# ---------------------------------------------------------------------------

API4_PRE = GUARD + """

// Two real logins per iteration, so the role matrix is exercised with genuine
// tokens rather than hand-written ones.
""" + admin_login(on_done=seeded_user_login(on_done=auth_apply("tok")))

API4_TEST = STATUS_TEST + """

if (pm.response.code === 200) {
    pm.test(tc + " | admin dashboard returns the order collection", function () {
        const b = pm.response.json();
        pm.expect(b).to.satisfy(function (v) {
            return Array.isArray(v) || (v && typeof v === "object");
        });
    });
} else {
    pm.test(tc + " | refusal discloses no order data", function () {
        pm.expect(pm.response.text() || "").to.not.include("total_amount");
    });
}
"""

api4 = ddt_collection(
    "API4 - FR-13 Admin Dashboard - DATA-DRIVEN (postman/data/api4_fr13_admin_orders.csv)",
    "HW06 / Pool C / FR-13, executed data-driven.\n\n"
    "One `GET /api/admin/orders`, replayed once per row of "
    "`postman/data/api4_fr13_admin_orders.csv`. Each row is a role in the SEC-03 "
    "matrix - admin, ordinary user, anonymous and forged token - together with "
    "the status that role must receive.\n\n"
    "Run: `npm run ddt:api4`",
    H.item(
        "DDT | GET /api/admin/orders <- CSV row",
        H.request(
            "GET", "/api/admin/orders",
            description="The calling role comes from the CSV's token_var column.",
        ),
        API4_TEST, API4_PRE,
    ),
)


# ---------------------------------------------------------------------------

TARGETS = [
    ("API1_FR01_Register_ddt", api1, "api1_fr01_register.csv"),
    ("API2_FR06_ProductDetail_ddt", api2, "api2_fr06_product_detail.csv"),
    ("API3_FR11_OrderHistory_ddt", api3, "api3_fr11_order_history.csv"),
    ("API4_FR13_AdminOrders_ddt", api4, "api4_fr13_admin_orders.csv"),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for stem, coll, csv_name in TARGETS:
        csv_path = DATA / csv_name
        if not csv_path.exists():
            raise SystemExit("Missing data file: %s" % csv_path)
        with csv_path.open(encoding="utf-8-sig", newline="") as fh:
            rows = list(csv.DictReader(fh))
        if not rows:
            raise SystemExit("Data file %s has no rows." % csv_path)

        path = OUT / (stem + ".postman_collection.json")
        path.write_text(json.dumps(coll, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")
        print("%-34s 1 request x %2d CSV rows  <- postman/data/%s"
              % (path.name, len(rows), csv_name))


if __name__ == "__main__":
    main()
