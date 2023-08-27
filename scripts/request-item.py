from __future__ import print_function

import os.path
import requests

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1aRM8-P40vTeRAhvyRsxbEcUIEKSmvP1HEnxU9NU31Yg'
SAMPLE_RANGE_NAME = 'Itens!A1:K80'


def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('../json/google-sheets-api/token.json'):
        creds = Credentials.from_authorized_user_file('../json/google-sheets-api/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../json/google-sheets-api/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('../json/google-sheets-api/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Obter informações da planilha.
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range="A3:A67").execute()
        dataSheet = result['values'];  ## Nome dos itens da planilha.

        def menorpreco(item):
            menor_preco = min(item, key=lambda d: d['valor'])['valor']
            return [ite for ite in item if ite['valor'] == menor_preco]

        api_url = 'https://serpapi.com/search.json?engine=google_shopping&q=Geladeira+Electrolux&location=Uberlandia,+Minas+Gerais,+Brazil&hl=pt&gl=br&api_key=41f64670fd12a5992c579f36ea06eed6f460e2631302a1d1c947c4fa5584c199'
        response = requests.get(api_url)
        slip = response.json()
        listaItens = []

        for i in slip["shopping_results"]:
            item = {
                "posicao": i["position"],
                "titulo": i["title"],
                "valor": i["extracted_price"],
                "link": i["link"]
            }
            listaItens.append(item)

        print(listaItens)
        menor_preco_items = menorpreco(listaItens)
        print(menor_preco_items)

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
