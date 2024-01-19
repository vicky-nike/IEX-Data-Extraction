import requests
import pandas as pd
import json
'''
url = 'https://www.iexindia.com/IEXPublish/AppServices.svc/IEXGetTradeData'
myobj = {
"APITokenNo":"NCLIEXHkl7900@8Uyhkj",
"Product_Code":1,
"From_Date":"21/02/2023",
"From_Token":1,
"To_Date":"21/03/2023",
"To_Token":96,
"Date_Type":2
}

x = requests.post(url, json = myobj)

json_string = json.dumps(x.json(), sort_keys=True, allow_nan=False, indent = 6)
#print(json_string)
#df = pd.read_json(x.json())
with open("json1.json", "w") as f:
    f.write(json_string)
'''
#data = pd.read_json(json_string)
data = pd.read_json("json.json")
#print(data.head())
print(data["Delivery_Date_Details"])
# Get the data by changing the integer value
data["Delivery_Date_Details"][1]['DeliveryDate']
#For a single Time Block - Iterate through this 
data["Delivery_Date_Details"][0]["Token_Wise"][0]
#For MCV and MCP data of each Time Block
data["Delivery_Date_Details"][0]["Token_Wise"][0]['All_India_DAM_GDAM_RTM']
#Each data of area wise code
data["Delivery_Date_Details"][0]["Token_Wise"][0]['Area_Details'][0]
#To get area code value
data["Delivery_Date_Details"][0]["Token_Wise"][0]['Area_Details'][0]['Area_code']