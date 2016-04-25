def default_handler(request, response):
    response.body = {'greetings': 'hello world'}
    return response
