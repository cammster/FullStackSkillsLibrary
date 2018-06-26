##################################################################################################
# Desciption: This script reads a file of employee information and reformats it by performing 
#             the following operations:
#             -Splits name into first and last name 
#             -Reorders date to read d/m/Y
#             -Display last 4 digits of SSN only
#             -Display state as abbreviation
# This information is output to a csv file in same working directory
# # Assumptions: The input file is a csv containing the following pieces of information:
#              1) Employee ID
#              2) Name (containing first and last with a space between)
#              3) Date of Birth m/d/Y
#              4) SSN (***-**-****)
#              5) State with full spelling
#               Input file is assumed to be in same working directory
###################################################################################################
import os
import csv
us_state_abbrev = {'State':'ST','Alabama': 'AL','Alaska': 'AK','Arizona': 'AZ','Arkansas': 'AR',
    'California': 'CA','Colorado': 'CO','Connecticut': 'CT','Delaware': 'DE','Florida': 'FL',
    'Georgia': 'GA','Hawaii': 'HI','Idaho': 'ID','Illinois': 'IL','Indiana': 'IN','Iowa': 'IA',
    'Kansas': 'KS','Kentucky': 'KY','Louisiana': 'LA','Maine': 'ME','Maryland': 'MD',
    'Massachusetts': 'MA','Michigan': 'MI','Minnesota': 'MN','Mississippi': 'MS','Missouri': 'MO',
    'Montana': 'MT','Nebraska': 'NE','Nevada': 'NV','New Hampshire': 'NH','New Jersey': 'NJ',
    'New Mexico': 'NM','New York': 'NY','North Carolina': 'NC','North Dakota': 'ND','Ohio': 'OH',
    'Oklahoma': 'OK','Oregon': 'OR','Pennsylvania': 'PA','Rhode Island': 'RI','South Carolina': 'SC',
    'South Dakota': 'SD','Tennessee': 'TN','Texas': 'TX','Utah': 'UT','Vermont': 'VT',
    'Virginia': 'VA','Washington': 'WA','West Virginia': 'WV','Wisconsin': 'WI', 'Wyoming': 'WY',
}
filename1='employee_data1.csv'
filepath1=os.path.join(filename1)
employeeid=[]
firstname=[]
lastname=[]
dob=[]
ssn=[]
state=[]
info=[]
###################################################################################################
#Open File, Collect Data and Reformat (title row is deleted to ensure proper reformatting)
##################################################################################################
with open (filepath1,'r',newline='') as csvfile:
    filedata=csv.reader(csvfile,delimiter=",")
    for row in filedata:
        info.append(row)
del info[0]
for person in info:
    employeeid.append(person[0])
    firstname.append(person[1].split(" ")[0])
    lastname.append(person[1].split(" ")[1])
    dob.append(person[2].split("/")[1]+"/"+person[2].split("/")[0]+"/"+person[2].split("/")[2])
    ssn.append("****-**-"+person[3][-4:])
    state.append(us_state_abbrev[person[4]])
#################################################################################################
# Output to File 
#################################################################################################
outputrows=zip(employeeid,firstname,lastname,dob,ssn,state)   
fileoutputname='PyBossOutput.csv'
fileoutputpath=os.path.join(fileoutputname)
with open (fileoutputpath,'w', newline='') as csvfile:
    outputdata=csv.writer(csvfile,delimiter=",")
    outputdata.writerow(["Emp ID","First Name","Last Name","DOB","SSN","State"])
    for row in outputrows:
        outputdata.writerow(row)
###################################################################################################