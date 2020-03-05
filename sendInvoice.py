from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from requests import Session
from zeep import Client
from zeep.transports import Transport 
import zipfile
import io
import os 
import hashlib
import datetime
import config
import UBL_TR

user , sifre, vk = config.foriba_test_api.values()

session = Session()
session.auth = HTTPBasicAuth(user , sifre) 
client = Client('ClientEArsivServicesPort.wsdl',          
            transport=Transport(session=session)) 

uuid = '61765be6-f00a-4f27-97ae-c093c9fda14a'

data = {
    'ID':'KBN2019000000001',
    'UUID': '3ad35815-86a7-445a-8aa0-5486092964bd', 
    'InvoiceTypeCode': 'SATIS',
    'IssueDate': datetime.datetime.now().strftime('%Y-%m-%d'),
    'IssueTime': datetime.datetime.now().strftime('%H:%M:%S.%f%z'), 
    'InvoiceLines' : [{'part' : '123456',}],
    'Notes' : ['DENEME','DENEME2'],
    'DocumentCurrencyCode' : 'TRY',
    'AdditionalDocumentReferences': [{
        'ID' : '0100',
        'IssueDate' : '2020-01-20',
        'DocumentTypeCode': 'OUTPUT_TYPE'
        },{
        'ID' : 'ELEKTRONIK',
        'IssueDate' : '2020-01-20',
        'DocumentTypeCode': 'EREPSENDT'
        },    
    ],
    'Signatures' : [{
        'ID' : '3880718497',
        'WebsiteURI' : 'www.fitsolutions.com.tr',
        'Name' :'FIT DANISMANLIK VE TEKNOLOJI BILISIM HIZMETLERI A.S.',
        'PostalAddress' : {
            'Room' : '45',
            'StreetName': 'Öz Sokak',
            'BuildingName' : 'Gold Plaza',
            'BuildingNumber':'19',
            'CitySubdivisionName' : 'Altayçesme Mahellesi',
            'CityName' : 'ISTANBUL',
            'PostalZone' : '34843',
            'Region' : 'Marmara',
            'Country' : 'TÜRKİYE'
        },
        'Contact' : {
            'Telephone' : '0(216) 445 93 79',
            'Telefax' : '0(216) 445 92 87',
            'ElectronicMail' : 'muhasebe@fitcons.com',
        }
    }],
    'AccountingSupplierParty': {
        'WebsiteURI': 'www.alelma.com.tr',
        'ID' : '0510294989',
        'Name': 'ALELMA ELEKTRONİK PAZARLAMA VE SERVİS HİZMETLERİ TİC.LTD.ŞTİ',
        'PostalAddress' : {
            'Room' :'A',
            'StreetName' : 'ILGAZ',
            'BuildingNumber' : '37',
            'CitySubdivisionName' :'KARTAL',
            'CityName':'ISTANBUL',
            'PostalZone':'34600',
            'District':'ESENTEPE',
            'Country' :'TÜRKİYE',
        },
        'PartyTaxScheme' : {
            'Name' : 'İSTANBUL',
            'TaxTypeCode' : '34000'    
        }
    },
    'AccountingCustomerParty': {        
        'ID' : '31414819674',   
        'PostalAddress' : {
            'Room' :'A',
            'StreetName' : 'ILGAZ',
            'BuildingNumber' : '37',
            'CitySubdivisionName' :'KARTAL',
            'CityName':'ISTANBUL',
            'PostalZone':'34600',
            'District':'ELMALI',
            'Country' :'TÜRKİYE',
        },
        'PartyTaxScheme' : {
            'Name' : 'ANADOLU KURUMLAR VERGİ DAİRESİ BAŞ.',
            'TaxTypeCode' : '34244'    
        },
        'Contact':{
            'Telephone' : '0 (533) 390 78 09',
            'ElectronicMail': 'mehmet@liman.com.tr',    
        },
        'Person' : {
          'FirstName':'MEHMET', 
          'FamilyName' : '.',           
        }
    },
    'AllowanceCharge': {
        'ChargeIndicator' : 'false',
         'Amount' : '0',      
    },
    'TaxtTotal' : {
        'TaxAmount': '15',       
        'TaxSubtotal': {
            'TaxableAmount': '15',
            'TaxAmount' : '2.7',
             'CalculationSequenceNumeric': '1',
             'Percent': '18',
             'TaxCategory': {
                'TaxScheme': {
                    'Name' : 'KDV',
                    'TaxTypeCode': '0015'   
                }    
             }

        }

    },
    'LegalMonetaryTotal': {
        'LineExtensionAmount': '15',
        'TaxExclusiveAmount' : '15',
        'TaxInclusiveAmount' : '17.7',
        'AllowanceTotalAmount' : '0',
        'PayableAmount' : '17.7',    
    },
    'InvoiceLines': [{
        'ID': '1',
        'InvoicedQuantity': '1',       
        'LineExtensionAmount' : '15',        
        'unitCode':'C62',
        'Item' : {
            'Name' : '40048',
            'Description': 'deneme',
        },
        'PriceAmount' : '15',
    }]
}

xml = UBL_TR.EUBL21(**data).get_invoice()
 
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

result = client.service.sendInvoice(vk,'1111111111','XML',uuid + '.zip',hashed,binaryData,params,output)
print(result)
os.remove(uuid + '.zip')

#print(history.last_sent)
#print(history.last_received)
 

 

