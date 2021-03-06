# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 14:52:43 2020

@author: Melissa Gray

Parsing profiler data
"""


#%% VARIABLES & IMPORTS

import re

# samples [sample #] [rank] [taxid] --->> Abundance
'''
Data Tree:
    - {Sample # : dict}
                - {rank : dict}
                        - {tax_id : abundance}
'''


#%% CLASS

class Parser():
    def __init__(self):
        return
    
    def get_file(self, f):
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
        file = open(f, "r")
        contents = file.readlines()
        file.close()
        return contents

    def divide_content(self, content):
        '''

        Parameters
        ----------
        content : list
            containing all the lines of the file as strings

        Returns
        -------
        parts : list
            where the elements are lists of sections of content, separated by sample number

        '''
        parts = []
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

    def _get_sample_number(self, part):
        '''

        Parameters
        ----------
        part : list
            containing lines (as strings) from one sample in a profile

        Returns
        -------
        int
            the sample number in each part

        '''
        return int(part[0][-1])

    def _turn_into_number(self, temp_l):
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

    def _get_ranks(self, content):
        '''

        Parameters
        ----------
        content : list
            containing all the lines of the file as strings

        Returns
        -------
        ranks : list
            contains the names of the ranks in a sample

        '''
        ranks = []
    
        for element in content:
            if "@Ranks" in element:
                r = element.split(":")
                ranks = r[1].split("|")
                last = ranks[-1]
                ranks[-1] =  last.strip()
                break
        return ranks

    def _parse_rank(self, rank, part):
        '''

        Parameters
        ----------
        rank : string
            the name of a rank in a sample
        part : list
            containing lines from a sample in the file

        Returns
        -------
        tax_id_holder : dictionary
            where tax_id is the key and abundance is the value

        '''
        tax_id_holder = {}
    
        for line in part:
            t = re.split("\t| +", line)
            t_l = []
            for e in range(len(t)):
                if len(t[e]) > 0:
                    t_l.append(t[e])
            if rank in t_l:
                val = self._turn_into_number(t_l)
                tax_id_holder[int(t_l[0])] = val
    
        return tax_id_holder

    def _parse_tax_IDs(self, part, ranks, t):
        '''

        Parameters
        ----------
        part : list
            containing lines from a sample in the file
        ranks : list
            containing the names of ranks in a sample
        t : integer
            to toggle how the data will be parsed. 0 and 1 are the options. 
            The default is 0 and it's format is shown under Data Tree under 
            VARIABLES & IMPORTS.

        Returns
        -------
        rank_tax_ids : dictionary
            that can either contain rank as key and {tax_id : abundance} as value,
            or tax_id as key and [rank, name] as value

        '''
        if t == 0:
            rank_tax_ids = {}
            for r in ranks:
                rank_tax_ids[r] = self._parse_rank(r, part)
        elif t == 1:
            rank_tax_ids = {}
            for line in part:
                t_l = re.split("\t| +", line)
                for rank in ranks:
                    if rank in t_l:
                        rank_tax_ids[int(t_l[0])] = [rank, t_l[3]]
            
        return rank_tax_ids

    def parse_data(self, parts, t=0):
        '''

        Parameters
        ----------
        parts : list
            containing lines (string) from one sample
        t : integer
            to toggle the type of parsing. 0 (default) and 1 are the options

        Returns
        -------
        samples : dictionary
            where the sample number is the key and a dictionary of dictionaries 
            is the value (see Data Tree under 'VARIABLES' section)

        '''
        samples = {}
    
        for p in parts:
            ranks = self._get_ranks(p)
            sn = self._get_sample_number(p)
        
            parsed_taxID = self._parse_tax_IDs(p, ranks, t)
            samples[sn] = parsed_taxID
        return samples

    def print_samples(self, samples, t=0):
        '''

        Parameters
        ----------
        sample : dictionary
            where rank (string) is the key and a dictionary of {tax_id : abundance}
            is the value (from one sample)

        Returns
        -------
        None.

        '''
        if t == 0:
            for sample_num in samples:
                print("Sample Number:", sample_num)
                for rank in samples[sample_num]:
                    print("\tRank:", rank)
                    for tax_id in samples[sample_num][rank]:
                        print("\t\t{} - {}".format(tax_id, samples[sample_num][rank][tax_id]))
        elif t ==1:
            for sample_num in samples:
                print("Sample Number:", sample_num)
                for tax_id in samples[sample_num]:
                    print("\tTax ID:", tax_id)
                    print("\t\tRank - {}, Name - {}".format(samples[sample_num][tax_id][0], samples[sample_num][tax_id][1]))
        return

    def main(self, f, t=0):
        '''
        # For when this file isn't being directly run

        Parameters
        ----------
        f : string
            first part of the profile file name (don't include the ".profile" part, 
                                             ie. "A_1" or "C_3")
        t : integer, optional
            to toggle the type of parsing. 0 (default) and 1 are the options

        Returns
        -------
        samples : dictionary
            where the sample number is the key and a dictionary of dictionaries 
            is the value (see Data Tree under 'VARIABLES' section)

        '''
        samples = self.parse_data(self.divide_content(self.get_file(f)), t)
        #print("done (pp).")
        return samples


#%% MAIN

if __name__ == "__main__":
    '''
    Chai = Parser()
    f = input("Which file: \n")
    Samples = Chai.main(f)
    Chai.print_sample(Samples)
    '''
    Chai = Parser()
    print(Chai.main("pred.profile", 0))
    print(Chai.main("pred.profile", 1))
    