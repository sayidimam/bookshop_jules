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
- **`BookImage`**: Multiple images per book.
- **`Publisher`**: Publisher details.

### 3. Logistics (`backend/logistics`)
- **`ShippingZone`**: Inside Dhaka, Sub Dhaka, Outside Dhaka, etc.
- **`ShippingRate`**: Tiered pricing (e.g., 0-1kg = 60tk).
- **`OverweightCharge`**: Incremental pricing (e.g., +20tk per extra kg).
- **`Courier`**: Pathao, Steadfast, etc.

### 4. Orders (`backend/orders`)
- **`Order`**: Central model.
    - **Status Workflow**: `CONFIRMED` -> `PENDING` -> `COLLECTING` -> `PACKING` -> `RTS` -> `SHIPPED` -> `DELIVERED`.
    - **Snapshot**: Stores shipping address and price snapshot to preserve history.
- **`OrderItem`**: Links Order to Book.
- **`OrderStatusHistory`**: Tracks all status changes (audit log).

### 5. Payments (`backend/payments`)
- **`Transaction`**: Records payments (Manual or Gateway).
- **`PaymentMethod`**: Configurable methods (Bkash, Nagad, etc.).
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

### Shipping Calculation Logic
1.  Determine `ShippingZone` based on Customer's District/Thana.
2.  Calculate Total Weight of Order.
3.  Check `ShippingRate` for the zone and weight tier.
4.  If weight exceeds max tier, apply `OverweightCharge` (Base Rate + (Excess Weight * Rate per Unit)).

### Payment Verification
- Users can input TrxID.
- System receives SMS via Webhook (stored in `raw_data`).
- Admin or Automator matches TrxID/Sender Number to verify payment.

## Setup Instructions
1.  **Database**: The system is configured to use PostgreSQL if `DB_NAME` env var is present. Otherwise, it defaults to SQLite.
2.  **Migrations**: Run `python manage.py migrate`.
3.  **Superuser**: Run `python manage.py createsuperuser`.

## Next Steps
- Implement DRF Serializers and Views.
- Connect MeiliSearch indexing signals.
- Build Next.js Frontend.
