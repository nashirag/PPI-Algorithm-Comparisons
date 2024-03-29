import sys
import numpy as np
import pandas as pd
import glob
import argparse
import re

#PARSE COMMAND LINE ARGUMENTS FOR LOCATION OF PIPE FILES, SPPS FILES, AND SPRINT FILE
parser = argparse.ArgumentParser()

parser.add_argument("--pipe", "-p", help="the directory containing the pipe result files")
parser.add_argument("--spps", "-s", help="the directory containing the spps result files")
parser.add_argument("--sprint", "-r", help="the file containing the sprint predicted PPIs")
parser.add_argument("--out", "-o", help="the directory to put the formatted and sorted PPI pairs and scores")

args = parser.parse_args()

#CHECK USER INPUT
if args.pipe is None:
    print("ERROR: You need to specify a proper directory for PIPE results. The directory: " + args.pipe + " was not accepted.")
elif args.spps is None: 
    print("ERROR: You need to specify a proper directory for SPPS results. The directory: " + args.spps + " was not accepted.")
elif args.sprint is None:
    print("ERROR: You need to specify a proper directory for SPRINT results. The directory: " + args.sprint + " was not accepted.")

#RESULT FORMATTING FOR RESULT OUTPUT OF PIPE, SPRINT, AND SPPS FOR INPUT INTO R

#PIPE
#READ IN PIPE RESULT OUTPUT FILES TO CREATE ONE RESULT FILE
pipe_files = glob.glob(args.pipe + '/*.out')
i = 0
pi = []
print("Now reading PIPE files \n")
for filename in pipe_files:
    pf = pd.read_csv(filename, sep='\t', names=['protein_a', 'protein_b', 'PIPE_score', 'Matrix_max', 'running_time', 'sim_weighted_score_old', 'sim_weighted_score_new', 'site1_height', 'site1a_start', 'site1a_end', 'site1b_start', 'site1b_end', 'site2_heaight', 'site2a_start', 'site2a_end', 'site2b_start', 'site2b_end', 'site3_height', 'site3a_start', 'site3a_end', 'site3b_start', 'site3b_end'])
    #MERGE FIRST AND SECOND COLUMN TO CREATE PROTEINS COLUMN
    pf['proteins'] = pf['protein_a']+ ' ' + pf['protein_b']
    fd = pf[['proteins', 'sim_weighted_score_new']]
    pi.append(fd)
    if i % 100 == 0:
        print(str(i) + " files read.")
    i+=1
pipeep4 = pd.concat(pi, axis=0)   #Concat everything together
pipeep4.to_csv(args.out + '/combinedPIPE.csv', sep='\t', index=None)   #Output to a csv file
print("Done reading PIPE files.\n")

#SORT PIPE RESULTS AND OUTPUT INTO A SORTED FILE FOR FURTHER ANALYSIS
psorted = pipeep4.sort_values(by='sim_weighted_score_new', ascending=False)
psorted.to_csv(args.out + '/sortedPIPE.csv', sep='\t', index=None)

#SPPS
#READ IN SPPS FILES
print("Now reading SPPS files\n")
spps_files = glob.glob(args.spps + '/*.spps')

#GO THROUGH THE SPPS FILES AND APPEND THEM TO A DATAFRAME
si = []
for filename in spps_files:
    df = pd.read_csv(filename, sep='\t')
    #ADD COLUMN FOR FILE NAME AND MERGE NAMES COLUMN TO CREATE PROTEINS COLUMN
    tempname = re.sub('\.spps$', '', filename)
    epname = re.sub(args.spps + '/' , '', tempname)
    df['proteins'] = epname + '-' + df['Names']
    fd = df[['proteins', '1']]   #Keep '1' scores and proteins column
    si.append(fd)
f = pd.concat(si, axis=0)

#SORT SPPS DATAFRAME OF ALL VALUES AND OUTPUT TO CSV FILE
sppsep4 = f.sort_values(by='1', ascending=False)
f.to_csv(args.out + '/combinedSPPS.csv', sep='\t', index=None)
sppsep4.to_csv(args.out + '/sortedSPPS.csv', sep='\t', index=None)
print("Finished reading SPPS files.\n")

#SPRINT
#READ IN SPRINT RESULT FILE
df = pd.read_csv(args.sprint, sep=' ', header=None)
print("Now reading SPRINT file.\n")

#ISOLATE ONLY EP4 PREDICTIONS
temp = df[df[1].str.contains("EP4")]

#SORT THE EP4 PREDICTIONS
results = temp.sort_values(by=2, ascending=False)

#SEND TO CSV FILE FOR FURTHER ANALYSIS
results.to_csv(args.out + '/sortedSPRINT.txt', sep='\t', index=False)
print("Done reading SPRINT file.\n")
