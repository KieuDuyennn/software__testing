#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test-case specification for API 1 - FR-01 Account Registration.

Endpoint: POST /api/register     Pool A     Requirement FR-01

This module is the single source of truth for API 1's test cases. Rendering it
(scripts/render-cases.py --api 1) produces the Postman collection, the Excel
sheet and the machine-readable case export - so a correction made here shows up
everywhere at once.

ORACLE DISCIPLINE
-----------------
Every expected result below is derived from the specification and from FR-01 /
SEC-01..SEC-07, never from what the SUT currently returns. Cases that the
running system fails are therefore not broken cases - they are the ones doing
their job. Where the specification is genuinely silent, the case carries a
`gap` note instead of an invented expectation.

FR-01 as written in the requirement document:
  - the user must supply Họ Tên (name), Email and Mật khẩu (password);
  - email must be well formed (`user@domain.com`) and unique in the system;
  - password: >= 8 characters with at least one uppercase letter, one lowercase
    letter, one digit and one special character from @ $ ! % * ? &;
  - a confirm-password field must be present, and registration is refused when
    the two do not match.
"""

from __future__ import annotations

OMIT = object()          # distinct from None, which means an explicit JSON null

CASES = []


def add(**kw):
    CASES.append(kw)
    return kw


def rb(name="Nguyen Van A", email="{{uniq}}@domain.com",
       password="Password123!", confirmPassword=None, **extra):
    """Build a request body, omitting any field passed as OMIT."""
    d = {}
    if name is not OMIT:
        d["name"] = name
    if email is not OMIT:
        d["email"] = email
    if password is not OMIT:
        d["password"] = password
    if confirmPassword is not OMIT:
        if confirmPassword is None:
            d["confirmPassword"] = "Password123!" if password is OMIT else password
        else:
            d["confirmPassword"] = confirmPassword
    d.update(extra)
    return d


# ---------------------------------------------------------------------------
# Assertion helpers - each returns a JavaScript fragment for the test script.
# ---------------------------------------------------------------------------

def st(*codes):
    if len(codes) == 1:
        return ('pm.test("Status is %d", function () {\n'
                '    pm.response.to.have.status(%d);\n});' % (codes[0], codes[0]))
    lst = ", ".join(str(c) for c in codes)
    return ('pm.test("Status is one of [%s]", function () {\n'
            '    pm.expect(pm.response.code).to.be.oneOf([%s]);\n});' % (lst, lst))


def rejected(reason):
    """FR-01 says this input is invalid: the API must refuse it with a 4xx."""
    return (
        'pm.test("Rejected with a 4xx (%s)", function () {\n'
        '    pm.expect(pm.response.code, "status code").to.be.within(400, 499);\n'
        '});\n'
        'pm.test("Error response names the problem", function () {\n'
        '    pm.expect(pm.response.text()).to.not.be.empty;\n'
        '});' % reason
    )


def accepted():
    """A valid registration: 200 plus the success body the spec documents."""
    return (
        'pm.test("Status is 200", function () {\n'
        '    pm.response.to.have.status(200);\n'
        '});\n'
        'pm.test("Body matches the documented success shape", function () {\n'
        '    const b = pm.response.json();\n'
        '    pm.expect(b).to.have.property("message", "User registered successfully");\n'
        '    pm.expect(b.id, "id").to.be.a("number");\n'
        '});'
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
        '    ["sqlite", "sql error", "syntax error", "at object.", "stack"]\n'
        '        .forEach(function (needle) {\n'
        '            pm.expect(t, "response must not contain \\"" + needle + "\\"")\n'
        '                .to.not.include(needle);\n'
        '        });\n'
        '});'
    )


def js(raw):
    return raw.strip()


# ===========================================================================
# STEP 2 - DOMAIN PARTITIONS
# ===========================================================================
# One case per equivalence class and per boundary, for every parameter the
# endpoint accepts - plus the request envelope itself (body shape, content
# type, HTTP method), which is also part of the endpoint's input domain.

# --- name ------------------------------------------------------------------

add(id="A1-DP-001", dim="Domain", param="name", rule="FR-01",
    partition="valid: ordinary full name",
    title="Registration succeeds with a valid name",
    body=rb(), expected="200 with {message, id}", tests=accepted())

add(id="A1-DP-002", dim="Domain", param="name", rule="FR-01",
    partition="invalid: key absent",
    title="Missing name field is rejected",
    body=rb(name=OMIT), expected="4xx - FR-01 makes name mandatory",
    tests=rejected("name is mandatory"))

add(id="A1-DP-003", dim="Domain", param="name", rule="FR-01",
    partition="invalid: explicit null",
    title="Null name is rejected",
    body=rb(name=None), expected="4xx", tests=rejected("name must not be null"))

add(id="A1-DP-004", dim="Domain", param="name", rule="FR-01",
    partition="invalid: empty string",
    title="Empty name is rejected",
    body=rb(name=""), expected="4xx", tests=rejected("name must not be empty"))

add(id="A1-DP-005", dim="Domain", param="name", rule="FR-01",
    partition="invalid: whitespace only",
    title="Whitespace-only name is rejected",
    body=rb(name="     "), expected="4xx - whitespace is not a name",
    tests=rejected("name must not be blank"))

add(id="A1-DP-006", dim="Domain", param="name", rule="FR-01",
    partition="boundary: single character",
    title="Single-character name is accepted",
    body=rb(name="A"), expected="200 - FR-01 sets no minimum length",
    tests=accepted(),
    gap="FR-01 does not state a minimum name length; treated as valid.")

add(id="A1-DP-007", dim="Domain", param="name", rule="FR-01",
    partition="valid: Vietnamese diacritics",
    title="Name with Vietnamese diacritics is accepted and preserved",
    body=rb(name="Lê Phạm Kiều Duyên"), expected="200, name stored unchanged",
    tests=accepted())

add(id="A1-DP-008", dim="Domain", param="name", rule="FR-01",
    partition="boundary: 255 characters",
    title="255-character name is handled without error",
    body=rb(name="N" * 255), expected="200 or a 4xx limit error, never a 5xx",
    tests=no500(),
    gap="FR-01 states no maximum length; the only firm expectation is no 5xx.")

add(id="A1-DP-009", dim="Domain", param="name", rule="FR-01",
    partition="boundary: 5000 characters",
    title="Oversized name does not crash the server",
    body=rb(name="N" * 5000), expected="4xx limit error or 200, never a 5xx",
    tests=no500() + "\n" + no_leak(),
    gap="No documented maximum; asserted only that the server stays healthy.")

add(id="A1-DP-010", dim="Domain", param="name", rule="FR-01",
    partition="invalid: wrong JSON type (number)",
    title="Numeric name is rejected",
    body=rb(name=12345), expected="4xx - name is specified as a string",
    tests=rejected("name must be a string"))

add(id="A1-DP-011", dim="Domain", param="name", rule="FR-01",
    partition="invalid: wrong JSON type (object)",
    title="Object as name is rejected",
    body=rb(name={"first": "Nguyen"}),
    expected="4xx", tests=rejected("name must be a string"))

add(id="A1-DP-012", dim="Domain", param="name", rule="FR-01",
    partition="edge: surrounding whitespace",
    title="Name with leading and trailing spaces is trimmed or rejected",
    body=rb(name="   Nguyen Van A   "),
    expected="200 with the value trimmed, or a 4xx; never stored padded",
    tests=no500(),
    gap="Spec is silent on trimming; recorded as a gap rather than guessed.")

add(id="A1-DP-013", dim="Domain", param="name", rule="FR-01",
    partition="edge: emoji / astral-plane characters",
    title="Name containing emoji is handled without corruption",
    body=rb(name="Duyên 🌸 QA"), expected="200 or 4xx, never a 5xx",
    tests=no500())


# --- email -----------------------------------------------------------------

add(id="A1-DP-014", dim="Domain", param="email", rule="FR-01",
    partition="valid: user@domain.com",
    title="Registration succeeds with a well-formed email",
    body=rb(email="{{uniq}}@domain.com"), expected="200", tests=accepted())

add(id="A1-DP-015", dim="Domain", param="email", rule="FR-01",
    partition="invalid: key absent",
    title="Missing email field is rejected",
    body=rb(email=OMIT), expected="4xx - FR-01 makes email mandatory",
    tests=rejected("email is mandatory"))

add(id="A1-DP-016", dim="Domain", param="email", rule="FR-01",
    partition="invalid: explicit null",
    title="Null email is rejected",
    body=rb(email=None), expected="4xx", tests=rejected("email must not be null"))

add(id="A1-DP-017", dim="Domain", param="email", rule="FR-01",
    partition="invalid: empty string",
    title="Empty email is rejected",
    body=rb(email=""), expected="4xx", tests=rejected("email must not be empty"))

add(id="A1-DP-018", dim="Domain", param="email", rule="FR-01",
    partition="invalid: whitespace only",
    title="Whitespace-only email is rejected",
    body=rb(email="    "), expected="4xx", tests=rejected("email must not be blank"))

add(id="A1-DP-019", dim="Domain", param="email", rule="FR-01",
    partition="invalid: no @ separator",
    title="Email without '@' is rejected",
    body=rb(email="{{uniq}}domain.com"),
    expected="4xx - FR-01 requires the user@domain.com form",
    tests=rejected("email needs an @"))

add(id="A1-DP-020", dim="Domain", param="email", rule="FR-01",
    partition="invalid: missing domain part",
    title="Email with nothing after '@' is rejected",
    body=rb(email="{{uniq}}@"), expected="4xx",
    tests=rejected("email needs a domain"))

add(id="A1-DP-021", dim="Domain", param="email", rule="FR-01",
    partition="invalid: missing local part",
    title="Email with nothing before '@' is rejected",
    body=rb(email="@domain.com"), expected="4xx",
    tests=rejected("email needs a local part"))

add(id="A1-DP-022", dim="Domain", param="email", rule="FR-01",
    partition="invalid: no top-level domain",
    title="Email without a TLD is rejected",
    body=rb(email="{{uniq}}@domain"), expected="4xx - user@domain.com form required",
    tests=rejected("email needs a TLD"))

add(id="A1-DP-023", dim="Domain", param="email", rule="FR-01",
    partition="invalid: two @ separators",
    title="Email with a duplicated '@' is rejected",
    body=rb(email="{{uniq}}@@domain.com"), expected="4xx",
    tests=rejected("email has two @ signs"))

add(id="A1-DP-024", dim="Domain", param="email", rule="FR-01",
    partition="invalid: leading dot in local part",
    title="Email starting with a dot is rejected",
    body=rb(email=".{{uniq}}@domain.com"), expected="4xx",
    tests=rejected("local part must not start with a dot"))

add(id="A1-DP-025", dim="Domain", param="email", rule="FR-01",
    partition="invalid: trailing dot in local part",
    title="Email with a dot immediately before '@' is rejected",
    body=rb(email="{{uniq}}.@domain.com"), expected="4xx",
    tests=rejected("local part must not end with a dot"))

add(id="A1-DP-026", dim="Domain", param="email", rule="FR-01",
    partition="invalid: consecutive dots",
    title="Email with consecutive dots is rejected",
    body=rb(email="us..er{{uniq}}@domain.com"), expected="4xx",
    tests=rejected("consecutive dots are not allowed"))

add(id="A1-DP-027", dim="Domain", param="email", rule="FR-01",
    partition="invalid: embedded space",
    title="Email containing a space is rejected",
    body=rb(email="us er{{uniq}}@domain.com"), expected="4xx",
    tests=rejected("email must not contain spaces"))

add(id="A1-DP-028", dim="Domain", param="email", rule="FR-01",
    partition="invalid: illegal characters in local part",
    title="Email with parentheses in the local part is rejected",
    body=rb(email="us()er{{uniq}}@domain.com"), expected="4xx",
    tests=rejected("illegal characters in local part"))

add(id="A1-DP-029", dim="Domain", param="email", rule="FR-01",
    partition="valid: plus-addressing",
    title="Email with a '+' tag is accepted",
    body=rb(email="{{uniq}}+qa@domain.com"), expected="200 - valid per RFC 5322",
    tests=accepted())

add(id="A1-DP-030", dim="Domain", param="email", rule="FR-01",
    partition="valid: subdomain",
    title="Email on a subdomain is accepted",
    body=rb(email="{{uniq}}@mail.domain.com"), expected="200", tests=accepted())

add(id="A1-DP-031", dim="Domain", param="email", rule="FR-01",
    partition="valid: hyphenated domain",
    title="Email on a hyphenated domain is accepted",
    body=rb(email="{{uniq}}@my-shop.com.vn"), expected="200", tests=accepted())

add(id="A1-DP-032", dim="Domain", param="email", rule="FR-01",
    partition="valid: uppercase characters",
    title="Email in uppercase is accepted",
    body=rb(email="{{uniqUpper}}@DOMAIN.COM"),
    expected="200 - the local part is case-preserving, the domain case-insensitive",
    tests=accepted())

add(id="A1-DP-033", dim="Domain", param="email", rule="FR-01",
    partition="invalid: already registered (uniqueness)",
    title="Registering an email that already exists is rejected",
    body=rb(email="dup{{uniq}}@domain.com"),
    expected='4xx - FR-01: email must be "duy nhất trong hệ thống"',
    pre=js("""
