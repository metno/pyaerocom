#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 11:43:38 2021

@author: jonasg
"""
import abc

class EvalEntry(abc.ABC):
    @abc.abstractmethod
    def get_all_vars(self) -> list:
        """


        Returns
        -------
        list
            list of variables associated with entry.

        """
        pass