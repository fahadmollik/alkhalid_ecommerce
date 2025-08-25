from django.utils import timezone
from datetime import timedelta
from .models import UserVisit, OnlineUser

class UserTrackingMiddleware:
    """Middleware to track user visits and online users"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip tracking for certain request types
        if self.should_skip_tracking(request):
            response = self.get_response(request)
            return response
        
        # Track visit and online users only for relevant requests
        try:
            # Track visit
            self.track_visit(request)
            
            # Update online users
            self.track_online_user(request)
        except Exception:
            # If database operations fail, continue without blocking the request
            pass
        
        response = self.get_response(request)
        return response

    def should_skip_tracking(self, request):
        """Determine if we should skip tracking for this request"""
        # Skip media files, static files, and admin requests
        skip_paths = ['/media/', '/static/', '/favicon.ico']
        
        # Skip if it's a media or static file request
        for skip_path in skip_paths:
            if request.path.startswith(skip_path):
                return True
        
        # Skip AJAX requests to avoid excessive tracking
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return True
            
        return False

    def track_visit(self, request):
        """Track daily unique visits per session"""
        if not request.session.session_key:
            request.session.create()
        
        session_key = request.session.session_key
        ip_address = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
        page_visited = request.path
        
        # Create visit record (unique per session per day)
        UserVisit.objects.get_or_create(
            session_key=session_key,
            date=timezone.now().date(),
            defaults={
                'ip_address': ip_address,
                'user_agent': user_agent,
                'page_visited': page_visited,
            }
        )

    def track_online_user(self, request):
        """Track currently online users"""
        if not request.session.session_key:
            request.session.create()
        
        session_key = request.session.session_key
        ip_address = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
        current_page = request.path
        
        # Update or create online user record
        OnlineUser.objects.update_or_create(
            session_key=session_key,
            defaults={
                'ip_address': ip_address,
                'user_agent': user_agent,
                'current_page': current_page,
                'last_activity': timezone.now(),
            }
        )
        
        # Clean up old online users (inactive for more than 5 minutes)
        # Only do cleanup occasionally to reduce database load
        import random
        if random.randint(1, 20) == 1:  # 5% chance to run cleanup
            cutoff_time = timezone.now() - timedelta(minutes=5)
            OnlineUser.objects.filter(last_activity__lt=cutoff_time).delete()

    def get_client_ip(self, request):
        """Get the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip or '127.0.0.1'
