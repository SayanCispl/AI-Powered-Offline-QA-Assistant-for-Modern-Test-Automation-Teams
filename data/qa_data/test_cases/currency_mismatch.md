# currency_mismatch.md

# 💱 Currency Mismatch Issue

## Issue Summary

Displayed checkout currency differs from charged currency.

---

## Environment

- Environment: Production
- Region: International Payments

---

## Steps to Reproduce

1. Select USD currency
2. Complete checkout
3. Verify bank statement

---

## Expected Result

Charged currency should match displayed currency.

---

## Actual Result

- UI shows USD
- Gateway charges INR

---

## Root Cause

Currency conversion service fallback issue.

---

## Suggested Validation

- Validate exchange rate API
- Validate currency mapping
- Validate gateway currency configuration

---

## QA Scenarios

- Multi-currency validation
- Exchange rate verification
- UI/API consistency testing
- Currency fallback testing

---

## Severity

High

## Priority

High
