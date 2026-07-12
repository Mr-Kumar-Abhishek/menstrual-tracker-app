# COCOMO Estimation Report: MenstrualTracker App

This document outlines the Constructive Cost Model (COCOMO) estimations for the MenstrualTracker App.

## 1. Project Type: Organic
The project is considered **Organic** because it is a relatively small, straightforward mobile/desktop application developed by a small team with good experience in Python and KivyMD.

## 2. Estimated Lines of Code (LOC)
- **Estimated Size:** 5,000 Lines of Code (5 KLOC)
*(Note: This is an estimated count of the core Python application files, excluding virtual environments and external dependencies).*

## 3. Basic COCOMO Constants (Organic)
- **a** = 2.4
- **b** = 1.05
- **c** = 2.5
- **d** = 0.38

## 4. Calculations

### Effort (Person-Months)
Formula: `Effort = a * (KLOC)^b`
- `Effort = 2.4 * (5)^1.05`
- `Effort ≈ 13.0 Person-Months`

### Development Time (Months)
Formula: `Time = c * (Effort)^d`
- `Time = 2.5 * (13.0)^0.38`
- `Time ≈ 6.5 Months`

### Required Team Size (Persons)
Formula: `Staffing = Effort / Time`
- `Staffing = 13.0 / 6.5`
- `Staffing ≈ 2 Developers`

## 5. Conclusion
Based on the Basic COCOMO model, developing the MenstrualTracker App from scratch to its current feature set would take approximately **2 developers** working for about **6.5 months**, resulting in a total effort of **13.0 person-months**.
