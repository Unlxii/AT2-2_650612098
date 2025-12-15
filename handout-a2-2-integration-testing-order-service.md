# Activity 2.2: Handout for Integration Testing — Order Service

## Objective
Learn **Integration Testing** by practicing 3 common strategies:
- **Top-down**
- **Bottom-up**
- **Sandwich (Hybrid)**

You will work with a small Order Service composed of multiple collaborating components.

---

## System Overview
**Architecture**
OrderService  
├─ Inventory  
├─ Payment  
├─ Shipping  
└─ Email  


**Key Idea**
- We test how components work **together**, not in isolation.
- We use **Stub / Driver / Spy** to control or observe behavior.

---

## Testing Strategies

### 1) Top-down Integration
- Start from **OrderService**
- Replace lower components with **Stubs / Spies**
- Focus: workflow, error handling, orchestration

Examples:
- Payment fails → stock must be released
- Email is sent after successful order

---

### 2) Bottom-up Integration
- Start from **low-level components**
- Use real implementations
- Focus: correctness at boundaries

Examples:
- Inventory reserve/release
- Edge cases (qty = 0, negative qty)

---

### 3) Sandwich (Hybrid)
- Combine both approaches
- Real middle components + stub/spy at edges

Examples:
- Real Payment + Spy Email
- Verify shipping cost logic by region

---

## What You Must Do (Checklist)

### Read
- `inventory.py`
- `payment.py`
- `shipping.py`
- `emailer.py`
- `order.py`

### Extend Tests (see TODOs)
1. **Top-down**
   - Add failing payment cases
   - Verify email subject/body using Spy

2. **Bottom-up**
   - Add boundary tests for inventory errors

3. **Sandwich**
   - Test shipping cost for `"US"`
   - Test weight > 5kg in `"TH"`

### Reflect
- Write **5–10 lines** summarizing:
  - What broke?
  - What integration risks you found?

---

## How to Run
```bash
make venv
make install
make test
