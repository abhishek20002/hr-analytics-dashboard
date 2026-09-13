"""
HR Analytics Project - Human Resources Data Set (HRDataset_v14)
Step 1: Data Cleaning + Exploratory Data Analysis (EDA)

Isse chalane ke liye: python3 01_hr_clean_and_eda.py
Requires: pandas, matplotlib, seaborn (pip install pandas matplotlib seaborn --break-system-packages)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# ---------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------
df = pd.read_csv("HRDataset_v14.csv")
print("Original shape:", df.shape)

# ---------------------------------------------------------
# 2. CLEANING
# ---------------------------------------------------------

# Convert date columns
df["DateofHire"] = pd.to_datetime(df["DateofHire"], format="%m/%d/%Y", errors="coerce")
df["DateofTermination"] = pd.to_datetime(df["DateofTermination"], format="%m/%d/%Y", errors="coerce")
df["DOB"] = pd.to_datetime(df["DOB"], format="%m/%d/%y", errors="coerce")
# Fix any DOB parsed into the future (2-digit year quirk, e.g. '65 -> 2065 instead of 1965)
df.loc[df["DOB"].dt.year > 2020, "DOB"] = df.loc[df["DOB"].dt.year > 2020, "DOB"] - pd.DateOffset(years=100)

# DateofTermination is NaN for active employees - this is expected, not an error
# ManagerID is NaN for the top executive - expected too

# Feature engineering
df["HireYear"] = df["DateofHire"].dt.year
df["Age"] = ((pd.Timestamp("2018-01-01") - df["DOB"]).dt.days / 365.25).round().astype("Int64")
df["IsActive"] = df["EmploymentStatus"] == "Active"

# Sanity checks
print("\nMissing values (DateofTermination and ManagerID nulls are expected):")
print(df.isnull().sum()[df.isnull().sum() > 0])
print("Duplicate rows:", df.duplicated().sum())

# Save cleaned dataset - this is what SQL/Tableau will use
df.to_csv("hr_cleaned.csv", index=False)
print("\nSaved cleaned file: hr_cleaned.csv")
print("Cleaned shape:", df.shape)

# ---------------------------------------------------------
# 3. EXPLORATORY DATA ANALYSIS
# ---------------------------------------------------------

# --- Q1: Headcount overview ---
print("\nEmployment status breakdown:")
print(df["EmploymentStatus"].value_counts())
print(f"\nActive: {df['IsActive'].sum()} ({df['IsActive'].mean()*100:.0f}%)")
print(f"Terminated: {(~df['IsActive']).sum()} ({(~df['IsActive']).mean()*100:.0f}%)")

# --- Q2: Headcount by department ---
dept_counts = df["Department"].value_counts()
print("\nHeadcount by department:")
print(dept_counts)

plt.figure(figsize=(9, 5))
dept_counts.plot(kind="barh", color="steelblue")
plt.gca().invert_yaxis()
plt.xlabel("Number of Employees")
plt.title("Headcount by Department")
plt.tight_layout()
plt.savefig("chart_headcount_by_department.png", dpi=150)
plt.close()

# --- Q3: Attrition rate by department ---
attrition_by_dept = df.groupby("Department")["IsActive"].apply(lambda x: (1 - x.mean()) * 100).sort_values(ascending=False)
print("\nAttrition rate (%) by department:")
print(attrition_by_dept.round(1))

plt.figure(figsize=(9, 5))
attrition_by_dept.plot(kind="barh", color="darkorange")
plt.gca().invert_yaxis()
plt.xlabel("Attrition Rate (%)")
plt.title("Attrition Rate by Department")
plt.tight_layout()
plt.savefig("chart_attrition_by_department.png", dpi=150)
plt.close()

# --- Q4: Performance score distribution ---
perf_counts = df["PerformanceScore"].value_counts()
print("\nPerformance score distribution:")
print(perf_counts)

plt.figure(figsize=(8, 5))
perf_counts.plot(kind="bar", color="seagreen")
plt.ylabel("Number of Employees")
plt.title("Employee Performance Score Distribution")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig("chart_performance_score.png", dpi=150)
plt.close()

# --- Q5: Recruitment source effectiveness ---
recruitment_counts = df["RecruitmentSource"].value_counts()
print("\nEmployees by recruitment source:")
print(recruitment_counts)

plt.figure(figsize=(9, 5))
recruitment_counts.plot(kind="barh", color="purple")
plt.gca().invert_yaxis()
plt.xlabel("Number of Employees")
plt.title("Employees by Recruitment Source")
plt.tight_layout()
plt.savefig("chart_recruitment_source.png", dpi=150)
plt.close()

# --- Q6: Salary by department ---
salary_by_dept = df.groupby("Department")["Salary"].mean().sort_values(ascending=False)
print("\nAverage salary by department:")
print(salary_by_dept.round(0))

# --- Q7: Employee satisfaction distribution ---
plt.figure(figsize=(7, 5))
sns.countplot(x="EmpSatisfaction", data=df, color="teal")
plt.xlabel("Employee Satisfaction Score (1-5)")
plt.ylabel("Number of Employees")
plt.title("Employee Satisfaction Distribution")
plt.tight_layout()
plt.savefig("chart_satisfaction_distribution.png", dpi=150)
plt.close()

# --- Q8: Gender diversity ---
print("\nGender breakdown:")
print(df["Sex"].value_counts())

# --- Q9: Marital status breakdown ---
print("\nMarital status breakdown:")
print(df["MaritalDesc"].value_counts())

print("\nEDA complete. 5 charts saved as PNG files.")
print("Next step: load 'hr_cleaned.csv' into SQL for deeper querying.")
