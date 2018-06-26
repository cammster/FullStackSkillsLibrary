# ###############################################################################################
# Description: Revenue Data is analyzed and a key summary provided
# Assumptions: Input file should be formatted such that
# ------------Column 1: Date as string sorted old to new, 1 entry per month, no blank months
# ------------Column 2: Revenue as string, without leading $
#################################################################################################
# Import Modules, Set FilePaths
#################################################################################################
import os
import csv
filename='budget_data_1.csv'
filepath=os.path.join(filename)
fileoutputname='PyBankOutput.txt'
fileoutputpath=os.path.join('PyBankOutput.txt')
################################################################################################
# Open CSV File, Write Dates and Revenues into 2 Lists
################################################################################################
datelist=[]
revenuelist=[]
datenum=[]
with open (filepath,'r',newline="") as csvfile:
    revenuedata=csv.reader(csvfile,delimiter=",") 
    for row in revenuedata:
        datelist.append(row[0])
        revenuelist.append(row[1])
################################################################################################
# Calculate Total Months (List Length - Title Row)
################################################################################################
nummonths2=len(datelist)-1  
################################################################################################
#Total Amount of Revenue Gained Over Entire Period
################################################################################################
revenueitems=len(revenuelist)
revnum=[]
for i in range(1,revenueitems):
    revnum.append(int(revenuelist[i]))
totalrev=sum(revnum)
#################################################################################################
#Calculate Average Revenue Change Between Months
################################################################################################# 
revchange=[]
revnumlength=len(revnum)
for i in range(1,revnumlength):
    revchange.append(revnum[i]-revnum[i-1])
avgrevchange=sum(revchange)/len(revchange)
#################################################################################################
#Greatest Increase in Revenue (date/amount) over entire period-MAX Change in Revenue
#################################################################################################
revmax=max(revchange)
revmaxindex=revchange.index(revmax)+1
dateslice=datelist[1:] 
datemax=dateslice[revmaxindex]
##################################################################################################
#Greatest Decrease in Revenue (date/amount) over entire period-MIN Change in Revenue
##################################################################################################
revmin=min(revchange)
revminindex=revchange.index(revmin)+1
datemin=dateslice[revminindex]
##################################################################################################
#Print Analysis to Terminal and Text File
print("Financial Analysis")
print("-----------------------------------")
print("Total Months: ",nummonths2)
print("Total Revenue: $",totalrev)
print("Average Revenue Change: $",avgrevchange)
print("Greatest Revenue Increase: ",datemax,revmax)
print("Greatest Revenue Decrease: ",datemin,revmin)
with open(fileoutputpath,'w') as text:
    text.write("Financial Analysis\n")
    text.write("-------------------\n")
    text.write("Total Months {}\n".format(nummonths2))
    text.write("Total Revenue: ${}\n".format(totalrev))
    text.write("Average Revenue Change: ${}\n".format(avgrevchange))
    text.write("Greatest Revenue Increase: {}\n".format(datemax,revmax))
    text.write("Greatest Revenue Decrease: {}\n".format(datemin,revmin))
####################################################################################################




