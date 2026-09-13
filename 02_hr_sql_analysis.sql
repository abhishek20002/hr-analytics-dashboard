-- =========================================================
-- HR Analytics Project - Human Resources Data Set
-- Step 2: SQL Schema + Business Analysis Queries
-- Database: MySQL / PostgreSQL compatible
-- =========================================================

-- ---------------------------------------------------------
-- 1. CREATE TABLE
-- ---------------------------------------------------------
DROP TABLE IF EXISTS hr_employees;

CREATE TABLE hr_employees (
    employee_name           VARCHAR(150),
    emp_id                  INT PRIMARY KEY,
    salary                  DECIMAL(12,2),
    termd                   INT,
    position                VARCHAR(100),
    state                   VARCHAR(10),
    zip                     VARCHAR(10),
    dob                     DATE,
    sex                     VARCHAR(5),
    marital_desc            VARCHAR(50),
    citizen_desc            VARCHAR(50),
    hispanic_latino         VARCHAR(10),
    race_desc               VARCHAR(50),
    date_of_hire            DATE,
    date_of_termination     DATE,
    term_reason             VARCHAR(150),
    employment_status       VARCHAR(50),
    department              VARCHAR(100),
    manager_name            VARCHAR(100),
    recruitment_source      VARCHAR(100),
    performance_score       VARCHAR(50),
    engagement_survey       DECIMAL(4,2),
    emp_satisfaction        INT,
    special_projects_count  INT,
    days_late_last30        INT,
    absences                INT,
    hire_year               INT,
    age                     INT,
    is_active               BOOLEAN
);

-- ---------------------------------------------------------
-- 2. LOAD DATA
-- ---------------------------------------------------------
-- MySQL:
-- LOAD DATA LOCAL INFILE 'hr_cleaned.csv'
-- INTO TABLE hr_employees
-- FIELDS TERMINATED BY ',' ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;

-- PostgreSQL:
-- \copy hr_employees FROM 'hr_cleaned.csv' WITH (FORMAT csv, HEADER true);

-- Note: only the relevant columns from hr_cleaned.csv are listed above;
-- adjust the column list in your LOAD/COPY statement to match the actual CSV header order.

-- ---------------------------------------------------------
-- 3. BUSINESS ANALYSIS QUERIES
-- ---------------------------------------------------------

-- Q1: Headcount and attrition rate by department
SELECT
    department,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN employment_status = 'Active' THEN 1 ELSE 0 END) AS active_employees,
    SUM(CASE WHEN employment_status != 'Active' THEN 1 ELSE 0 END) AS terminated_employees,
    ROUND(100.0 * SUM(CASE WHEN employment_status != 'Active' THEN 1 ELSE 0 END) / COUNT(*), 1) AS attrition_rate_pct
FROM hr_employees
GROUP BY department
ORDER BY attrition_rate_pct DESC;

-- Q2: Average salary by department and position
SELECT
    department,
    position,
    COUNT(*) AS num_employees,
    ROUND(AVG(salary), 0) AS avg_salary
FROM hr_employees
GROUP BY department, position
ORDER BY avg_salary DESC;

-- Q3: Performance score distribution by department
SELECT
    department,
    performance_score,
    COUNT(*) AS num_employees
FROM hr_employees
GROUP BY department, performance_score
ORDER BY department, num_employees DESC;

-- Q4: Recruitment source effectiveness (volume + average performance)
SELECT
    recruitment_source,
    COUNT(*) AS num_hires,
    ROUND(AVG(emp_satisfaction), 2) AS avg_satisfaction,
    ROUND(AVG(engagement_survey), 2) AS avg_engagement,
    SUM(CASE WHEN employment_status != 'Active' THEN 1 ELSE 0 END) AS terminated_count
FROM hr_employees
GROUP BY recruitment_source
ORDER BY num_hires DESC;

-- Q5: Reasons for termination (top exit reasons)
SELECT
    term_reason,
    COUNT(*) AS num_employees
FROM hr_employees
WHERE employment_status != 'Active'
GROUP BY term_reason
ORDER BY num_employees DESC;

-- Q6: Employee satisfaction vs performance score
SELECT
    performance_score,
    ROUND(AVG(emp_satisfaction), 2) AS avg_satisfaction,
    ROUND(AVG(engagement_survey), 2) AS avg_engagement,
    COUNT(*) AS num_employees
FROM hr_employees
GROUP BY performance_score
ORDER BY avg_satisfaction DESC;

-- Q7: Gender pay gap check by department
SELECT
    department,
    sex,
    COUNT(*) AS num_employees,
    ROUND(AVG(salary), 0) AS avg_salary
FROM hr_employees
GROUP BY department, sex
ORDER BY department, sex;

-- Q8: Absenteeism and late arrivals by department
SELECT
    department,
    ROUND(AVG(absences), 1) AS avg_absences,
    ROUND(AVG(days_late_last30), 1) AS avg_days_late
FROM hr_employees
GROUP BY department
ORDER BY avg_absences DESC;

-- Q9: Hiring trend by year
SELECT
    hire_year,
    COUNT(*) AS num_hires
FROM hr_employees
GROUP BY hire_year
ORDER BY hire_year;

-- Q10: Marital status and gender diversity breakdown
SELECT
    marital_desc,
    sex,
    COUNT(*) AS num_employees
FROM hr_employees
GROUP BY marital_desc, sex
ORDER BY marital_desc, sex;
