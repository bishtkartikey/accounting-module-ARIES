
# Odoo Custom Modules – ARIES Internship

## 📌 Introduction

This repository contains the work I completed during my internship at **ARIES (Aryabhatta Research Institute of Observational Sciences)** as part of the Odoo development team.

The primary goal was to **automate and improve internal workflows** at ARIES by developing custom modules for:

* Medical reimbursement
* Financial tracking
* IT infrastructure management

Odoo ERP was chosen to streamline these administrative functions, reduce paperwork, and ensure greater transparency across departments.

---

## 🛰 About ARIES

ARIES is a **premier research institute in observational astronomy**. Along with its scientific activities, ARIES manages a wide range of administrative processes, including HR, reimbursements, IT asset management, and financial tracking.

By integrating Odoo as an ERP system, ARIES was able to:

* Digitize paper-based workflows
* Speed up approval cycles
* Maintain accurate records with transparency

---

## ⚙️ Overview of Odoo ERP System

**Odoo** is an **open-source ERP platform** that integrates multiple business applications such as inventory, accounting, HR, and project management.

For this project, I worked primarily with:

* **Python-based Odoo framework**
* **PostgreSQL database**

The focus was on building **custom modules** to address ARIES-specific workflows.

---

## 🖥 Setting up the Odoo Environment

### 🔹 Odoo Installation

* **Operating System:** Ubuntu
* **Python & Dependencies:** Installed libraries like `python-dev`, `libxml2-dev`, `libxslt-dev`, etc.
* **PostgreSQL Configuration:** Configured for handling ERP data requirements.
* **Odoo Instance:** Created a virtual environment for development.

### 🔹 Odoo Module Structure

Each Odoo module typically includes:

* `__init__.py` → Initializes the module
* `__manifest__.py` → Contains metadata
* `models/` → Business logic & database models
* `views/` → XML files for UI
* `security/` → Access control & permissions

---

## 🛠️ Custom Modules Developed

### 1️⃣ Hospital Reimbursement Module

Automates the medical reimbursement process for ARIES employees.

**Key Features:**

* Employee claim submission (name, designation, treatment details, hospital info)
* Expenditure tracking (amount paid, advance, medicines, dosage, costs)
* Approval workflow (real-time approval status & comments)
* Reports for admins to monitor claims

✅ **Impact:** Reduced processing time & improved transparency in reimbursements.

---

### 2️⃣ Accounts Module

Focused on automating financial transactions related to reimbursements.

**Core Features:**

* Billing details (bill number, amount paid, approved amount)
* Payment tracking (bank transfer, cheque, etc.)
* Invoice management linked to reimbursements
* Audit trail for transparency in financial records

✅ **Impact:** Enabled better financial oversight with accurate tracking.

---

### 3️⃣ IT Infrastructure Management Module

Designed for managing ARIES’ hardware and software assets.

**Features:**

#### 🖥 Desktop Model

* **Technical Details:** OS, Product ID, Processor, RAM, IP address, department, location
* **Credentials:** User ID, Username
* **Warranty Tracking:** Purchase date, warranty period, expiration, remaining time
* **Commercial Details:** Source document number, issued to employee, supplier details
* **Supplier Information:** Contact details, website, OEM info
* **Maintenance History:** Record of repairs and servicing

✅ **Impact:** Centralized IT asset tracking and efficient maintenance management.

---

## 🚀 Key Learnings

* Setting up and configuring an Odoo ERP development environment
* Designing **modular ERP applications** with Python and PostgreSQL
* Implementing **workflows, approvals, and financial records** in Odoo
* Enhancing **administrative efficiency** through digital transformation

---

## 📂 Repository Structure

```
odoo_custom_modules/
│── hospital_reimbursement/
│   ├── __init__.py
│   ├── __manifest__.py
│   ├── models/
│   ├── views/
│   └── security/
│
│── accounts_module/
│   ├── __init__.py
│   ├── __manifest__.py
│   ├── models/
│   ├── views/
│   └── security/
│
│── it_infrastructure_management/
│   ├── __init__.py
│   ├── __manifest__.py
│   ├── models/
│   ├── views/
│   └── security/
```

---

## 🏁 Conclusion

This internship allowed me to gain hands-on experience in **ERP development using Odoo** while solving real-world administrative challenges at ARIES.

By building these custom modules, ARIES was able to:

* Speed up reimbursement approvals
* Ensure financial transparency
* Manage IT infrastructure efficiently

