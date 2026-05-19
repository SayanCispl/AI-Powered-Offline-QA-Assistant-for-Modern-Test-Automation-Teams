# partial_payment.md

# 💰 Partial Payment Issue

## Issue Summary

Payment gateway deducts amount partially but order status remains failed.

---

## Environment

- Environment: UAT
- Payment Method: Net Banking

---

## Steps to Reproduce

1. Initiate payment
2. Interrupt payment flow during processing
3. Return to merchant site

---

## Expected Result

System should reconcile partial payment correctly.

---

## Actual Result

- Amount deducted partially
- Order not confirmed
- Payment status mismatch

---

## Root Cause

Webhook confirmation not received before session timeout.

---

## Suggested Validation

- Validate reconciliation process
- Validate refund trigger
- Validate transaction recovery

---

## QA Scenarios

- Interrupted payment flow
- Session timeout validation
- Reconciliation validation
- Retry payment validation

---

## Severity

High

## Priority

High
