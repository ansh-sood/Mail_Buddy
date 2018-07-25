from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from future.standard_library import install_aliases

install_aliases()

from django.http import HttpResponse
from django.shortcuts import render
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError



import json
import os

from flask import Flask
from flask import request
from flask import make_response

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import google.oauth2.credentials
import google_auth_oauthlib.flow



def processRequest(request):
    SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
    store = file.Storage('/home/ansh/PycharmProjects/cfd/gmail/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('/home/ansh/PycharmProjects/cfd/gmail/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    GMAIL = build('gmail', 'v1', http=creds.authorize(Http()))

    threads = GMAIL.users().threads().list(userId='me').execute().get('threads', [])
    i = 0
    sub = list()
    for thread in threads:
        if i > 9:
            break
        i += 1

        tdata = GMAIL.users().threads().get(userId='me', id=thread['id']).execute()
        nmsgs = len(tdata['messages'])

        if nmsgs > 0:
            msg = tdata['messages'][0]['snippet']
            jj = tdata['messages'][0]['payload']
            for header in jj['headers']:
                if (header['name'] == 'From'):
                    sub.append(header['value'])
                if (header['name'] == 'Date'):
                    sub.append(header['value'])
                if (header['name'] == 'Subject'):
                    sub.append(header['value'])

            if msg:
                print('%s (%d msgs)' % (msg, nmsgs))
                sub.append(msg)
    print(sub)
    print(sub)
    return render(request, 'home.html', {'sub': sub})
