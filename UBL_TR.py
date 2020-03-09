from lxml import etree 
import datetime

class EUBL21:
    """E-arşiv fatura UBL 2.1"""
    
    namespacemap={
        None : 'urn:oasis:names:specification:ubl:schema:xsd:Invoice-2',    
        'n4':'http://www.altova.com/samplexml/other-namespace',
        'xsi':'http://www.w3.org/2001/XMLSchema-instance',
        'cac':'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
        'cbc':'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2', 
        'ext':'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2',
    }

    def_para_brm = None
    
    def __init__(self, **kwargs):        
        CopyIndicator    = kwargs.get('CopyIndicator','false') 
        Notes            = kwargs.get('Notes',[])        
        IssueDate =  kwargs.get('IssueDate', datetime.datetime.now().strftime('%Y-%m-%d'))  
        IssueTime =  kwargs.get('IssueTime',datetime.datetime.now().strftime('%H:%M:%S.%f%z'))    
        AdditionalDocumentReferences = kwargs.get('AdditionalDocumentReferences',[])
        Signatures = kwargs.get('Signatures',[]) 
        AccountingSupplierParty = kwargs.get('AccountingSupplierParty',{}) 
        AccountingCustomerParty = kwargs.get('AccountingCustomerParty',{}) 
        TaxtTotal       =  kwargs.get('TaxtTotal',{})
        AllowanceCharge =  kwargs.get('AllowanceCharge',{})
        LegalMonetaryTotal = kwargs.get('LegalMonetaryTotal',{})
        InvoiceLines = kwargs.get('InvoiceLines',[])
        LineCountNumeric = str(len(InvoiceLines)) 
        self.__class__.def_para_brm = kwargs.get('DocumentCurrencyCode','TRY')       
        self._Invoice = etree.Element('{urn:oasis:names:specification:ubl:schema:xsd:Invoice-2}Invoice', 
             nsmap=self.namespacemap)
        self._Invoice.set('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation','urn:oasis:names:specification:ubl:schema:xsd:Invoice-2 ../xsdrt/maindoc/UBL-Invoice-2.1.xsd')               
        UBLExtensions       = self.SubElement(self._Invoice, 'ext', 'UBLExtensions')
        UBLExtension        = self.SubElement(UBLExtensions, 'ext', 'UBLExtension')
        ExtensionContent    = self.SubElement(UBLExtension, 'ext', 'ExtensionContent')
        self.SubElement(self._Invoice, 'cbc', 'UBLVersionID').text = '2.1'
        self.SubElement(self._Invoice, 'cbc', 'CustomizationID').text = 'TR1.2'
        self.SubElement(self._Invoice, 'cbc', 'ProfileID').text = 'EARSIVFATURA'
        self.SubElement(self._Invoice, 'cbc', 'ID').text = kwargs.get('ID')
        self.SubElement(self._Invoice, 'cbc', 'CopyIndicator').text = CopyIndicator
        self.SubElement(self._Invoice, 'cbc', 'UUID').text = kwargs.get('UUID')
        self.SubElement(self._Invoice, 'cbc', 'IssueDate').text =  IssueDate
        self.SubElement(self._Invoice, 'cbc', 'IssueTime').text =  IssueTime
        self.SubElement(self._Invoice, 'cbc', 'InvoiceTypeCode').text =  kwargs.get('InvoiceTypeCode')
        for Note in Notes   : self.SubElement(self._Invoice, 'cbc', 'Note').text = Note
        self.SubElement(self._Invoice, 'cbc', 'DocumentCurrencyCode').text = self.def_para_brm 
        self.SubElement(self._Invoice, 'cbc', 'LineCountNumeric').text = LineCountNumeric
        for AdditionalDocumentReference in AdditionalDocumentReferences: \
            self._Invoice.append(self.AdditionalDocumentReference(**AdditionalDocumentReference))
        for Signature in Signatures: \
            self._Invoice.append(self.Signature(**Signature))

        self.SubElement(self._Invoice, 'cac', 'AccountingSupplierParty').append(self.Party(**AccountingSupplierParty))
        self.SubElement(self._Invoice, 'cac', 'AccountingCustomerParty').append(self.Party(**AccountingCustomerParty))
        self._Invoice.append(self.AllowanceCharge(**AllowanceCharge))
        self._Invoice.append(self.TaxtTotal(**TaxtTotal))
        self._Invoice.append(self.LegalMonetaryTotal(**LegalMonetaryTotal))
        for InvoiceLine in InvoiceLines: \
            self._Invoice.append(self.InvoiceLine(**InvoiceLine))
    
      
    def get_invoice(self):
        return etree.tostring(self._Invoice, encoding='utf8')
    
    @classmethod
    def SubElement(cls,parent, prefix, tag ):
        """Kisa yol fonksiyonu"""
        return etree.SubElement(parent, etree.QName(cls.namespacemap.get(prefix), tag))
    
    @classmethod
    def Element(cls,prefix, tag ):
        """Kisa yol fonksiyonu"""
        return etree.Element(etree.QName(cls.namespacemap.get(prefix), tag))

    @classmethod
    def AdditionalDocumentReference(cls,**kwargs):
        node = cls.Element('cac', 'AdditionalDocumentReference')
        cls.SubElement(node, 'cbc', 'ID').text = kwargs.get('ID') 
        cls.SubElement(node, 'cbc', 'IssueDate').text = kwargs.get('IssueDate')    
        cls.SubElement(node, 'cbc', 'DocumentTypeCode').text = kwargs.get('DocumentTypeCode')   
        cls.SubElement(node, 'cbc', 'DocumentType').text = kwargs.get('DocumentType')     
        return node
    
    @classmethod
    def PostalAddress(cls,**kwargs):    
        node = cls.Element('cac', 'PostalAddress')    
        cls.SubElement(node, 'cbc', 'ID').text = kwargs.get('ID') 
        cls.SubElement(node, 'cbc', 'Postbox').text = kwargs.get('Postbox')        
        cls.SubElement(node, 'cbc', 'Room').text = kwargs.get('Room')   
        cls.SubElement(node, 'cbc', 'StreetName').text = kwargs.get('StreetName')   
        cls.SubElement(node, 'cbc', 'BlockName').text = kwargs.get('BlockName')   
        cls.SubElement(node, 'cbc', 'BuildingName').text = kwargs.get('BuildingName') 
        cls.SubElement(node, 'cbc', 'BuildingNumber').text = kwargs.get('BuildingNumber')    
        cls.SubElement(node, 'cbc', 'CitySubdivisionName').text = kwargs.get('CitySubdivisionName')  
        cls.SubElement(node, 'cbc', 'CityName').text = kwargs.get('CityName')  
        cls.SubElement(node, 'cbc', 'PostalZone').text = kwargs.get('PostalZone')   
        cls.SubElement(node, 'cbc', 'Region').text = kwargs.get('Region')   
        cls.SubElement(node, 'cbc', 'District').text = kwargs.get('District')    
        cntry = cls.SubElement(node, 'cac', 'Country')
        cls.SubElement(cntry, 'cbc', 'Name').text = kwargs.get('Country')   
        return node
    
    @classmethod
    def Contact(cls,**kwargs):
        node = cls.Element('cac', 'Contact')
        cls.SubElement(node, 'cbc', 'Telephone').text = kwargs.get('Telephone') 
        cls.SubElement(node, 'cbc', 'Telefax').text = kwargs.get('Telefax')
        cls.SubElement(node, 'cbc', 'ElectronicMail').text = kwargs.get('ElectronicMail')     
        cls.SubElement(node, 'cbc', 'Note').text = kwargs.get('Note')     
        return node
    
    @classmethod
    def Person(cls,**kwargs):
        node = cls.Element('cac', 'Person')
        cls.SubElement(node, 'cbc', 'FirstName').text = kwargs.get('FirstName') 
        cls.SubElement(node, 'cbc', 'FamilyName').text = kwargs.get('FamilyName')            
        cls.SubElement(node, 'cbc', 'MiddleName').text = kwargs.get('MiddleName')     
        cls.SubElement(node, 'cbc', 'NameSuffix').text = kwargs.get('NameSuffix') 
        cls.SubElement(node, 'cbc', 'NationalityID').text = kwargs.get('NationalityID')     
        return node

    @classmethod
    def PartyTaxScheme(cls, Name=None,TaxTypeCode=None):
        node = cls.Element('cac', 'PartyTaxScheme')
        sub = cls.SubElement(node, 'cac', 'TaxScheme')
        cls.SubElement(sub, 'cbc', 'Name').text = Name
        cls.SubElement(sub, 'cbc', 'TaxTypeCode').text = TaxTypeCode     
        return node            

    @classmethod
    def Signature(cls, **kwargs):
        Signature = cls.Element('cac', 'Signature')
        cls.SubElement(Signature, 'cbc', 'ID').text = kwargs.get('ID') 
        SignatoryParty      = cls.SubElement(Signature, 'cac', 'SignatoryParty')
        cls.SubElement(SignatoryParty, 'cbc', 'WebsiteURI').text = kwargs.get('WebsiteURI')
        PartyIdentification = cls.SubElement(SignatoryParty, 'cac', 'PartyIdentification')
        PartyIdentification.text = kwargs.get('PartyIdentification')
        ID                  = cls.SubElement(PartyIdentification, 'cbc', 'ID')
        ID.text = kwargs.get('ID')
        schemeID = 'VKN' if len(kwargs.get('ID','')) == 10 else 'TCKN'
        ID.set('schemeID', schemeID)
        PartyName           = cls.SubElement(SignatoryParty, 'cac', 'PartyName')
        cls.SubElement(PartyName, 'cbc', 'Name').text = kwargs.get('Name')         
        SignatoryParty.append(cls.PostalAddress(**kwargs.get('PostalAddress',{})))        
        SignatoryParty.append(cls.Contact(**kwargs.get('Contact',{}) ))
        DigitalSignatureAttachment = cls.SubElement(Signature, 'cac', 'DigitalSignatureAttachment')
        ExternalReference   = cls.SubElement(DigitalSignatureAttachment, 'cac', 'ExternalReference')
        cls.SubElement(ExternalReference, 'cbc', 'URI').text = '#Signature'
        return Signature 

    @classmethod
    def Party(cls, **kwargs):
        Party      = cls.Element('cac', 'Party')
        cls.SubElement(Party, 'cbc', 'WebsiteURI').text = kwargs.get('WebsiteURI')
        PartyIdentification = cls.SubElement(Party, 'cac', 'PartyIdentification')
        PartyIdentification.text = kwargs.get('PartyIdentification')
        ID                  = cls.SubElement(PartyIdentification, 'cbc', 'ID')
        ID.text = kwargs.get('ID')
        schemeID = 'VKN' if len(kwargs.get('ID','')) == 10 else 'TCKN'
        ID.set('schemeID', schemeID)
        PartyName           = cls.SubElement(Party, 'cac', 'PartyName')
        cls.SubElement(PartyName, 'cbc', 'Name').text = kwargs.get('Name')       
        Party.append(cls.PostalAddress(**kwargs.get('PostalAddress',{})))        
        Party.append(cls.PartyTaxScheme(**kwargs.get('PartyTaxScheme',{})))
        Party.append(cls.Contact(**kwargs.get('Contact',{})))
        Party.append(cls.Person(**kwargs.get('Person',{})))        
        return Party   

    @classmethod
    def AllowanceCharge(cls, **kwargs):
        AllowanceCharge      = cls.Element('cac', 'AllowanceCharge')
        cls.SubElement(AllowanceCharge, 'cbc', 'ChargeIndicator').text = kwargs.get('ChargeIndicator')
        cls.SubElement(AllowanceCharge, 'cbc', 'AllowanceChargeReason').text = kwargs.get('AllowanceChargeReason')
        Amount = cls.SubElement(AllowanceCharge, 'cbc', 'Amount')
        Amount.text = kwargs.get('Amount')         
        Amount.set('currencyID',kwargs.get('currencyID',cls.def_para_brm))             
        return AllowanceCharge 

    @classmethod
    def TaxScheme(cls, **kwargs):
        TaxScheme      = cls.Element('cac', 'TaxScheme')
        cls.SubElement(TaxScheme, 'cbc', 'ID').text = kwargs.get('ID')
        cls.SubElement(TaxScheme, 'cbc', 'Name').text = kwargs.get('Name')
        cls.SubElement(TaxScheme, 'cbc', 'TaxTypeCode').text = kwargs.get('TaxTypeCode')              
        return TaxScheme      

    @classmethod
    def TaxCategory(cls, **kwargs):
        TaxCategory      = cls.Element('cac', 'TaxCategory')
        cls.SubElement(TaxCategory, 'cbc', 'Name').text = kwargs.get('Name')
        if kwargs.get('TaxExemptionReasonCode'):
            cls.SubElement(TaxCategory, 'cbc', 'TaxExemptionReasonCode').text = kwargs.get('TaxExemptionReasonCode')
        if kwargs.get('TaxExemptionReason'):
            cls.SubElement(TaxCategory, 'cbc', 'TaxExemptionReason').text = kwargs.get('TaxExemptionReason')
        TaxCategory.append(cls.TaxScheme(**kwargs.get('TaxScheme',{})))             
        return TaxCategory   

    @classmethod
    def TaxSubtotal(cls, **kwargs):
        TaxSubtotal      = cls.Element('cac', 'TaxSubtotal')
        TaxableAmount = cls.SubElement(TaxSubtotal, 'cbc', 'TaxableAmount')
        TaxAmount = cls.SubElement(TaxSubtotal, 'cbc', 'TaxAmount')
        cls.SubElement(TaxSubtotal, 'cbc', 'CalculationSequenceNumeric').text = kwargs.get('CalculationSequenceNumeric')
        cls.SubElement(TaxSubtotal, 'cbc', 'Percent').text = kwargs.get('Percent')
        if kwargs.get('BaseUnitMeasure'):
            cls.SubElement(TaxSubtotal, 'cbc', 'BaseUnitMeasure').text = kwargs.get('BaseUnitMeasure')
        if kwargs.get('PerUnitAmount'):
            cls.SubElement(TaxSubtotal, 'cbc', 'PerUnitAmount').text = kwargs.get('PerUnitAmount')
        
        TaxableAmount.text = kwargs.get('TaxableAmount')
        TaxableAmount.set('currencyID', kwargs.get('currencyID',cls.def_para_brm)) 
        TaxAmount.text = kwargs.get('TaxAmount')
        TaxAmount.set('currencyID', kwargs.get('currencyID',cls.def_para_brm)) 
        TaxSubtotal.append(cls.TaxCategory(**kwargs.get('TaxCategory',{}))) 
        return TaxSubtotal

    @classmethod
    def TaxtTotal(cls, **kwargs):
        TaxtTotal      = cls.Element('cac', 'TaxTotal')
        TaxAmount = cls.SubElement(TaxtTotal, 'cbc', 'TaxAmount')
        TaxAmount.text = kwargs.get('TaxAmount')         
        TaxAmount.set('currencyID',kwargs.get('currencyID',cls.def_para_brm)) 
        TaxtTotal.append(cls.TaxSubtotal(**kwargs.get('TaxSubtotal',{})))                     
        return TaxtTotal 

    @classmethod
    def LegalMonetaryTotal(cls, **kwargs):
        LegalMonetaryTotal  = cls.Element('cac', 'LegalMonetaryTotal')
        LineExtensionAmount = cls.SubElement(LegalMonetaryTotal, 'cbc', 'LineExtensionAmount')
        TaxExclusiveAmount  = cls.SubElement(LegalMonetaryTotal, 'cbc', 'TaxExclusiveAmount')
        TaxInclusiveAmount  = cls.SubElement(LegalMonetaryTotal, 'cbc', 'TaxInclusiveAmount')
        AllowanceTotalAmount= cls.SubElement(LegalMonetaryTotal, 'cbc', 'AllowanceTotalAmount')
        PayableAmount       = cls.SubElement(LegalMonetaryTotal, 'cbc', 'PayableAmount')        
         
        LineExtensionAmount.text = kwargs.get('LineExtensionAmount') 
        TaxExclusiveAmount.text = kwargs.get('TaxExclusiveAmount') 
        TaxInclusiveAmount.text = kwargs.get('TaxInclusiveAmount') 
        AllowanceTotalAmount.text = kwargs.get('AllowanceTotalAmount') 
        PayableAmount.text = kwargs.get('PayableAmount')         
        
       
        LineExtensionAmount.set('currencyID',kwargs.get('currencyID',cls.def_para_brm))             
        TaxExclusiveAmount.set('currencyID',kwargs.get('currencyID',cls.def_para_brm))
        TaxInclusiveAmount.set('currencyID',kwargs.get('currencyID',cls.def_para_brm)) 
        AllowanceTotalAmount.set('currencyID',kwargs.get('currencyID',cls.def_para_brm)) 
        PayableAmount.set('currencyID',kwargs.get('currencyID',cls.def_para_brm))             
        return LegalMonetaryTotal

    @classmethod
    def Item(cls, **kwargs):
        Item  = cls.Element('cac', 'Item')
        cls.SubElement(Item, 'cbc', 'Description').text = kwargs.get('Description')      
        cls.SubElement(Item, 'cbc', 'Name').text = kwargs.get('Name')      
        cls.SubElement(Item, 'cbc', 'BrandName').text = kwargs.get('BrandName')      
        cls.SubElement(Item, 'cbc', 'ModelName').text = kwargs.get('ModelName')      
        return Item  

    @classmethod
    def InvoiceLine(cls, **kwargs):
        InvoiceLine  = cls.Element('cac', 'InvoiceLine')
        cls.SubElement(InvoiceLine, 'cbc', 'ID').text = kwargs.get('ID')    
        InvoicedQuantity = cls.SubElement(InvoiceLine, 'cbc', 'InvoicedQuantity')
        LineExtensionAmount = cls.SubElement(InvoiceLine, 'cbc', 'LineExtensionAmount')
        InvoicedQuantity.text = kwargs.get('InvoicedQuantity') 
        InvoicedQuantity.set('unitCode', kwargs.get('unitCode',''))
        LineExtensionAmount.text = kwargs.get('LineExtensionAmount') 
        LineExtensionAmount.set('currencyID', kwargs.get('currencyID',cls.def_para_brm))
        if kwargs.get('AllowanceCharge'):
            InvoiceLine.append(cls.AllowanceCharge(**kwargs.get('AllowanceCharge',{})))
        if kwargs.get('TaxtTotal'):
            InvoiceLine.append(cls.TaxtTotal(**kwargs.get('TaxtTotal',{})))
        InvoiceLine.append(cls.Item(**kwargs.get('Item',{})))
        Price = cls.SubElement(InvoiceLine, 'cac', 'Price') 
        PriceAmount = cls.SubElement(Price, 'cbc', 'PriceAmount')
        PriceAmount.text = kwargs.get('PriceAmount')
        PriceAmount.set('currencyID', kwargs.get('currencyID', cls.def_para_brm) )
        return InvoiceLine                

    def __str__(self):
        return etree.tostring(self._Invoice, pretty_print=True, encoding='utf8').decode('utf8')    
    
