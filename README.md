# PPI-Algorithm-Comparisons
Various scripts for processing result output from PPI prediction algorithms including PIPE, SPRINT and SPPS

# FormatResults.py
To format the outputs from SPRINT, PIPE and SPPS into a consistent format for further analysis, decreasingly orders the result scores. 

Usage:
python FormatResults.py -p /<directory of PIPE output files/> -s <directory of SPPS output files> -r <file containing SPRINT predictions> -o <output directory to store formatted result files>
