import requests
import xlwt
from xlwt import Workbook 
from bs4 import BeautifulSoup
 
   

#Setup for reading site data
URL = 'https://www.irrigationaustralia.com.au/search-directory/search/?command=getresults&pageNo=1&Filter::StreetState::SelectOne=NSW&LocationRadius=100&Filter::Category::SelectOne=Certified+Meter+Installer'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id='directoryResults')
count=1


#Setup excel
serchRes=results.find_all(class_='searchResults clearfix')
wb = Workbook()      
sheet1 = wb.add_sheet('Sheet 1') 
sheet1.write(0, 0, 'Name') 
sheet1.write(0, 1, 'Address') 
sheet1.write(0, 2, 'Email') 
sheet1.write(0, 3, 'Tel' )
sheet1.write(0, 4, 'Website')
sheet1.write(0, 5, 'Image')


lines=1
thereisData=True
#Iterate through the data
while(thereisData): 
     for sec in serchRes :
          companyName = sec.find("h3")
          companyAddress = sec.find("div", class_="address")
          CompanyTel= sec.find("div", class_="phone")
          CompanyEmail= sec.find("div", class_="email")
          CompanyImage= sec.find("img")
          companyWeb=""
          companyImg=""
          add=str(companyAddress.text.strip())
          add=add.replace('\n','').replace('\r','').replace('\t',' ') 
          for link in sec.find_all('img'):
                companyImg=link.get('src')
          for link in sec.find_all('a'):
                companyWeb=link.get('href')
          sheet1.write(lines, 0, companyName.text.strip())  
          sheet1.write(lines, 1, add) 
          sheet1.write(lines, 2, CompanyEmail.text.strip()) 
          sheet1.write(lines, 3, CompanyTel.text.strip()) 
          sheet1.write(lines, 4, companyWeb)
          sheet1.write(lines, 5, companyImg)

          lines+=1
     URL=URL.replace("pageNo="+str(count),"pageNo="+str(count+1)) 
     count+=1
     page = requests.get(URL)
     soup = BeautifulSoup(page.content, 'html.parser')
     results = soup.find(id='directoryResults')
     serchRes=[]
     serchRes=results.find_all(class_='searchResults clearfix')
     if not serchRes :  
         thereisData=False
     #count+=1
#
wb.save('SearchResults.xls') 
print("cont is : %d",count)
#         location_elem = job_elem.find("div", class_="location")
#job_elems = results.find_all('section', class_='card-content')
#for job_elem in job_elems:
#    print("===================================================\n===============================================")
#    print(job_elem, end='\n'*2)
#
## Print out all available jobs from the scraped webpage
#job_elems = results.find_all("section", class_="card-content")
#for job_elem in job_elems:
#    title_elem = job_elem.find("h2", class_="title")
#    company_elem = job_elem.find("div", class_="company")
#    location_elem = job_elem.find("div", class_="location")
#    if None in (title_elem, company_elem, location_elem):
#        continue
#    print(company_elem.text.strip())
#    print(location_elem.text.strip())
#    print()