// Fixture: claim the address first, so the request under test is a duplicate.
const email = "dup" + pm.variables.get("uniq") + "@domain.com";
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/register",
    method: "POST",
    header: { "Content-Type": "application/json",
              "X-Student-Id": pm.environment.get("student_id") },
    body: { mode: "raw", raw: JSON.stringify({
        name: "First Owner", email: email, password: "Password123!",
        confirmPassword: "Password123!" }) }
}, function (err, res) {
    console.log("[HW06] A1-DP-033 fixture claimed " + email +
                " -> " + (res ? res.code : err));
});
"""),
    tests=rejected("email must be unique"))

add(id="A1-DP-034", dim="Domain", param="email", rule="FR-01",
    partition="invalid: already registered, different case",
    title="Uniqueness is enforced case-insensitively",
    body=rb(email="DUP{{uniq}}@DOMAIN.COM"),
    expected="4xx - email addresses differing only in case are the same account",
    pre=js("""
const email = "dup" + pm.variables.get("uniq") + "@domain.com";
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/register",
    method: "POST",
    header: { "Content-Type": "application/json",
              "X-Student-Id": pm.environment.get("student_id") },
    body: { mode: "raw", raw: JSON.stringify({
        name: "First Owner", email: email, password: "Password123!",
        confirmPassword: "Password123!" }) }
}, function () { console.log("[HW06] A1-DP-034 fixture claimed " + email); });
"""),
    tests=rejected("uniqueness must ignore case"))

add(id="A1-DP-035", dim="Domain", param="email", rule="FR-01",
    partition="boundary: local part longer than 64 characters",
    title="Over-long email local part is rejected",
    body=rb(email="a" * 65 + "@domain.com"),
    expected="4xx - RFC 5321 caps the local part at 64 characters",
    tests=rejected("local part exceeds 64 characters"))

add(id="A1-DP-036", dim="Domain", param="email", rule="FR-01",
    partition="invalid: wrong JSON type (number)",
    title="Numeric email is rejected",
    body=rb(email=12345), expected="4xx", tests=rejected("email must be a string"))

add(id="A1-DP-037", dim="Domain", param="email", rule="FR-01",
    partition="edge: trailing whitespace",
    title="Email with a trailing space is trimmed or rejected",
    body=rb(email="{{uniq}}@domain.com "),
    expected="200 with the value trimmed, or 4xx; never stored with the space",
    tests=no500(),
    gap="Spec does not say whether inputs are trimmed.")


# --- password --------------------------------------------------------------

add(id="A1-DP-038", dim="Domain", param="password", rule="FR-01",
    partition="valid: satisfies every complexity rule",
    title="Registration succeeds with a compliant password",
    body=rb(password="Password123!"), expected="200", tests=accepted())

add(id="A1-DP-039", dim="Domain", param="password", rule="FR-01",
    partition="invalid: key absent",
    title="Missing password field is rejected",
    body=rb(password=OMIT), expected="4xx", tests=rejected("password is mandatory"))

add(id="A1-DP-040", dim="Domain", param="password", rule="FR-01",
    partition="invalid: explicit null",
    title="Null password is rejected",
    body=rb(password=None), expected="4xx", tests=rejected("password must not be null"))

add(id="A1-DP-041", dim="Domain", param="password", rule="FR-01",
    partition="invalid: empty string",
    title="Empty password is rejected",
    body=rb(password=""), expected="4xx", tests=rejected("password must not be empty"))

add(id="A1-DP-042", dim="Domain", param="password", rule="FR-01",
    partition="boundary: 7 characters (minimum minus one)",
    title="Seven-character password is rejected",
    body=rb(password="Pass12!"),
    expected="4xx - FR-01 requires at least 8 characters",
    tests=rejected("shorter than the 8-character minimum"))

add(id="A1-DP-043", dim="Domain", param="password", rule="FR-01",
    partition="boundary: exactly 8 characters (the minimum)",
    title="Eight-character compliant password is accepted",
    body=rb(password="Pass123!"), expected="200 - exactly at the minimum",
    tests=accepted())

add(id="A1-DP-044", dim="Domain", param="password", rule="FR-01",
    partition="boundary: 9 characters (minimum plus one)",
    title="Nine-character compliant password is accepted",
    body=rb(password="Pass1234!"), expected="200", tests=accepted())

add(id="A1-DP-045", dim="Domain", param="password", rule="FR-01",
    partition="invalid: no uppercase letter",
    title="Password without an uppercase letter is rejected",
    body=rb(password="password123!"), expected="4xx",
    tests=rejected("no uppercase letter"))

add(id="A1-DP-046", dim="Domain", param="password", rule="FR-01",
    partition="invalid: no lowercase letter",
    title="Password without a lowercase letter is rejected",
    body=rb(password="PASSWORD123!"), expected="4xx",
    tests=rejected("no lowercase letter"))

add(id="A1-DP-047", dim="Domain", param="password", rule="FR-01",
    partition="invalid: no digit",
    title="Password without a digit is rejected",
    body=rb(password="Password!!"), expected="4xx", tests=rejected("no digit"))

add(id="A1-DP-048", dim="Domain", param="password", rule="FR-01",
    partition="invalid: no special character",
    title="Password without a special character is rejected",
    body=rb(password="Password123"), expected="4xx",
    tests=rejected("no special character"))

add(id="A1-DP-049", dim="Domain", param="password", rule="FR-01",
    partition="invalid: special character outside the permitted set",
    title="Password whose only special character is '#' is rejected",
    body=rb(password="Password123#"),
    expected="4xx - FR-01 permits only @ $ ! % * ? &",
    tests=rejected("'#' is not in the permitted special-character set"))

# One case per permitted special character - FR-01 enumerates them, so each is
# its own equivalence class.
for _i, (_ch, _label) in enumerate([
    ("@", "at sign"), ("$", "dollar sign"), ("!", "exclamation mark"),
    ("%", "percent sign"), ("*", "asterisk"), ("?", "question mark"),
    ("&", "ampersand"),
]):
    add(id="A1-DP-%03d" % (50 + _i), dim="Domain", param="password", rule="FR-01",
        partition="valid: permitted special character '%s'" % _ch,
        title="Password using '%s' (%s) is accepted" % (_ch, _label),
        body=rb(password="Passw0rd%s" % _ch),
        expected="200 - '%s' is in the FR-01 permitted set" % _ch,
        tests=accepted())

add(id="A1-DP-057", dim="Domain", param="password", rule="FR-01",
    partition="invalid: digits only",
    title="All-numeric password is rejected",
    body=rb(password="12345678"), expected="4xx - no letters, no special character",
    tests=rejected("digits only"))

add(id="A1-DP-058", dim="Domain", param="password", rule="FR-01",
    partition="invalid: letters only",
    title="All-alphabetic password is rejected",
    body=rb(password="Passwordd"), expected="4xx - no digit, no special character",
    tests=rejected("letters only"))

add(id="A1-DP-059", dim="Domain", param="password", rule="FR-01",
    partition="invalid: whitespace only",
    title="Whitespace-only password is rejected",
    body=rb(password="        "), expected="4xx",
    tests=rejected("whitespace is not a password"))

add(id="A1-DP-060", dim="Domain", param="password", rule="FR-01",
    partition="valid: common weak password shape",
    title="A weak but non-compliant password like 'password' is rejected",
    body=rb(password="password"), expected="4xx - fails three complexity rules",
    tests=rejected("weak password"))

add(id="A1-DP-061", dim="Domain", param="password", rule="FR-01",
    partition="edge: embedded space",
    title="Password containing a space is handled consistently",
    body=rb(password="Pass 123!"),
    expected="200 - FR-01 does not forbid spaces; must not 5xx",
    tests=no500(),
    gap="FR-01 neither permits nor forbids whitespace inside a password.")

add(id="A1-DP-062", dim="Domain", param="password", rule="FR-01",
    partition="boundary: 1000 characters",
    title="Very long password does not crash the server",
    body=rb(password="Aa1!" + "x" * 996), expected="200 or 4xx, never a 5xx",
    tests=no500(),
    gap="No documented maximum length.")

add(id="A1-DP-063", dim="Domain", param="password", rule="FR-01",
    partition="invalid: wrong JSON type (number)",
    title="Numeric password is rejected",
    body=rb(password=12345678), expected="4xx",
    tests=rejected("password must be a string"))

add(id="A1-DP-064", dim="Domain", param="password", rule="FR-01",
    partition="valid: unicode characters",
    title="Password containing non-ASCII characters is handled without corruption",
    body=rb(password="Mật khẩu1!"), expected="200 or 4xx, never a 5xx",
    tests=no500())


# --- confirm password ------------------------------------------------------
# FR-01 mandates a confirm-password field. api_specification.md documents only
# {name, email, password}. That contradiction is itself a finding, so the cases
# below test the requirement and record the gap.

add(id="A1-DP-065", dim="Domain", param="confirmPassword", rule="FR-01",
    partition="valid: confirmation matches",
    title="Registration succeeds when the password confirmation matches",
    body=rb(confirmPassword="Password123!"), expected="200",
    tests=accepted(),
    gap="Field required by FR-01 but absent from api_specification.md.")

add(id="A1-DP-066", dim="Domain", param="confirmPassword", rule="FR-01",
    partition="invalid: confirmation differs",
    title="Mismatched password confirmation is rejected",
    body=rb(password="Password123!", confirmPassword="Password456!"),
    expected='4xx - FR-01: "hệ thống từ chối nếu hai trường không khớp"',
    tests=rejected("password confirmation does not match"))

add(id="A1-DP-067", dim="Domain", param="confirmPassword", rule="FR-01",
    partition="invalid: confirmation absent",
    title="Missing password confirmation is rejected",
    body=rb(confirmPassword=OMIT),
    expected="4xx - FR-01 makes the confirmation field mandatory",
    tests=rejected("confirmation field is mandatory"),
    gap="Tests FR-01 against a spec that omits the field - expect disagreement.")


# --- request envelope ------------------------------------------------------

add(id="A1-DP-068", dim="Domain", param="body", rule="FR-01",
    partition="invalid: empty JSON object",
    title="Empty request body is rejected",
    body={}, expected="4xx - all three fields are mandatory",
    tests=rejected("no fields supplied"))

add(id="A1-DP-069", dim="Domain", param="body", rule="FR-01",
    partition="invalid: no body at all",
    title="Request with no body is rejected",
    raw_body="", expected="4xx", tests=rejected("no body supplied"))

add(id="A1-DP-070", dim="Domain", param="body", rule="spec conformance",
    partition="invalid: malformed JSON",
    title="Malformed JSON is rejected with a 400, not a 500",
    raw_body='{"name": "Broken", "email": "{{uniq}}@domain.com", ',
    expected="400 - a parse failure is a client error",
    tests=st(400) + "\n" + no_leak())

add(id="A1-DP-071", dim="Domain", param="body", rule="spec conformance",
    partition="invalid: wrong Content-Type",
    title="Non-JSON Content-Type is rejected",
    raw_body='name=Test&email=a@b.com&password=Password123!',
    content_type="text/plain",
    expected="400 or 415 - the endpoint is documented as JSON",
    tests=st(400, 415) + "\n" + no500())

add(id="A1-DP-072", dim="Domain", param="body", rule="spec conformance",
    partition="invalid: JSON array instead of object",
    title="Array request body is rejected",
    body=[{"name": "A", "email": "a@b.com", "password": "Password123!"}],
    expected="4xx", tests=rejected("body must be an object"))

add(id="A1-DP-073", dim="Domain", param="body", rule="spec conformance",
    partition="valid: unknown extra fields",
    title="Unknown extra fields are ignored, not stored",
    body=rb(nickname="duyen", favouriteColour="pink"),
    expected="200 - undocumented fields are ignored",
    tests=accepted())

add(id="A1-DP-074", dim="Domain", param="body", rule="FR-01",
    partition="invalid: every field null",
    title="All-null request body is rejected",
    body=rb(name=None, email=None, password=None), expected="4xx",
    tests=rejected("no usable field supplied"))

add(id="A1-DP-075", dim="Domain", param="body", rule="spec conformance",
    partition="boundary: very large payload (~100 KB)",
    title="Oversized payload is refused without a server error",
    body=rb(name="N" * 100000),
    expected="400 or 413, never a 5xx",
    tests=no500() + "\n" + no_leak(),
    gap="No documented payload limit.")


# --- HTTP method -----------------------------------------------------------

for _i, _method in enumerate(["GET", "PUT", "DELETE", "PATCH"]):
    add(id="A1-DP-%03d" % (76 + _i), dim="Domain", param="http method",
        rule="spec conformance",
        partition="invalid: %s on a POST-only route" % _method,
        title="%s /api/register is not routed" % _method,
        method=_method, body=None,
        expected="404 or 405 - the spec documents POST only",
        tests=st(404, 405))


# ===========================================================================
# STEP 3 - STATE TRANSITIONS
# ===========================================================================
# Account lifecycle reachable from registration:
#   (no account) -> registered -> authenticated
# Each case sets up its own starting state so it is independent of run order.

_REGISTER_FIXTURE = """
// Fixture: create a fresh account and remember its credentials.
const email = "st" + pm.variables.get("uniq") + "@domain.com";
const password = "Password123!";
pm.variables.set("stEmail", email);
pm.variables.set("stPassword", password);
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/register",
    method: "POST",
    header: { "Content-Type": "application/json",
              "X-Student-Id": pm.environment.get("student_id") },
    body: { mode: "raw", raw: JSON.stringify({
        name: "State Fixture", email: email, password: password,
        confirmPassword: password }) }
}, function (err, res) {
    if (res && res.json()) { pm.variables.set("stUserId", res.json().id); }
    console.log("[HW06] state fixture registered " + email);
});
"""

_REGISTER_AND_LOGIN = _REGISTER_FIXTURE + """
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/login",
    method: "POST",
    header: { "Content-Type": "application/json",
              "X-Student-Id": pm.environment.get("student_id") },
    body: { mode: "raw", raw: JSON.stringify({
        email: pm.variables.get("stEmail"),
        password: pm.variables.get("stPassword") }) }
}, function (err, res) {
    if (res && res.json() && res.json().token) {
        pm.variables.set("stToken", res.json().token);
    }
});
"""

add(id="A1-ST-001", dim="State", param="-", rule="FR-01 / FR-02",
    partition="transition: registered -> authenticated",
    title="A newly registered account can immediately log in",
    method="POST", path="/api/login",
    body={"email": "{{stEmail}}", "password": "{{stPassword}}"},
    pre=js(_REGISTER_FIXTURE),
    expected="200 with a JWT - registration leaves the account usable",
    tests=js("""
