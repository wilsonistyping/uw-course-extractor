from bs4 import BeautifulSoup

# Checks if the table is a course title/header
def is_title(self):
    return self.find('td', {'width': '50%'})

def is_section(self):
    return self.find('pre')