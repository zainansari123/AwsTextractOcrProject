
from dateutil.parser import parse
from pdf2image import convert_from_path
from PIL import Image
import json
import csv
import boto3
import io
from PIL import Image, ImageDraw
from pprint import pprint

requiredData={
    'name':'str',
    'address':'str',
    'total dues':'str',
    'amount':'str',
    'payment due date':'str',
    'statement date':'str',
    'total amount due':'int',
    'minimum amount due':'int',
    'invoice no':'str',
    'cin no':'str',
    'payments/credits':'int',
    'payment/credits':'int',
    'previous balance':'int',
    'available cash':'int',
    'purchases/charges':'int',
    'purchase/debits':'int',
    'financecharges':'int',
    'over limit':'int',
    'current dues':'int',
    'cash advances':'int',
    'credit limit':'int',
    'available credit':'int',
    'available credit limit':'int',
    'cash limit':'int',
    'available cash limit':'int',
    'opening balance':'int',
    'openingbalance':'int',
    'gstin':'str',
    'hsn':'str',
    'email':'str',
    'card no':'str',
    'available credit (including cash)':'int',
    'credit limit (including cash)':'int',
    'total credit limit':'int',
    'card number':'str',
    'total amount due pay now':'int',
    'total payment due':'int',
    'minimum payment due':'int',
    'min.amt.due':'int',
    'payments & credits':'int',
    'statement period':'str',
    'statement generation date':'str',
    'credit card number':'str',
    'last bill amount':'int',
    'mobile':'str',
    'available reward points':'int',
    'e-mail':'str',
    'customer name':'str',
    'current cash advance':'int',
    'last payments received':'int',
    'gstin-':'str',
    'previous balance':'int',
    'gst registration no.':'str',
    'cashback earned':'str'
}

# variable declared

pdfPath="/home/zainul/CreditCardSecond/PdfDocs/Credit Card Statement-1_unlocked.pdf"
# usrPwd=("bhas0502" or "hari1209") or ("BHAS050278" or "BHAS0078") or ("ABDU0312" or "abdu0312" or "ABDU031291")
usrPwd="NILE23AUG"
output_filename=pdfPath.split('/')[-1].split('.')[0]

# define our AWS Access Key, Secret Key, and Region
ACCESS_KEY = "AKIAWP7KVI6U3SAN3LQQ"
SECRET_KEY = "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"
REGION = "us-east-1"
FinalData=[]
rawData=[]

# Step 1 : To convert pdf file to image file
def convertpdf2image():
    pdfs = r"{}".format(pdfPath)
    pages = convert_from_path(pdfs, 350,userpw=usrPwd)
    i = 1
    for page in pages:
        image_name = "Page_" + str(i) + ".jpg"  
        page.save(image_name, "JPEG")
        i = i+1        

def is_date(stringg, fuzzy=False):
    if not '/' in stringg:
        return False
    try:
        parse(stringg, fuzzy=fuzzy)
        return True
    except:
        return False

def filterOutData(text):
    for r in (("\u20b9", ""),("Dr",""),("(RS)",""),("()",""),(".",""),("Rs.", ""), ("\n", ""),("" if is_date(text) else ":", ""),(" / ", "/"),(",", "")):
        text = text.replace(*r)
    return text.strip()

    
def checkType(val,typ):
    print(typ,val.isalpha())
    if typ=='str' and val.isalpha()==True:
        return True
    elif typ=='int' and val.isalpha()==False:
        return True
    else:
        return False


def filterKeys(key):
    return key.lower().replace(" / ","/")
# Takes a field as an argument and prints out the detected labels and values
def print_labels_and_values(field):
    temp={}
    # Only if labels are detected and returned
    if "LabelDetection" in field:
        temp['Label']=filterOutData(field.get("LabelDetection")["Text"])

    if "ValueDetection" in field:
        temp['value']=filterOutData(field.get("ValueDetection")["Text"])

    if 'Label' in temp and 'value' in temp:
        rawData.append(temp)
        if filterKeys(temp['Label']) in requiredData.keys():
            ind=list(requiredData.keys()).index(filterKeys(temp['Label']))
            vall=list(requiredData.values())[ind]
            print('valll'+vall)
            keys=[]
            keys=[x['Label'] for x in FinalData]
            if vall=='int':
                try:
                    float(temp['value'])
                    if temp['Label'] not in keys:
                        FinalData.append(temp)
                except:
                    pass
            else:
                # if str(type(temp['value'])).split("'")[1]==vall:
                if temp['Label'] not in keys:
                    FinalData.append(temp)
                
            

def outPutFile(data,name):
    with open(name, "w") as outfile:
        json.dump(data, outfile, indent=4)