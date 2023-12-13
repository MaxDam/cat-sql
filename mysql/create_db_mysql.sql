CREATE DATABASE mydb;
use mydb;


CREATE TABLE employees (
    emp_no      INT             NOT NULL,
    birth_date  DATE            NOT NULL,
    first_name  VARCHAR(14)     NOT NULL,
    last_name   VARCHAR(16)     NOT NULL,
    gender      CHAR(1)         NOT NULL CHECK (gender IN ('M', 'F')),    
    hire_date   DATE            NOT NULL,
    PRIMARY KEY (emp_no)
);

CREATE TABLE departments (
    dept_no     CHAR(4)         NOT NULL,
    dept_name   VARCHAR(40)     NOT NULL,
    PRIMARY KEY (dept_no)
);

CREATE TABLE dept_manager (
    emp_no      INT             NOT NULL,
    dept_no     CHAR(4)         NOT NULL,
    from_date   DATE            NOT NULL,
    to_date     DATE            NOT NULL,
    FOREIGN KEY (emp_no) REFERENCES employees (emp_no) ON DELETE CASCADE,
    FOREIGN KEY (dept_no) REFERENCES departments (dept_no) ON DELETE CASCADE,
    PRIMARY KEY (emp_no, dept_no)
); 

CREATE TABLE dept_emp (
    emp_no      INT             NOT NULL,
    dept_no     CHAR(4)         NOT NULL,
    from_date   DATE            NOT NULL,
    to_date     DATE            NOT NULL,
    FOREIGN KEY (emp_no) REFERENCES employees (emp_no) ON DELETE CASCADE,
    FOREIGN KEY (dept_no) REFERENCES departments (dept_no) ON DELETE CASCADE,
    PRIMARY KEY (emp_no, dept_no)
);

CREATE TABLE titles (
    emp_no      INT             NOT NULL,
    title       VARCHAR(50)     NOT NULL,
    from_date   DATE            NOT NULL,
    to_date     DATE,
    FOREIGN KEY (emp_no) REFERENCES employees (emp_no) ON DELETE CASCADE,
    PRIMARY KEY (emp_no, title, from_date)
); 

CREATE TABLE salaries (
    emp_no      INT             NOT NULL,
    salary      INT             NOT NULL,
    from_date   DATE            NOT NULL,
    to_date     DATE            NOT NULL,
    FOREIGN KEY (emp_no) REFERENCES employees (emp_no) ON DELETE CASCADE,
    PRIMARY KEY (emp_no, from_date)
);

INSERT INTO employees VALUES
    (1, '1990-01-01', 'John', 'Doe', 'M', '2020-01-01'),
    (2, '1992-05-15', 'Jane', 'Smith', 'F', '2020-02-15'),
    (3, '1985-08-20', 'Michael', 'Johnson', 'M', '2019-12-10');

INSERT INTO departments VALUES
    ('HR', 'Human Resources'),
    ('IT', 'Information Technology'),
    ('SALE', 'Sales');

INSERT INTO dept_manager VALUES
    (1, 'HR', '2020-01-01', '2021-01-01'),
    (2, 'IT', '2020-02-15', '2021-02-15'),
    (3, 'SALE', '2019-12-10', '2020-12-10');

INSERT INTO dept_emp VALUES
    (1, 'HR', '2020-01-01', '2021-01-01'),
    (2, 'IT', '2020-02-15', '2021-02-15'),
    (3, 'SALE', '2019-12-10', '2020-12-10');

INSERT INTO titles VALUES
    (1, 'Manager', '2020-01-01', NULL),
    (2, 'Developer', '2020-02-15', NULL),
    (3, 'Sales Representative', '2019-12-10', NULL);

INSERT INTO salaries VALUES
    (1, 80000, '2020-01-01', '2021-01-01'),
    (2, 70000, '2020-02-15', '2021-02-15'),
    (3, 75000, '2019-12-10', '2020-12-10');
