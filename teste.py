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
            print(lead, '++++++++++++++++')
        except FacebookRequestError as e:
            return False

        lead_data = lead.get("field_data", None)
        for data in lead_data:
            if data.get("name", None) in ["e-mail", "email", "E-mail", 'EMAIL']:
                email = data.get("values")[0]
            if data.get("name", None) in ["Nome completo", "Nome_completo", 'FULL_NAME']:
                name = data.get("values")[0]
            if data.get("name", None) in ["Telefone", 'PHONE']:
                tell = data.get("values")[0]
        result =  {'email': email.strip().lower(), 'name': name.strip().lower(), 'phone': tell.strip().lower()}
        
        if result:
            return result
        return False


if __name__ == '__main__':
    data = {
        "entry": [
            {"id": "101924702815843",
             "time": 1675083559,
             "changes": [
                 {"value": {
                     "created_time": 1675083559,
                     "leadgen_id": "901173494350265",
                     "page_id": "101924702815843",
                     "form_id": "1863551417331169"},
                  "field": "leadgen"
                  }
             ]}
        ],
        "object": "page"
    }
    entry = data.get("entry", None)
    for data in entry:
        changes = data["changes"]
        for change in changes:
            leadgen_id = change["value"]["leadgen_id"]
            print(leadgen_id)
            lead_email = FacebookLeadAds().get_lead(str(leadgen_id))
            print(lead_email)
