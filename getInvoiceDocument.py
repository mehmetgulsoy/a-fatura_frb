from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from requests import Session
from zeep import Client
from zeep.transports import Transport 
import zipfile
import io 
from lxml import etree
import config

user , sifre, vk = config.foriba_test_api.values()

session = Session()
session.auth = HTTPBasicAuth(user , sifre)

client = Client('https://earsivwstest.fitbulut.com/ClientEArsivServicesPort.svc?singleWsdl',
                 transport=Transport(session=session))
 
result = client.service.getInvoiceDocument('c99a79fb-151e-4abb-82de-8d9dfa831ee9',vk,None, 'HTML')

print('UUID: ', result.UUID,'Hash: ', result.Hash, 'invoiceNumber: ', result.invoiceNumber,'StatusCode: ', result.StatusCode)
print(result.binaryData.decode('utf8'))