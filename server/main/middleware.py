from django.http import HttpResponse

class AuthMidleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_request(self, request):
        print("=========================")
        return HttpResponse("test only")

        try:
            request.session['django_language'] = request.META['HTTP_HOST'].split('.')[0]
        except KeyError:
            pass