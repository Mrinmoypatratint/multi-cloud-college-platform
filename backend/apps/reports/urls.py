from django.urls import path
from apps.reports.views import HealthCheckView, DashboardStatsView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('dashboard/', DashboardStatsView.as_view(), name='dashboard-stats'),
]
