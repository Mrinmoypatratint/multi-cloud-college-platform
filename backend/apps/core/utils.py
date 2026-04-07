from rest_framework.response import Response
from rest_framework import status

def api_response(data=None, message="Success", errors=None, status_code=status.HTTP_200_OK, success=True):
    """
    Standardized API response helper.
    """
    return Response(
        {
            "success": success,
            "message": message,
            "data": data if data is not None else {},
            "errors": errors if errors is not None else {}
        },
        status=status_code
    )
