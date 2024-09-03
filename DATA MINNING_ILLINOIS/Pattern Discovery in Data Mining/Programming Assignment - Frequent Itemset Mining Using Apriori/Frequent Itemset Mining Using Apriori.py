#!/usr/bin/python3
import os
import operator
from collections import defaultdict
from itertools import combinations, chain


class Apriori:
    """
   Parameters
   ----------
   minSupport: float
                           Minimum support value for a transaction
                           to be called interesting.
   support_count: collection.defaultdict(int)
                           Contains support count of itemsets.
                           {
                                   frozenset(): int,
                                   frozenset(): int,
                                   frozenset(): int,
                                   ...
                           }
                           frozenset(): set of items
                           int: support count of the itemset
   Methods
   -------
   read_transactions_from_file()
           Read transactions from the input file.
   get_one_itemset()
           Gets unique items from the list of transactions.
   self_cross()
           Takes union of a set with itself to form bigger sets.
   get_min_supp_itemsets()
           Returns those itemsets whose support is > minSupport
   apiori()
           Uses Apriori algotithm to find interesting
           k-itemsets.
   subsets()
           Returns subsets of a set.
   """

    def __init__(self, minSupport):
        self.support_count = defaultdict(int)
        self.minSupport = minSupport

    def read_transactions_from_file(self, transaction_file):
        """
       Parameters
       ----------
       transaction_file: txt file
       Return Type
       -----------
       List of transactions as read from file.
       Each transaction is a set of items.
               [{a, b, c}, {b, d, p, q}, {p, e}, .....]
               {a, b, c} - 1st itemset (3-itemset)
               {b, d, p, q} - 2nd itemset (4-itemset)
               {p, e} - 3rd itemset (2-itemset)
               ...
       """
        with open(transaction_file, "r") as infile:
            transactions = [set(line.rstrip("\n").split(";"))
                            for line in infile]

            return transactions

    def get_one_itemset(self, transactions):
        """
       Parameters
       ----------
       List of transactions. Each transasction
       is a set of items.
               [{a, b, c}, {b, d, p, q}, {p, e}, .....]
               {a, b, c} - 1st itemset (3-itemset)
               {b, d, p, q} - 2nd itemset (4-itemset)
               {p, e} - 3rd itemset (2-itemset)
               ...
       Return Type
       -----------
       one_itemset: set of unique items;
               {
                       frozenset({"a"}), frozenset({"b"}), frozenset({"c"}),
                       frozenset({"d"}), frozenset({"e"}), frozenset({"p"}),
                       frozenset({"q"})
               }
       """
        one_itemset = set()
        for transaction in transactions:
            for item in transaction:
                one_itemset.add(frozenset([item]))

        return one_itemset

    def self_cross(self, Ck, itemset_size):
        """
       Parameters
       ----------
       Ck: set
               a set of k-itemsets
               Size if each itemset in Ck is k(=itemset_size-1)
       itemset_size: int
               Required size of each itemset in resulting set(=k+1)
       Ck:
       {
               frozenset({"book", "pen"}),
               frozenset({"book", "dog"}),
               frozenset({"ox", "coke"}),
               ...
       }
       for a 2-itemset
       Return Type
       -----------
       Ck_plus_1: set
               a set of (k+1)-itemsets
       Ck_plus_1:
       {
               frozenset({"book", "pen", "dog"}),
               frozenset({"book", "dog", "ox"}),
               frozenset({"book", "coke", "dog"}),
               ...
       }
       """
        Ck_plus_1 = {itemset1.union(itemset2)
                     for itemset1 in Ck for itemset2 in Ck
                     if len(itemset1.union(itemset2)) == itemset_size}
        return Ck_plus_1

    def prune_Ck(self, Ck, Lk_minus_1, itemset_size):
        """
       Parameters
       ----------
       Ck: set
               a set of k-itemsets(k=itemset_size)
       Lk_minus_1: set
               a set of (k-1)-itemsets
       itemset_size: int
               (= k)
       Ck:
       {
               frozenset({"book", "dog", "copper"}),
               frozenset({"book", "dog", "water"}),
       }
       Ck_minus_1:
       {
               frozenset({"book", "dog"}),
               frozenset({"book", "copper"}),
               frozenset({"dog", "copper"})
               frozenset({"book", "water"}),
               frozenset({"dog", "water"}),
       }
       Lk_minus_1:
       {
               frozenset({"book", "copper"}),
               frozenset({"book", "dog"}),
               frozenset({"book", "water"}),
               frozenset({"water", "dog"})
       }
       Returns
       -------
       Ck_: set
               a set of k-itemsets
       Ck_:
       {
               frozenset({"book", "dog", "water"})
       } those Ck's whose Ck_minus_1's are in Lk_minus_1
       """
        Ck_ = set()
        for itemset in Ck:
            Ck_minus_1 = list(combinations(itemset, itemset_size-1))
            flag = 0
            for subset in Ck_minus_1:
                if not frozenset(subset) in Lk_minus_1:
                    flag = 1
                    break
            if flag == 0:
                Ck_.add(itemset)
        return Ck_

    def get_min_supp_itemsets(self, Ck, transactions):
        """
       Parameters
       ----------
       Ck: set
               a set of k-itemsets
       Transactions: list
               list of transactions. Each transaction is
               a set of items.
               [{a, b, c}, {b, d, p, q}, {p, e}, .....]
       Returns
       -------
       Lk: set
               a set of k-itemsets
               set of itemsets whose support is > minSupport
       """
        temp_freq = defaultdict(int)

        # update support count of each itemset
        for transaction in transactions:
            for itemset in Ck:
                if itemset.issubset(transaction):
                    temp_freq[itemset] += 1
                    self.support_count[itemset] += 1

        N = len(transactions)
        Lk = [itemset for itemset, freq in temp_freq.items()
              if freq/N > self.minSupport]
        return set(Lk)

    def frequent_item_set(self, transactions):
        """
       Parameters
       ----------
       transactions: list
               list of transactions. Each transaction is
                       a set of items.
                       [{a, b, c}, {b, d, p, q}, {p, e}, .....]
       Returns
       -------
       K_itemsets: dict
       {
               1: {frozenset({"dog"}), frozenset({"ox"}), ....}
               2: {frozenset({"dog", "water"}), frozenset({"book", "copper"}), .....}
               3: {frozenset({"dog", "ox", "gold"}), frozenset({"water", "dog", ox}), ...}
       }
               key: value
               int: set of frozensets of size = value of key
               each itemset in K_itemset has support > minSupport
       """
        K_itemsets = dict()
        Ck = self.get_one_itemset(transactions)
        Lk = self.get_min_supp_itemsets(Ck, transactions)
        k = 2
        while len(Lk) != 0:
            K_itemsets[k-1] = Lk
            Ck = self.self_cross(Lk, k)
            Ck = self.prune_Ck(Ck, Lk, k)
            Lk = self.get_min_supp_itemsets(Ck, transactions)
            k += 1

        return K_itemsets

    def subsets(self, iterable):
        """
        Parameters
        ----------
        iterable: an itearble container like set
        Returns
        -------
        subsets_: list powerset of elements in the iterable container
                [
                        frozenset(),
                        frozenset({a}), frozenset({b}),
                        frozenset({a, b})  
                ] if iterable is like {a, b}
       """
        list_ = list(iterable)
        subsets_ = chain.from_iterable(combinations(list_, len)
                                       for len in range(len(list_)+1))
        subsets_ = list(map(frozenset, subsets_))

        return subsets_

    def write_part_1(self, K_itemsets):
        """
        Writes the frequent itemsets with their support to a file.
        """
        main_dir = "./results/part_1/"
        if not os.path.exists(main_dir):
            os.makedirs(main_dir)

        outfile_path = "./results/part_1/patterns.txt"
        with open(outfile_path, "w") as outfile:
            for key, values in K_itemsets.items():
                if key > 1:
                    break
                for value in values:
                    support_ct = self.support_count[value]
                    outfile.write("{support}:{label}\n".format(
                        support=support_ct,
                        label=";".join(list(value))
                    ))

    def write_part_2(self, K_itemsets):
        """
        Writes the frequent itemsets with their support to a file.
        """
        main_dir = './results/part_2'
        if not os.path.exists(main_dir):
            os.makedirs(main_dir)

        outfile_path = "./results/part_2/patterns.txt"
        with open(outfile_path, "w") as outfile:
            for key, values in K_itemsets.items():
                for value in values:
                    support_ct = self.support_count[value]
                    outfile.write("{support}:{label}\n".format(
                        support=support_ct,
                        label=";".join(list(value))
                    ))


if __name__ == "__main__":
    in_transaction_file = "./categories.txt"

    ap = Apriori(minSupport=0.01)
    transactions = ap.read_transactions_from_file(in_transaction_file)
    K_itemsets = ap.frequent_item_set(transactions)
    ap.write_part_1(K_itemsets)
    ap.write_part_2(K_itemsets)