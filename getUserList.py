from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from requests import Session
from zeep import Client
from zeep.transports import Transport 
import zipfile
import io 
from lxml import etree

session = Session()
 
client = Client('https://earsivwstest.fitbulut.com/ClientEArsivServicesPort.svc?singleWsdl',
                 transport=Transport(session=session)) 

 
result = client.service.getUserList('0510294989')

data = None
with zipfile.ZipFile(io.BytesIO(result)) as zf:
    data = zf.read('GIBPKUsers.xml')

data = etree.fromstring(data)

for elem in data.iter('{http:/fitcons.com/earchive/getuserlist}identifier'):    
    print(elem.text) 
        
