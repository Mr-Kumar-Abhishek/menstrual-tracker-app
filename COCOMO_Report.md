# COCOMO Estimation Report: MenstrualTracker App

This document outlines the Constructive Cost Model (COCOMO) estimations for the MenstrualTracker App across all three development modes: **Organic**, **Semi-Detached**, and **Embedded**.

## 1. Estimated Lines of Code (LOC)
- **Estimated Size:** 5,000 Lines of Code (5 KLOC)
*(Note: This is an estimated count of the core application files, excluding virtual environments and external dependencies).*

## 2. Basic COCOMO Constants

| Mode | a | b | c | d |
| :--- | :--- | :--- | :--- | :--- |
| **Organic** | 2.4 | 1.05 | 2.5 | 0.38 |
| **Semi-Detached** | 3.0 | 1.12 | 2.5 | 0.35 |
| **Embedded** | 3.6 | 1.20 | 2.5 | 0.32 |

## 3. Calculations

We assume an average developer salary of **₹1,00,000 per month** for the cost calculations.

Formulas:
- **Effort (Person-Months):** `Effort = a * (KLOC)^b`
- **Development Time (Months):** `Time = c * (Effort)^d`
- **Required Team Size (Persons):** `Staffing = Effort / Time`
- **Total Estimated Cost (INR):** `Cost = Effort * Average Monthly Salary`

### 3.1 Organic Mode
*Appropriate for small teams, familiar environments, and well-understood requirements.*

- **Effort:** 2.4 * (5)^1.05 ≈ **13.0 Person-Months**
- **Time:** 2.5 * (13.0)^0.38 ≈ **6.5 Months**
- **Staffing:** 13.0 / 6.5 ≈ **2 Developers**
- **Cost:** 13.0 * ₹1,00,000 = **₹13,00,000** (13 Lakhs INR)

### 3.2 Semi-Detached Mode
*Appropriate for medium-sized teams, mixed experience levels, and somewhat rigid requirements.*

- **Effort:** 3.0 * (5)^1.12 ≈ **18.2 Person-Months**
- **Time:** 2.5 * (18.2)^0.35 ≈ **6.9 Months**
- **Staffing:** 18.2 / 6.9 ≈ **3 Developers**
- **Cost:** 18.2 * ₹1,00,000 = **₹18,20,000** (18.2 Lakhs INR)

### 3.3 Embedded Mode
*Appropriate for complex projects with strict constraints, rigid requirements, and specialized hardware/software.*

- **Effort:** 3.6 * (5)^1.20 ≈ **24.8 Person-Months**
- **Time:** 2.5 * (24.8)^0.32 ≈ **7.0 Months**
- **Staffing:** 24.8 / 7.0 ≈ **4 Developers**
- **Cost:** 24.8 * ₹1,00,000 = **₹24,80,000** (24.8 Lakhs INR)

## 4. Summary & Conclusion

| Mode | Effort (Person-Months) | Time (Months) | Staffing | Cost (INR) |
| :--- | :--- | :--- | :--- | :--- |
| **Organic** | 13.0 | 6.5 | 2 Developers | ₹13,00,000 |
| **Semi-Detached** | 18.2 | 6.9 | 3 Developers | ₹18,20,000 |
| **Embedded** | 24.8 | 7.0 | 4 Developers | ₹24,80,000 |

While the MenstrualTracker App most closely aligns with the **Organic** model due to its straightforward nature and small team requirements, scaling it to a **Semi-Detached** or **Embedded** level (e.g., integrating strictly with proprietary medical hardware or stringent HIPAA compliance systems) would significantly increase the effort, team size, and cost to upwards of **₹24.8 Lakhs INR**.
