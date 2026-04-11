from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.timetable.models import TimetableSlot
from apps.timetable.serializers import TimetableSlotSerializer
from apps.users.permissions import IsCollegeAdmin

class TimetableSlotViewSet(viewsets.ModelViewSet):
    queryset = TimetableSlot.objects.all().order_by('day_of_week', 'start_time')
    serializer_class = TimetableSlotSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['day_of_week', 'subject', 'faculty', 'section']
    search_fields = ['subject__code', 'subject__name', 'room_number', 'section']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsCollegeAdmin()]
        return [permissions.IsAuthenticated()]
