import requests
import json

## Methods for mapping TAC code to common phone name to be used in search query for scrapers.


# Make api request to alpha.imeicheck.com with generated IMEI

def process_tac_code(code):
    imei = generate_check_sum(code+"111111")
    imei_json = requests.api.get("https://alpha.imeicheck.com/api/modelBrandName?imei=" + imei + "&format=json").text
    site_json = json.loads(imei_json)  # Load as json object for easy parsing
    if imei_json == '{"status":"rejected","result":"ERROR: Model not found S2"}':
        return "-2"
    return(site_json)

# Generates a fake IMEI using checksum algorithm. This is necessary since the API being used takes in a whole IMEI,
# not just a TAC. Six 1's are appended, and the final digit (checksum) is calculated using algorithm to guarantee
# IMEI validity.

def generate_check_sum(code: str):
    digitReplacements = {"0": 0, "1": 2, "2": 4, "3": 6, "4": 8, "5": 1, "6": 3, "7": 5, "8": 7, "9": 9}
    checksum = 0
    for index, value in enumerate(code):
        if index%2==0:
            checksum+=int(value)
        else:
            checksum+=digitReplacements[value]
    checksum = 10-(checksum%10)
    return code + str(checksum)

