from base64 import b64encode
import requests
import json

USERNAME = 'sylvan.gidayajr@lexisnexisrisk.com'
PASSWORD = 'AnyaGia@2022'
BASE_URL = 'https://jira.rsi.lexisnexis.com'


class JiraAPI():
    def __init__(self):
        self.username = USERNAME
        self.password = PASSWORD
        self.base_url = BASE_URL
        self.auth_token = basic_auth(username=USERNAME, 
                                       password=PASSWORD)
        self.headers = {
            'Authorization':f'Basic {self.auth_token}'
        }
        pass

    def _get_issue_details(self):
        payload = {}
        request_url = f'{self.base_url}/rest/servicedeskapi/request'
        response = requests.request("GET", 
                                    url=request_url, 
                                    headers=self.headers, 
                                    data=payload)
        results = json.loads(response.text)
        return results
        
def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return token

def main():
    jira_api = JiraAPI()
    request_details = jira_api._get_issue_details()
    print(request_details)

if __name__ == "__main__":
    main()
