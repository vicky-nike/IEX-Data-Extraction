import pandas as pd

#Read data
data = pd.read_json("json.json")

#Headers list
headers = ['Date', 'Time Block', 'A1', 'A2', 'E1', 'E2', 'N1', 'N2', 'N3', 'S1', 'S2', 'S3', 'W1', 'W2', 'W3', 'MCP']
df = pd.DataFrame(columns=headers)

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
        #print(a)
        df.loc[len(df)] = a
        a[1:] = []
    a.clear()

print(df)
df.to_excel('try.xlsx', index=False, index_label=None)