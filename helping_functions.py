import pandas as pd
import json
from io import StringIO
import requests

month_days_dict = {
    "1": 31,
    "2": 28,
    "3": 31,
    "4": 30,
    "5": 31,
    "6": 30,
    "7": 31,
    "8": 31,
    "9": 30,
    "10": 31,
    "11": 30,
    "12": 31,
}

leap_month_days_dict = {
    "1": 31,
    "2": 29,
    "3": 31,
    "4": 30,
    "5": 31,
    "6": 30,
    "7": 31,
    "8": 31,
    "9": 30,
    "10": 31,
    "11": 30,
    "12": 31
}

def check_leap_year(year):
    #check if the year is leap year
    if (year % 400 == 0) and (year % 100 == 0):
        print("Leap year")
        return 1    #leap year

    # not divided by 100 means not a century year
    # year divided by 4 is a leap year
    elif (year % 4 ==0) and (year % 100 != 0):
        print("Leap year")
        return 1

    # if not divided by both 400 (century year) and 4 (not century year)
    # year is not leap year
    else:
        print("Not Leap year")
        return 0    #not leap year
    
def extract(df, start_date, end_date):
    url = 'https://www.iexindia.com/IEXPublish/AppServices.svc/IEXGetTradeData'
    myobj = {
    "APITokenNo":"NCLIEXHkl7900@8Uyhkj",
    "Product_Code":1,
    "From_Date":start_date,
    "From_Token":1,
    "To_Date":end_date,
    "To_Token":96,
    "Date_Type":2
    }
    
    try:
        x = requests.post(url, json = myobj)
        x.raise_for_status()
        print(x)
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
    
    json_string = json.dumps(x.json(), sort_keys=True, allow_nan=False, indent = 6)
    x.close()
    try:
        data = pd.read_json(StringIO(json_string))
    except:
        print(json_string)
        exit()

    a = []

    for date in data["Delivery_Date_Details"]:
        a.append(date['DeliveryDate'])
        for token in date["Token_Wise"]:
            #print(token["Token_NO"])
            a.append(token["Token_NO"])
            #print(token["Area_Details"])
            for area_code in token["Area_Details"]:
                #print(area_code["Area_code"])
                for key, values in area_code["Area_Codes"].items():   
                    if key == 'Area_Price':
                        #print("Area_Price", values)
                        a.append(values)
            for MCPrice, MCPValues in token["All_India_DAM_GDAM_RTM"].items():
                if MCPrice == 'Clearing_Price':
                    #print(MCPValues)
                    a.append(MCPValues)
            #print(df)
            df = df._append(pd.Series(a, index=df.columns[:len(a)]), ignore_index=True)
            #df.loc[len(df)] = a
            a[1:] = []
        a.clear()
    #print(df)
    print("Extracted")
    return df

def execute_within_year(df, start_year, start_month, start_day, end_year, end_month, end_day, leap):
    
    # if its not leap year
    if leap == 0:
        print("Not Leap Year")
        #iter through months
        for i in range (start_month, end_month+1, 1):
            if i==start_month:
                s_day = start_day
                e_day = month_days_dict[str(start_month)]
                #print(e_day)
            elif i==end_month:
                #check if the end_day is 1
                if end_day == 1:
                    s_day = month_days_dict[str(end_month-1)]
                    e_day = end_day
                else:
                    s_day = 1
                    e_day = end_day
            else:
                s_day = 1
                e_day = month_days_dict[str(i)]
            
            start_date = str(s_day)+"/"+str(i)+"/"+str(start_year)
            end_date = str(e_day)+"/"+str(i)+"/"+str(end_year)
            print(start_date)
            df = extract(df, start_date, end_date)
    #if its leap year
    else:
        # sepearate days for feb
        print("Leap Year")
        #iter through months
        for i in range (start_month, end_month+1, 1):
            if i==start_month:
                s_day = start_day
                e_day = leap_month_days_dict[str(start_month)]
                #print(e_day)
            elif i==end_month:
                #check if the end_day is 1
                if end_day == 1:
                    s_day = leap_month_days_dict[str(end_month-1)]
                    e_day = end_day
                else:
                    s_day = 1
                    e_day = end_day
            else:
                s_day = 1
                e_day = leap_month_days_dict[str(i)]

            start_date = str(s_day)+"/"+str(i)+"/"+str(start_year)
            end_date = str(e_day)+"/"+str(i)+"/"+str(end_year)
            print(start_date, " to ", end_date)
            df = extract(df, start_date, end_date)
    
    return df