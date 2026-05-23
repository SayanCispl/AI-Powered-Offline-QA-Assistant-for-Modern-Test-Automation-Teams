---
type: flaky_test
framework: playwright
severity: high
---
# Playwright Locator Failure

## Symptoms

- locator.click timeout
- strict mode violation
- locator not found

---

## Root Cause

- Dynamic selector
- Delayed rendering
- Incorrect locator strategy

---

## Recommended Fix

- Use stable data-testid
- Use locator.wait_for()
- Improve selector strategy

---

## Prevention

- Avoid nth-child locators
- Use semantic locators
- Add proper synchronization

---

## Keywords

playwright flaky,
locator failure,
strict mode,
dynamic selector
