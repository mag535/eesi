# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 14:52:43 2020

@author: Melissa Gray

Parsing profiler data
"""


#%% VARIABLES

import re

# samples [sample #] [rank] [taxid] --->> Abundance
'''
Data Tree:
    - {Sample # : dict}
                - {rank : dict}
                        - {tax_id : abundance}
'''


#%% FUNCTIONS

def get_file(f):
    '''

    Parameters
    ----------
    f : string
        first part of the profile file name (don't include the ".profile" part)

    Returns
    -------
    contents : list
        containing all the lines of the file as strings

    '''
    filename = f + ".profile"
    file = open(filename, "r")
    contents = file.readlines()
    file.close()
    return contents

def divide_content(content):
    '''

    Parameters
    ----------
    content : list
        containing all the lines of the file as strings

    Returns
    -------
    parts : list
        where the elements are sections of content, separated by sample number

    '''
    cutoff = "@SampleID:"
    loop = 0
    parts = []
    cutoff_pos = [0]
    
    for l in content:
        if cutoff in l:
            loop += 1
    
    #Cycle through backwards?
    '''
    for i in range(loop):
        cutoff_pos.append(content.index(cutoff+str(i)+"\n", cutoff_pos[-1]))
    
    for j in range(loop):
        try:
            p = content[cutoff_pos[j+1]:cutoff_pos[j+2]]
        except IndexError:
            p = content[cutoff_pos[j+1]:]
        parts.append(p)
    '''
    try:
        content_str = ""
        for l in content:
            content_str += l
        parts2 = re.split("@SampleID:", content_str)
        parts2.pop(0)
        for p in parts2:
            parts.append(p.split("\n"))
    except:
        print("an error occured in *div_content()*.")
    
    return parts

def _get_sample_number(part):
    '''

    Parameters
    ----------
    part : list
        containing lines (as strings) from one sample in a profile

    Returns
    -------
    s : int
        the sample number

    '''
    return int(part[0][-1])

def _turn_into_number(temp_l):
    '''

    Parameters
    ----------
    temp_l : list
        a line from the sample split by tabs

    Returns
    -------
    val : float / string
        The abudance value from the sample line

    '''
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
    return val

def _get_ranks(content):
    ranks = []
    
    for element in content:
        if "@Ranks" in element:
            r = element.split(":")
            ranks = r[1].split("|")
            last = ranks[-1]
            ranks[-1] =  last.strip()
            break
    return ranks

def _parse_rank(rank, part):
    tax_id_holder = {}
    
    for line in part:
        t_l = re.split("\t| +", line)
        if rank in t_l:
            val = _turn_into_number(t_l)
            tax_id_holder[t_l[0]] = val
    
    return tax_id_holder

def _parse_tax_IDs(part, ranks, t=0):
    
    if t == 0:
        rank_tax_ids = {}
        for r in ranks:
            rank_tax_ids[r] = _parse_rank(r, part)
    elif t == 1:
        rank_tax_ids = {}
        for line in part:
            t_l = re.split("\t| +", line)
            for rank in ranks:
                if rank in t_l:
                    rank_tax_ids[int(t_l[0])] = [rank, t_l[3]]
            
    return rank_tax_ids

def parse_data(parts, t):
    '''

    Parameters
    ----------
    parts : list
        containing lines (string) from one sample

    Returns
    -------
    samples : dictionary
        where the sample number is the key and a dictionary of dictionaries 
        is the value (see Data Tree under 'VARIABLES' section)

    '''
    samples = {}
    
    for p in parts:
        ranks = _get_ranks(p)
        sn = _get_sample_number(p)
        
        parsed_taxID = _parse_tax_IDs(p, ranks, t)
        samples[sn] = parsed_taxID
    return samples

def print_sample(samples):
    '''

    Parameters
    ----------
    s_num : int
        the sample number
    sample : dictionary
        where rank (string) is the key and a dictionary of {tax_id : abundance}
        is the value (from one sample)

    Returns
    -------
    None.

    '''
    for sample_num in samples:
        print("Sample Number:", sample_num)
        for rank in samples[sample_num]:
            print("\tRank:", rank)
            for tax_id in samples[sample_num][rank]:
                print("\t\t{} - {}".format(tax_id, samples[sample_num][rank][tax_id]))
    return

def main(f, t=0):
    '''
    # For when this file isn't being directly run

    Parameters
    ----------
    f : string
        first part of the profile file name (don't include the ".profile" part, 
                                             ie. "A_1" or "C_3")

    Returns
    -------
    samples : dictionary
        where the sample number is the key and a dictionary of dictionaries 
        is the value (see Data Tree under 'VARIABLES' section)

    '''
    samples = parse_data(divide_content(get_file(f)), t)
    #print("done (pp).")
    return samples


#%% MAIN

if __name__ == "__main__":
    '''
    f = input("Which file: \n")
    Samples = main(f)
    '''
    
    