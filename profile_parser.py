# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 14:52:43 2020

@author: Melissa Gray
"""

'''
Parsing profiler data
'''
#%% VARIABLES

# samples [sample #] [rank] [taxid] --->> Abundance

#%% FUNCTIONS
'''
Input: string - first part of file name
Output: list - of the contents of the file

The ".profile" extension will be added here.
File will be opened, read, and contents saved in a returned variable
'''
def getfile(f):
    filename = f + ".profile"
    file = open(filename, "r")
    contents = file.readlines()
    file.close()
    return contents

'''
Input: list - content of a profile file
Output: list of lists with file content in them

Divides the file contents by sample ID
'''
def divContent(con):
    cutoff = "@SampleID:marmgCAMI2_short_read_sample_"
    loop = 0
    parts = []
    c_pos = [0]
    
    for l in con:
        if cutoff in l:
            loop += 1
    
    #Cycle through backwards?
    for i in range(loop):
        c_pos.append(con.index(cutoff+str(i)+"\n", c_pos[-1]))
    
    for j in range(10):
        try:
            p = con[c_pos[j+1]:c_pos[j+2]]
        except IndexError:
            p = con[c_pos[j+1]:]
        parts.append(p)
    
    return parts

'''
Input: list - a part (sample)
Output: integer - the sample number

Checks each string in the part list for the @SampleID line
Takes the nunmber at the end, turns it into an integer
'''
def _getSampleNum(part):
    s = -1
    for line in part:
        if "@SampleID:marmgCAMI2_short_read_sample_" in line:
                s = int(line[-2])
                break
    return s

'''
Input: list - the split line from a part (sample)
Output: a float - the abundance value

Turns "e" into 10^ and the string into a float number
'''
def _turnNum(temp_l):
    val = 0
    
    if len(temp_l) > 1:
        b = temp_l[-1].replace("\n", "")
        if "e" in b:
            c = b.split("e")
            val = float(c[0])*(10**int(c[1]))
        else:
            try:
                val = float(b)
            except ValueError:
                val = b
                #print("skipped:", b)
    return val

'''
Input: list - a part (sample)
Output: list - of rank dictionaries

Checks which rank is in each line and saves the TaxID and Abundance value
into its respective rank dictionary.
'''
def _parseTA(part):
    strain = {}
    species = {}
    genus = {}
    fam = {}
    order = {}
    clss = {}
    phylum = {}
    sprkd = {}
    
    for l in part:
        t_l = l.split("\t")
        v = _turnNum(t_l)
        if "strain" in t_l:
            strain[t_l[0]] = v
        elif "species" in t_l:
            species[t_l[0]] = v
        elif "genus" in t_l:
            genus[t_l[0]] = v
        elif "family" in t_l:
            fam[t_l[0]] = v
        elif "order" in t_l:
            order[t_l[0]] = v
        elif "class" in t_l:
            clss[t_l[0]] = v
        elif "phylum" in t_l:
            phylum[t_l[0]] = v
        elif "superkingdom" in t_l:
            sprkd[t_l[0]] = v
    
    return [strain, species, genus, fam, order, clss, phylum, sprkd]

'''
Input: list - of rank dicationaries, list - rank names
Output: dictoinary - where rank name is the key and the rank dictionary is the
value
'''
def _parseRank(rd, r):
    sr = {}
    
    for i in range(len(rd)):
        sr[r[i]] = rd[i]
    
    return sr

'''
Input: list - of lists of the separated sample content
Output: dictionary - where the key is the sample number and a dictionary of 
ranks is the value

Data Tree:
    - {Sample # : dict}
                - {rank : dict}
                        - {TaxID : Abundance}

Finds, separates, and stores the various parts of data in a dictionary
'''
def parseData(parts):
    samples = {}
    ranks = ["strain", "species", "genus", "family", "order", "class", "phylum", "superkingdom"]
    
    for p in parts:
        sn = _getSampleNum(p)
        
        pd = _parseTA(p)
        sr = _parseRank(pd, ranks)
        
        samples[sn] = sr
            
    return samples

'''
Input: dictionary - one of the samples
Output: formats the dictionary content
'''
def print_sample(n, s):
    print("Sample Number:", n)
    for r in s:
        print("\tRank:", r)
        for t in s[r]:
            print("\t\t\t{}\t:\t{}".format(t, s[r][t]))
    return

#%% MAIN
if __name__ == "__main__":
    f = input("Which file: \n")
    Samples = parseData(divContent(getfile(f)))
    
    print_sample(0, Samples[0])