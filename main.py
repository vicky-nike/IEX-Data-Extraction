import pandas as pd
from dateutil import parser
import helping_functions as h_func

start_date = input("Enter the Starting Date in the form DD/MM/YYYY-->")
end_date = input("Enter the End Date in the form DD/MM/YYYY-->")

start_year = parser.parse(start_date).year
start_day = parser.parse(start_date).month
start_month = parser.parse(start_date).day

end_year = parser.parse(end_date).year
end_day = parser.parse(end_date).month
end_month = parser.parse(end_date).day

#Headers list
headers = ['Date', 'Time Block', 'A1', 'A2', 'E1', 'E2', 'N1', 'N2', 'N3', 'S1', 'S2', 'S3', 'W1', 'W2', 'W3', 'MCP']
df = pd.DataFrame(columns=headers)

def separate_date(df, start_year, start_month, start_day, end_year, end_month, end_day):
    # To check if Same year
    if end_year - start_year == 0:
        leap = h_func.check_leap_year(start_year)
        df = h_func.execute_within_year(df, start_year, start_month, start_day, end_year, end_month, end_day, leap)
    #It if is for different years
    else:
        #in between two years
        for i in range (start_year, end_year+1, 1):
            leap = h_func.check_leap_year(start_year)
            #print(i)
            # if its not leap year
            if leap == 0:
                if i == start_year:
                    s_month = start_month
                    #print("start month", s_month)
                    e_month = 12
                    s_year = start_year
                    e_year = start_year
                    s_day = start_day
                    e_day = 31
                    df = h_func.execute_within_year(df, s_year, s_month, s_day, e_year, e_month, e_day, leap)
                elif i == end_year:
                    s_month = 1
                    e_month = end_month
                    s_year = end_year
                    e_year = end_year
                    s_day = 1
                    e_day = end_day
                    df = h_func.execute_within_year(df, s_year, s_month, s_day, e_year, e_month, e_day, leap)
                else:
                    s_month = 1
                    e_month = 12
                    s_year = i
                    e_year = i
                    s_day = 1
                    e_day = 31
                    df = h_func.execute_within_year(df, s_year, s_month, s_day, e_year, e_month, e_day, leap)
    df.to_excel(str(start_day)+"-"+str(start_month)+"-"+str(start_year)+" to "+str(end_day)+"-"+str(end_month)+"-"+str(end_year)+'.xlsx', index=False, index_label=None)

# To know the difference between the dates
delta = pd.to_datetime(end_date, format="%d/%m/%Y") - pd.to_datetime(start_date, format="%d/%m/%Y")
print(delta)

#If less than a month, then return the month number, else sepeate the dates
if delta.days < 33:
    print("less than 33 days")
else:
    separate_date(df, start_year, start_month, start_day, end_year, end_month, end_day)
    print("Completed")