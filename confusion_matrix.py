# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 15:26:55 2020

@author: Melissa Gray
"""

#%% VAIABLES AND IMPORTS

import numpy as np
import pandas as pd
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
    false_negative : integer
        the number of false positives for the tax_id

    '''
    false_negative = 0
    
    for sample_num in predicted:
        if (tax_id not in predicted[sample_num]) and (tax_id in truth[sample_num]):
            false_negative += 1
    return false_negative

def check_false_negatives(truth, predicted, common, combined_set):
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
    false_negatives : dictionary
        where tax_id is the key and the number of false negatives is the value

    '''
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
    false_positive : integer
        the number of false positives for the tax_id

    '''
    false_positive = 0
    
    for sample_num in predicted:
        if (tax_id not in truth[sample_num]) and (tax_id in predicted[sample_num]):
            false_positive += 1
    return false_positive

def check_false_positives(truth, predicted, combined_set):
    '''

    Parameters
    ----------
    truth : dictionary
        where sample number is the key and a set of tax_IDs is the value
        Used as the gold standard
    predicted : dictionary
        where sample number is the key and a set of tax_IDs is the value
    combined_set : set
        containing all the tax_ids from truth and predicted.

    Returns
    -------
    false_positives : dictionary
        where tax_id is the key and the number of false postives for that 
        tax_id

    '''
    # FP = when tax_id is there but it's not supposed to be
    false_positives = {}
    
    for tax_id in combined_set:
        false_positives[tax_id] = _check_false_positives(tax_id, truth, predicted)
    return false_positives

def _check_true_negatives(tax_id, truth, predicted):
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
    true_negative : integer
        the number of true positives for the tax_id

    '''
    true_negative = 0
    
    for sample_num in truth:
        if (tax_id not in truth[sample_num]) and (tax_id not in predicted[sample_num]):
            true_negative += 1
    return true_negative

def check_true_negatives(truth, predicted, combined_set):
    '''

    Parameters
    ----------
    truth : dictionary
        where sample number is the key and a set of tax_IDs is the value
        Used as the gold standard
    predicted : dictionary
        where sample number is the key and a set of tax_IDs is the value
    combined_set : set
        containing all the tax_ids from truth and predicted.

    Returns
    -------
    true_negatives : dictionary
        where tax_id is the key and the number of true negatives for that 
        tax_id is the value

    '''
    # TN = when tax_id is not there and it's supposed to not be there
    
    true_negatives = {}
    #truth_set = dictionary_to_set(truth)
    
    for tax_id in combined_set:
        true_negatives[tax_id] = _check_true_negatives(tax_id, truth, predicted)
    return true_negatives

def confusion_matrix(truth, predicted, common, combined):
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
    matrix : dictionary
        where tax_id is the key and an array of its true positives, false 
        negatives, false positives, and true negatives is the value

    '''
    matrix = {}
    
    combined_set = dictionary_to_set(combined)      # universal set
    
    True_Pos = check_true_positives(truth, predicted, common, combined)
    False_Neg = check_false_negatives(truth, predicted, common, combined_set)
    False_Pos = check_false_positives(truth, predicted, combined_set)
    True_Neg = check_true_negatives(truth, predicted, combined_set)
    
    for tax_id in True_Pos:
        m = np.array([True_Pos[tax_id], False_Neg[tax_id], False_Pos[tax_id], True_Neg[tax_id]])
        matrix[int(tax_id)] = m
    return matrix

def main(pred, t=0):
    '''

    Parameters
    ----------
    pred : string
        first part of the profile file name (don't include the ".profile" part, 
                                             ie. "A_1" or "C_3")
    t : integer, optional
        to toggle the type of parsing. 0 (default) and 1 are the options

    Returns
    -------
    matrix : dictionary
        where tax_id is the key and an array of its true positives, false 
        negatives, false positives, and true negatives is the value

    '''
    global Truth
    truth = comp.save_tax_ID(comp.pp.main(Truth, t))
    predicted = comp.save_tax_ID(comp.pp.main(pred, t))
    
    common, combined = comp.main(Truth, pred, t)
    
    matrix = confusion_matrix(truth, predicted, common, combined)
    return matrix

def print_matrix_chart(matrix):
    '''

    Parameters
    ----------
    matrix : dictionary
        where tax_id is the key and an array of its true positives, false 
        negatives, false positives, and true negatives is the value

    Returns
    -------
    None.

    '''
    # For viewing
    # [TP, FN, FP, TN]
    
    list_tid = []
    for tax_id in matrix:
        list_tid.append(tax_id)
    
    list_tid.sort()
    
    for e in list_tid:
        print("Tax ID:", e)
        print("\t\t\t\tPREDICTED")
        print("\t\t\t\t(+)\t(-)")
        print("\t\t\t(T)\t{}\t{}".format(matrix[e][0], matrix[e][3]))
        print("\tTRUTH")
        print("\t\t\t(F)\t{}\t{}\n".format(matrix[e][2], matrix[e][1]))
    return

def add_other_info(matrix):
    '''

    Parameters
    ----------
    matrix : dictionary
        where tax_id is the key and an array of its true positives, false 
        negatives, false positives, and true negatives is the value

    Returns
    -------
    whole_matrix : dictionary
        where tax_id is the key and a list of 
        [rank, name, abundance, TP, FN, FP, TN] is the value

    '''
    global Truth
    truth_other = comp.pp.main(Truth, 1)
    other_info = {}
    whole_matrix = {}
    
    for sample in truth_other:
        for tax_id in truth_other[sample]:
            other_info[tax_id] = truth_other[sample][tax_id]
    
    for tax_id in matrix:
        whole_matrix[tax_id] = np.array((other_info[tax_id]) + list(matrix[tax_id]))
    
    return whole_matrix

def reformat_matrix(whole_matrix):
    reformatted_matrix = {}
    sorted_matrix_table = {}
    rank_list = []
    name_list = []
    TP_list = []
    FN_list = []
    FP_list = []
    TN_list = []
    
    m_t_keys = sorted(whole_matrix)
    for k in m_t_keys:
        sorted_matrix_table[k] = whole_matrix[k]
    
    # saving tax_ids
    reformatted_matrix["Tax ID"] = list(sorted_matrix_table.keys())
    #saving other info
    for k in sorted_matrix_table:
        rank_list.append(sorted_matrix_table[k][0])
        name_list.append(sorted_matrix_table[k][1])
        TP_list.append(sorted_matrix_table[k][2])
        FN_list.append(sorted_matrix_table[k][3])
        FP_list.append(sorted_matrix_table[k][4])
        TN_list.append(sorted_matrix_table[k][5])
    
    reformatted_matrix["Rank"] = rank_list
    reformatted_matrix["Name"] = name_list
    reformatted_matrix["TP"] = TP_list
    reformatted_matrix["FN"] = FN_list
    reformatted_matrix["FP"] = FP_list
    reformatted_matrix["TN"] = TN_list
    return reformatted_matrix

def create_matrix_table(reformatted_matrix):
    '''

    Parameters
    ----------
    matrix_table : list
        containing {tax_id : [rank, name, TP, FN, FP, TN]}

    Returns
    -------
    None.

    '''
    m = pd.DataFrame.from_dict(reformatted_matrix)
    return m

def save_matrix_table(matrix_table):
    export_file_path = input("Enter file name: \n")
    matrix_table.to_csv (export_file_path+".csv", index = False, header=True)
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
    a = {1: {1,2,3}, 2: {4,5,6}, 3 : {7,8,9}}    #example truth
    b = {1: {1,2,8}, 2: {3,5,6,7}, 3: {9,10}}      #example predicted
    print("truth: \t\t{}\npredicted: \t{}\n".format(a, b))
    
    common_AB = comp.common_tax_ID(a, b)
    combined_AB = comp.combine_tax_ID(a, b)
    
    print_matrix_chart(confusion_matrix(a, b, common_AB, combined_AB))
    return

def example3():
    m1 = main("pred")
    m2 = main(Truth)
    
    print("PREDICTED:\n")
    print_matrix_chart(m1)
    
    print()
    
    print("Predicted:")
    create_matrix_table(add_other_info(m1))
    print("\nTruth:")
    create_matrix_table(add_other_info(m2))
    return

def example4():
    matrix = main("truth")
    matrix_plus = add_other_info(matrix)
    reformated_matrix_plus = reformat_matrix(matrix_plus)
    re_matrix_plus_table = create_matrix_table(reformated_matrix_plus)
    
    save_matrix_table(re_matrix_plus_table)
    return


#%% MAIN

if __name__ == "__main__":
    '''
    file = input("Enter the file you're adding to the confusion matrix with \'A_1.profile\' (only type file name before \'.profile\' and separate by space):\n")
    truth = comp.save_tax_ID(comp.pp.main(Truth, 0))
    predicted = comp.save_tax_ID(comp.pp.main(file, 0))
    
    common, combined = comp.main(Truth, file, 0)
    
    matrix = confusion_matrix(truth, predicted, common, combined)
    
    print_matrix_chart(matrix)
    '''
    
    #example1()
    #example2()
    
    #example3()
    example4()
        