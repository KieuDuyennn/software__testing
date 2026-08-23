# API 1 - FR-01 Account Registration - Phase 3: Extend

> Pipeline step 3 of 4. At least five test cases of your own that the AI missed,
> weighted towards security and state transitions, each with an explanation of
> *why* the AI missed it.

| Field | Value |
|---|---|
| Endpoint | `POST /api/register` |
| Requirement | FR-01 |
| Cases added | (>= 5) |

## Added test cases

### EXT-01 |

- **Dimension:** security / state transition / domain / schema
- **Requirement or SEC id:**
- **Precondition:**
- **Steps:**
- **Expected result:**
- **Actual result:**
- **Why the AI missed it:** prompt quality / model limitation / a property of
  the API that is not visible in the specification (be specific - "the spec
  documents the happy path only, so nothing in the text hints that the detail
  route has no auth middleware" is a real reason; "the AI was lazy" is not)

### EXT-02 |

### EXT-03 |

### EXT-04 |

### EXT-05 |

## Why these gaps existed

Group the five reasons into causes. The three that usually appear:

1. **The spec does not describe it.** The AI reads `api_specification.md`; a
   missing auth middleware or a wrong comparison operator is invisible there.
   Only the requirement document, or the implementation, exposes it.
2. **The prompt framed the endpoint in isolation.** Cross-resource attacks
   (IDOR, privilege escalation, ownership) need a second actor, which a
   single-endpoint prompt never introduces.
3. **The AI asserts observed behaviour.** Asked what a response looks like, it
   describes what the SUT returns - which cannot, by construction, find a bug.