pm.test("Login succeeds for the new account", function () {
    pm.response.to.have.status(200);
    pm.expect(pm.response.json()).to.have.property("token");
});"""))

add(id="A1-ST-002", dim="State", param="-", rule="FR-01",
    partition="transition: registered -> duplicate attempt must not overwrite",
    title="A duplicate registration does not replace the existing account",
    method="POST", path="/api/login",
    body={"email": "{{stEmail}}", "password": "{{stPassword}}"},
    pre=js(_REGISTER_FIXTURE + """
// Attempt to re-register the same address with a DIFFERENT password.
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/register",
    method: "POST",
    header: { "Content-Type": "application/json",
              "X-Student-Id": pm.environment.get("student_id") },
    body: { mode: "raw", raw: JSON.stringify({
        name: "Impostor", email: pm.variables.get("stEmail"),
        password: "Hijacked999!", confirmPassword: "Hijacked999!" }) }
}, function () { console.log("[HW06] A1-ST-002 duplicate attempt sent"); });
"""),
    expected="200 - the original password still works; the duplicate changed nothing",
    tests=js("""
pm.test("The original credentials still authenticate", function () {
    pm.response.to.have.status(200);
    pm.expect(pm.response.json()).to.have.property("token");
});"""))

add(id="A1-ST-003", dim="State", param="-", rule="FR-01 / FR-04",
    partition="transition: registered -> profile readable",
    title="The registered account's profile is retrievable after login",
    method="GET", path="/api/users/me", auth_var="stToken",
    pre=js(_REGISTER_AND_LOGIN),
    expected="200 and the profile matches the registered email",
    tests=js("""
