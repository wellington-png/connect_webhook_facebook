from django.conf import settings
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.lead import Lead
from facebook_business.exceptions import FacebookRequestError
from rest_framework.views import APIView
from rest_framework.response import Response
from decouple import config
# from .models import Lead
from django.http import HttpResponse

class FacebookLeadAds:
    access_token = config('FACEBOOK_PAGE_ACCESS_TOKEN')
    app_secret = config('FACEBOOK_APP_SECRET')
    app_id = config('FACEBOOK_APP_ID')

    def __init__(self):
        FacebookAdsApi.init(
            access_token=self.access_token, app_secret=self.app_secret, app_id=self.app_id
        )

    def get_lead(self, lead_id):
        try:
            lead = Lead(lead_id).api_get()
        except FacebookRequestError as e:
            return False

        lead_data = lead.get("field_data", None)

        for data in lead_data:
            if data.get("name", None) in ["e-mail", "email", "E-mail"]:
                email = data.get("values")[0]
            if data.get("name", None) in ["Nome completo", "Nome_completo", 'nome_completo', 'nome completo']:
                name = data.get("values")[0]
            if data.get("name", None) in ["Telefone", 'telefone', 'phone', 'numero', 'phone_number']:
                tell = data.get("values")[0]
                return {'email': email.strip().lower(), 'name': name.strip().lower(), 'phone': tell.strip().lower()}
        return False

        return False

class FacebookWebhook(APIView):
    def get(self, request):
        """Necessary for webhook url validation from Facebook"""
        verify_token = request.GET.get("hub.verify_token", "")
        if verify_token != "MyVerificationToken":
            return Response("Wrong verification token", status=403)
        return Response(int(request.GET.get("hub.challenge", 0)))

    def post(self, request):
        entry = request.data.get("entry", None)
        for data in entry:
            changes = data["changes"]
            for change in changes:
                leadgen_id = change["value"]["leadgen_id"]
                print(leadgen_id)

                lead_email = FacebookLeadAds().get_lead(str(leadgen_id))
                print(lead_email)
                if not lead_email:
                    return Response({"success": False})
        return Response({"success": True})


def get_lead(request):
    return HttpResponse('HEllo word', status=200)
