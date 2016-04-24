def default_handler(request):
    response = 'HTTP/1.0 200 OK\r\nDate: Fri, 31 Dec 1999 23:59:59 GMT\r\nContent-Type: text/html\r\n' + \
               'Content-Length: 1354\r\n\r\nHello world'
    return response
