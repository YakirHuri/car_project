
#https://developers.google.com/gmail/api/guides/sending#python

import xmltojson
import json
import requests
import datetime
from datetime import date
import time
from datetime import datetime
import smtplib 
import sys
import os

class Company:

    def __init__(self, maker, wantedModels):

        self.wantedModels = wantedModels
        self.maker = maker




class CarEntity:

    def __init__(self):

        self.id = ''
        self.maker = ''
        self.carmodel =  ''
        self.car_type =  ''
        self.kilometers =  ''
        self.listprice =  ''
        self.owners =  ''
        self.img =  ''
        self.year = ''
        self.patch_text = ''
        self.finish_level = ''

    def fillData(self, raw_data):

        for filed_car_index in range(len(raw_data)):
            raw_line = raw_data[filed_car_index].split(':')
            if filed_car_index == 0:
                self.id = raw_line[0]
                
            elif raw_line[0] == '"maker"':
                self.maker = raw_line[1]
            elif raw_line[0] == '"carmodel"':
                self.carmodel = raw_line[1]
            elif raw_line[0] == '"car_type"':
                self.car_type = raw_line[1]
            elif raw_line[0] == '"kilometers"':
                self.kilometers = (int(raw_line[1].replace('"', '')+'000'))
            elif raw_line[0] == '"listprice"':
                self.listprice = (int(raw_line[1].replace('"', '')+'000'))
            elif raw_line[0] == '"owners"':
                self.owners = raw_line[1]
            elif raw_line[0] == '"img"':
                self.img = raw_line[1]+raw_line[2]
            elif raw_line[0] == '"year"':
                self.year = int(raw_line[1].replace('"', ''))
            elif raw_line[0] == '"patch_text"':
                self.patch_text = raw_line[1]
            elif raw_line[0] == '"finish_level"':
                self.finish_level = raw_line[1]

    def printDate(self):

        
        print('id ' + self.id)
        print('maker ' + self.maker)
        print('carmodel ' + self.carmodel)
        print('car_type ' + self.car_type)
        print('kilometers ' + str(self.kilometers))
        print('listprice ' + str(self.listprice))
        print('owners ' + self.owners)
        print('img ' + self.img)
        print('year ' + str(self.year))
        print('patch_text ' + str(self.patch_text))
        print('finish_level ' + str(self.finish_level))

        print('                     ')

    

def checkIfCarModelGood(wantedModels, carMd, price, maxPrice, year, minYear,  kilometers, maxKilometerss):

    for i in range(len(wantedModels)):

        if (wantedModels[i]== carMd and year >= minYear and price <= maxPrice):

            return True

    return False        


def sendMail(userMail, title, data_to_send):


    
    adminMail = "yakirhuri21@gmail.com"
    adminPassword = "yakir27keva"

    # creates SMTP session 
    email = smtplib.SMTP('smtp.gmail.com', 587) 
    
    # TLS for security 
    email.starttls() 
    
    # authentication
    # compiler gives an error for wrong credential. 
    email.login(adminMail, adminPassword ) 
    
    # message to be sent 
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (userMail, ", ".join(userMail), title, data_to_send)


    # sending the mail 
    email.sendmail(productMail, userMail, message) # from, to, msg
    
    # terminating the session 
    email.quit()


# סוזוקי: ויטרה, sx4, איגניס
# יונדאי: i25, i30, i35, טוסון, ix35, איוניק
# קיה: נירו, ספורטז׳, סיד


def main():

   
    final_cars_list = []    
    
    maxKim = 130000
    minYear = 2015
    maxPrice = 100000

    check_evry_min = 30

    companyHyundai = Company('hyundai', ['"i25"','"sx4"', '"i35"', '"i30"', '"טוסון"' ,'"ix35"'])
    companySuzuki = Company('suzuki',['"sx4"','"ויטרה"', '"איגניס"'])
    companyKia = Company('kia',['"נירו"','"ספורטאז׳"', '"סיד"'])
    compList = [companyHyundai, companySuzuki, companyKia]


    mailsToSend =['yakirhuri21@gmail.com','shellycarme@gmail.com']   
    
    titleFile = 'wanted : maxKim ' + str(maxKim) + ', minYear ' + str(minYear) +', maxPrice ' + str(maxPrice)
    print(titleFile)
    start_time = time.time()

    firstTimeChecking = False
    while True:

        end_time = time.time()
        diff_minutes = int(end_time - start_time)  / 60
        if not (diff_minutes  > check_evry_min) and firstTimeChecking == True:
            time.sleep(1)
            continue
        
        firstTimeChecking = True

        start_time = end_time
        print('ccccchecking ..........................')
        for comp in range(len(compList)):

            maker = compList[comp].maker
            wantedModels = compList[comp].wantedModels
            print(' check the maker: ' + maker)
            for pag_num in range(50):

                # Sample URL to fetch the html page
                url = "https://www.colmobil-tradein.co.il/cars/"+maker+"/?page=" + \
                    str(pag_num)+""

                # Headers to mimic the browser
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
                }

                # Get the page through get() method
                html_response = requests.get(url=url, headers=headers)

                json_obj = html_response.text

                if json_obj == None or json_obj == '':
                    break

                lines = json_obj.splitlines()

                substring = '"car_title":'

                for x in range(len(lines)):

                    if substring in lines[x]:

                        line_with_date = (lines[x])

                        cars_in_page = line_with_date.split('{"id":')

                        # loop each car
                        for i in range(len(cars_in_page)):
                            car_raw = (cars_in_page[i]).split(',')

                            car = CarEntity()
                            car.fillData(car_raw)


                            if (checkIfCarModelGood(wantedModels, car.carmodel, car.listprice, maxPrice, car.year, minYear, 
                                car.kilometers, maxKim)):

                                final_cars_list.append(car)
        

        ##########################################################
        ### FINAL LIST
        print('##########################################################')
        print(' found total relevant cars: ' +str(len(final_cars_list)))

        if(len(final_cars_list) > 0):

            # title = ' we found for you '+str(len(final_cars_list)) +' relevant cars'
            now = datetime.now()
            dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
            file_name = str(dt_string+'.txt')
            with open(file_name, "w") as f:
                
                f.write(titleFile+'\n')
                for i in range(len(final_cars_list)):
                    
                    final_cars_list[i].printDate()                    
    
                    f.write('id ' + final_cars_list[i].id+'\n')
                    f.write('maker ' + final_cars_list[i].maker+'\n')
                    f.write('carmodel ' + final_cars_list[i].carmodel+'\n')
                    f.write('car_type ' + final_cars_list[i].car_type+'\n')
                    f.write('kilometers ' + str(final_cars_list[i].kilometers)+'\n')
                    f.write('listprice ' + str(final_cars_list[i].listprice)+'\n')
                    f.write('owners ' + final_cars_list[i].owners+'\n')
                    f.write('img ' + final_cars_list[i].img+'\n')
                    f.write('year ' + str(final_cars_list[i].year)+'\n')
                    f.write('patch_text ' + str(final_cars_list[i].patch_text)+'\n')
                    f.write('finish_level ' + str(final_cars_list[i].finish_level)+'\n')
                    f.write('                           '+'\n')
            f.close()

            #sendMail("yakirhuri21@gmail.com", title, msg)

        





   


if __name__ == "__main__":

   
    main()
