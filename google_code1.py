from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://mail.google.com/']

flow = InstalledAppFlow.from_client_secrets_file(
    './client_secret_80603762808-o1751ha984pfuhpgpqb39dfbqdt83fac.apps.googleusercontent.com.json',SCOPES)

creds = flow.run_local_server(port=0)

with open('token.json','w') as token:
    token.write(creds.to_json())