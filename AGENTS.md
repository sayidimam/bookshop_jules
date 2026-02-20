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
- **`CollectorTask`**: Assign procurement tasks to collectors.
- **`CourierAccount`**: Manage multiple merchant accounts (e.g., Pathao Main, Steadfast Backup).
- **`CourierConsignment`**: Track financial status of each shipment (Expected vs Received COD).
- **`CourierLedger`**: Audit log for bulk payments from courier companies.
- **`CourierDispute`**: Track lost parcels or charge mismatches.

### 4. Orders (`backend/orders`)
- **`Order`**: Central model with status workflow (`CONFIRMED` -> `DELIVERED`).
    - **Indices**: Composite index on `status` + `created_at`.
    - **Lead Management**: `is_lead` flag for incomplete orders (phone captured).
    - **Queue System**: `QUEUE` status for high-traffic management.
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
- **Courier Webhook**: Endpoint `/api/integrations/courier-webhook/` for scalable real-time status updates.
- **SSLCommerz**: Library integration for payment gateway.

## Critical Workflows

### Scalability Strategy (100k Orders/Day)
1.  **Queue System**: Orders initially go to `QUEUE` status to prevent DB lock during high traffic. Background workers process them.
2.  **Webhook Tracking**: Instead of polling 100k orders, we use `CourierWebhookView` to receive updates *only* when status changes.
3.  **Search**: MeiliSearch handles catalog queries (millions of records) with <50ms latency.

### Automated Inventory & Returns
1.  **Return Request**: Admin marks as `COMPLETED`.
2.  **Auto Restock**: Signal triggers. If `GOOD` -> Stock increases. If `DAMAGED` -> DamageLog created.
3.  **Virtual Stock**: If item not in warehouse, `CollectorTask` is generated for JIT procurement.

### Manual Payment Verification (Smart Auto-Match)
1.  **SMS Received**: Gateway app forwards SMS to webhook -> Saved in `MobilePaymentLog`.
2.  **User Input**: Customer enters TrxID on frontend.
3.  **Auto Match**: System searches `MobilePaymentLog` for TrxID.
    - If found: Marks as claimed, links to `Transaction`, updates Order to `CONFIRMED`.
    - If not found: Keeps transaction `PENDING` until SMS arrives (late arrival handling).

## Setup Instructions
1.  **Database**: The system is configured to use PostgreSQL if `DB_NAME` env var is present. Otherwise, it defaults to SQLite.
2.  **Migrations**: Run `python manage.py migrate`.
3.  **Superuser**: Run `python manage.py createsuperuser`.

## Next Steps
- Implement DRF Serializers and Views.
- Connect MeiliSearch indexing signals.
- Build Next.js Frontend.
