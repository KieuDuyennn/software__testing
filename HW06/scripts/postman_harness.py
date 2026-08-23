#!/usr/bin/env python3
"""Shared Postman collection-building primitives for HW06.

Imported by build-collections.py (skeletons for APIs 2-4) and by
render-cases.py (renders a case specification into a full collection). Keeping
the harness in one place means every collection injects X-Student-Id the same
way and asserts the same global invariants.
"""

from __future__ import annotations

import json
import uuid

# Stable namespace so regenerating a collection keeps its _postman_id instead of
# churning a new UUID into the diff on every run.
NAMESPACE = uuid.UUID("6f1d1f9a-0f4f-5b6e-9c2a-1f0b7c9d3e41")

# ---------------------------------------------------------------------------
# Collection-level scripts
# ---------------------------------------------------------------------------

PRE_REQUEST = r"""
// ---------------------------------------------------------------------------
// HW06 mandatory harness: every request must carry X-Student-Id.
// The console line below is the anti-AI-cheat evidence (Section 11 of the
// brief) - screenshot the Postman console showing it.
// ---------------------------------------------------------------------------
const studentId = pm.environment.get("student_id") || "23127184";

pm.request.headers.upsert({ key: "X-Student-Id", value: studentId });

// A fresh token per request, so cases that must create a new account can do so
// without colliding with earlier runs. Use {{uniq}} inside request bodies.
const uniq = Date.now().toString(36) + Math.floor(Math.random() * 1e8).toString(36);
pm.variables.set("uniq", uniq);
pm.variables.set("uniqUpper", uniq.toUpperCase());

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


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------

def script(exec_src, listen):
    return {
        "listen": listen,
        "script": {"type": "text/javascript", "exec": exec_src.split("\n")},
    }


def request(method, path, body=None, auth_var=None, extra_headers=None,
            raw_query=None, content_type="application/json", raw_body=None,
            description=""):
    """Build a Postman request node.

    body       dict/list -> serialised as JSON
    raw_body   str       -> sent verbatim (for malformed-JSON cases)
    """
    url_raw = "{{base_url}}" + path + (raw_query or "")
    segments = [s for s in path.strip("/").split("/") if s]
    url = {"raw": url_raw, "host": ["{{base_url}}"], "path": segments}
    if raw_query:
        url["query"] = [
            {"key": kv.split("=")[0], "value": kv.split("=", 1)[1]}
            for kv in raw_query.lstrip("?").split("&") if "=" in kv
        ]

    headers = list(extra_headers or [])
    has_payload = body is not None or raw_body is not None
    if has_payload and content_type:
        headers.append({"key": "Content-Type", "value": content_type})
    if auth_var:
        headers.append({"key": "Authorization", "value": "Bearer {{%s}}" % auth_var})

    req = {"method": method, "header": headers, "url": url}
    if description:
        req["description"] = description
    if has_payload:
        if raw_body is not None:
            raw = raw_body
        else:
            raw = json.dumps(body, indent=2, ensure_ascii=False)
        language = "json" if content_type == "application/json" else "text"
        req["body"] = {"mode": "raw", "raw": raw,
                       "options": {"raw": {"language": language}}}
    return req


def item(name, req, test_src, pre_src=None):
    events = []
    if pre_src:
        events.append(script(pre_src.strip(), "prerequest"))
    events.append(script(test_src.strip(), "test"))
    return {"name": name, "event": events, "request": req, "response": []}


def folder(name, items, description=""):
    return {"name": name, "item": items, "description": description}


def collection(name, description, items):
    return {
        "info": {
            "_postman_id": str(uuid.uuid5(NAMESPACE, name)),
            "name": name,
            "description": description,
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "item": items,
        "event": [script(PRE_REQUEST, "prerequest"), script(GLOBAL_TEST, "test")],
        "variable": [],
    }


def login_item(name, email_var, pwd_var, token_var):
    """Reusable setup step: log in and stash the JWT in an environment variable."""
    return item(
        name,
        request("POST", "/api/login", {"email": "{{%s}}" % email_var,
                                       "password": "{{%s}}" % pwd_var},
                description="Setup step: obtains a JWT used by later requests."),
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
    )
