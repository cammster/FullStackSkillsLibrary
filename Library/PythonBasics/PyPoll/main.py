###############################################################################################
# Description: This script takes in a csv file with votes for candidates and outputs the tally
#              to the terminal and a txt file in same working directory
# Assumptions: Input file is a csv in the same working directory formatted with 3 columns:
#              1). VoterID
#              2). County
#              3). Candidate voted for
##############################################################################################
import os
import csv
filename='election_data_1.csv'
filepath=os.path.join(filename)
voterid=[]
candidate=[]
#################################################################################################
# Open File, Read Data, Count Votes
#################################################################################################
with open (filepath,'r',newline="") as csvfile:
    polldata=csv.reader(csvfile,delimiter=",") 
    for row in polldata:
        voterid.append(row[0])
        candidate.append(row[2])
del candidate[0]
votedfor=[]
for i in range(len(candidate)):
    if candidate[i] not in votedfor:
        votedfor.append(candidate[i])
print(votedfor)
votecount=[]
for cand in votedfor:
    votecount.append(candidate.count(cand))
print(votecount)
winningcount=max(votecount)
winindex=votecount.index(winningcount)
winner=votedfor[winindex]
totalvotes=len(voterid)-1
###############################################################################################
#Print Results
##############################################################################################
print("Election Results")
print("-------------------------")
print("Total Votes: "+str(totalvotes))
print("-------------------------")
for i in range(len(votedfor)):
    print(votedfor[i]+":"+str(round(((votecount[i]/totalvotes)*100),1))+"% ("+str(votecount[i])+")")
print("-------------------------")
print("Winner:"+winner)
print("-------------------------")
outputfilename='PyPolloutput.txt'
outfilepath=os.path.join(outputfilename)
with open(outfilepath,'w') as text:
    text.write("Election Results\n")
    text.write("-------------------------\n")
    text.write("Total Votes:"+str(totalvotes)+"\n")
    text.write("-------------------------\n")
    for i in range(len(votedfor)):
        text.write(votedfor[i]+":"+str(round(((votecount[i]/totalvotes)*100),1))+"% ("+str(votecount[i])+")\n")
    text.write("-------------------------\n")
    text.write("Winner:"+winner+"\n")
    text.write("-------------------------\n")
#######################################################################################################