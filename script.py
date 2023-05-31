import tabula
import re
from icalendar import Calendar, Event
from datetime import datetime

from pathlib import Path



# function to convert pdf to ics
cal = Calendar()


def convert_pdf_to_ics(df,reg1,reg2,reg3,ics_file):
    # create icalendar object
    
    # iterate over rows of dataframe
    for index, row in df.iterrows():
        # convert each cell to string, if cell is empty, convert to empty string
        cell_1 = str(row[0]) # in brackets is the column number
        cell_2 = str(row[1])
        cell_3 = str(row[2])
        summery_tbl = str(row[5])
        cast = str(row[4])
            
        # extract date, start time and end time from each row and convert to list
        date_list = re.findall(reg1, cell_1 or '')
        start_t_lst= re.findall(reg2, cell_2 or '')
        end_t_lst= re.findall(reg3, cell_3 or '')

        # if data shouldnt go in ics file, skip to next row
        if len(date_list)==0 or len(start_t_lst)==0 or len(end_t_lst)==0 or cast.lower() == 'kleiner chor':
                
            continue
        # format date and time to ics format
        else:
            dt_start = date_list[0][0] +' '+  start_t_lst[0]
            dt_end = date_list[0][0] +' '+ end_t_lst[0]
            if dt_start[-3]!= ':':
                dt_start += ':00'
            elif dt_end[-3]!= ':':
                dt_end += ':00'    
                
            # convert to datetime object
            dt_start_ob = datetime.strptime(dt_start, "%d.%m.%y %H:%M")
            dt_end_ob = datetime.strptime(dt_end, "%d.%m.%y %H:%M")
                
            # create ical event

            event = Event()
            event.add('Summary', summery_tbl)
            event.add('Description',cast)
            event.add('dtstart',dt_start_ob )
            event.add('dtend',dt_end_ob)
            cal.add_component(event)
        # write to ics file
    

def pdf_to_ics(pdf_file, ics_file):
    
    '''convert pdf file to ics file no return value'''
    # read pdf file and convert to dataframe tabula
    dfs = tabula.read_pdf(pdf_file, multiple_tables = True, pages='all') 
    # create icalendar object
    cal = Calendar()
    # reg for date string starts with a day, capture group 1 is the date
    reg_pattern_col_0 = r'^[A-Z][a-z]{1,2},*\s*((\d{1,2}\.){1,2}\d{1,2})' 
    # reg for start time, capture group 1 is the time
    reg_pattern_col_1= r'(^\s*\d+:\d+).+$' # reg to start hour incl 'Uhr'
    # reg to hours range, ending hour in capture group 1 
    reg_pattern_col_2 = r'^\s*\d+:\d+-(\d+[:]*\d*).*$' 

    for df in dfs:
        convert_pdf_to_ics(df,reg_pattern_col_0,reg_pattern_col_1, reg_pattern_col_2,ics_file_p)   
pdf_file_p = Path.cwd() / 'convertor/kinder.pdf' 

ics_file_p = Path.cwd() / 'convertor/kinder.ics'
# call function
pdf_to_ics(pdf_file_p, ics_file_p)

with open(ics_file_p, 'wb') as f:
        f.write(cal.to_ical())  












