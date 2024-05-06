
import pytz
from datetime import datetime

now = datetime.now()
dt_string = datetime.now(pytz.timezone('Africa/Nairobi')).strftime("%Y-%m-%d %H:%M:%S")
date_string = datetime.now(pytz.timezone('Africa/Nairobi')).strftime("%Y-%m-%d")

def construct_data_section(message):
    data_section = {
        "content": message,
        "signature": "",
        "dataDescription": {
            "codeType": "0",
            "encryptCode": "1",
            "zipCode": "0"
        }
    }
    return data_section


def construct_global_info_section(device_number,tin, ic):
    global_info_section = {
        "appId": "AP04",
        "version": "1.1.20191201",
        "dataExchangeId": "9230489223014123",
        "interfaceCode": str(ic),
        "requestCode": "TP",
        "requestTime": str(dt_string),
        "responseCode": "TA",
        "userName": "admin",
        "deviceMAC": "FFFFFFFFFFFF",
        "deviceNo": str(device_number),
        "tin": str(tin),
        "brn": "",
        "taxpayerID": "1",
        "longitude": "116.397128",
        "latitude": "39.916527",
        "extendField": {
            "responseDateFormat": "dd/MM/yyyy",
            "responseTimeFormat": "dd/MM/yyyy HH:mm:ss"
        }
    }
    return global_info_section


def construct_return_state_info_section():
    return_state_info_section = {
        "returnCode": "",
        "returnMessage": ""
    }
    return return_state_info_section


def query_invoice_json(fdn, type):
    request_message = {
    "Request Message": "",  # Descriptive message
    "oriInvoiceNo": "",
    "invoiceNo": str(fdn),
    "deviceNo": "",
    "buyerTin": "",
    "buyerNinBrn": "",
    "buyerLegalName": "",
    "combineKeywords": "",
    "invoiceType": "",
    "invoiceKind": type,
    "isInvalid": "",
    "isRefund": "",
    "startDate": "",
    "endDate": "",
    "pageNo": "1",
    "pageSize": "98",
    "referenceNo": "",
    "branchName": "",
    "queryType": "",
    "dataSource": "",
    "sellerTinOrNin": "",
    "sellerLegalOrBusinessName": ""
    }
    return request_message

def invoice_details_json(fdn):
    request_message = {
    "invoiceNo": str(fdn),
    }
    return request_message


# invoice upload jsons
def sellers_details(tin, name, reference_no):
    data = {
        "tin": tin,
        "ninBrn": "",
        "legalName": name,
        "businessName": "",
        "address": "",
        "mobilePhone": "",
        "linePhone": "",
        "emailAddress": "",
        "placeOfBusiness": "",
        "referenceNo": reference_no,
        "branchId": "",
        "branchName": "Main",
        "isCheckReferenceNo": ""
    }
    return data

def basic_info(operator, currency, type, kind):
    data ={
        "invoiceNo": "",
        "antifakeCode": "",
        "deviceNo": "",
        "issuedDate": str(dt_string),
        "operator": operator,
        "currency": currency,
        "oriInvoiceId": "",
        "invoiceType": type,
        "invoiceKind": kind,
        "dataSource": "106",
        "invoiceIndustryCode": "",
        "isBatch": ""
    }
    return data


def buyer_details(tin, buyer_type):
    data = {
        "buyerTin": tin,
        "buyerNinBrn": "",
        "buyerPassportNum": "",
        "buyerLegalName": "",
        "buyerBusinessName": "",
        "buyerAddress": "",
        "buyerEmail": "",
        "buyerMobilePhone": "",
        "buyerLinePhone": "",
        "buyerPlaceOfBusi": "",
        "buyerType": buyer_type,
        "buyerCitizenship": "",
        "buyerSector": "",
        "buyerReferenceNo": "",
        "nonResidentFlag": ""
    }
    return data

def buyer_extend():
    data = {
        "propertyType": "",
        "district": "",
        "municipalityCounty": "",
        "divisionSubcounty": "",
        "town": "",
        "cellVillage": "",
        "effectiveRegistrationDate": "",
        "meterStatus": ""
    }
    return data