pm.test("Profile is returned", () => pm.response.to.have.status(200));
pm.test("Profile belongs to the account just registered", function () {
    const u = pm.response.json();
    pm.expect(String(u.email).toLowerCase())
      .to.eql(String(pm.variables.get("stEmail")).toLowerCase());
});"""))

add(id="A1-ST-004", dim="State", param="-", rule="FR-01 / SEC-03",
    partition="initial state: role",
    title="A newly registered account starts with role 'user'",
    method="GET", path="/api/users/me", auth_var="stToken",
    pre=js(_REGISTER_AND_LOGIN),
    expected="role is exactly 'user' - registration never grants admin",
    tests=js("""
pm.test("Initial role is 'user'", function () {
    pm.expect(pm.response.json().role).to.eql("user");
});"""))

add(id="A1-ST-005", dim="State", param="-", rule="FR-01 / FR-02",
    partition="initial state: lockout counters",
    title="A newly registered account is not locked and has zero failed attempts",
    method="GET", path="/api/users/me", auth_var="stToken",
    pre=js(_REGISTER_AND_LOGIN),
    expected="login_attempts = 0 and locked_until is null",
    tests=js("""
const u = pm.response.json();
pm.test("No failed attempts recorded", function () {
    pm.expect(Number(u.login_attempts || 0)).to.eql(0);
});
pm.test("Account is not locked", function () {
    pm.expect(u.locked_until == null, "locked_until must be null").to.be.true;
});"""))

add(id="A1-ST-006", dim="State", param="-", rule="FR-01 / FR-03",
    partition="transition: registered -> password reset available",
    title="Password reset can be initiated for a newly registered account",
    method="POST", path="/api/forgot-password", body={"email": "{{stEmail}}"},
    pre=js(_REGISTER_FIXTURE),
    expected="200 - the account exists, so a reset token is issued",
    tests=js("""
