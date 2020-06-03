# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 14:40:35 2020

@author: kpurc

these were websites I found helpful in making this
https://pythonprogramming.net/tables-xml-scraping-parsing-beautiful-soup-tutorial/
https://stackoverflow.com/questions/22410416/beautifulsoup-extracting-data-from-multiple-tables
https://www.almanac.com/content/when-water-your-vegetable-garden-watering-chart

since this is one of the first times I used GUI in Python I relied heavily on the first link and found 
    help in the second link ofr style changes
https://github.com/spyder-ide/spyder/wiki/How-to-run-PyQt-applications-within-Spyder
https://www.geeksforgeeks.org/pyqt5-how-to-change-color-of-the-label/


The weather websites can be reached through the links in the Beautiful Soup code
"""


#program to fetch the water level and temp of the past 3 days
#im going to use this to know if I need to water my garden


from bs4 import BeautifulSoup
from urllib.request import urlopen

water_link = "https://w1.weather.gov/data/obhistory/KPTW.html" #the link to pottstown, PA ariport weather
html = urlopen(water_link)
soup = BeautifulSoup(html, 'html.parser')
table = soup.find_all('table') #use find all cause theres more than one table in the HTML
rows = table[3].find_all('tr') #find when the HTML goes to new line 'tr' to find the lines
                                #table[3] since its the fourth 'table' in the HTML


temp = [] #declaring the list globaly so we can use the results outside the for loop
for tr in rows[3:-3]: #this is finding when the row divides into another table element
    td = tr.find_all('td')[6:-11] # 'td' is the new element HTML code 
                                    # the 7th element is the temp we want
    row_temp = [i.text for i in td]  #this makes it look nice
    #row_temp = list(map(int,row_temp))
    temp.append(int("".join(row_temp)))
    #print(temp) #now we have all the temps we want

    
#last 3 lines are the precip. if it is empty it didnt rain, last 1 hr, 3 hr, 6 hrs
    #measured in inches, we would want the first element hour because it updated every hour
    
rain = []
for tr in rows[3:-3]:
    td = tr.find_all('td')[15:-3]# the 16th element is the temp we want
    row_rain = [i.text for i in td] 
    if row_rain == []:
        row_rain = '0'
    else:
        row_rain=row_rain

    rain.append(int("".join(row_rain)))
    #print(row_rain) #now we have all the rain inches we want
    
avg_temp = sum(temp)/len(temp)
avg_rain = sum(rain)/len(rain)

#print(avg_temp,avg_rain)

#it is too hot if it is over 70 degrees average and should be watered more
#the garden needs abt 1 inch of water a week so we are looking for .5 avg per 3 days to be safe
#my plants need extra water anyway so this is a good check



pred_link = "https://forecast.weather.gov/MapClick.php?lat=40.2578&lon=-75.7264&unit=0&lg=english&FcstType=dwml" #the link to pottstown, PA ariport weather
html = urlopen(pred_link) #finding the chance of rain in the next 3 days
soup = BeautifulSoup(html, 'html.parser')
table_p = soup.find_all('probability-of-precipitation') #use find all cause theres more than one table in the HTML
#rows = table.find_all('value') #find when the HTML goes to new line 'tr' to find the lines
                                #table[3] since its the fourth 'table' in the HTML
value = soup.find_all('value')
pred = [i.text for i in value]
pred = [int(i) for i in pred[14:23]] #we only want the percents for rain
avg_pred = sum(pred)/len(pred)


#if the average is higher than 25% we can assume it will rain or be cloudy/humid enough to not water
   


def message(avg_pred,avg_rain,avg_temp):
    if avg_pred > 45:
        mess = ("Don't water the garden, it's going to rain a lot soon.") 
    elif avg_pred > 25:
        mess = ("You don't have to water. It should rain soon.")
    elif avg_rain < 0.2:
        mess = ("You need to water the garden.")
    elif avg_rain < 0.5:
        mess = ("You should think about watering the garden.")
    elif avg_temp > 80 and avg_rain < 0.6:
        mess = ('You really should water the garden.')
    elif avg_temp > 70 and avg_rain < 0.7:
        mess = ('You really should water the garden.')
    else:
        mess = ('The garden should be fine. Its warm and wet. Don\'t worry!')
    return mess

'''
#comment this out since we are using the GUI    
print("\n Here is my prediction for your garden in the Pottstown area: \n ")
print(message(avg_pred,avg_rain,avg_temp))
print("\n\n")
print('The average temp of the past 3 days was %1.2f F\N{DEGREE SIGN} and the average rainfall has been %i inches. \n' % (avg_temp, avg_rain))
print('The predicted rainfall as a percent, incramented in 12 hr intervals over the next few days is: ')  
print(str(pred).strip('[]')+'\n\n Please plan accoringly. \n Thanks for using the program!')
'''
   



 
'''
NOW WE ARE GOING TO PRINT THAT ALL OUT NICELY ON THE GUI
'''

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QSize    
     
class GardenWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
 
        self.setMinimumSize(QSize(300, 300))    
        self.setWindowTitle("Garden Time") 
        
        centralWidget = QWidget(self)          
        self.setCentralWidget(centralWidget)   
 
        gridLayout = QGridLayout(self)     
        centralWidget.setLayout(gridLayout)
        self.setStyleSheet("background : lightgreen;")
 
        title = QLabel("Here is my prediction for your garden in the Pottstown area: ", self) 
        title.setAlignment(QtCore.Qt.AlignCenter)
        gridLayout.addWidget(title, 0, 0)
        
        title2 = QLabel(message(avg_pred,avg_rain,avg_temp), self)
        title2.setStyleSheet("color: white; background-color: darkgreen; border: 1px solid black; text: white;")
        title2.setAlignment(QtCore.Qt.AlignCenter)
        gridLayout.addWidget(title2, 100, 0)
        
        title3 = QLabel('The average temp of the past 3 days was %1.2f F\N{DEGREE SIGN} and the average rainfall has been %i inches.' % (avg_temp, avg_rain), self) 
        title3.setAlignment(QtCore.Qt.AlignCenter)
        gridLayout.addWidget(title3, 200, 0)
        
        title4 = QLabel('The predicted rainfall as a percent, incramented in 12 hr intervals over the next few days is: ', self) 
        title4.setAlignment(QtCore.Qt.AlignCenter)
        gridLayout.addWidget(title4, 300, 0)
        
        title5 = QLabel(str(pred).strip('[]')+'\n\n Please plan accordingly. \n Thanks for using the program!', self) 
        title5.setAlignment(QtCore.Qt.AlignCenter)
        gridLayout.addWidget(title5, 400, 0)
      

if __name__ == "__main__":
    def run_app():
        app = QtWidgets.QApplication(sys.argv)
        mainWin = GardenWindow()
        mainWin.show()
        app.exec_()
    run_app()
