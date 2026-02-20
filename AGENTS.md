# Complex Book Shop System - Developer Guide

## Project Overview
This project is a high-scale e-commerce platform for books (similar to Rokomari/Wafilife) tailored for the Bangladeshi market. It features complex order management, shipping logic, dynamic promotions, and manual payment verification.

## Technology Stack
- **Backend:** Django + Django REST Framework (DRF)
- **Database:** PostgreSQL (Production), SQLite (Dev/Fallback)
- **Search:** MeiliSearch (Planned integration)
- **Frontend:** Next.js (Planned)

## App Structure & Key Models

### 1. Users (`backend/users`)
- **`User`**: Custom user model using **Mobile Number** as the primary identifier.
- **Roles**: Admin, Customer, Collector, Packer, Courier Manager.
- **User Segmentation**: `UserTag` for categorizing users (VIP, Inactive, etc.).
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
- **`CollectorTask`**: Assign procurement tasks to collectors (Market/Shop specific).

### 4. Orders (`backend/orders`)
- **`Order`**: Central model with status workflow (`CONFIRMED` -> `DELIVERED`).
    - **Indices**: Composite index on `status` + `created_at` for fast dashboard queries.
- **`ReturnRequest` & `ReturnItem`**: Handles partial/full returns.
- **`PreOrder`**: Advance booking system for upcoming books.
- **`Subscription`**: Recurring book plans (e.g., Monthly Book Box).

### 5. Inventory (`backend/inventory`)
- **`Supplier`**: Vendor management.
- **`PurchaseOrder`**: Procurement tracking.
- **`Warehouse` & `StockItem`**: Multi-location inventory tracking.
    - `is_virtual_stock`: Flag for Just-in-Time (JIT) market stock.
    - `last_sold_at`: To identify Dead Stock.
- **`StockLog`**: Audit trail for all stock movements (Purchase, Sale, Damage, Internal).
- **`DamageLog`**: Track wasted/damaged books with reasons.
- **`InternalConsumption`**: Track books taken by staff/admin.

### 6. Promotions (`backend/promotions`)
- **`Offer`**: Dynamic pricing engine (BOGO, Tiered Discount).
- **`OfferCondition`**: Logic rules (e.g., Min Qty > 2, Specific Category).
- **`OfferReward`**: Benefits (e.g., Free Item, 10% Off).

### 7. Marketing (`backend/marketing`)
- **`AffiliateProgram`**: Manage commission rates.
- **`AffiliateLink`**: Track user referrals.
- **`AffiliateCommission`**: Calculate earnings per order.

### 8. Payments (`backend/payments`)
- **`MobilePaymentLog`**: Buffer table for raw SMS messages from Bkash/Nagad.
- **`Transaction`**: Records verified payments. Links to `MobilePaymentLog` for audit.
- **`Wallet`**: User store credit system.

### 9. Social & Community (`backend/social`)
- **`Review`**: User product reviews with verified purchase check.
- **`Question` & `Answer`**: Q&A platform for products.
- **`UserCollection`**: Public/Private user wishlists.

### 10. Communications (`backend/communications`)
- **`NotificationLog`**: Track SMS/Email delivery status.
- **`MessageTemplate`**: Manage dynamic message content.

### 11. Analytics (`backend/analytics`)
- **`UserActivity`**: Track user clicks, views, and cart actions.
- **`SearchTerm`**: Monitor popular search queries.

### 12. Integrations (`backend/integrations`)
- **Pathao Courier**: Full OAuth 2.0 integration for order creation, store management, and price calculation.
- **Steadfast Courier**: API wrapper for creating orders and checking status.
- **Manual SMS Webhook**: Endpoint `/api/integrations/sms-webhook/` to receive and auto-match payment SMS.
- **SSLCommerz**: Library integration for payment gateway.

## Critical Workflows

### Manual Payment Verification (Smart Auto-Match)
1.  **SMS Received**: Gateway app forwards SMS to webhook -> Saved in `MobilePaymentLog`.
2.  **User Input**: Customer enters TrxID on frontend.
3.  **Auto Match**: System searches `MobilePaymentLog` for TrxID.
    - If found: Marks as claimed, links to `Transaction`, updates Order to `CONFIRMED`.
    - If not found: Keeps transaction `PENDING` until SMS arrives (late arrival handling).

### Warehouse Selection & JIT
1.  **Order Placement**: System checks `StockItem` across active `Warehouse`s.
2.  **Virtual Stock**: If item not in warehouse but `is_virtual_stock` is True -> Assign `CollectorTask`.
3.  **Allocation**: Assigns order to the nearest warehouse with sufficient stock.

## Setup Instructions
1.  **Database**: The system is configured to use PostgreSQL if `DB_NAME` env var is present. Otherwise, it defaults to SQLite.
2.  **Migrations**: Run `python manage.py migrate`.
3.  **Superuser**: Run `python manage.py createsuperuser`.

## Next Steps
- Implement DRF Serializers and Views.
- Connect MeiliSearch indexing signals.
- Build Next.js Frontend.
