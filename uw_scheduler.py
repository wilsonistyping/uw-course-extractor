from bs4 import BeautifulSoup
import requests
import json
import re
# from course_parser import *
from helpers import *

# Initial setup
output_file = "course_data.json"
page_to_scrape = requests.get('https://www.washington.edu/students/timeschd/AUT2023/cse.html')
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
        
        # jesus christ don't ask about the regex pattern
        text = table.find('pre').text.strip()
        # pattern = r"(Restr)?\s*(\d+)?\s+(\w+)?\s+(\S+)?\s+(\w+)?\s+(\S+)?\s+(\w+)?\s+(\S+)?\s+(.+?)?\s+(Open|Closed|\d+)?\s+(\d+)/ *(\S+)?(.*)?"
        # pattern = r"(Restr)?\s*(\d+)?\s+(\w+)?\s+(\S+)?\s+(to be arranged|\w+)?\s+(\S+)?\s+(\w+)?\s+(\S+)?\s+(.+?)?\s+(Open|Closed|\d+)?\s+(\d+)/ *(\S+)?(.*)?"
        pattern = r"(Restr)?\s*(\d+)?\s+(\w+)?\s+(\S+)?\s+(to be arranged|\w+)?\s+(\d+-\d+)?\s+([A-Z]+)?\s+(\d+)?\s+(.+?)?\s+(Open|Closed|\d+)?\s+(\d+)/ *(\S+)?(.*)?"
        matches = re.match(pattern, text)

        if matches:
            restrictions = matches.group(1)
            SLN = matches.group(2)
            section_id = matches.group(3)
            credits = matches.group(4)
            dates = matches.group(5)
            times = matches.group(6)
            building = matches.group(7)
            room = matches.group(8)
            instructor = matches.group(9)
            status = matches.group(10)
            enrollment = matches.group(11)
            enrollment_limit = matches.group(12)
            other = matches.group(13)

            current_course['sections'].append({
                'SLN': SLN,
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
                'other': other,
                'section_string': table.find('pre').text.strip()
            })

# Write to JSON file
with open(output_file, "w") as json_file:
    json.dump(courses, json_file, indent=4)

