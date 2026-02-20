# 📚 Complex Book Shop System (Enterprise E-commerce)

A high-scale, feature-rich e-commerce platform for books tailored for the Bangladeshi market (inspired by Rokomari/Wafilife/Amazon). This system is designed to handle complex logistics, manual payment verification, dynamic promotions, and multi-warehouse inventory management.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-5.0-green?style=for-the-badge&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?style=for-the-badge&logo=postgresql)
![MeiliSearch](https://img.shields.io/badge/MeiliSearch-v1.6-orange?style=for-the-badge&logo=meilisearch)

## 🚀 Key Features

### 📦 Logistics & Financial Accounting (Advanced)
- **Multi-Account Support:** Manage multiple accounts for Pathao, Steadfast, RedX simultaneously.
- **Audit & Reconciliation:** Automatically track `Expected COD` vs `Received COD`.
- **Dispute Management:** System flags lost parcels or overcharged delivery fees for dispute resolution.
- **Zone-Based Shipping:** Complex weight-based calculation (e.g., 0-500g: 60tk, +1kg: 20tk).

### 💰 Payment & Wallet System
- **Smart Manual Verification:** Auto-match incoming Bkash/Nagad SMS via Webhook. Users only need to provide TrxID.
- **User Wallet:** Store credit system for refunds and advance payments.
- **SSLCommerz:** Integrated payment gateway for automated online payments.

### 🏭 Inventory & Warehouse
- **Multi-Warehouse:** Track stock across different locations (Banglabazar, Nilkhet).
- **Collector Workflow:** Assign specific procurement tasks (`CollectorTask`) to field agents.
- **Internal Consumption:** Track books taken by staff/admin (Gift, Review Copy, Damaged).
- **Stock Logs:** Full audit trail of every movement (Purchase, Sale, Return, Damage).

### 🏷️ Dynamic Promotions & Social
- **Offer Engine:** BOGO, Bundle Discounts, Tiered Pricing (Buy 5k get 10% off).
- **Affiliate System:** User referral links and commission tracking.
- **Reviews & Q&A:** Verified purchase reviews and question-answer forum.
- **Public Collections:** Users can create and share book lists.

### 👥 User Management
- **Mobile Auth:** Registration via Phone Number (Bangladeshi standard).
- **Segmentation:** Auto-tagging users (VIP, Inactive, New) for targeted marketing.

## 🛠️ Technology Stack

- **Backend:** Django + Django REST Framework (DRF)
- **Database:** PostgreSQL (Production), SQLite (Dev)
- **Search Engine:** MeiliSearch (Ultra-fast search)
- **Integrations:** Pathao API, Steadfast API, SSLCommerz, SMS Gateway
- **Frontend:** Next.js (Planned)

## 📂 System Modules

| Module | Description |
| :--- | :--- |
| `users` | Auth, Roles (Admin/Collector/Packer), Segmentation |
| `catalog` | Books, Authors, Bundles, Categories |
| `orders` | Order Workflow (Incomplete -> Delivered), Returns, Pre-orders |
| `logistics` | Courier Integration, Shipping Rates, Financial Auditing |
| `inventory` | Warehouses, Suppliers, Stock Logs, Damage Tracking |
| `payments` | Transactions, Wallets, Coupons, Mobile Payment Logs |
| `integrations`| External API Clients (Steadfast, Pathao, SSLCommerz) |
| `promotions` | Dynamic Offer Engine |
| `marketing` | Affiliate System |
| `social` | Reviews, Q&A, Collections |
| `analytics` | User Activity Tracking, Search Logs |
| `communications`| SMS/Email Notification Logs |

## 🗺️ Project Roadmap

### ✅ Phase 1: Database Architecture (Completed)
- [x] Core Models (User, Book, Order)
- [x] Complex Shipping Logic
- [x] Payment Models

### ✅ Phase 2: Advanced Logic & Integrations (Completed)
- [x] Multi-Warehouse Inventory & Collector Tasks
- [x] Logistics Accounting (Ledgers, Disputes)
- [x] Smart SMS Verification (MobilePaymentLog)
- [x] Courier API Clients (Pathao, Steadfast)
- [x] Social Features (Reviews, Q&A)

### 🔜 Phase 3: API Development (Next Steps)
- [ ] DRF Serializers & ViewSets
- [ ] Authentication API (JWT/Token)
- [ ] Public Catalog API with Search
- [ ] Cart & Checkout API

### 🔜 Phase 4: Frontend Development
- [ ] Next.js Project Setup
- [ ] UI Components & Pages

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
