# 📚 Complex Book Shop System (Enterprise E-commerce)

A high-scale, feature-rich e-commerce platform for books tailored for the Bangladeshi market (inspired by Rokomari/Wafilife/Amazon). This system is designed to handle complex logistics, manual payment verification, dynamic promotions, and multi-warehouse inventory management.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-5.0-green?style=for-the-badge&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?style=for-the-badge&logo=postgresql)
![MeiliSearch](https://img.shields.io/badge/MeiliSearch-v1.6-orange?style=for-the-badge&logo=meilisearch)

## 🚀 Key Features

### 📦 Advanced Logistics & Shipping
- **Zone-Based Shipping:** Different rates for Inside Dhaka, Sub-Dhaka, Outside Dhaka.
- **Weight-Based Calculation:** Tiered pricing (e.g., 0-500g: 60tk, 500g-1kg: 70tk).
- **Overweight Charges:** Automatic calculation for heavy parcels.
- **Courier Integration:** Pathao, Steadfast API hooks.

### 💰 Payment & Wallet System
- **Manual Verification:** Verify Bkash/Nagad payments via Transaction ID & SMS Webhooks.
- **User Wallet:** Store credit system for refunds and advance payments.
- **Partial Refunds:** Handle complex return scenarios efficiently.

### 🏭 Inventory & Warehouse
- **Multi-Warehouse:** Track stock across different locations (Banglabazar, Nilkhet, etc.).
- **Purchase Orders:** Manage supplier procurement and stock intake.
- **Stock Logs:** Full audit trail of every inventory movement.

### 🏷️ Dynamic Promotions (Offer Engine)
- **BOGO:** Buy One Get One Free.
- **Bundle Discounts:** Special pricing for book sets (e.g., Humayun Ahmed Collection).
- **Tiered Discounts:** "Buy 5000tk+ get 10% off".

### 👥 User Management
- **Mobile Auth:** Registration via Phone Number (Bangladeshi standard).
- **Segmentation:** Auto-tagging users (VIP, Inactive, New) for targeted marketing.
- **Affiliate System:** User referral links and commission tracking.

## 🛠️ Technology Stack

- **Backend:** Django + Django REST Framework (DRF)
- **Database:** PostgreSQL (Production), SQLite (Dev)
- **Search Engine:** MeiliSearch (Ultra-fast search)
- **Frontend:** Next.js (Planned)
- **Task Queue:** Celery + Redis (Planned)

## 📂 Project Structure

```
backend/
├── users/          # Auth & Customer Segmentation
├── catalog/        # Books, Authors, Publishers, Bundles
├── orders/         # Order Workflow, Returns, Pre-orders
├── logistics/      # Shipping Zones & Rates
├── inventory/      # Warehouses, Suppliers, POs
├── payments/       # Transactions, Wallets, Coupons
├── promotions/     # Dynamic Offer Engine
└── marketing/      # Affiliate System
```

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
