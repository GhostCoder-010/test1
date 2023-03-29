from .models import CompanyProfile


def check_company_exist():
    if CompanyProfile.objects.first():
        return True
    return False