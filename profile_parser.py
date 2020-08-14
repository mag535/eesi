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
                        - {TaxID : Abundance}
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
    return part[0][-1]

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

def _parse_tax_ID(part, ranks):
    rank_tax_ids = {}
    
    for line in part:
        t_l = re.split("\t| +", line)
        for rank in ranks:
            if rank in t_l:
                print(t_l)
                val = _turn_into_number(t_l)
                rank_tax_ids[rank] = {t_l[0] : val}
    return rank_tax_ids

def _parse_rank(rank_list, ranks):
    '''

    Parameters
    ----------
    rank_list : list
        contains dictionaries where the key is a tax_id and the value is the 
        corresponding abundance.
    ranks : list
        contains strings of the taxonomic ranks, in order

    Returns
    -------
    sample_ranks : Tdictionary
        where the taxonomic rank (string) is the key and a dictionary of
        {tax_id : abundance} is the value

    '''
    sample_ranks = {}
    
    for i in range(len(rank_list)):
        sample_ranks[ranks[i]] = rank_list[i]
    return sample_ranks

def _get_ranks(content):
    ranks = []
    
    for line in content:
        if "@Ranks" in line:
            r = line.split(":")
            ranks = r[1].split("|")
            ranks[-1] = ranks[-1].replace("\n", "")
            break
    return ranks

def parse_data(parts):
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
    ranks = _get_ranks(parts[0])
    
    for p in parts:
        sn = _get_sample_number(p)
        
        parsed_data = _parse_tax_id(p)
        sample_ranks = _parse_rank(parsed_data, ranks)
        
        samples[sn] = sample_ranks
            
    return samples

def print_sample(s_num, sample):
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
    print("Sample Number:", s_num)
    for rank in sample:
        print("\tRank:", rank)
        for tax_id in sample[rank]:
            print("\t\t\t{}\t:\t{}".format(tax_id, sample[rank][tax_id]))
    return

def main(f):
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
    samples = parse_data(divide_content(get_file(f)))
    print("done.")
    return samples


#%% MAIN

if __name__ == "__main__":
    '''
    f = input("Which file: \n")
    Samples = main(f)
    '''
    c = get_file("pred")
    con = divide_content(c)
    
    
    print(_parse_tax_ID(con[0], _get_ranks(c)))
    