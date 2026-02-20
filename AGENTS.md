# Complex Book Shop System - Developer Guide

## Project Overview
This project is a high-scale e-commerce platform for books (similar to Rokomari/Wafilife) tailored for the Bangladeshi market. It features complex order management, shipping logic, and manual payment verification.

## Technology Stack
- **Backend:** Django + Django REST Framework (DRF)
- **Database:** PostgreSQL (Production), SQLite (Dev/Fallback)
- **Search:** MeiliSearch (Planned integration)
- **Frontend:** Next.js (Planned)

## App Structure & Key Models

### 1. Users (`backend/users`)
- **`User`**: Custom user model using **Mobile Number** as the primary identifier.
- **Roles**: Admin, Customer, Collector, Packer, Courier Manager.
- **Tracking**: Fields for Server-Side Tracking (`fbp`, `fbc`).

### 2. Catalog (`backend/catalog`)
- **`Book`**: Core product. Has M2M relations with `Author`, `Category`, `Tag`.
    - `is_bundle`: Boolean to mark bundle products.
- **`BundleItem`**: Links component books to a bundle product.
- **`BookImage`**: Multiple images per book.
- **`Publisher`**: Publisher details.

### 3. Logistics (`backend/logistics`)
- **`ShippingZone`**: Inside Dhaka, Sub Dhaka, Outside Dhaka, etc.
- **`ShippingRate`**: Tiered pricing (e.g., 0-1kg = 60tk).
- **`OverweightCharge`**: Incremental pricing (e.g., +20tk per extra kg).
- **`Courier`**: Pathao, Steadfast, etc.

### 4. Orders (`backend/orders`)
- **`Order`**: Central model with status workflow (`CONFIRMED` -> `DELIVERED`).
    - **Indices**: Composite index on `status` + `created_at` for fast dashboard queries.
- **`ReturnRequest` & `ReturnItem`**: Handles partial/full returns with reasons (Damaged, Mind Changed, etc.).
- **`OrderStatusHistory`**: Audit log for status changes.

### 5. Inventory (`backend/inventory`)
- **`Supplier`**: Vendor management.
- **`PurchaseOrder` & `PurchaseItem`**: Track procurement from suppliers.
- **`StockLog`**: Audit trail for all stock movements (Sale, Purchase, Return, Adjustment).

### 6. Payments (`backend/payments`)
- **`Transaction`**: Records payments (Manual or Gateway).
- **`Wallet` & `WalletTransaction`**: Store credit system for refunds and advance deposits.
- **Manual Verification**: Supports Transaction ID matching and SMS Webhook logs.

## Critical Workflows

### Order Processing Flow
1.  **Customer** places order -> Status: `INCOMPLETE` / `QUEUE`.
2.  **Admin** confirms order -> Status: `CONFIRMED`.
3.  **System** moves to Fulfillment -> Status: `PENDING`.
4.  **Collector** gets list -> Status: `COLLECTING`.
5.  **Packer** packs items -> Status: `PACKING` -> `RTS`.
6.  **Courier** picks up -> Status: `SHIPPED`.
7.  **Customer** receives -> Status: `DELIVERED`.

### Return & Refund Flow
1.  **Customer** requests return via UI.
2.  **Admin** approves `ReturnRequest`.
3.  **Logistics** collects item -> `StockLog` (Return In).
4.  **Finance** processes refund -> Credit to `Wallet` or reversed transaction.

### Shipping Calculation Logic
1.  Determine `ShippingZone` based on Customer's District/Thana.
2.  Calculate Total Weight of Order.
3.  Check `ShippingRate` for the zone and weight tier.
4.  If weight exceeds max tier, apply `OverweightCharge`.

## Setup Instructions
1.  **Database**: The system is configured to use PostgreSQL if `DB_NAME` env var is present. Otherwise, it defaults to SQLite.
2.  **Migrations**: Run `python manage.py migrate`.
3.  **Superuser**: Run `python manage.py createsuperuser`.

## Next Steps
- Implement DRF Serializers and Views.
- Connect MeiliSearch indexing signals.
- Build Next.js Frontend.
