from django.shortcuts import redirect

class AdminChecker:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.path.startswith('myadmin'):
            if not request.user.is_authenticated:
                return redirect('myadmin')
            if not request.user.is_staff:
                return redirect('myadmin_home')
            
        response          = self.get_response(request)

        return response 