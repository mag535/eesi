# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 10:22:09 2020

@author: Melissa Gray

For calculating True Positives and True Negatives

A_1.profile willl be the Truth or gold standard for this
"""


#%% VAIRABLES AND IMPORTS

import numpy as np
import comparator as comp

Truth = "A_1"
confusion_matrix = np.array([])

'''
 matrix -> ([ {tax_id : #}, ..., ...],
            [ {tax_id : #}, ..., ...], 
            [ ..., ..., ..., ..., ...])
1 = Positive Detection (False/True)
0 = Negative Detection (False/True)
'''


#%%% FUNCTIONS

def check_for_error(common, combined):
    for sample_num in combined:
        for entry in combined[sample_num]:
            if entry in common[sample_num]:
                print("{}: matches Truth".format(entry))
            else:
                print("{}: ...".format(entry))
    return

def check_false_positives(truth, combined):
    false_positives = set()
    
    for sample_num in combined:
        for entry in combined[sample_num]:
            if entry not in truth[sample_num]:
                false_positives.add(entry)
                print(entry, "is only in the predicted class (b)")
    return

def check_false_negatives(data1, combined):
    false_negatives = set()
    
    for sample_num in combined:
        for entry in combined[sample_num]:
            if entry not in data1[sample_num]:
                false_negatives.add(entry)
                print(entry, "is in Truth (a) but not predicted class (b)")
    return

def example():
    a = {1 : {1,2,3,4,75,20,119}}
    print("a:", a)
    b = {1 : {7,5,2,4,10}}
    print("b:", b)
    
    #Combined = 1,2,3,4,5,7
    #Common = 2,4
    #a is truth in this example
    common_AB = comp.common_tax_ID(a, b)
    print("\nCommon:", common_AB)
    combined_AB = comp.combine_tax_ID(a, b)
    print("\nCombined:", combined_AB)
    
    check_for_error(common_AB, combined_AB)
    print("\nFalse Positives:")
    check_false_positives(a, combined_AB)
    print("\nFalse Negatives:")
    check_false_negatives(b, combined_AB)
    return


#%% MAIN

if __name__ == "__main__":
    '''
    f = input("Enter the file you're adding to the confusion matrix with \'A_1.profile\' (only type file name before \'.profile\' and separate by space):\n")
    common, combined = comp.main(Truth, f)
    '''
    
    example()
    