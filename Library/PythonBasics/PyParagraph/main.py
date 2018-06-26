###################################################################################################
# Description: Script to Automate the basic analysis of a passage by taking in a txt file
# Assumptions: Txt file is in the same working directory as this script
#              Script accounts for commas, periods and dashes
###################################################################################################
# Import Modules and File
###################################################################################################
import os
filename='Passage1.txt'
filepath=os.path.join(filename)
with open(filepath,'r') as text:
    lines=text.read()
    print("Paragraph Analysis")
    print("-------------------") 
    strlength=len(lines)   #Total Number of characters in passage (letters,space,punctuation)
###################################################################################################
#Approximate Word Count (split by space)
###################################################################################################
    words=lines.split(" ")  #store words in array
    numdashes=lines.count(" -")
    numwords=len(words)-numdashes    #obtain number of words
    print("Approximate Word Count: "+str(numwords))
###################################################################################################
# Approximate Sentence Count (split by period)
###################################################################################################
    numperiods=lines.count(".")
    print("Average Sentence Count: "+str(numperiods))
###################################################################################################
#Average Letter Count 
###################################################################################################
    numcommas=lines.count(",")
    numspaces=numwords
    avglettercount=(strlength-numspaces-numcommas-numperiods)/numwords
    print("Average Letter Count per Word: "+str(float(avglettercount)))  
##################################################################################################  
#Average Sentence Length (in words) - Take Word Count and Divide by Sentence Count
###################################################################################################
    sentencelength=float(numwords/numperiods)
    print("Average Sentence Length (in words): "+str(sentencelength))
################################################################################################
