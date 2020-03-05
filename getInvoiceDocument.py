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

 
result = client.service.getInvoiceDocument('c99a79fb-151e-4abb-82de-8d9dfa831ee9','0510294989',None, 'HTML')

print('UUID: ', result.UUID,'Hash: ', result.Hash, 'invoiceNumber: ', result.invoiceNumber,'StatusCode: ', result.StatusCode)
print(result.binaryData.decode('utf8'))