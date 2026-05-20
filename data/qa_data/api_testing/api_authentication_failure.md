# API Authentication Failure During Token Expiry

## Incident Summary

Users received unauthorized API responses after token expiration during active session usage.

---

## Error Response

```json
{
  "status": 401,
  "message": "JWT token expired"
}
```

---

## Symptoms

- Random logout
- API request failures
- Session expiration loops
- Infinite refresh token calls

---

## Root Cause

- Refresh token logic failure
- Expired JWT token reused
- Token refresh race condition

---

## QA Validation

- Token expiry testing
- Session timeout testing
- Refresh token validation
- Concurrent API request testing

---

## Security Validation

- Unauthorized API access prevention
- Expired token rejection
- Session hijacking validation

---

## Related Keywords

401 unauthorized,
jwt token expired,
authentication failure,
api security,
session timeout,
refresh token issue