pm.test("Reset can be initiated", () => pm.response.to.have.status(200));
pm.test("A reset token is returned", function () {
    pm.expect(pm.response.json()).to.have.property("resetToken");
});"""))

add(id="A1-ST-007", dim="State", param="-", rule="FR-01",
    partition="transition: two registrations produce distinct identities",
    title="Consecutive registrations receive distinct, increasing ids",
    body=rb(email="second{{uniq}}@domain.com"),
    pre=js(_REGISTER_FIXTURE),
    expected="200 and an id strictly greater than the fixture account's id",
    tests=js("""
pm.test("Status is 200", () => pm.response.to.have.status(200));
pm.test("New id is distinct from and greater than the previous one", function () {
    const previous = Number(pm.variables.get("stUserId"));
    const current = Number(pm.response.json().id);
    pm.expect(current, "new id").to.be.greaterThan(previous);
});"""))

add(id="A1-ST-008", dim="State", param="-", rule="FR-01",
    partition="transition: rejected registration creates no account",
    title="A registration rejected for an invalid email leaves no usable account",
    method="POST", path="/api/login",
    body={"email": "bad{{uniq}}", "password": "Password123!"},
    pre=js("""
// Attempt a registration FR-01 says must be refused (malformed email).
const email = "bad" + pm.variables.get("uniq");
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/register",
    method: "POST",
    header: { "Content-Type": "application/json",
              "X-Student-Id": pm.environment.get("student_id") },
    body: { mode: "raw", raw: JSON.stringify({
        name: "Should Not Exist", email: email, password: "Password123!",
        confirmPassword: "Password123!" }) }
}, function () { console.log("[HW06] A1-ST-008 invalid registration attempted"); });
"""),
    expected="401 - no account was created, so login must fail",
    tests=js("""
pm.test("No account exists for the rejected registration", function () {
    pm.expect(pm.response.code).to.be.oneOf([400, 401, 404]);
});"""))

add(id="A1-ST-009", dim="State", param="-", rule="FR-01 / FR-07",
    partition="initial state: no residual shopping state",
    title="A newly registered account starts with an empty cart",
    method="GET", path="/api/cart", auth_var="stToken",
    pre=js(_REGISTER_AND_LOGIN),
    expected="200 with an empty array",
    tests=js("""
pm.test("Cart is returned", () => pm.response.to.have.status(200));
pm.test("Cart is empty for a brand-new account", function () {
    pm.expect(pm.response.json()).to.be.an("array").that.is.empty;
});"""))

add(id="A1-ST-010", dim="State", param="-", rule="FR-01 / FR-11",
    partition="initial state: no order history",
    title="A newly registered account has no orders",
    method="GET", path="/api/orders/my-orders", auth_var="stToken",
    pre=js(_REGISTER_AND_LOGIN),
    expected="200 with an empty array",
    tests=js("""
pm.test("Order history is returned", () => pm.response.to.have.status(200));
pm.test("Order history is empty for a brand-new account", function () {
    pm.expect(pm.response.json()).to.be.an("array").that.is.empty;
});"""))


# ===========================================================================
# STEP 4 - SECURITY (SEC-01 .. SEC-07)
# ===========================================================================

add(id="A1-SEC-001", dim="Security", param="password", rule="SEC-01",
    partition="credential disclosure via login response",
    title="The login response must not disclose the stored password",
    method="POST", path="/api/login",
    body={"email": "{{stEmail}}", "password": "{{stPassword}}"},
    pre=js(_REGISTER_FIXTURE),
    expected="no password field, and certainly not the plaintext just submitted",
    tests=js("""
const u = pm.response.json().user || {};
pm.test("Response carries no password field", function () {
    pm.expect(u, "user object").to.not.have.property("password");
});
pm.test("Submitted plaintext is not echoed back", function () {
    pm.expect(u.password).to.not.eql(pm.variables.get("stPassword"));
});"""))

add(id="A1-SEC-002", dim="Security", param="password", rule="SEC-01",
    partition="credential echo in the registration response",
    title="The registration response must not echo the password",
    body=rb(password="Password123!"),
    expected="the response body contains neither the password nor a password field",
    tests=js("""
pm.test("Password is absent from the response body", function () {
    pm.expect(pm.response.text()).to.not.include("Password123!");
});
pm.test("No password key in the response", function () {
    pm.expect(pm.response.text().toLowerCase()).to.not.include('"password"');
});"""))

add(id="A1-SEC-003", dim="Security", param="password", rule="SEC-01",
    partition="credential disclosure via the profile endpoint",
    title="The profile endpoint must not expose the password",
    method="GET", path="/api/users/me", auth_var="stToken",
    pre=js(_REGISTER_AND_LOGIN),
    expected="no password field in the profile payload",
    tests=js("""
pm.test("Profile carries no password field", function () {
    pm.expect(pm.response.json()).to.not.have.property("password");
});"""))

add(id="A1-SEC-004", dim="Security", param="password", rule="SEC-01",
    partition="storage form: password must be hashed",
    title="The stored password must not equal the submitted plaintext",
    method="POST", path="/api/login",
    body={"email": "{{stEmail}}", "password": "{{stPassword}}"},
    pre=js(_REGISTER_FIXTURE),
    expected="if any password material is returned it must look hashed, not plaintext",
    tests=js("""
const u = pm.response.json().user || {};
pm.test("Any returned password material is not the plaintext", function () {
    if (u.password === undefined) {
        pm.expect(true, "no password field - compliant").to.be.true;
    } else {
        pm.expect(u.password).to.not.eql(pm.variables.get("stPassword"));
        pm.expect(String(u.password).length,
                  "a hash is longer than the plaintext").to.be.above(40);
    }
});"""))

add(id="A1-SEC-005", dim="Security", param="name", rule="SEC-04",
    partition="stored XSS via the name field",
    title="A script payload in the name is stored as inert data",
    method="GET", path="/api/users/me", auth_var="stToken",
    pre=js("""
