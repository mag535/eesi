# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 09:38:24 2020

@author: Melissa Gray
"""

#%% VARIABLES & IMPORTS

import profile_parser as pp

# samples [sample #] [rank] [taxid] --->> Abundance
'''
Data Tree:
    - {sample # : set}
                   - {TaxIDs}
'''


#%% FUNCTIONS

def get_tax_ID(sample):
    '''
    
    Parameters
    ----------
    sample : dictionary
        where taxID is the key and abundance is the value

    Returns
    -------
    tax_id : set
        filled with taxIDs from the dictionary sample

    '''
    tax_id = set()
    
    for rank in sample:
        for tid in sample[rank]:
            tax_id.add(tid)
    #print("done adding.")
    return tax_id

def save_tax_ID(samples):
    '''

    Parameters
    ----------
    samples : dictionary
        where sample # is the key and a dictionary of {taxID : abundance} is
        the value

    Returns
    -------
    taxIDs : dictionary
        where sample # is the key and a set of taxIDs from that sample is the 
        value

    '''
    taxIDs = {}
    
    for sample_num in samples:
        taxIDs[sample_num] = get_tax_ID(samples[sample_num])
    #print("done indexing.")
    return taxIDs

def _common_tax_ID(tax_id_1, tax_id_2):
    '''
    
    Parameters
    ----------
    tax_id_1 : set
        of TaxIDs from a sample
    tax_id_2 : set
        of TaxIDs from a sample

    Returns
    -------
    set
        with the values both sets share

    '''
    #print("done comparing.")
    return tax_id_1 & tax_id_2

def common_tax_ID(tax_id_1, tax_id_2):
    '''

    Parameters
    ----------
    tax_id_1 : dictionary
        where sample # is the key and a set of taxIDs from that sample is the 
        value
    tax_id_2 : dictionary
        where sample # is the key and a set of taxIDs from that sample is the 
        value

    Returns
    -------
    common_data_points : dictionary
        where the sample # is the key and a set with the overlapping data points
        between the two samples is the value

    '''
    common_data_points = {}
    
    for n in tax_id_1:
        common_data_points[n] = _common_tax_ID(tax_id_1[n], tax_id_2[n])
    
    return common_data_points

def _combine_tax_ID(tax_id_1, tax_id_2):
    '''

    Parameters
    ----------
    tax_id_1 : set
        with TaxIDs from one sample
    tax_id_2 : set
        with TaxIDs from one sample

    Returns
    -------
    set
        combined set of t1 and t2 with no repeated values

    '''
    #print("done combining.")
    return tax_id_1 | tax_id_2

def combine_tax_ID(tax_id_1, tax_id_2):
    '''

    Parameters
    ----------
    tax_id_1 : dictionary
        where sample # is the key and a set with TaxIDs from that sample is 
        the value
    tax_id_2 : dictionary
        where sample # is the key and a set with TaxIDs from that sample is 
        the value

    Returns
    -------
    combined_tax_IDs : dictionary
        where the sample # is the key and a set of the combined data points 
        (with no repeats) is the value

    '''
    combined_tax_IDs = {}
    
    for n in tax_id_1:
        combined_tax_IDs[n] = (_combine_tax_ID(tax_id_1[n], tax_id_2[n]))
    #print("done listing")
    return combined_tax_IDs

def main(file1, file2):
    '''

    Parameters
    ----------
    file1 : string
        the profile file name before ".profile"
    file2 : string
        the profile file name before ".profile"

    Returns
    -------
    common_1_2: dictionary
        where sample # is the key and a set of common data points between the 
        two files is the value
    combined_1_2: dictionary
        where sample # is the key and a set of combined data points from the 
        two files is the value (no repeats)

    '''
    Sample1 = pp.main(file1)
    Sample2 = pp.main(file2)
    
    t1 = save_tax_ID(Sample1)
    t2 = save_tax_ID(Sample2)
    
    common_1_2 = common_tax_ID(t1, t2)
    combined_1_2 = combine_tax_ID(t1, t2)
    return common_1_2, combined_1_2

def print_tax_ID(tax_id):
    '''

    Parameters
    ----------
    tax_id : dictionary
        where sample # is the key and a set with taxIDs is the value

    Returns
    -------
    None.

    '''
    for n in tax_id:
        print("Sample Number:", n)
        for t in tax_id[n]:
            print("\t\t{}".format(t))
    return

def example():
    '''

    Returns
    -------
    None.

    '''
    a = {1 : {1,2,3}, 2 : {3,4,5}}
    print("a - ", a)
    b = {1 : {1,3,4}, 2 : {4,5,6}}
    print("b - ", b, "\n")
    
    ab = common_tax_ID(a, b)
    a_b  = combine_tax_ID(a, b)
    print("COMMON:")
    print_tax_ID(ab)
    print()
    print("COMBINED")
    print_tax_ID(a_b)
    return


#%% MAIN

if __name__ == "__main__":
    f = input("Which two files do you want to compare \n (only type file name before \'.profile\' and separate by space):\n")
    f_2 = f.split(" ")
    S1 = pp.main(f_2[0])
    S2 = pp.main(f_2[1])
    
    t1 = save_tax_ID(S1)
    t2 = save_tax_ID(S2)
    
    comT = common_tax_ID(t1, t2)
    combT = combine_tax_ID(t1, t2)
    
    #example()
    