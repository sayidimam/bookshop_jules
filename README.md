# 📚 Complex Book Shop System (Enterprise E-commerce)

A high-scale, feature-rich e-commerce platform for books tailored for the Bangladeshi market (inspired by Rokomari/Wafilife/Amazon). This system is designed to handle complex logistics, manual payment verification, dynamic promotions, and multi-warehouse inventory management.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-5.0-green?style=for-the-badge&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?style=for-the-badge&logo=postgresql)
![MeiliSearch](https://img.shields.io/badge/MeiliSearch-v1.6-orange?style=for-the-badge&logo=meilisearch)

## 🚀 Key Features

### 🛒 Automated Product Scraping
- **Wafilife Scraper:** Automatically fetch book details (Title, Author, Price, Cover Image) from Wafilife URLs using JSON-LD parsing.
- **Admin Integration:** Simply paste a URL in the admin panel to populate your inventory.

### 📦 Logistics & Order Workflow (Data Ocean)
- **Complex Statuses:** Detailed tracking from `Lead/Incomplete` -> `Confirmed` -> `Collecting` -> `Packing` -> `RTS` -> `Shipped`.
- **Zone-Based Shipping:** Auto-calculates fees based on Division (Inside Dhaka/Sub-Dhaka/Outside) and Weight (e.g., +20tk per extra kg).
- **Courier Auditing:** Track finances (`Expected vs Received COD`) and manage multiple accounts (Pathao/Steadfast).

### 💰 Payment & Tracking
- **Smart SMS Verification:** Matches incoming manual payment SMS (Bkash/Nagad) with customer Order ID for auto-verification.
- **Server-Side Tracking:** Configurable Pixel/CAPI events (`Purchase`) fired either on **Checkout** or **Confirmation**.
- **SMS Notifications:** Integration with **Greenweb API** to send order updates.

### 🏭 Inventory & Warehouse
- **Multi-Warehouse:** Track stock across different locations (Banglabazar, Nilkhet).
- **Collector Tasks:** Assign procurement lists to agents in the field.
- **Internal Logs:** Track damages, gifts, and internal consumption.

### 👥 User & Auth
- **OTP Login:** Secure phone-number based login/registration.
- **Role Management:** Separate dashboards for Admin, Collector, and Packer.

## 🛠️ Technology Stack

- **Backend:** Django + Django REST Framework (DRF)
- **Authentication:** Djoser + SimpleJWT (OTP support)
- **Database:** PostgreSQL (Production), SQLite (Dev)
- **Search:** MeiliSearch Ready
- **Integrations:** Pathao, Steadfast, Greenweb SMS, SSLCommerz

## 📂 System Modules

| Module | Description |
| :--- | :--- |
| `users` | Auth (OTP), Roles, Customer Segmentation |
| `catalog` | Books, Scraper Service, Bundles, Categories |
| `orders` | Complex Workflow, Weight-based Shipping Calc |
| `logistics` | Courier Integration, Shipping Rates, Ledgers |
| `payments` | Transactions, Smart Verification, Wallets |
| `integrations`| External Clients (Greenweb, Pathao, Steadfast) |
| `analytics` | Server-Side Tracking Signals, User Activity |
| `communications`| Notification Logs |

## 🗺️ Project Roadmap

### ✅ Phase 1: Database Architecture (Completed)
- [x] Core Models (User, Book, Order)
- [x] Logistics & Inventory Schema

### ✅ Phase 2: Logic & Integrations (Completed)
- [x] Wafilife Scraper Service
- [x] Greenweb SMS Integration
- [x] Tracking Signal Logic

### ✅ Phase 3: API Development (Completed)
- [x] **Auth:** `/api/auth/otp/send/` & `/api/auth/otp/verify/`
- [x] **Catalog:** `/api/catalog/books/` & `/api/catalog/scrape/`
- [x] **Orders:** `/api/orders/checkout/` (Calculates Shipping)
- [x] **Payments:** `/api/payments/verify/` (Manual TrxID Match)

## ⚡ Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/bookshop_jules.git
   cd bookshop_jules
   ```

2. **Setup Backend:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create Superuser:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run Server:**
   ```bash
   python manage.py runserver
   ```

## 📝 Documentation
For detailed architecture and workflow diagrams, please refer to [AGENTS.md](AGENTS.md).

---
*Built with ❤️ by Jules.*
