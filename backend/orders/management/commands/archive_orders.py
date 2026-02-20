from django.core.management.base import BaseCommand
from django.utils import timezone
from orders.models import Order
# from orders.models_archive import OrderArchive

class Command(BaseCommand):
    help = 'Archives orders older than 2 years to a separate table.'

    def handle(self, *args, **options):
        # cutoff_date = timezone.now() - timezone.timedelta(days=730)
        # old_orders = Order.objects.filter(created_at__lt=cutoff_date)

        # logic to move data to OrderArchive and delete from Order

        self.stdout.write(self.style.SUCCESS('Successfully archived orders (Mock Implementation)'))
