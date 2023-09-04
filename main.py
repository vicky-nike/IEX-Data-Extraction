import helping_functions as h_func
import constants as const
from dateutil import parser
import pandas as pd
import os
from os import listdir

''' GIVE YOUR INPUTS HERE '''
delivery_type = const.delivery_type
#input the date in this format MM/DD/YY
start_date = const.start_date
end_date = const.end_date

''' MAIN CODE '''
start_year = parser.parse(start_date).year
start_month = parser.parse(start_date).month
start_day = parser.parse(start_date).day

end_year = parser.parse(end_date).year
end_month = parser.parse(end_date).month
end_day = parser.parse(end_date).day

''' *** if not using pandas then change this *** '''
delta = pd.to_datetime(end_date, format="%m/%d/%Y") - pd.to_datetime(start_date, format="%m/%d/%Y")

def separate_date(delivery_type, start_year, start_month, start_day, end_year, end_month, end_day):
    # Same year
    if end_year - start_year == 0:
        leap = h_func.check_leap_year(start_year)
        h_func.execute_within_year(delivery_type, start_year, start_month, start_day, end_year, end_month, end_day, leap)
    #For different years
    else:
        #in between two years
        for i in range (start_year, end_year+1, 1):
            leap = h_func.check_leap_year(start_year)
            print(i)
            # if its not leap year
            if leap == 0:
                if i == start_year:
                    s_month = start_month
                    print("start month", s_month)
                    e_month = 12
                    s_year = start_year
                    e_year = start_year
                    s_day = start_day
                    e_day = 31
                    h_func.execute_within_year(delivery_type, s_year, s_month, s_day, e_year, e_month, e_day, leap)
                elif i == end_year:
                    s_month = 1
                    e_month = end_month
                    s_year = end_year
                    e_year = end_year
                    s_day = 1
                    e_day = end_day
                    h_func.execute_within_year(delivery_type, s_year, s_month, s_day, e_year, e_month, e_day, leap)
                else:
                    s_month = 1
                    e_month = 12
                    s_year = i
                    e_year = i
                    s_day = 1
                    e_day = 31
                    h_func.execute_within_year(delivery_type, s_year, s_month, s_day, e_year, e_month, e_day, leap)

#files_directory = glob.glob(const.directory+'*')

print(os.path.abspath(os.curdir))
files_directory = const.directory
for f in listdir(files_directory):
    os.remove(files_directory+'/'+f)

if delta.days < 33:
    print(h_func.get_string_month(start_month))
else:
    separate_date(delivery_type, start_year, start_month, start_day, end_year, end_month, end_day)
    h_func.all_to_single(start_year, start_month, start_day, end_year, end_month, end_day)