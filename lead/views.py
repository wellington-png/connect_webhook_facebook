from django.conf import settings
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.lead import Lead
from facebook_business.exceptions import FacebookRequestError
from rest_framework.views import APIView
from rest_framework.response import Response
from decouple import config
from .models import Lead

class FacebookLeadAds:
    access_token = settings.FACEBOOK_PAGE_ACCESS_TOKEN
    app_secret = settings.FACEBOOK_APP_SECRET
    app_id = settings.FACEBOOK_APP_ID

    def __init__(self):
        FacebookAdsApi.init(
            access_token=self.access_token, app_secret=self.app_secret, app_id=self.app_id
        )

    def get_lead_email(self, lead_id):
        try:
            lead = Lead(lead_id).api_get()
        except FacebookRequestError as e:
            return False

        lead_data = lead.get("field_data", None)

        for data in lead_data:
            if data.get("name", None) in ["e-mail", "email"]:
                email = data.get("values")[0]
                return email.strip().lower()

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
        print('Post request received')
        for data in entry:
            changes = data["changes"]
            for change in changes:
                leadgen_id = change["value"]["leadgen_id"]

                lead_email = FacebookLeadAds().get_lead_email(leadgen_id)
                if not lead_email:
                    return Response({"success": False})

    
        return Response({"success": True})