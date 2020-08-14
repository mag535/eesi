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

'''
 matrix -> Tax_ID: [ TP | FN | FP | TN]
             
# one matrix for each tax_id
    {tax_id : np.array([TP, FN, FP, TN])}

Data Tree:
    - {sample number : dict}
                    - {tax_id : vector}
                                - np.array([TP, FN, FP, TN])
'''


#%%% FUNCTIONS

def get_universal_tax_id_index(Sample):       # Uses the parsed Truth data
    '''

    Parameters
    ----------
    Sample : dictionary
        where sample number is the key and a dicitonary of 
        {rank : {tax_id : abundance}} is the value

    Returns
    -------
    universal_tax_IDs : set
        A set of every tax_id found in the file, across all ten samples

    '''
    universal_tax_IDs = set()
    
    for sample_num in Sample:
        for e in Sample[sample_num]:
            universal_tax_IDs.add(e)
    return universal_tax_IDs

def _check_false_positive(sample_num, truth, combined):
    false_positive = 0
    
    for entry in combined[sample_num]:
        if entry not in truth[sample_num]:
            false_positive +=1
    return false_positive

def check_false_positives(truth, combined):
    false_positives = {}
    
    for sample_num in combined:
        false_positives[sample_num] = _check_false_positive(sample_num, truth, combined)
    return false_positives

def _check_false_negative(sample_num, data1, combined):
    false_negative = 0
    
    for entry in combined[sample_num]:
        if entry not in data1[sample_num]:
            false_negative += 1
    return false_negative

def check_false_negatives(data1, combined):
    false_negatives = {}
    
    for sample_num in combined:
        false_negatives[sample_num] = _check_false_negative(sample_num, data1, combined)
    return false_negatives

def _check_true_positive(sample_num, common):
    return len(common[sample_num])

def check_true_positives(common):
    true_positives = {}
    
    for sample_num in common:
        true_positives[sample_num] = _check_true_positive(sample_num, common)
    return true_positives

def _check_true_negative(sample_num, truth, data1, universal_index):
    '''

    Parameters
    ----------
    sample_num : integer
        a key to access the sets in truth and data1
    truth : dictionary
        where sample number is the key and a set of tax_IDs is the value
        Used as the gold standard
    data1 : dictionary
        where sample number is the key and a set of text_IDs is the value.
        Used as the predicted class
    universal_tax_IDs : set
        A set of every tax_id found in the file, across all ten samples

    Returns
    -------
    true_negative : integer
        the number of true positives (any tax_id from other samples that wasn't
        detected) in the current sample

    '''
    true_negative = 0
    
    for entry in universal_index:
        if (entry not in truth[sample_num]) and (entry not in data1[sample_num]):
            true_negative += 1
    return true_negative

def check_true_negatives(truth, data1, universal_index):
    '''

    Parameters
    ----------
    truth : dictionary
        where sample number is the key and a set of tax_IDs is the value
        Used as the gold standard
    data1 : dictionary
        where sample number is the key and a set of text_IDs is the value.
        Used as the predicted class
    universal_tax_IDs : set
        A set of every tax_id found in the file, across all ten samples

    Returns
    -------
    true_negatives : dictionary
        where sample number is the key and the number of true positives is the
        value

    '''
    true_negatives = {}
    
    for sample_num in truth:
        true_negatives[sample_num] = _check_true_negative(sample_num, truth, data1, universal_index)
    return true_negatives

def confusion_matrix(truth, data1):
    matrix = {}
    
    universal_index = get_universal_tax_id_index(truth)
    common = comp.common_tax_ID(truth, data1)
    combined = comp.combine_tax_ID(truth, data1)
    
    FP = check_false_positives(truth, combined)
    FN = check_false_negatives(data1, combined)
    TP = check_true_positives(common)
    TN = check_true_negatives(truth, data1, universal_index)
    
    for sample_num in FP:
        m = np.array([TP[sample_num], FN[sample_num], FP[sample_num], TN[sample_num]])
        matrix[sample_num] = m
    return matrix

def print_matrix(matrix):
    for sample_num in matrix:
        print("\t\tSAMPLE", sample_num)
        print("\tPredicted")
    return

def example():
    a = {1 : {1,2,3,4,75,20,119}, 2 : {4,5,6,7,10,20}}
    print("a:", a)
    b = {1 : {7,5,2,4,10}, 2: {5,6,20,30}}
    print("b:", b)
        
    #Combined = 1,2,3,4,5,7
    #Common = 2,4
    #a is truth in this example
    common_AB = comp.common_tax_ID(a, b)
    print("\nCommon:", common_AB)
    combined_AB = comp.combine_tax_ID(a, b)
    print("\nCombined:", combined_AB)
    
    print("\nFalse Positives:", check_false_positives(a, combined_AB))
    print("\nFalse Negatives:", check_false_negatives(b, combined_AB))
    print("\nTrue Positives:", check_true_positives(common_AB))
    return

def example2():
    s = {1 : {"rank1" : {1 : 0.1, 2 : 0.2, 3 : 0.3}}, 2: {"rank1" : {4 : 0.4, 5 : 0.5, 6 : 0.6}}}
    uni_index = get_universal_tax_id_index(s)
    
    tru = {1 : {1,2,3}, 2 :{4,5,6}}
    print("truth:", tru)
    b = {1 : {1,3,4}, 2: {5,7,6}}
    print("b:", b)
    
    print("True Negatives:", check_true_negatives(tru, b, uni_index))
    return

def example3():
    s = {1 : {"rank1" : {1 : 0.1, 2 : 0.2, 3 : 0.3}}, 2: {"rank1" : {4 : 0.4, 5 : 0.5, 6 : 0.6}}}
    truth = comp.save_tax_ID(s)
    b = {1 : {1,2,3}, 2: {4,5,6}}
    
    print(confusion_matrix(truth, b))
    return



#%% MAIN

if __name__ == "__main__":
    '''
    Parse Here:
    
    f = input("Enter the file you're adding to the confusion matrix with \'A_1.profile\' (only type file name before \'.profile\' and separate by space):\n")
    common, combined = comp.main(Truth, f)
    '''
    
    example()
    #example2()
    #example3()