const email = "xss" + pm.variables.get("uniq") + "@domain.com";
const password = "Password123!";
pm.variables.set("stEmail", email);
pm.variables.set("stPassword", password);
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/register",
    method: "POST",
    header: { "Content-Type": "application/json",
              "X-Student-Id": pm.environment.get("student_id") },
    body: { mode: "raw", raw: JSON.stringify({
        name: "<script>alert('XSS')</script>", email: email, password: password,
        confirmPassword: password }) }
}, function () {
    pm.sendRequest({
        url: pm.environment.get("base_url") + "/api/login",
        method: "POST",
        header: { "Content-Type": "application/json",
                  "X-Student-Id": pm.environment.get("student_id") },
        body: { mode: "raw", raw: JSON.stringify({ email: email, password: password }) }
    }, function (err, res) {
        if (res && res.json() && res.json().token) {
            pm.variables.set("stToken", res.json().token);
        }
    });
});
"""),
    expected="returned as a JSON string, with Content-Type application/json",
    tests=js("""
pm.test("Response is JSON data, not HTML", function () {
    pm.expect(pm.response.headers.get("Content-Type") || "")
      .to.include("application/json");
});
pm.test("Payload is preserved as data, not interpreted", function () {
    pm.expect(pm.response.json().name).to.be.a("string");
});"""))

add(id="A1-SEC-006", dim="Security", param="name", rule="SEC-04",
    partition="stored XSS via an image/onerror payload",
    title="An onerror payload in the name is stored without a server error",
    body=rb(name="<img src=x onerror=alert(1)>"),
    expected="handled as data; no 5xx and no HTML content type",
    tests=no500() + js("""
pm.test("Response is JSON, not rendered HTML", function () {
    pm.expect(pm.response.headers.get("Content-Type") || "")
      .to.include("application/json");
});"""))

add(id="A1-SEC-007", dim="Security", param="email", rule="SEC-05",
    partition="SQL injection: statement termination in email",
    title="A DROP TABLE payload in the email must be neutralised",
    body=rb(email="sqli{{uniq}}'); DROP TABLE users;--@domain.com"),
    expected="rejected or stored literally; never a 5xx, never a SQL error",
    tests=no500() + "\n" + no_leak())

add(id="A1-SEC-008", dim="Security", param="name", rule="SEC-05",
    partition="SQL injection: tautology in name",
    title="An OR 1=1 payload in the name must be neutralised",
    body=rb(name="' OR '1'='1"),
    expected="stored literally; never a 5xx, never a SQL error",
    tests=no500() + "\n" + no_leak())

add(id="A1-SEC-009", dim="Security", param="email", rule="SEC-05",
    partition="SQL injection: UNION SELECT in email",
    title="A UNION SELECT payload must not return extra data",
    body=rb(email="u{{uniq}}' UNION SELECT id,email,password FROM users--@domain.com"),
    expected="no 5xx, no leaked rows, no SQL error text",
    tests=no500() + "\n" + no_leak() + js("""
pm.test("No credential material leaks into the response", function () {
    pm.expect(pm.response.text()).to.not.include("Admin123!");
});"""))

add(id="A1-SEC-010", dim="Security", param="password", rule="SEC-05",
    partition="SQL injection: comment sequence in password",
    title="A comment-sequence payload in the password must be neutralised",
    body=rb(password="Aa1!'--"), expected="no 5xx, no SQL error text",
    tests=no500() + "\n" + no_leak())

add(id="A1-SEC-011", dim="Security", param="-", rule="SEC-05",
    partition="SQL injection: data integrity after the attempts above",
    title="The users table survives the injection attempts intact",
    method="POST", path="/api/login",
    body={"email": "{{admin_email}}", "password": "{{admin_password}}"},
    pre=js("""
// Fire the injection payloads first, then check the seeded admin still exists.
const base = pm.environment.get("base_url");
const sid = pm.environment.get("student_id");
const uniq = pm.variables.get("uniq");
[
    { name: "drop", email: "z" + uniq + "'); DROP TABLE users;--@domain.com" },
    { name: "' OR '1'='1", email: "y" + uniq + "@domain.com" }
].forEach(function (payload) {
    pm.sendRequest({
        url: base + "/api/register",
        method: "POST",
        header: { "Content-Type": "application/json", "X-Student-Id": sid },
        body: { mode: "raw", raw: JSON.stringify({
            name: payload.name, email: payload.email, password: "Password123!",
            confirmPassword: "Password123!" }) }
    }, function () {});
});
"""),
    expected="200 - the seeded admin account is still there and still works",
    tests=js("""
pm.test("Seeded admin account survived the injection attempts", function () {
    pm.response.to.have.status(200);
    pm.expect(pm.response.json()).to.have.property("token");
});"""))

add(id="A1-SEC-012", dim="Security", param="role", rule="SEC-06",
    partition="privilege escalation: role injected at registration",
    title="A client-supplied role must not create an admin account",
    method="POST", path="/api/login",
    body={"email": "{{stEmail}}", "password": "{{stPassword}}"},
    pre=js("""
const email = "esc" + pm.variables.get("uniq") + "@domain.com";
const password = "Password123!";
pm.variables.set("stEmail", email);
pm.variables.set("stPassword", password);
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/register",
    method: "POST",
    header: { "Content-Type": "application/json",
              "X-Student-Id": pm.environment.get("student_id") },
    body: { mode: "raw", raw: JSON.stringify({
        name: "Escalation Probe", email: email, password: password,
        confirmPassword: password,
        role: "admin" }) }
}, function () { console.log("[HW06] A1-SEC-012 registered with role=admin injected"); });
"""),
    expected="the account's role is 'user' - the injected value was ignored",
    tests=js("""
pm.test("Injected role did not take effect", function () {
    const u = pm.response.json().user || {};
    pm.expect(u.role, "role of the new account").to.eql("user");
});"""))

add(id="A1-SEC-013", dim="Security", param="role", rule="SEC-03 / SEC-06",
    partition="authorization: ordinary user reaches an admin route",
    title="A newly registered ordinary user cannot reach admin APIs",
    method="GET", path="/api/admin/users", auth_var="stToken",
    pre=js("""
const email = "esc2" + pm.variables.get("uniq") + "@domain.com";
const password = "Password123!";
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/register",
    method: "POST",
    header: { "Content-Type": "application/json",
              "X-Student-Id": pm.environment.get("student_id") },
    body: { mode: "raw", raw: JSON.stringify({
        name: "Escalation Probe 2", email: email, password: password,
        confirmPassword: password,
        role: "admin" }) }
}, function () {
    pm.sendRequest({
        url: pm.environment.get("base_url") + "/api/login",
        method: "POST",
        header: { "Content-Type": "application/json",
                  "X-Student-Id": pm.environment.get("student_id") },
        body: { mode: "raw", raw: JSON.stringify({ email: email, password: password }) }
    }, function (err, res) {
        if (res && res.json() && res.json().token) {
            pm.variables.set("stToken", res.json().token);
        }
    });
});
"""),
    expected="401 or 403 - SEC-03 requires a genuine admin role",
    tests=js("""
pm.test("Escalated account is refused by the admin API", function () {
    pm.expect(pm.response.code).to.be.oneOf([401, 403]);
});"""))

add(id="A1-SEC-014", dim="Security", param="id", rule="SEC-06",
    partition="mass assignment: primary key injected",
    title="A client-supplied id must not override the generated one",
    body=rb(id=1, email="idinj{{uniq}}@domain.com"),
    expected="200 with a server-generated id that is not the injected 1",
    tests=js("""
pm.test("Server generated its own id", function () {
    pm.expect(Number(pm.response.json().id), "id").to.not.eql(1);
});"""))

add(id="A1-SEC-015", dim="Security", param="login_attempts", rule="SEC-06",
    partition="mass assignment: lockout counters injected",
    title="Injected lockout fields must not affect the new account",
    method="POST", path="/api/login",
    body={"email": "{{stEmail}}", "password": "{{stPassword}}"},
    pre=js("""
