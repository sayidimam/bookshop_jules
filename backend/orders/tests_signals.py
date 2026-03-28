from django.test import TestCase
from django.contrib.auth import get_user_model
from catalog.models import Book
from inventory.models_warehouse import Warehouse, StockItem
from inventory.models import StockLog
from inventory.models_internal import DamageLog
from orders.models import Order, OrderItem
from orders.models_return import ReturnRequest, ReturnItem
from decimal import Decimal

User = get_user_model()

class ReturnRequestSignalTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(phone_number="01700000000", password="password123")

        # Create a book
        self.book = Book.objects.create(
            title="Test Book",
            regular_price=Decimal("100.00"),
            stock=10
        )

        # Create a warehouse
        self.warehouse = Warehouse.objects.create(name="Main Warehouse")

        # Create stock for the book
        self.stock_item = StockItem.objects.create(
            warehouse=self.warehouse,
            book=self.book,
            quantity=10
        )

        # Create an order
        self.order = Order.objects.create(
            user=self.user,
            shipping_phone="01700000000",
            total_amount=Decimal("100.00"),
            status=Order.Status.DELIVERED
        )

        # Create an order item
        self.order_item = OrderItem.objects.create(
            order=self.order,
            book=self.book,
            quantity=2,
            price=Decimal("100.00")
        )

    def create_return_request(self, status=ReturnRequest.Status.PENDING):
        return ReturnRequest.objects.create(
            order=self.order,
            user=self.user,
            status=status,
            reason=ReturnRequest.Reason.DAMAGED
        )

    def add_item_to_return(self, return_request, quantity=1, condition='GOOD'):
        return ReturnItem.objects.create(
            return_request=return_request,
            order_item=self.order_item,
            quantity=quantity,
            condition=condition
        )

    def test_track_previous_status_new_instance(self):
        """Test that a new ReturnRequest instance has _previous_status as None."""
        return_req = self.create_return_request()
        self.assertIsNone(getattr(return_req, '_previous_status', None))

    def test_track_previous_status_existing_instance(self):
        """Test that an existing ReturnRequest instance captures its current status before update."""
        return_req = self.create_return_request(status=ReturnRequest.Status.PENDING)

        # Re-fetch from DB to simulate a fresh instance being loaded and then saved
        return_req = ReturnRequest.objects.get(id=return_req.id)
        return_req.status = ReturnRequest.Status.APPROVED
        return_req.save()

        self.assertEqual(getattr(return_req, '_previous_status'), ReturnRequest.Status.PENDING)

    def test_restock_good_condition_item(self):
        """Test that an item with GOOD condition is restocked when return status becomes COMPLETED."""
        return_req = self.create_return_request(status=ReturnRequest.Status.PENDING)
        self.add_item_to_return(return_req, quantity=2, condition='GOOD')

        initial_stock = self.stock_item.quantity # Should be 10

        # Change status to COMPLETED
        return_req.status = ReturnRequest.Status.COMPLETED
        return_req.save()

        # Check stock update
        self.stock_item.refresh_from_db()
        self.assertEqual(self.stock_item.quantity, initial_stock + 2)

        # Check StockLog creation
        self.assertTrue(StockLog.objects.filter(
            book=self.book,
            action=StockLog.Action.RETURN_IN,
            quantity=2,
            reference=f"Return #{return_req.id}"
        ).exists())

    def test_damage_log_for_damaged_item(self):
        """Test that a DamageLog is created for an item with DAMAGED condition when return status becomes COMPLETED."""
        return_req = self.create_return_request(status=ReturnRequest.Status.PENDING)
        self.add_item_to_return(return_req, quantity=1, condition='DAMAGED')

        initial_stock = self.stock_item.quantity

        # Change status to COMPLETED
        return_req.status = ReturnRequest.Status.COMPLETED
        return_req.save()

        # Check stock update (should NOT change for damaged items)
        self.stock_item.refresh_from_db()
        self.assertEqual(self.stock_item.quantity, initial_stock)

        # Check DamageLog creation
        self.assertTrue(DamageLog.objects.filter(
            book=self.book,
            quantity=1,
            reported_by=self.user
        ).exists())

    def test_no_double_restock_on_already_completed_return(self):
        """Test that re-saving a COMPLETED return request doesn't restock again."""
        return_req = self.create_return_request(status=ReturnRequest.Status.COMPLETED)
        self.add_item_to_return(return_req, quantity=2, condition='GOOD')

        # First restocking happens during creation if it's already COMPLETED (though normally created as PENDING)
        # But wait, our signal checks instance.id in track_previous_status.
        # If created as COMPLETED:
        # 1. pre_save: instance.id is None, _previous_status is None.
        # 2. post_save: status is COMPLETED, previous_status is None. COMPLETED != None -> Restocks.

        # Let's say it's already in DB and COMPLETED.
        return_req = ReturnRequest.objects.get(id=return_req.id)
        initial_stock = self.stock_item.quantity

        # Re-save it
        return_req.save()

        # Check stock update (should NOT change)
        self.stock_item.refresh_from_db()
        self.assertEqual(self.stock_item.quantity, initial_stock)

    def test_no_restock_on_non_completed_status(self):
        """Test that restocking does not occur for other status transitions."""
        return_req = self.create_return_request(status=ReturnRequest.Status.PENDING)
        self.add_item_to_return(return_req, quantity=2, condition='GOOD')

        initial_stock = self.stock_item.quantity

        # Change status to APPROVED
        return_req.status = ReturnRequest.Status.APPROVED
        return_req.save()

        # Check stock update (should NOT change)
        self.stock_item.refresh_from_db()
        self.assertEqual(self.stock_item.quantity, initial_stock)
