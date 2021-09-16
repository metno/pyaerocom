#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 11:43:38 2021

@author: jonasg
"""
import abc

class EvalEntry(abc.ABC):
    """
    Base class for model or obs evaluation entries for AeroVal experiment

    See also :class:`pyaerocom.aeroval.obsentry.ObsEntry` and
    :class:`pyaerocom.aeroval.modelentry.ModelEntry` for implementations.
    """
    @abc.abstractmethod
    def get_all_vars(self) -> list:
        """
        Get list of all variables defined in the evaluation entry

        Returns
        -------
        list
            list of variables associated with entry.

        """
        pass

    def has_var(self, var_name):
        """
        Check if input variable is defined in entry

        Returns
        -------
        bool
            True if entry has variable available, else False

        """
        return True if var_name in self.get_all_vars() else False