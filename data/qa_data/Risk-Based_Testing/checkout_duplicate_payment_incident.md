# Duplicate Payment Incident During Checkout

## Incident Summary

Users were charged multiple times while retrying payment submission during network interruption.

---

## Environment

- Production
- Razorpay Integration
- Mobile Web Checkout

---

## User Behavior

Users clicked:
"Pay Now"
multiple times after observing delayed response.

---

## Observed Behavior

- Multiple transaction IDs created
- Duplicate charges recorded
- Order status mismatch
- Multiple webhook events received

---

## Database Findings

```sql
SELECT * FROM payment_transactions
WHERE order_id='ORD-84727';
```

Result:

- 3 payment entries found

---

## Root Cause

- Payment button not disabled
- Missing idempotency validation
- Retry requests processed independently

---

## QA Coverage

- Double-click validation
- Retry testing
- API idempotency validation
- Concurrent request testing

---

## Suggested Fixes

- Disable CTA after first click
- Add request token validation
- Add backend idempotency key

---

## Related Keywords

duplicate payment,
payment retry,
double click issue,
multiple transactions,
idempotency failure,
checkout issue,
concurrent payment requests
