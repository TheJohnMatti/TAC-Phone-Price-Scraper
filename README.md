### TAC Code Phone Price Web Scraper

# Intro
TAC codes are 8 digit codes used to identify a phone's make and model. These 8 digits are the first of 15 digits in the phone's IMEI. Given any 8-digit input, this application scrapes pricing information and other data from 5 Canadian websites, and displays it on 
a PyQt GUI application. As IMEI checker API's are much more common then TAC checker API's, the first question is how can we get a valid IMEI from a given TAC code?


# Tac Mapper
Using Luhn's algorithm (source: https://sndeep.info/en/tools/checksum_calculator), we can calculate the last digit of the IMEI, known as the checksum. Therefore, by appending the same 6 digits to the TAC, then calculating the checksum, we can always obtain a valid
IMEI and use an IMEI checker to obtain the common phone name. THe IMEI checker api used in this application is: https://alpha.imeicheck.com/api

# Web Scraper
Scrapes data from Amazon, Ebay, Bestbuy, Canada Computers and Walmart. Finds prices, names, conditions, sellers, and product links. Uses playwright to access pages and selectolax to parse HTML.

# Processing
Data is processed to ensure each product contains all product name words in its title. Overly cheap products are filtered out since they are likely to be accessories.

# Running
Simply run gui.exe in the dist folder if on Windows. On Linux or Mac, installing the requirements and running gui.py should work.
<b>Note: </b>Playwright's Firefox browser must be installed on your computer to use this application. You can run ````py -m playwright install```` after running ````pip install playwright````. Alternatively, if you run the app, it will try to install the browsers
for you automatically.