const email = "lock" + pm.variables.get("uniq") + "@domain.com";
const password = "Password123!";
pm.variables.set("stEmail", email);
pm.variables.set("stPassword", password);
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/register",
    method: "POST",
    header: { "Content-Type": "application/json",
              "X-Student-Id": pm.environment.get("student_id") },
    body: { mode: "raw", raw: JSON.stringify({
        name: "Lock Probe", email: email, password: password,
        confirmPassword: password,
        login_attempts: 99, locked_until: "2099-01-01T00:00:00.000Z" }) }
}, function () { console.log("[HW06] A1-SEC-015 registered with lock fields injected"); });
"""),
    expected="200 - the injected lock was ignored, so login still works",
    tests=js("""
pm.test("Injected lockout fields were ignored", function () {
    pm.response.to.have.status(200);
    pm.expect(pm.response.json()).to.have.property("token");
});"""))

add(id="A1-SEC-016", dim="Security", param="reset_token", rule="SEC-06 / SEC-07",
    partition="mass assignment: reset token injected",
    title="A client-supplied reset token must not be usable",
    method="POST", path="/api/reset-password",
    body={"email": "rst{{uniq}}@domain.com", "resetToken": "123456",
          "newPassword": "Hijacked999!"},
    pre=js("""
const email = "rst" + pm.variables.get("uniq") + "@domain.com";
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/register",
    method: "POST",
    header: { "Content-Type": "application/json",
              "X-Student-Id": pm.environment.get("student_id") },
    body: { mode: "raw", raw: JSON.stringify({
        name: "Reset Probe", email: email, password: "Password123!",
        confirmPassword: "Password123!",
        reset_token: "123456" }) }
}, function () { console.log("[HW06] A1-SEC-016 registered with reset_token injected"); });
"""),
    expected="4xx - a token the client chose must never authorise a reset",
    tests=rejected("client-supplied reset token must not be honoured"))

add(id="A1-SEC-017", dim="Security", param="body", rule="SEC-06",
    partition="prototype pollution",
    title="A __proto__ payload does not crash or escalate",
    raw_body='{"name":"Proto Probe","email":"proto{{uniq}}@domain.com",'
             '"password":"Password123!","__proto__":{"role":"admin"}}',
    expected="no 5xx; the payload is ignored",
    tests=no500() + "\n" + no_leak())

add(id="A1-SEC-018", dim="Security", param="-", rule="SEC-01",
    partition="information disclosure: no session issued at registration",
    title="Registration must not return an authentication token",
    body=rb(email="tok{{uniq}}@domain.com"),
    expected="no token/JWT in the response - FR-01 sends the user to the login page",
    tests=js("""
pm.test("No token is issued by registration", function () {
    const t = pm.response.text().toLowerCase();
    pm.expect(t).to.not.include('"token"');
    pm.expect(t).to.not.include("bearer");
});"""))

add(id="A1-SEC-019", dim="Security", param="-", rule="SEC-05",
    partition="information disclosure: error responses",
    title="A failed registration must not leak database internals",
    body=rb(name={"nested": {"deep": True}}, email="err{{uniq}}@domain.com"),
    expected="a clean 4xx message with no driver, table or stack detail",
    tests=no_leak() + "\n" + no500())

add(id="A1-SEC-020", dim="Security", param="-", rule="SEC-02 (not applicable)",
    partition="authentication requirement: endpoint is public by design",
    title="Registration works without any Authorization header",
    body=rb(email="pub{{uniq}}@domain.com"),
    expected="200 - SEC-02 does not apply; registration must stay public",
    tests=accepted(),
    gap="Documents why SEC-02 is not applicable to this endpoint.")


# ===========================================================================
# STEP 5 - SCHEMA VALIDATION
# ===========================================================================
# The response shape must match api_specification.md exactly - no missing
# fields, no extra fields, correct JSON types.

_SUCCESS_SCHEMA = """
const schema = {
    type: "object",
    required: ["message", "id"],
    additionalProperties: false,
    properties: {
        message: { type: "string" },
        id: { type: "integer" }
    }
};
"""

add(id="A1-SCH-001", dim="Schema", param="-", rule="spec conformance",
    partition="success body: strict schema",
    title="The success response contains exactly {message, id}",
    body=rb(email="sch{{uniq}}@domain.com"),
    expected="body validates against the spec schema with additionalProperties false",
    tests=_SUCCESS_SCHEMA + js("""
pm.test("Success body matches the specified schema exactly", function () {
    pm.response.to.have.jsonSchema(schema);
});"""))

add(id="A1-SCH-002", dim="Schema", param="-", rule="spec conformance",
    partition="success body: message text",
    title="The success message is exactly the documented string",
    body=rb(email="sch2{{uniq}}@domain.com"),
    expected='message === "User registered successfully"',
    tests=js("""
pm.test("Message matches the specification verbatim", function () {
    pm.expect(pm.response.json().message).to.eql("User registered successfully");
});"""))

add(id="A1-SCH-003", dim="Schema", param="-", rule="spec conformance",
    partition="success body: id type",
    title="The returned id is a JSON integer, not a string",
    body=rb(email="sch3{{uniq}}@domain.com"),
    expected="typeof id === 'number' and Number.isInteger(id)",
    tests=js("""
pm.test("id is an integer number", function () {
    const id = pm.response.json().id;
    pm.expect(id).to.be.a("number");
    pm.expect(Number.isInteger(id), "id must be an integer").to.be.true;
});"""))

add(id="A1-SCH-004", dim="Schema", param="-", rule="spec conformance",
    partition="success body: id range",
    title="The returned id is a positive identifier",
    body=rb(email="sch4{{uniq}}@domain.com"), expected="id > 0",
    tests=js("""
pm.test("id is positive", function () {
    pm.expect(pm.response.json().id).to.be.above(0);
});"""))

add(id="A1-SCH-005", dim="Schema", param="-", rule="spec conformance",
    partition="response headers: content type",
    title="The response is served as application/json",
    body=rb(email="sch5{{uniq}}@domain.com"),
    expected="Content-Type includes application/json",
    tests=js("""
pm.test("Content-Type is application/json", function () {
    pm.expect(pm.response.headers.get("Content-Type") || "")
      .to.include("application/json");
});"""))

add(id="A1-SCH-006", dim="Schema", param="-", rule="spec conformance",
    partition="status code: documented success code",
    title="A successful registration returns HTTP 200 as documented",
    body=rb(email="sch6{{uniq}}@domain.com"),
    expected="200 - the spec documents 200 OK, not 201",
    tests=st(200))

add(id="A1-SCH-007", dim="Schema", param="-", rule="spec conformance",
    partition="error body: validation failure shape",
    title="A validation error returns a structured error body",
    body={}, expected='4xx with {"error": "<string>"}',
    tests=js("""
pm.test("Validation failure returns a 4xx", function () {
    pm.expect(pm.response.code).to.be.within(400, 499);
});
pm.test("Error body is structured JSON with an error field", function () {
    const b = pm.response.json();
    pm.expect(b).to.have.property("error");
    pm.expect(b.error).to.be.a("string");
});"""))

add(id="A1-SCH-008", dim="Schema", param="-", rule="spec conformance / SEC-01",
    partition="response body: forbidden fields",
    title="The response exposes no credential or role fields",
    body=rb(email="sch8{{uniq}}@domain.com"),
    expected="no password, role, token or reset_token key anywhere in the body",
    tests=js("""
