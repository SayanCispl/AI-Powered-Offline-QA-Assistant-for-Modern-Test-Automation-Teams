---
type: flaky_test
framework: selenium
severity: high
---
# Selenium Stale Element Failure

## Symptoms

- StaleElementReferenceException
- Element becomes detached from DOM
- Intermittent failure during page refresh

---

## Root Cause

- DOM re-render
- AJAX refresh
- React component reload
- Dynamic UI updates

---

## Recommended Fix

- Re-locate element before interaction
- Use explicit waits
- Avoid storing WebElement references

---

## Prevention

- Implement retry wrapper
- Wait for DOM stabilization
- Use robust locators

---

## Keywords

stale element,
dom refresh,
ajax update,
react rerender,
flaky selenium
