from main.utils import create_basket


class BasketMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        basket = create_basket(request)
        setattr(request, 'basket', basket)
        response = self.get_response(request)
        return response
