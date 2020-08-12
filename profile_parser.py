# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 14:52:43 2020

@author: Melissa Gray

Parsing profiler data
"""


#%% VARIABLES

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
    cutoff = "@SampleID:marmgCAMI2_short_read_sample_"
    loop = 0
    parts = []
    cutoff_pos = [0]
    
    for l in content:
        if cutoff in l:
            loop += 1
    
    #Cycle through backwards?
    for i in range(loop):
        cutoff_pos.append(content.index(cutoff+str(i)+"\n", cutoff_pos[-1]))
    
    for j in range(10):
        try:
            p = content[cutoff_pos[j+1]:cutoff_pos[j+2]]
        except IndexError:
            p = content[cutoff_pos[j+1]:]
        parts.append(p)
    
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
    s = -1
    for line in part:
        if "@SampleID:marmgCAMI2_short_read_sample_" in line:
                s = int(line[-2])
                break
    return s

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
                #print("skipped:", b)
    return val

def _parse_tax_id(part):
    '''

    Parameters
    ----------
    part : list
        contains strings, one sample

    Returns
    -------
    list
        contains dictionaries for each taxonomic rank. The dictionaries are 
        formatted as {tax_id : abundance}

    '''
    strain = {}
    species = {}
    genus = {}
    fam = {}
    order = {}
    clss = {}
    phylum = {}
    superkingdom = {}
    
    for line in part:
        t_l = line.split("\t")
        val = _turn_into_number(t_l)
        if "strain" in t_l:
            strain[t_l[0]] = val
        elif "species" in t_l:
            species[t_l[0]] = val
        elif "genus" in t_l:
            genus[t_l[0]] = val
        elif "family" in t_l:
            fam[t_l[0]] = val
        elif "order" in t_l:
            order[t_l[0]] = val
        elif "class" in t_l:
            clss[t_l[0]] = val
        elif "phylum" in t_l:
            phylum[t_l[0]] = val
        elif "superkingdom" in t_l:
            superkingdom[t_l[0]] = val
    
    return [strain, species, genus, fam, order, clss, phylum, superkingdom]

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
    ranks = ["strain", "species", "genus", "family", "order", "class", "phylum", "superkingdom"]
    
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
    f = input("Which file: \n")
    Samples = main("A_1")
    
    #print_sample(0, Samples[0])
    