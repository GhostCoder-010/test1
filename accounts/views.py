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
        
        
class CompanyRegister(APIView):
    authentication_classes = []
    permission_classes = [AllowAny, ]

    def post(self, request):
        company_name = request.data.get('company_name')
        username = request.data.get('username')
        password = request.data.get('password')
        mobile = request.data.get('mobile')
        email = request.data.get('email')
        logo = request.FILES.get('logo')

        if check_company_exist():

            return Response(
                {
                    'success': False,
                    'data': None,
                    'message': 'Company Details already exist, Please login with your company credentials',
                    'errors': 'Company already exist'
                }
            )

        user = User.objects.create_user(
            name=company_name,
            username=username,
            password=password,
            mobile=mobile,
            email=email,
            fk_role='company',
        )
        user_serializer = UserSerializer(user)

        company = CompanyProfile.objects.create(
            company_name=company_name,
            email=email,
            mobile=mobile,
            fkAdmin=user,
            logo = logo
        )
        company_serializer = CompanyProfileSerializer(company)

        data = {
            'company': company_serializer.data,
            'user': user_serializer.data
        }

        return Response(
            {
                'success': True,
                'data': data,
                'message': 'Company Details created successfully ',
                'errors': None
            }
        )

# Create your views here.
