from flask import Flask, jsonify, make_response, request
from markupsafe import escape
from datetime import datetime
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from requests import Session
from zeep import Client
from zeep.transports import Transport
import zipfile
import io 
import os
from uuid import uuid4
from lxml import etree
import datetime
import hashlib 
from UBL_TR import EUBL21 
import config 
from requests.adapters import HTTPAdapter, Retry
import logging
    

user, sifre, vk = config.foriba_test_api.values()

app = Flask(__name__)
logging.basicConfig(filename='error.log',level=logging.ERROR) 

session = Session()
retry = Retry(total=5, read=5, connect=5, backoff_factor=0.3, status_forcelist=(500, 502, 503, 504), method_whitelist=False)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter) 
session.auth = HTTPBasicAuth(user, sifre)
client = Client('ClientEArsivServicesPort.wsdl', transport=Transport(session=session))


@app.route("/ping")
def ping():
    """Ping servisi"""
    now = datetime.datetime.now()
    return now.strftime("%A, %d %B, %Y at %X")

@app.route("/user_lists")
def get_user_list():
    """E-Fatura müşteri listesini döner"""
    user_lists = []
    result = client.service.getUserList(vk)

    data = None
    with zipfile.ZipFile(io.BytesIO(result)) as zf:
        data = zf.read('GIBPKUsers.xml')

    data = etree.fromstring(data)

    for elem in data.iter('{http:/fitcons.com/earchive/getuserlist}identifier'):    
        user_lists.append(elem.text)
    return jsonify(user_lists)

@app.route("/fatura/<uuid:fatura_id>")
def getInvoiceDocument(fatura_id):    
    fat_id = str(fatura_id)
    try:
        result = client.service.getInvoiceDocument(fat_id, vk, None, 'PDF')        
        response = make_response(result.binaryData)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = \
            'inline; filename=%s.pdf' % fat_id
        return response
    except Exception as e:
        data = {'hata': e.message}
        return data, 404

@app.route("/fatura_imzali/<uuid:fatura_id>")
def getSignedInvoice(fatura_id):
    fat_id = str(fatura_id)
    try:
        result = client.service.getSignedInvoice(fat_id, vk) 
        response = make_response(result.binaryData)
        response.headers['Content-Type'] = 'application/xml' 
        response.headers['Content-Disposition'] = \
            'inline; filename=%s.xml' % fat_id      
        return response 
    except Exception as e:
        data = {'hata': e.message}
        return data, 404

@app.route('/fatura', methods=['POST'])
def send_invoice(): 
    content = request.get_json(silent=true)
    xml = EUBL21(**content).get_invoice()
    
    with zipfile.ZipFile(uuid + '.zip', 'w') as zf:
        zf.writestr(uuid + '.xml',xml)

    binaryData = None
    with open(uuid + '.zip', 'rb') as f:
        binaryData = f.read()
        
    hashed = hashlib.md5(binaryData).hexdigest()
    ns1 = client.type_factory('ns1')
    ns0 = client.type_factory('ns0')

    params = ns1.CustomizationParam('BRANCH','default')
    output = ns0.ResponsiveOutput('XML')
    output = None
    try:
        result = client.service.sendInvoice(vk,'1111111111','XML',uuid + '.zip',hashed,binaryData,params,output) 
        os.remove(uuid + '.zip')      
        return {
            'Detail': result.Detail,
            'UUID':  result.preCheckErrorResults.preCheckError[0].UUID and 'deneem',
            'InvoiceNumber': result.preCheckErrorResults.preCheckError[0].InvoiceNumber and 'deneem',   
        }   
    except Exception as e:
        data = {'hata': str(e)}
        return data, 404

@app.route('/fatura_test', methods=['POST'])
def fatura_test():    
    content = request.get_json(silent=True) 
    xml = str(EUBL21(**content))  
    return xml


if __name__ == "__main__":
    # https://stackoverflow.com/questions/58261464/how-to-host-python-3-7-flask-application-on-windows-server 
    app.run(host='0.0.0.0', ssl_context='adhoc')
 