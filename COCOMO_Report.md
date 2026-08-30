# COCOMO Estimation Report: MenstrualTracker App

This document outlines the Constructive Cost Model (COCOMO) estimations for the MenstrualTracker App across all three development modes: **Organic**, **Semi-Detached**, and **Embedded**.

## 1. Estimated Lines of Code (LOC)
- **Estimated Size:** ~1,909 Lines of Code (1.91 KLOC)
*(Note: This is the actual counted size of the core application Python and KV files, excluding virtual environments and external dependencies).*

## 2. Basic COCOMO Constants

| Mode | a | b | c | d |
| :--- | :--- | :--- | :--- | :--- |
| **Organic** | 2.4 | 1.05 | 2.5 | 0.38 |
| **Semi-Detached** | 3.0 | 1.12 | 2.5 | 0.35 |
| **Embedded** | 3.6 | 1.20 | 2.5 | 0.32 |

## 3. Calculations

We assume an average US software developer salary of **$10,000 USD per month** (approx. **₹8,35,000 INR** based on an exchange rate of $1 = ₹83.50) for the cost calculations, reflecting USA living standards and tech industry averages.

Formulas:
- **Effort (Person-Months):** `Effort = a * (KLOC)^b`
- **Development Time (Months):** `Time = c * (Effort)^d`
- **Required Team Size (Persons):** `Staffing = Effort / Time`
- **Total Estimated Cost:** `Cost = Effort * Average Monthly Salary`

### 3.1 Organic Mode
*Appropriate for small teams, familiar environments, and well-understood requirements.*

- **Effort:** 2.4 * (1.91)^1.05 ≈ **4.77 Person-Months**
- **Time:** 2.5 * (4.77)^0.38 ≈ **4.53 Months**
- **Staffing:** 4.77 / 4.53 ≈ **1 Developer**
- **Cost (USD):** 4.77 * $10,000 = **$47,700**
- **Cost (INR):** $47,700 * ₹83.50 ≈ **₹39,82,950**

### 3.2 Semi-Detached Mode
*Appropriate for medium-sized teams, mixed experience levels, and somewhat rigid requirements.*

- **Effort:** 3.0 * (1.91)^1.12 ≈ **6.19 Person-Months**
- **Time:** 2.5 * (6.19)^0.35 ≈ **4.73 Months**
- **Staffing:** 6.19 / 4.73 ≈ **1-2 Developers**
- **Cost (USD):** 6.19 * $10,000 = **$61,900**
- **Cost (INR):** $61,900 * ₹83.50 ≈ **₹51,68,650**

### 3.3 Embedded Mode
*Appropriate for complex projects with strict constraints, rigid requirements, and specialized hardware/software.*

- **Effort:** 3.6 * (1.91)^1.20 ≈ **7.79 Person-Months**
- **Time:** 2.5 * (7.79)^0.32 ≈ **4.76 Months**
- **Staffing:** 7.79 / 4.76 ≈ **1-2 Developers**
- **Cost (USD):** 7.79 * $10,000 = **$77,900**
- **Cost (INR):** $77,900 * ₹83.50 ≈ **₹65,04,650**

## 4. Summary & Conclusion

| Mode | Effort (Person-Months) | Time (Months) | Staffing | Cost (USD) | Cost (INR) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Organic** | 4.77 | 4.53 | 1 Developer | $47,700 | ₹39,82,950 |
| **Semi-Detached** | 6.19 | 4.73 | 1-2 Developers | $61,900 | ₹51,68,650 |
| **Embedded** | 7.79 | 4.76 | 1-2 Developers | $77,900 | ₹65,04,650 |

Based on the actual size of the codebase (~1.91 KLOC) and USA developer market rates, the MenstrualTracker App most closely aligns with the **Organic** model, requiring approximately **4.5 months** for a **solo developer**, at an estimated cost of **$47,700 USD (₹39.8 Lakhs)**. Scaling it to an **Embedded** model (e.g., rigid compliance, proprietary systems) would increase the required effort to just over **7.8 Person-Months**, raising the cost to **$77,900 USD (₹65 Lakhs)**.
