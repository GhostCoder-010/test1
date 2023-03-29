from rest_framework.views import APIView, Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .serializers import *
from .functions import *


class CompanyCheck(APIView):
    authentication_classes = []
    permission_classes = [AllowAny,]

    def get(self, request):
        if check_company_exist():
            return Response(
                {
                    'success': True,
                    'data': {'exist': True},
                    'message': 'Access Denied',
                    'errors': 'Company already exist'
                }
            )

        return Response(
            {
                'success': True,
                'data': {'exist': False},
                'message': 'Company Details doesn\'t exist, Please create company account',
                'errors': 'Company doesn\'t exist'
            }
        )

# Create your views here.
