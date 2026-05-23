---
type: flaky_test
framework: selenium
severity: critical
---
# Selenium TimeoutException

## Symptoms

- TimeoutException
- Element not clickable
- Explicit wait timeout

---

## Root Cause

- Slow page loading
- Spinner overlay
- Network latency
- Incorrect wait condition

---

## Recommended Fix

- Increase explicit wait
- Wait for spinner invisibility
- Add network idle wait

---

## Prevention

- Avoid Thread.sleep()
- Use WebDriverWait
- Improve synchronization logic

---

## Keywords

timeout exception,
spinner issue,
element not clickable,
wait issue,
sync failure
