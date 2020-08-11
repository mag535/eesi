# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 09:38:24 2020

@author: Melissa Gray
"""

#%% VARIABLES & IMPORTS

import profile_parser as pp

# samples [sample #] [rank] [taxid] --->> Abundance

#%% FUNCTIONS

def getTaxID(sample):
    '''
    
    Parameters
    ----------
    sample : dictionary
        where taxID is the key and abundance is the value

    Returns
    -------
    tid : set
        filled with taxIDs from the dictionary sample

    '''
    tid = set()
    
    for r in sample:
        for t in sample[r]:
            tid.add(t)
    print("done adding.")
    return tid

def saveTaxID(samples):
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
    
    for n in range(len(samples)):
        taxIDs[n] = getTaxID(samples[n])
    print("done indexing.")
    return taxIDs

def _cTID(t1, t2):
    '''
    
    Parameters
    ----------
    t1 : set
        of TaxIDs from a sample
    t2 : set
        of TaxIDs from a sample

    Returns
    -------
    set
        with the values both sets share

    '''
    print("done comparing.")
    return t1 & t2

def commonTID(tid1, tid2):
    '''

    Parameters
    ----------
    tid1 : dictionary
        where sample # is the key and a set of taxIDs from that sample is the 
        value
    tid2 : dictionary
        where sample # is the key and a set of taxIDs from that sample is the 
        value

    Returns
    -------
    comDP : dictionary
        where the sample # is the key and a set with the overlapping data points
        between the two samples is the value

    '''
    comDP = {}
    
    for n in tid1:
        comDP[n] = _cTID(tid1[n], tid2[n])
    
    return comDP

def _coTID(t1, t2):
    '''

    Parameters
    ----------
    t1 : set
        with TaxIDs from one sample
    t2 : set
        with TaxIDs from one sample

    Returns
    -------
    set
        combined set of t1 and t2 with no repeated values

    '''
    print("done combining.")
    return t1 | t2

def combineTID(tid1, tid2):
    '''

    Parameters
    ----------
    tid1 : dictionary
        where sample # is the key and a set with TaxIDs from that sample is 
        the value
    tid2 : dictionary
        where sample # is the key and a set with TaxIDs from that sample is 
        the value

    Returns
    -------
    combTID : dictionary
        where the sample # is the key and a set of the combined data points 
        (with no repeats) is the value

    '''
    combTID = {}
    
    for n in tid1:
        combTID[n] = (_coTID(tid1[n], tid2[n]))
    print("done listing")
    return combTID

def main(f1, f2):
    '''

    Parameters
    ----------
    f1 : string
        the profile file name before ".profile"
    f2 : string
        the profile file name before ".profile"

    Returns
    -------
    None.

    '''
    S1 = pp.main(f1)
    S2 = pp.main(f2)
    
    t1 = saveTaxID(S1)
    t2 = saveTaxID(S2)
    
    comT = commonTID(t1, t2)
    combT = combineTID(t1, t2)
    
    print_tid(comT)
    print_tid(combT)
    return

def print_tid(tid):
    '''

    Parameters
    ----------
    tid : dictionary
        where sample # is the key and a set with taxIDs is the value

    Returns
    -------
    None.

    '''
    for n in tid:
        print("Sample Number:", n)
        for t in tid[n]:
            print("\t\t{}".format(t))
    return

'''
Data Tree:
    - {sample # : set}
                   - {TaxIDs}
'''

#%% MAIN

if __name__ == "__main__":
    f = input("Which two files do you want to compare \n (only type file name before \'.profile\' and separate by space):\n")
    f_2 = f.split(" ")
    S1 = pp.main(f_2[0])
    S2 = pp.main(f_2[1])
    
    t1 = saveTaxID(S1)
    t2 = saveTaxID(S2)
    
    comT = commonTID(t1, t2)
    combT = combineTID(t1, t2)
    
    print_tid(comT)
    
    
    
