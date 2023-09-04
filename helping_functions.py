from datetime import datetime
import os
import pandas as pd
import extract_web
import constants as const

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
    "2_L": 29
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

month_dict = {
    "1": "Jan",
    "2": "Feb",
    "3": "Mar",
    "4": "Apr",
    "5": "May",
    "6": "Jun",
    "7": "Jul",
    "8": "Aug",
    "9": "Sep",
    "10": "Oct",
    "11": "Nov",
    "12": "Dec"
}

def get_string_month(month):
    #return month is string on a integer value of month
    return month_dict[str(month)]

def check_leap_year(year):
    #check if the year is leap year
    if (year % 400 == 0) and (year % 100 == 0):
        return 1    #leap year

    # not divided by 100 means not a century year
    # year divided by 4 is a leap year
    elif (year % 4 ==0) and (year % 100 != 0):
        return 1

    # if not divided by both 400 (century year) and 4 (not century year)
    # year is not leap year
    else:
        return 0    #not leap year

def all_to_single(start_year, start_month, start_day, end_year, end_month, end_day):
    '''
    for any other location
    path_file = "C:/Users/Vicky/Downloads/"
    print(os.listdir(path_file))
    '''
    path_file = const.directory
    #print(os.listdir(path_file))       #list files in that directory

    date_dict = {}

    for filename in os.listdir(path_file):
        if filename.startswith('PriceMinute'):
            #print(filename)
            path_excel = os.path.join(path_file, filename)
            data_excel = pd.read_excel(path_excel, header=0, index_col=False)
            date_cell = data_excel.iloc[1, 0]       #to get the starting and ending date from excel
            s_date = date_cell.split()[1]           #start date
            #print(s_date)
            s_date = datetime.strptime(s_date, "%d-%m-%Y").date()
            e_date = date_cell.split()[3]           #end date in this excel
            #print(e_date)
            if s_date not in date_dict.keys():
                date_dict[s_date] = filename

    # Sorting the dictionary with dates and filenames
    date_dict = dict(sorted(date_dict.items()))
    iter_turn = 1
    #iterate through the dict by filenames
    for filename in date_dict.values():
        if iter_turn == 1:
            #print(filename)
            path_excel = os.path.join(path_file, filename)
            data_excel = pd.read_excel(path_excel, header=None, index_col=False)
            #print(data_excel)
            temp_table = data_excel
            #Removing the 2nd table from the excel
            loc = temp_table[temp_table[0]=="Date"]
            temp_table = temp_table.iloc[:(loc.index[0]-2)]
            #Selecting table except 1st and 2nd row
            temp_table = temp_table.drop([0, 1, 2], axis=0)
            new_table = temp_table
            iter_turn = 0
        else:
            print(filename)
            path_excel = os.path.join(path_file, filename)
            data_excel = pd.read_excel(path_excel, header=None, index_col=False)
            temp_table = data_excel
            #Removing the 2nd table from the excel
            loc = temp_table[temp_table[0]=="Date"]
            temp_table = temp_table.iloc[:(loc.index[0]-2)]
            #Selecting table except 1st, 2nd and 3rd row
            temp_table = temp_table.drop([0, 1, 2, 3], axis=0)
            new_table = pd.concat([new_table, temp_table], ignore_index=True)
            print(new_table)

    new_table.to_excel(str(start_day)+"-"+str(start_month)+"-"+str(start_year)+" to "+str(end_day)+"-"+str(end_month)+"-"+str(end_year)+'.xlsx', index=False, index_label=None, header=False)

def execute_within_year(delivery_type, start_year, start_month, start_day, end_year, end_month, end_day, leap):
    # if its not leap year
    if leap == 0:
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
            
            extract_web.run(delivery_type, str(start_year), get_string_month(i), str(s_day), str(end_year), get_string_month(i), str(e_day))
    #if its leap year
    else:
        # sepearate days for feb
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
            
            extract_web.run(delivery_type, str(start_year), get_string_month(i), str(s_day), str(end_year), get_string_month(i), str(e_day))