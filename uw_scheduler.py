from bs4 import BeautifulSoup
import requests
import json
import re
# from course_parser import *
from helpers import *

# Initial setup
filepath = "course_data/"
subject = "cse"
quarter = "AUT2023"
output_file = f"{filepath}{subject}.json"
page_to_scrape = requests.get(f'https://www.washington.edu/students/timeschd/{quarter}/{subject}.html')
soup = BeautifulSoup(page_to_scrape.text, "html.parser")

courses = []
current_course = None

tables = soup.find_all('table')

for table in tables:
    if is_title(table):
        # parse text and separate into 'code' and 'title'
        text = table.find('b').text.strip()
        text = text.replace('\xa0', ' ')
        text = re.sub(r'\s+', ' ', text)

        matches = re.match(r'(\S+\s+\S+)\s+(.*)', text)
        if matches:
            course_code = matches.group(1)
            course_title = matches.group(2)

            current_course = {
                'code': course_code,
                'title': course_title,
                'sections': []
            }
            courses.append(current_course)
        else:
            print("ERROR: course_header title string didn't match expected pattern")
        
    elif is_section(table) and current_course is not None:
        # parse text and separate into:
        # 'restrictions'
        # 'SLN'
        # 'section_id'
        # 'credits'
        # 'times'
        # 'building'
        # 'room'
        # 'instructor'
        # 'status'
        # 'enrollment'
        # 'enrollment_limit"
        # 'grades'
        # 'course_fee"
        # 'other"
       
        # making an assumption that properties will always be 
        # within a certain index range due to the nature of <pre>,
        # and extracting properties based on that assumption
        text = table.find('pre').text

        restrictions = text[0:7].strip()
        sln = text[7:14].strip()
        section_id = text[14:17].strip()
        credits = text[17:25].strip()

        if (text[25:43].strip() == 'to be arranged'):
            dates = 'TBD'
            times = 'TBD'
        else:
            dates = text[25:32].strip()
            times = text[32:43].strip()

        building = text[43:48].strip()
        room = text[48:57].strip()
        instructor = text[57:84].strip()
        status = text[84:91].strip()
        enrollment = text[91:95].strip()
        enrollment_limit = text[96:101].strip()
        grading = text[101:108].strip()
        course_fee = text[108:115].strip()

        other = text[115:].strip()
        # formatting for 'other'
        lines = other.splitlines()
        stripped_lines = [line.strip() for line in lines]
        other = '\r\n'.join(stripped_lines)

        current_course['sections'].append({
            'SLN': sln,
            'restrictions': restrictions,
            'section_id': section_id,
            'credits': credits,
            'dates': dates,
            'times': times,
            'building': building,
            'room': room,
            'instructor': instructor,
            'status': status,
            'enrollment': enrollment,
            'enrollment_limit': enrollment_limit,
            'grading': grading,
            'course_fee': course_fee,
            'other': other,
            'raw_string': table.find('pre').text
        })
        

# Write to JSON file
with open(output_file, "w") as json_file:
    json.dump(courses, json_file, indent=4)

