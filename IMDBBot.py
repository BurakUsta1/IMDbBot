from curses.ascii import isalnum
import os,csv
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class ımdb:
    def __init__(self):
        #Selnium to show only important alerts when running
        self.options = Options()
        self.options.add_argument("--log-level=3")
        self.browser = webdriver.Edge(options=self.options)
    
    def singIn(self):
        #Get the IMDb Ratings List address from the user and open them.
        self.link= input("\n"+'\033[93m'+"Enter the full address of your ratings list:"+'\033[97m')
        self.browser.get(self.link)
           
    def MakeCSV(self,fileName):
        #Save the CSV file to the location where IMDBBot runs.
        columnTittle=["Title","Title Type","IMDb Rating","RateCount","Your Rating","Date Rated","Director","ReleaseYear","Runtime","Link"]
        self.fileName=fileName
        print("\nCreating "+'\033[93m'+self.fileName+'\033[97m'+" file...\n")
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.csv_file_path = os.path.join(self.script_directory, self.fileName)
        with open(self.csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(columnTittle)

    def RatingList(self):

        #Total number of ratings 
        try:                           
            RatingCount= WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/main/div/section/div/section/div/div[1]/section/div[1]/ul/li"))).text
            print("\n"+RatingCount [:5] +"entry found.\n\nEntry are being prepared...")
            lis = self.browser.find_elements(By.CLASS_NAME,"ipc-metadata-list-summary-item")
        except TimeoutException:
            print("Zaman aşımına uğradı, sayfa beklenen şekilde yüklenmedi.")
        #Pull the slider down until the entire rating list is created.
        while int(RatingCount[:4]) != len (lis):
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.98);")
            lis = self.browser.find_elements(By.CLASS_NAME,"ipc-metadata-list-summary-item")
            continue
        else:
            #Create the csv file.
            self.MakeCSV('Rating List.csv')

            #Get the data
            for i,item in enumerate(lis):
                
                progress = (i + 1) / len(lis)
                barLength = 20
                bar = "█" * int(progress * barLength) + "-" * (barLength - int(progress * barLength))
                print('\033[93m' + f"\rLoading: [{bar}] %{int(progress * 100)}", end="")


                try:
                    Title = item.find_element(By.CLASS_NAME,"ipc-title__text").text
                except:
                    Title = " "
                try:
                    IMDbRating = item.find_element(By.CLASS_NAME, "ipc-rating-star--rating").text
                except:
                    IMDbRating=" "
                try:
                    Count = item.find_element(By.CLASS_NAME, "ipc-rating-star--voteCount").text
                    RateCount = Count.replace("(", "").replace(")", "")
                except:
                    RateCount=" "
                try:
                    YourRating = item.find_elements(By.CLASS_NAME, "ipc-rating-star--rating")[1].text
                except:
                    YourRating=" "
                try:
                    DateRated= item.find_element(By.CLASS_NAME, "sc-300a8231-10.bFZWGu.dli-user-list-item-date-added").text
                except:
                    DateRated=" "
                try:
                    Director= item.find_element(By.CLASS_NAME, "ipc-link.ipc-link--base.dli-director-item").text
                except:
                    Director=" "
                try:
                    ReleaseYear=item.find_elements(By.CLASS_NAME,"sc-300a8231-7.eaXxft.dli-title-metadata-item")[0].text
                except:
                    ReleaseYear=" "
                try:
                    Runtime=item.find_elements(By.CLASS_NAME,"sc-300a8231-7.eaXxft.dli-title-metadata-item")[1].text
                except:
                    Runtime=" "
                try:
                    TitleType=item.find_element(By.CLASS_NAME,"sc-300a8231-4.gICisZ.dli-title-type-data").text
                except:
                    TitleType="Movie"
                try:
                    Link= item.find_element(By.CLASS_NAME,"ipc-title-link-wrapper").get_attribute("href")
                except:
                    Link=" "

                #Write the data to CSV file
                try:   
                    row= [Title,TitleType,IMDbRating,RateCount,YourRating,DateRated[9:],Director,ReleaseYear,Runtime,Link]
                    with open(self.csv_file_path, mode='a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow(row)
                except Exception as e:
                    print("HATA",e)
            print ("\n\n"+'\033[97m'+str(len(lis))+" lines successfully written to "+'\033[93m'+self.fileName+'\033[97m'+" file.\n\nThe file is saved to "+'\033[93m'+self.script_directory+'\033[97m'+" location." )
ımdb=ımdb()
ımdb.singIn()
ımdb.RatingList()
