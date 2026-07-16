# COCOMO Estimation Report: MenstrualTracker App

This document outlines the Constructive Cost Model (COCOMO) estimations for the MenstrualTracker App across all three development modes: **Organic**, **Semi-Detached**, and **Embedded**.

## 1. Estimated Lines of Code (LOC)
- **Estimated Size:** ~1,556 Lines of Code (1.56 KLOC)
*(Note: This is the actual counted size of the core application Python and KV files, excluding virtual environments and external dependencies).*

## 2. Basic COCOMO Constants

| Mode | a | b | c | d |
| :--- | :--- | :--- | :--- | :--- |
| **Organic** | 2.4 | 1.05 | 2.5 | 0.38 |
| **Semi-Detached** | 3.0 | 1.12 | 2.5 | 0.35 |
| **Embedded** | 3.6 | 1.20 | 2.5 | 0.32 |

## 3. Calculations

We assume an average developer salary of **₹1,00,000 per month** (approx. **$1,198 USD** based on an exchange rate of $1 = ₹83.50) for the cost calculations.

Formulas:
- **Effort (Person-Months):** `Effort = a * (KLOC)^b`
- **Development Time (Months):** `Time = c * (Effort)^d`
- **Required Team Size (Persons):** `Staffing = Effort / Time`
- **Total Estimated Cost:** `Cost = Effort * Average Monthly Salary`

### 3.1 Organic Mode
*Appropriate for small teams, familiar environments, and well-understood requirements.*

- **Effort:** 2.4 * (1.56)^1.05 ≈ **3.82 Person-Months**
- **Time:** 2.5 * (3.82)^0.38 ≈ **4.16 Months**
- **Staffing:** 3.82 / 4.16 ≈ **1 Developer**
- **Cost (INR):** 3.82 * ₹1,00,000 = **₹3,81,787**
- **Cost (USD):** 3.82 * $1,198 = **$4,572**

### 3.2 Semi-Detached Mode
*Appropriate for medium-sized teams, mixed experience levels, and somewhat rigid requirements.*

- **Effort:** 3.0 * (1.56)^1.12 ≈ **4.92 Person-Months**
- **Time:** 2.5 * (4.92)^0.35 ≈ **4.37 Months**
- **Staffing:** 4.92 / 4.37 ≈ **1-2 Developers**
- **Cost (INR):** 4.92 * ₹1,00,000 = **₹4,92,234**
- **Cost (USD):** 4.92 * $1,198 = **$5,895**

### 3.3 Embedded Mode
*Appropriate for complex projects with strict constraints, rigid requirements, and specialized hardware/software.*

- **Effort:** 3.6 * (1.56)^1.20 ≈ **6.12 Person-Months**
- **Time:** 2.5 * (6.12)^0.32 ≈ **4.46 Months**
- **Staffing:** 6.12 / 4.46 ≈ **1-2 Developers**
- **Cost (INR):** 6.12 * ₹1,00,000 = **₹6,11,947**
- **Cost (USD):** 6.12 * $1,198 = **$7,328**

## 4. Summary & Conclusion

| Mode | Effort (Person-Months) | Time (Months) | Staffing | Cost (INR) | Cost (USD) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Organic** | 3.82 | 4.16 | 1 Developer | ₹3,81,787 | $4,572 |
| **Semi-Detached** | 4.92 | 4.37 | 1-2 Developers | ₹4,92,234 | $5,895 |
| **Embedded** | 6.12 | 4.46 | 1-2 Developers | ₹6,11,947 | $7,328 |

Based on the actual size of the codebase (~1.56 KLOC), the MenstrualTracker App most closely aligns with the **Organic** model, requiring approximately **4 months** for a **solo developer**, at a cost of roughly **₹3.8 Lakhs ($4,500 USD)**. Scaling it to an **Embedded** model (e.g., rigid compliance, proprietary systems) would increase the required effort to just over **6 Person-Months**, raising the cost to about **₹6.1 Lakhs ($7,300 USD)**.
