from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('firms', FirmViewSet)
router.register('clients', ClientViewSet)
router.register('matters', MatterViewSet)
router.register('documents', DocumentViewSet)
router.register('time-entries', TimeEntryViewSet)
router.register('invoices', InvoiceViewSet)
router.register('invoice-items', InvoiceItemViewSet)
router.register('payments', PaymentViewSet)
router.register('tasks', TaskViewSet)
router.register('notes', NoteViewSet)
router.register('events', EventViewSet)
router.register('messages', MessageViewSet)
router.register('notifications', NotificationViewSet)
router.register('activity-logs', ActivityLogViewSet)

urlpatterns = router.urls