const text = pm.response.text().toLowerCase();
["password", "role", "token", "reset_token"].forEach(function (key) {
    pm.test('Response contains no "' + key + '" field', function () {
        pm.expect(text).to.not.include('"' + key + '"');
    });
});"""))

add(id="A1-SCH-009", dim="Schema", param="-", rule="spec conformance",
    partition="response body: no extra fields",
    title="The success body carries no undocumented fields",
    body=rb(email="sch9{{uniq}}@domain.com"),
    expected="exactly two keys: message and id",
    tests=js("""
pm.test("Exactly the two documented keys are present", function () {
    const keys = Object.keys(pm.response.json()).sort();
    pm.expect(keys).to.eql(["id", "message"]);
});"""))

add(id="A1-SCH-010", dim="Schema", param="-", rule="spec conformance",
    partition="error body: duplicate email shape",
    title="A duplicate-email rejection returns a structured error body",
    body=rb(email="dupsch{{uniq}}@domain.com"),
    pre=js("""
const email = "dupsch" + pm.variables.get("uniq") + "@domain.com";
pm.sendRequest({
    url: pm.environment.get("base_url") + "/api/register",
    method: "POST",
    header: { "Content-Type": "application/json",
              "X-Student-Id": pm.environment.get("student_id") },
    body: { mode: "raw", raw: JSON.stringify({
        name: "First Owner", email: email, password: "Password123!",
        confirmPassword: "Password123!" }) }
}, function () { console.log("[HW06] A1-SCH-010 fixture claimed " + email); });
"""),
    expected='4xx with {"error": "<string>"} naming the conflict',
    tests=js("""
pm.test("Duplicate registration is refused", function () {
    pm.expect(pm.response.code).to.be.within(400, 499);
});
pm.test("Error body is structured", function () {
    pm.expect(pm.response.json()).to.have.property("error");
});"""))

add(id="A1-SCH-011", dim="Schema", param="-", rule="spec conformance",
    partition="identity uniqueness across responses",
    title="Two registrations never return the same id",
    body=rb(email="uniq2{{uniq}}@domain.com"),
    pre=js(_REGISTER_FIXTURE),
    expected="the returned id differs from the fixture account's id",
    tests=js("""
pm.test("Returned id is distinct from the previous registration", function () {
    pm.expect(Number(pm.response.json().id))
      .to.not.eql(Number(pm.variables.get("stUserId")));
});"""))

add(id="A1-SCH-012", dim="Schema", param="-", rule="spec conformance",
    partition="error body: not an HTML error page",
    title="Errors are JSON, never an HTML stack-trace page",
    raw_body='{"name": "Broken",',
    expected="the error response is JSON or plain text, never an HTML error page",
    tests=js("""
pm.test("Error response is not an HTML page", function () {
    pm.expect((pm.response.headers.get("Content-Type") || "").toLowerCase())
      .to.not.include("text/html");
});
pm.test("No stack trace is rendered", function () {
    pm.expect(pm.response.text().toLowerCase()).to.not.include("<pre>");
});"""))


# ===========================================================================
# PHASE 3 - STUDENT-DESIGNED EXTENSIONS
# ===========================================================================

add(id="A1-HR-001", dim="Security", param="email", rule="FR-01 / SEC-04",
    partition="invalid: horizontal-tab control character in email",
    title="An email containing a horizontal tab is rejected",
    body=rb(email="tab{{uniq}}\t@domain.com"), expected="4xx - control characters are not part of user@domain.com",
    tests=rejected("email contains a control character"),
    origin="Student-designed",
    rationale="The AI covered ordinary spaces but missed non-printing whitespace that often bypasses simplistic validators.")

add(id="A1-HR-002", dim="Security", param="email", rule="FR-01 / SEC-04",
    partition="invalid: CRLF sequence in email",
    title="An email containing CRLF is rejected without response splitting",
    body=rb(email="crlf{{uniq}}\r\nX-Injected: yes@domain.com"),
    expected="4xx, no 5xx and no reflected injected header",
    tests=rejected("email contains CRLF") + "\n" + no500() + js("""
pm.test("The injected header is not reflected", function () {
    pm.expect(pm.response.headers.has("X-Injected")).to.be.false;
});"""),
    origin="Student-designed",
    rationale="The generated injection set focused on SQL/XSS and omitted HTTP response-splitting input.")

add(id="A1-HR-003", dim="Security", param="name", rule="SEC-04",
    partition="invalid: NUL control character in a display name",
    title="A name containing a NUL character is rejected safely",
    body=rb(name="Nguyen\u0000Van A", email="nul{{uniq}}@domain.com"),
    expected="4xx and no internal error disclosure",
    tests=rejected("name contains a NUL control character") + "\n" + no_leak() + "\n" + no500(),
    origin="Student-designed",
    rationale="Control-character validation was absent from the AI's domain partitions.")

add(id="A1-HR-004", dim="Domain", param="Content-Type", rule="spec conformance",
    partition="valid: JSON media type with UTF-8 charset parameter",
    title="application/json with a UTF-8 charset is accepted",
    body=rb(name="Nguyễn Văn A", email="charset{{uniq}}@domain.com"),
    content_type="application/json; charset=utf-8", expected="200 with the documented success body",
    tests=accepted(), origin="Student-designed",
    rationale="The AI tested application/json and text/plain but missed a common valid media-type parameter.")

add(id="A1-HR-005", dim="Domain", param="confirmPassword", rule="FR-01",
    partition="invalid: confirmation has the wrong JSON type",
    title="A numeric password confirmation is rejected",
    body=rb(email="confirmtype{{uniq}}@domain.com", confirmPassword=12345678),
    expected="4xx - confirmation must be a string equal to password",
    tests=rejected("confirmPassword has the wrong type"),
    origin="Student-designed",
    rationale="The AI covered missing, matching and mismatching confirmation values but not its type partition.")


# ---------------------------------------------------------------------------

META = {
    "api": 1,
    "slug": "api1-fr01-register",
    "collection_name": "API1 - FR-01 Account Registration (POST /api/register)",
    "sheet": "API1 FR-01 Register",
    "endpoint": "POST /api/register",
    "pool": "A",
    "requirement": "FR-01",
    "description": (
        "HW06 / Pool A / FR-01 - Account registration.\n\n"
        "Spec: POST /api/register {name, email, password} -> 200 "
        '{"message": "User registered successfully", "id": <int>}.\n\n'
        "Generated from the case specification in "
        "scripts/cases/api1_fr01_register.py. Expected results are derived from "
        "FR-01 and SEC-01..SEC-07, never from the SUT's observed behaviour, so a "
        "failing case here is evidence about the implementation rather than a "
        "broken test."
    ),
    "folders": [
        ("01 - Domain partitions", "Domain",
         "Equivalence classes and boundaries for every parameter, plus the "
         "request envelope and the HTTP method."),
        ("02 - State transitions", "State",
         "Account lifecycle: none -> registered -> authenticated, and the "
         "initial state a new account must start in."),
        ("03 - Security (SEC-01..SEC-07)", "Security",
         "One or more cases per applicable SEC rule, with the not-applicable "
         "ones documented rather than silently skipped."),
        ("04 - Schema validation", "Schema",
         "The response shape against api_specification.md - strict, so extra "
         "fields fail too."),
    ],
    "subfolders": {
        "01 - Domain partitions": [
            ("name", "name"),
            ("email", "email"),
            ("password", "password"),
            ("confirm password", "confirmPassword"),
            ("request envelope", "body"),
            ("http method", "http method"),
        ],
    },
}
