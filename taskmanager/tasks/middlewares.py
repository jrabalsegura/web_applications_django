import time
import logging

logger = logging.getLogger(__name__)
class RequestTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()
        request_time = end_time - start_time
        
        logger.info(f'Request to {request.path} took {request_time:.2f} seconds')
        
        return response