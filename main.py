#!/usr/bin/python

def application(env, response):

    path_info = env['PATH_INFO'].split('/')
    query_str = env['QUERY_STRING'].split('?')
    while '' in path_info:
        path_info.remove('')
    while '' in query_str:
        query_str.remove('')
    print(str(path_info))
    print(str(query_str))

    response('200 OK', [('Content-Type', 'text/html')])
    return "success"

