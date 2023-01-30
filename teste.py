from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.lead import Lead
from facebook_business.exceptions import FacebookRequestError
from decouple import config
import requests

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
            if data.get("name", None) in ["Nome completo", "Nome_completo"]:
                name = data.get("values")[0]
            if data.get("name", None) in ["Telefone"]:
                tell = data.get("values")[0]
                return {'email': email.strip().lower(), 'name': name.strip().lower(), 'tell': tell.strip().lower()}
        return False


    
   
if __name__ == '__main__':
    lead = FacebookLeadAds()
    print(lead.get_lead_email(lead_id='532486685526415'))