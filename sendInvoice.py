from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from requests import Session
from zeep import Client
from zeep.transports import Transport
import zipfile
import io 
import hashlib
import config

user , sifre, vk = config.foriba_test_api.values()

session = Session()
session.auth = HTTPBasicAuth(user , sifre)
 
client = Client('https://earsivwstest.fitbulut.com/ClientEArsivServicesPort.svc?singleWsdl',          
            transport=Transport(session=session)) 

uuid = '61dc8ace-00ae-40ad-a1e8-13d52f22c324'


with zipfile.ZipFile(uuid + '.zip', 'w') as zf:
    zf.write(uuid + '.xml')

binaryData = None
with open(uuid + '.zip', 'rb') as f:
    binaryData = f.read()
     
hashed = hashlib.md5(binaryData).hexdigest()
ns1 = client.type_factory('ns1')
ns0 = client.type_factory('ns0')

params = ns1.CustomizationParam('BRANCH','default')
output = ns0.ResponsiveOutput('XML')
#result = client.service.sendInvoice(vk,'1111111111','XML',uuid + '.zip',hashed,binaryData,params,output)
print(result)
#print(history.last_sent)
#print(history.last_received)
 

 

