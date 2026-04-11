import json
from apps.audit.models import AuditLog

class AuditLogMiddleware:
    """
    Middleware to automatically record audit logs for mutating requests (POST, PUT, PATCH, DELETE).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Log mutating actions on /api/ endpoints
        if request.path.startswith('/api/') and request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            user = request.user if request.user.is_authenticated else None
            ip = self.get_client_ip(request)
            
            action_desc = f"{request.method} request to {request.path}"
            
            try:
                AuditLog.objects.create(
                    user=user,
                    ip_address=ip,
                    method=request.method,
                    path=request.path,
                    action=action_desc,
                    status_code=response.status_code,
                    details=f"Status: {response.status_code}"
                )
            except Exception:
                # Middleware logging should never break the request flow
                pass

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
