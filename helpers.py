from bs4 import BeautifulSoup
import re

# Checks if the table is a course title/header
def is_title(self):
    return self.find('td', {'width': '50%'})

def is_section(self):
    return self.find('pre')

def has_additional_meeting_times(self):
    return is_valid_date(self[7:16])

def is_valid_date(self):
    return re.match(r'\d{3,4}-\d{3,4}', self)

def extract_dates(date_str):
    days = []

    i = 0
    while i < len(date_str):
    # Check if the current character is 'Th'
        if i + 1 < len(date_str) and date_str[i:i+2] == 'Th':
            days.append('Th')
            i += 2
        else:
            day = date_str[i]
            days.append(day)
            i += 1
    return days

def standardize_time_string(time_str):
    parts = time_str.split('-')
    # pm_start = False

    # if the last character of part[0] is P, set pm_start to true and remove P
    # if parts[0][-1] == 'P':
    #     pm_start = True
    #     parts[0] = parts[0][:-1]

    for part in parts:
        if len(part) == 3:
            part = '0' + part

    # start_time = parts[0][:2] + ':' + parts[0][2:]
    # end_time = parts[1][:2] + ':' + parts[1][2:]

    start_hours = int(parts[0][:len(parts[0]) - 2])
    start_minutes = (parts[0][-2:])
    end_hours = int(parts[1][:len(parts[1]) - 2])
    end_minutes = int(parts[1][-2:])

    # Adjust hours based on AM/PM
    start_period = "AM" if parts[0][-1] == 'P' else "AM"
    end_period = "AM" if parts[0][-1] == 'P' else "AM"

    start_minutes = start_minutes[:-1]
    start_minutes = int(start_minutes)

    # Adjust AM/PM based on the hours
    if start_hours >= 12:
        start_period = "PM"
        if start_hours > 12:
            start_hours -= 12

    if end_hours >= 12:
        end_period = "PM"
        if end_hours > 12:
            end_hours -= 12

    # Format the times
    start_time = f"{start_hours}:{start_minutes:02d} {start_period}"
    end_time = f"{end_hours}:{end_minutes:02d} {end_period}"

    return f"{start_time} - {end_time}"
        

print(standardize_time_string("430P-1050"))