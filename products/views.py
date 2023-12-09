from rest_framework.decorators import api_view
from rest_framework.response import Response

import environ

env = environ.Env()
environ.Env.read_env()


@api_view(['GET'])
def getRoutes(request):
    routes = [
        f'{env("BASE")}/products',
        f'{env("BASE")}/products/new-product/',
        f'{env("BASE")}/products/delete-product/',
    ]
    return Response(routes)
