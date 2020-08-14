# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 15:26:55 2020

@author: Melissa Gray
"""

#%% VAIABLES AND IMPORTS

import numpy as np
import comparator as comp

Truth = "truth"

'''
 matrix -> Tax_ID: [ TP | FN | FP | TN]
             
# one matrix for each tax_id
    {tax_id : np.array([TP, FN, FP, TN])}

Data Tree:
    - {sample number : dict}
                    - {tax_id : vector}
                                - np.array([TP, FN, FP, TN])
'''


#%% FUNCTIONS

def dictionary_to_set(d):
    '''

    Parameters
    ----------
    d : dictionary
        where sample number is the key and a set of tax_IDs is the value

    Returns
    -------
    dict_set : set
        of all the tax_IDs in d (repeats not included)

    '''
    dict_set = set()
    
    for sample_num in d:
        for tax_id in d[sample_num]:
            dict_set.add(tax_id)
    return dict_set

def _check_true_positives(tax_id, truth, predicted):
    '''

    Parameters
    ----------
    tax_id : integer
        a tax_id from a sample
    truth : dictionary
        where sample number is the key and a set of tax_IDs is the value
        Used as the gold standard
    predicted : dictionary
        where sample number is the key and a set of tax_IDs is the value

    Returns
    -------
    true_positive : integer
        the number of true positives (when it appears where it's supposed to) for the tax_id in Parameters

    '''
    true_positive = 0
    
    for sample_num in predicted:
        for entry in predicted[sample_num]:
            if tax_id == entry:
                true_positive += 1
    return true_positive

def check_true_positives(truth, predicted, common, combined):
    '''

    Parameters
    ----------
    truth : dictionary
        where sample number is the key and a set of tax_IDs is the value
        Used as the gold standard
    predicted : dictionary
        where sample number is the key and a set of tax_IDs is the value
    common : dictionary
        where sample number is the key and a set of tax_IDs found in both 
        truth and predicted is the value
    combined: dictionary
        where sample number is the key and a set of tax_IDs from both 
        truth and predicted is the value

    Returns
    -------
    true_positives : dictionary
        where a tax_id is the key and the number of true positives (integer) 
        for that tax_id is the value

    '''
    true_positives = {}
    common_set = dictionary_to_set(common)
    
    for sample_num in combined:
        for tax_id in combined[sample_num]:
            if tax_id in common_set:
                true_positives[tax_id] = _check_true_positives(tax_id, truth, predicted)
            else:
                true_positives[tax_id] = 0
    return true_positives

def _check_false_negatives(tax_id, truth, predicted):
    false_negative = 0
    
    for sample_num in predicted:
        if (tax_id not in predicted[sample_num]) and (tax_id in truth[sample_num]):
            false_negative += 1
    return false_negative

def check_false_negatives(truth, predicted, common, combined_set):
    # FN = when the tax_id is supposed to be there but it's not
    false_negatives = {}
    common_set = dictionary_to_set(common)
    
    for tax_id in combined_set:
        if tax_id not in common_set:
            false_negatives[tax_id] = _check_false_negatives(tax_id, truth, predicted)
        else:
            false_negatives[tax_id] = 0
    return false_negatives

def _check_false_positives(tax_id, truth, predicted):
    false_positive = 0
    
    for sample_num in predicted:
        if (tax_id not in truth[sample_num]) and (tax_id in predicted[sample_num]):
            false_positive += 1
    return false_positive

def check_false_positives(truth, predicted, combined_set):
    # FP = when tax_id is there but it's not supposed to be
    false_positives = {}
    
    for tax_id in combined_set:
        false_positives[tax_id] = _check_false_positives(tax_id, truth, predicted)
    return false_positives

def _check_true_negatives(tax_id, truth, predicted):
    true_negative = 0
    
    for sample_num in truth:
        if (tax_id not in truth[sample_num]) and (tax_id not in predicted[sample_num]):
            true_negative += 1
    return true_negative

def check_true_negatives(truth, predicted, combined_set):
    # TN = when tax_id is not there and it's supposed to not be there
    
    # Use combined_set or truth_set ???
    true_negatives = {}
    truth_set = dictionary_to_set(truth)
    
    for tax_id in combined_set:
        true_negatives[tax_id] = _check_true_negatives(tax_id, truth, predicted)
    return true_negatives

def confusion_matrix(truth, predicted, common, combined):
    matrix = {}
    
    combined_set = dictionary_to_set(combined)      # universal set
    
    True_Pos = check_true_positives(truth, predicted, common, combined)
    False_Neg = check_false_negatives(truth, predicted, common, combined_set)
    False_Pos = check_false_positives(truth, predicted, combined_set)
    True_Neg = check_true_negatives(truth, predicted, combined_set)
    
    for tax_id in True_Pos:
        m = np.array([True_Pos[tax_id], False_Neg[tax_id], False_Pos[tax_id], True_Neg[tax_id]])
        matrix[tax_id] = m
    return matrix

def print_matrix(matrix):
    for tax_id in matrix:
        print("Tax ID:", tax_id)
        print("\t\t\tPREDICTED")
        print("\t\t\t(+)\t(-)")
        print("\t\t(+)\t{}\t{}".format(matrix[tax_id][0], matrix[tax_id][1]))
        print("TRUTH")
        print("\t\t(-)\t{}\t{}\n".format(matrix[tax_id][2], matrix[tax_id][3]))
    return

def setup():
    file = input("Enter the file you're adding to the confusion matrix with \'A_1.profile\' (only type file name before \'.profile\' and separate by space):\n")
    truth = comp.save_tax_ID(comp.pp.main(Truth))
    predicted = comp.save_tax_ID(comp.pp.main(file))
    
    common, combined = comp.main(Truth, file)
    
    matrix = confusion_matrix(truth, predicted, common, combined)
    
    print(matrix)
    return

def example1():
    a = {1: {1,2,3}, 2: {4,5,6}}    #example truth
    b = {1: {1,2}, 2: {3,5,6,7}}      #example predicted
    print("truth: \t\t{}\npredicted: \t{}\n".format(a, b))
    
    common_AB = comp.common_tax_ID(a, b)
    combined_AB = comp.combine_tax_ID(a, b)
    combined_AB_set = dictionary_to_set(combined_AB)
    print("True Positives:", check_true_positives(a, b, common_AB, combined_AB))
    print("False Negatives:", check_false_negatives(a, b, common_AB, combined_AB_set))
    print("False Positives:", check_false_positives(a, b, combined_AB_set))
    print("True Negatives:", check_true_negatives(a, b, combined_AB_set))
    return

def example2():
    a = {1: {1,2,3}, 2: {4,5,6}, 3 : {1,2,3}}    #example truth
    b = {1: {1,2}, 2: {3,5,6,7}, 3: {1,2,3}}      #example predicted
    print("truth: \t\t{}\npredicted: \t{}\n".format(a, b))
    
    common_AB = comp.common_tax_ID(a, b)
    combined_AB = comp.combine_tax_ID(a, b)
    
    print_matrix(confusion_matrix(a, b, common_AB, combined_AB))
    return


#%% MAIN

if __name__ == "__main__":
    '''
    file = input("Enter the file you're adding to the confusion matrix with \'A_1.profile\' (only type file name before \'.profile\' and separate by space):\n")
    truth = comp.save_tax_ID(pp.main(Truth))
    predicted = comp.save_tax_ID(pp.main(file))
    common, combined = comp.main(Truth, file)
    '''
    
    #example1()
    example2()
    #setup()