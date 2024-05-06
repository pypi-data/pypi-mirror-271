from rest_framework.routers import DefaultRouter

from django_audit_events.views import AuditEventViewSet

router = DefaultRouter()
router.register(r"events", AuditEventViewSet)

urlpatterns = router.urls