def goods_details():
    data = {
        "item": "",
        "itemCode": "",
        "qty": "",
        "unitOfMeasure": "",
        "unitPrice": "",
        "total": "",
        "taxRate": "",
        "tax": "",
        "discountTotal": "",
        "discountTaxRate": "",
        "orderNumber": "",
        "discountFlag": "",
        "deemedFlag": "",
        "exciseFlag": "",
        "categoryId": "",
        "categoryName": "",
        "goodsCategoryId": "",
        "goodsCategoryName": "",
        "exciseRate": "",
        "exciseRule": "",
        "exciseTax": "",
        "pack": "",
        "stick": "",
        "exciseUnit": "",
        "exciseCurrency": "",
        "exciseRateName": "",
        "vatApplicableFlag": "",
        "deemedExemptCode": "",
        "vatProjectId": "",
        "vatProjectName": ""
    }
    return data

def tax_details():
    data = {
        "taxCategoryCode": "",
        "netAmount": "",
        "taxRate": "",
        "taxAmount": "",
        "grossAmount": "",
        "exciseUnit": "",
        "exciseCurrency": "",
        "taxRateName": ""
    }
    return data

def summary_details():  
    data = {
        "netAmount": "",
        "taxAmount": "",
        "grossAmount": "",
        "itemCount": "",
        "modeCode": "",
        "remarks": "",
        "qrCode": ""
    }
    return data

def payment_details():  
    data = {
        "paymentMode": "",
        "paymentAmount": "",
        "orderNumber": ""
    }
    return data

def extend_details():  
    data = {
        "reason": "",
        "reasonCode": ""
    }
    return data

def import_services_seller():  
    data = {
        "importBusinessName": "",
        "importEmailAddress": "",
        "importContactNumber": "",
        "importAddress": "",
        "importInvoiceDate": "",
        "importAttachmentName": "",
        "importAttachmentContent": ""
    }
    return data

def airline_goods_details():  
    data = {
        "airlineGoodsDetails": ""
    }
    return data


def credit_note_json():
    data = {
    "referenceNo": "",
    "oriInvoiceNo": "",
    "invoiceNo": "",
    "combineKeywords": "",
    "approveStatus": "",
    "queryType": "1",
    "invoiceApplyCategoryCode": "",
    "startDate": "",
    "endDate": "",
    "pageNo": "1",
    "pageSize": "99",
    "creditNoteType": "",
    "branchName": "",
    "sellerTinOrNin": "",
    "sellerLegalOrBusinessName": ""
    }
    return data


def approve_credit_note(ref_no, status, id, remarks):
    data = {
    "referenceNo": ref_no,
    "approveStatus": status,
    "taskId": id,
    "remark": remarks
    }
    return data

def cancel_credit_note(fdn, cn_fdn, reason):
    data = {
    "oriInvoiceId": fdn,
    "invoiceNo": cn_fdn,
    "reason": reason,
    "reasonCode": "103",
    "invoiceApplyCategoryCode": "104",
    "attachmentList": [{
        "fileName": "",
        "fileType": "",
        "fileContent": ""
    }]
}

    return data

def product_upload_json():
    data = {
        "havePieceUnit": "101",
        "goodsName": "",
        "goodsCode": "",
        "measureUnit": "",
        "unitPrice": "",
        "currency": "",
        "commodityCategoryId": "",
        "haveExciseTax": "",
        "description": "",
        "stockPrewarning": "",
    }
    return data


