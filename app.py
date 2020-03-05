from flask  import Flask, jsonify
from datetime import datetime

from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from requests import Session
from zeep import Client
from zeep.transports import Transport 
import zipfile
import io 
from lxml import etree
import config

app = Flask(__name__)

user , sifre, vk = config.foriba_test_api.values()
session = Session()
session.auth = HTTPBasicAuth(user , sifre) 
client = Client('ClientEArsivServicesPort.wsdl',          
            transport=Transport(session=session)) 


@app.route("/ping")
def ping():
    now = datetime.now()
    return  now.strftime("%A, %d %B, %Y at %X")


@app.route("/user_lists")
def get_user_list():
    user_lists = []
    result = client.service.getUserList(vk)

    data = None
    with zipfile.ZipFile(io.BytesIO(result)) as zf:
        data = zf.read('GIBPKUsers.xml')

    data = etree.fromstring(data)

    for elem in data.iter('{http:/fitcons.com/earchive/getuserlist}identifier'):    
        user_lists.append(elem.text)
    return jsonify(user_lists)

@app.route("/fatura")
def fatura():
    res = client.service.getInvoiceDocument('3ad35815-86a7-445a-8aa0-5486092964bd',vk,None, 'HTML')
    return jsonify(res)




 
    
   
   