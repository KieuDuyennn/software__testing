# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: fr11_order_history\fr11.order-history.spec.ts >> FR-11 Order history view >> FR11-TC-19 [negative] a non-admin user must not be able to change an order's status
- Location: automation\tests\fr11_order_history\fr11.order-history.spec.ts:320:5

# Error details

```
Error: FR11-TC-19 set status: http://localhost:3000/api/admin/orders/27/status answered 200, expected one of [401, 403]. Body: {"message":"Order status updated"}

expect(received).toContain(expected) // indexOf

Expected value: 200
Received array: [401, 403]
```

```
Error: FR11-TC-19: status was changed to "confirmed" despite the refusal

expect(received).toBe(expected) // Object.is equality

Expected: "pending"
Received: "confirmed"
```

# Test source

```ts
  330 |       }
  331 | 
  332 |       const otherIds: number[] = [];
  333 |       for (let i = 0; i < (row.seed_other_orders ?? 0); i++) {
  334 |         otherIds.push(await api.checkout(request, await ensureOther(), 2_000_000));
  335 |       }
  336 | 
  337 |       /* ---------------- API channel ---------------- */
  338 | 
  339 |       if (row.channel === 'api') {
  340 |         const tokenFor = async (): Promise<string | null> => {
  341 |           switch (row.acting_as) {
  342 |             case 'owner': return ownerToken;
  343 |             case 'admin': return adminToken;
  344 |             case 'other': return ensureOther();
  345 |             case 'none': return null;
  346 |             case 'ghost':
  347 |               return api.mintToken(SUT_JWT_SECRET, { id: 2_147_483_647, role: 'user' });
  348 |             default:
  349 |               throw new Error(`${row.tc_id}: acting_as "${row.acting_as}" is not a known identity`);
  350 |           }
  351 |         };
  352 |         const token = await tokenFor();
  353 | 
  354 |         const expectsDenial = !row.expect_http_any_of!.includes(200);
  355 | 
  356 |         /**
  357 |          * Every status assertion in this branch is SOFT, on purpose.
  358 |          *
  359 |          * A hard `expect` throws, so when a denial case is answered `200` - which is
  360 |          * what 6 of these rows are predicted to do - the assertion aborts the test
  361 |          * before the follow-up check runs, and the report says only "expected 403, got
  362 |          * 200". The far more serious facts (the record was disclosed; the status was
  363 |          * written anyway) would never be collected. Soft failures still fail the test,
  364 |          * so nothing is weakened: both statements land in the same report. Same
  365 |          * reasoning as finding 3, which is where this pattern came from.
  366 |          */
  367 |         switch (row.api_call) {
  368 |           case 'order_detail': {
  369 |             // The id is either written literally in the data file (the malformed and
  370 |             // boundary probes) or resolved from what this run seeded.
  371 |             const id = row.detail_order_id ?? (
  372 |               row.detail_owned_by === 'other' ? String(otherIds[0]) : String(seededIds[0])
  373 |             );
  374 |             const response = await api.orderDetailRaw(request, token, id);
  375 |             // Evidence first, assertion second: reading the body cannot be skipped by a
  376 |             // status assertion that throws.
  377 |             const disclosed = response.status() === 200 ? await response.json() : null;
  378 | 
  379 |             await expectStatusAmong(
  380 |               response, row.expect_http_any_of!, `${row.tc_id} order detail`, { soft: true },
  381 |             );
  382 | 
  383 |             // Pattern 3: a refusal that still ships the record is not a refusal.
  384 |             if (expectsDenial && disclosed !== null) {
  385 |               expect(
  386 |                 disclosed,
  387 |                 `${row.tc_id}: the request was refused-by-requirement yet the order record ` +
  388 |                 `was returned in full - fields: ${Object.keys(disclosed).join(', ')}`,
  389 |               ).not.toHaveProperty('total_amount');
  390 |             }
  391 |             break;
  392 |           }
  393 | 
  394 |           case 'admin_orders_list': {
  395 |             const response = await api.adminOrdersListRaw(request, token!);
  396 |             const leaked = response.status() === 200 ? await response.json() : null;
  397 | 
  398 |             await expectStatusAmong(
  399 |               response, row.expect_http_any_of!, `${row.tc_id} admin order list`, { soft: true },
  400 |             );
  401 | 
  402 |             // Pattern 3: scale is the finding here. "A non-admin got 200" understates it
  403 |             // if the body was every order in the database, with each owner's name.
  404 |             if (expectsDenial && Array.isArray(leaked)) {
  405 |               expect(
  406 |                 leaked.length,
  407 |                 `${row.tc_id}: a non-admin account was served ${leaked.length} orders ` +
  408 |                 `belonging to other users`,
  409 |               ).toBe(0);
  410 |             }
  411 |             break;
  412 |           }
  413 | 
  414 |           case 'admin_set_status': {
  415 |             const response = await api.setStatusRaw(request, token!, seededIds[0], row.set_status!);
  416 |             await expectStatusAmong(
  417 |               response, row.expect_http_any_of!, `${row.tc_id} set status`, { soft: true },
  418 |             );
  419 | 
  420 |             // Pattern 3: a refused transition must also have left the row alone. A 400
  421 |             // that still wrote the new status would pass on the code alone. The
  422 |             // conditional guard makes transition_from mandatory on these rows, so the
  423 |             // check can never be silently skipped.
  424 |             if (expectsDenial) {
  425 |               const after = (await api.myOrders(request, ownerToken))
  426 |                 .find((o) => o.id === seededIds[0]);
  427 |               expect(
  428 |                 after?.status,
  429 |                 `${row.tc_id}: status was changed to "${row.set_status}" despite the refusal`,
> 430 |               ).toBe(row.transition_from);
      |                 ^ Error: FR11-TC-19: status was changed to "confirmed" despite the refusal
  431 |             }
  432 |             break;
  433 |           }
  434 | 
  435 |           case 'order_cancel': {
  436 |             const targetIsOther = row.cancel_owned_by === 'other';
  437 |             const target = targetIsOther ? otherIds[0] : seededIds[0];
  438 |             const response = await api.cancelRaw(request, token, target);
  439 |             await expectStatusAmong(
  440 |               response, row.expect_http_any_of!, `${row.tc_id} cancel`, { soft: true },
  441 |             );
  442 | 
  443 |             // Pattern 3: the order must still hold the status it had. Read through the
  444 |             // account that actually OWNS it - my-orders filters on user_id, so asking
  445 |             // with the owner's token for `other`'s order returns nothing and the check
  446 |             // would silently pass on `undefined`.
  447 |             if (expectsDenial) {
  448 |               const readerToken = targetIsOther ? await ensureOther() : ownerToken;
  449 |               const after = (await api.myOrders(request, readerToken))
  450 |                 .find((o) => o.id === target);
  451 |               expect(
  452 |                 after,
  453 |                 `${row.tc_id}: order #${target} is not visible to its own owner, so the ` +
  454 |                 `integrity check cannot run - the fixture is wrong, not the SUT`,
  455 |               ).toBeDefined();
  456 |               expect(
  457 |                 after?.status,
  458 |                 `${row.tc_id}: order #${target} was cancelled despite the request being ` +
  459 |                 `refused${targetIsOther ? ' - and it belongs to another user' : ''}`,
  460 |               ).toBe(row.cancel_target_status);
  461 |             }
  462 |             break;
  463 |           }
  464 | 
  465 |           case 'order_cancel_race': {
  466 |             const target = seededIds[0];
  467 |             const responses = await Promise.all([
  468 |               api.cancelRaw(request, token, target),
  469 |               api.cancelRaw(request, token, target),
  470 |             ]);
  471 |             const actual = responses.map((response) => response.status()).sort((a, b) => a - b);
  472 |             const expected = [...row.expect_http_multiset!].sort((a, b) => a - b);
  473 |             expect(
  474 |               actual,
  475 |               `${row.tc_id}: two simultaneous cancel requests must produce one success and ` +
  476 |               `one refusal, not acknowledge the same state transition twice`,
  477 |             ).toEqual(expected);
  478 |             const after = (await api.myOrders(request, ownerToken)).find((o) => o.id === target);
  479 |             expect(after?.status, `${row.tc_id}: final status after the race`)
  480 |               .toBe(row.expect_final_status);
  481 |             break;
  482 |           }
  483 | 
  484 |           case 'checkout': {
  485 |             const response = await api.checkoutRaw(request, ownerToken, row.checkout_total_amount);
  486 |             await expectStatusAmong(
  487 |               response, row.expect_http_any_of!, `${row.tc_id} checkout`, { soft: true },
  488 |             );
  489 | 
  490 |             // Pattern 3: a rejected checkout must not have created an order. Otherwise a
  491 |             // 400 that writes the row anyway passes on the status alone.
  492 |             if (expectsDenial && response.status() === 200) {
  493 |               const body = await response.json();
  494 |               const created = (await api.myOrders(request, ownerToken))
  495 |                 .find((o) => o.id === body.orderId);
  496 |               expect(
  497 |                 created,
  498 |                 `${row.tc_id}: checkout accepted total_amount ` +
  499 |                 `${JSON.stringify(row.checkout_total_amount)} and created order ` +
  500 |                 `#${body.orderId}, whose stored total is ` +
  501 |                 `${JSON.stringify(created?.total_amount)}`,
  502 |               ).toBeUndefined();
  503 |             }
  504 |             break;
  505 |           }
  506 | 
  507 |           case 'my_orders': {
  508 |             const response = await api.myOrdersRaw(request, token);
  509 |             await expectStatusAmong(
  510 |               response, row.expect_http_any_of!, `${row.tc_id} my-orders`, { soft: true },
  511 |             );
  512 |             if (!row.expect_http_any_of!.includes(200) && response.status() === 200) {
  513 |               const body = await response.json();
  514 |               expect(
  515 |                 body,
  516 |                 `${row.tc_id}: a correctly signed token for a user that does not exist ` +
  517 |                 `was accepted as a live session and received an order-history payload`,
  518 |               ).toBeNull();
  519 |             }
  520 |             break;
  521 |           }
  522 | 
  523 |           default:
  524 |             throw new Error(`${row.tc_id}: api_call "${row.api_call}" is not a known endpoint`);
  525 |         }
  526 |         return;
  527 |       }
  528 | 
  529 |       /* ---------------- UI channel ---------------- */
  530 | 
```