class InvoiceGenerator:
    """
    A class for generating invoice data.

    Attributes:
        None

    Methods:
        goods_details(prod, inv): Generates goods details dictionary for a given product and invoice.
        tax_details(tax, inv): Generates tax details dictionary for a given tax and invoice.
        summary(summary_details): Generates summary dictionary for given summary details.
        invoice_load(company, context, goodsDetails, taxDetails, summary_json, payment_details):
            Generates the complete invoice data dictionary.
    """

    def goods_details(self, prod, inv):
        """
        Generates goods details dictionary for a given product and invoice.

        Args:
            prod (Product): The product object.
            inv (Invoice): The invoice object.

        Returns:
            dict: A dictionary containing the goods details.
        """
        deemed = ''
        deemedFlag = '2'

        if inv.client.company_type == '3':
            deemedFlag = '1'
            deemed = ' ' + '(Deemed)'

        tax_type = ""
        if prod.tax_type == "01":
            tax_type = "0.18"
        elif prod.tax_type == "03":
            tax_type = "-"
        elif prod.tax_type == "04":
            tax_type = "0.18"
        else:
            tax_type = "0"

        goods = {
            "item": str(prod.product.name) + deemed,
            "itemCode": str(prod.product.code),
            "qty": str("{:.2f}".format(prod.quantity)),
            "unitOfMeasure": str(prod.product.unit_measure.code) if prod.product.unit_measure else "None",
            "unitPrice": "{:.2f}".format(prod.price),
            "total": str("{:.2f}".format(prod.total())),
            "taxRate": tax_type,
            "tax": str(prod.tax()),
            "discountTotal": "",
            "discountTaxRate": "",
            "orderNumber": str(prod.number),
            "discountFlag": "2",
            "deemedFlag": deemedFlag,
            "exciseFlag": "2",
            "categoryId": "",
            "categoryName": "",
            "goodsCategoryId": str(prod.product.commodity_id),
            "goodsCategoryName": str(prod.product.name),
            "exciseRate": "",
            "exciseRule": "",
            "exciseTax": "",
            "pack": "",
            "stick": "",
            "exciseUnit": "",
            "exciseCurrency": "",
            "exciseRateName": ""
        }
        return goods

    def tax_details(self, tax):
        """
        Generates tax details dictionary for a given tax and invoice.

        Args:
            tax (Tax): The tax object.
            inv (Invoice): The invoice object.

        Returns:
            dict: A dictionary containing the tax details.
        """
        tax_rate = ""
        if tax.tax_type == "01":
            tax_rate = "0.18"
        elif tax.tax_type == "02":
            tax_rate = "0"
        elif tax.tax_type == "03":
            tax_rate = "-"
        else:
            tax_rate = ""

        tax_request = {
            "taxCategoryCode": str(tax.tax_type),
            "netAmount": "{:.2f}".format(tax.net_amount()),
            "taxRate": tax_rate,
            "taxAmount": str("{:.2f}".format(tax.tax())),
            "grossAmount": str(tax.total()),
            "exciseUnit": "",
            "exciseCurrency": "",
        }
        return tax_request

    def summary(self, summary_details):
        """
        Generates summary dictionary for given summary details.

        Args:
            summary_details (dict): A dictionary containing the summary details.

        Returns:
            dict: A dictionary containing the summary.
        """
        inv_summary = {
            "netAmount": str("{:.2f}".format(summary_details['net'])),
            "taxAmount": str("{:.2f}".format(summary_details['tax_summary'])),
            "grossAmount": str("{:.2f}".format(summary_details['gross'])),
            "itemCount": str(summary_details['itemCount']),
            "modeCode": "1",
            "remarks": str(summary_details['remarks']),
            "qrCode": ""
        }
        return inv_summary

    def invoice_load(self, company, context, goodsDetails, taxDetails, summary_json, payment_details):
        """
        Generates the complete invoice data dictionary.

        Args:
            company (Company): The company object.
            context (dict): A dictionary containing the invoice context.
            goodsDetails (list): A list of goods details dictionaries.
            taxDetails (list): A list of tax details dictionaries.
            summary_json (dict): A dictionary containing the summary details.
            payment_details (dict): A dictionary containing the payment details.

        Returns:
            dict: A dictionary containing the complete invoice data.
        """
        message = {
            "sellerDetails": {
                "tin": str(company.tin),
                "ninBrn": "",
                "legalName": str(company.name),
                "businessName": "",
                "address": "",
                "mobilePhone": "",
                "linePhone": "",
                "emailAddress": company.email,
                "placeOfBusiness": "",
                "referenceNo": context["invoice"].inv_number(),
            },
            "basicInformation": {
                "invoiceNo": "",
                "antifakeCode": "",
                "deviceNo": str(company.device_number),
                "issuedDate": str(dt_string),
                "operator": context["operator"],
                "currency": context["currency"],
                "oriInvoiceId": "",
                "invoiceType": "1",
                "invoiceKind": "1",
                "dataSource": "106",
                "invoiceIndustryCode": context["industryCode"][0],
                "isBatch": "0",
            },
            "buyerDetails": {
                "buyerTin": str(context["buyerTin"]),
                "buyerNinBrn": "",
                "buyerPassportNum": "",
                "buyerLegalName": context["buyerLegalName"][0],
                "buyerBusinessName": context["buyerLegalName"][0],
                "buyerAddress": "",
                "buyerEmail": context['buyerEmail'][0],
                "buyerMobilePhone": "+258373748393",
                "buyerLinePhone": "",
                "buyerPlaceOfBusi": "",
                "buyerType": str(context['buyerType']),
                "buyerCitizenship": "",
                "buyerSector": "",
                "buyerReferenceNo": ""
            },
            "goodsDetails": goodsDetails,
            "taxDetails": taxDetails,
            "summary": summary_json,
            "payWay": payment_details,
            "extend": {
                "reason": "",
                "reasonCode": ""
            }
        }
        return message