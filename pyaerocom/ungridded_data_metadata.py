from copy import deepcopy
import logging
import sys
from typing import Any

import numpy as np
from pyaerocom.exceptions import MetaDataError
from pyaerocom.ungridded_data import UngriddedDataContainer


logger = logging.getLogger(__name__)


if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


class UngriddedDataMetadata(UngriddedDataContainer):
    """Metadata-implementation for UngriddedDataContainer implementing
    metadata, i.e. metadata, data_revision, var_idx/variables, filter_hist and
    _is_vertical_profile. It does not do anything on the data-structure.

    This will only implement the UngriddedDataContainer partially. The data
    part needs to be implemented independently.

    """

    def __init__(self):
        self.metadata = {}
        self.data_revision = {}
        self.var_idx = {}
        self.filter_hist = {}
        self._is_vertical_profile = False

    def _copy_metadata_to(self, other):
        """
        deepcopy metadata-fields to the other object
        """
        other.metadata = deepcopy(self.metadata)
        other.data_revision = deepcopy(self.data_revision)
        other.var_idx = deepcopy(self.var_idx)
        other.filter_hist = deepcopy(self.filter_hist)
        other.is_vertical_profile = self._is_vertical_profile

    def _get_data_revision_helper(self, data_id):
        """
        Helper method to get last data revision

        Parameters
        ----------
        data_id : str
            ID of dataset for which revision is to be retrieved

        Raises
        ------
        MetaDataError
            If multiple revisions are found for this dataset.

        Returns
        -------
        latest revision (None if no revision is available).

        """
        rev = None
        for meta in self.metadata.values():
            if meta["data_id"] == data_id:
                if rev is None:
                    rev = meta["data_revision"]
                elif not meta["data_revision"] == rev:
                    raise MetaDataError(f"Found different data revisions for dataset {data_id}")
        if data_id in self.data_revision:
            if not rev == self.data_revision[data_id]:
                raise MetaDataError(f"Found different data revisions for dataset {data_id}")
        self.data_revision[data_id] = rev
        return rev

    @property
    @override
    def first_meta_idx(self):
        # First available metadata index
        return list(self.metadata)[0]

    @property
    @override
    def last_meta_idx(self):
        """
        Index of last metadata block
        """
        return np.max(list(self.meta_idx))

    @property
    @override
    def is_vertical_profile(self):
        """Boolean specifying whether is vertical profile"""
        return self._is_vertical_profile

    @is_vertical_profile.setter
    @override
    def is_vertical_profile(self, value):
        """
        Boolean specifying whether is vertical profile.
        Note must be set in ReadUngridded based on the reader
        because the instance of class used during reading is
        not the same as the instance used later in the workflow
        """
        self._is_vertical_profile = value

    def _list_from_metadata(
        self, metafield, undef=None, unique=False, allow_none=True
    ) -> list[Any]:
        """retrieve a station-metadata field as list

        :param metafield: one of the metadata-fields like "longitude" or "instrument"
        :param undef: default value if undefined
        :param unique: remove None and duplicate, defaults to False
        :param allow_none: allow none in unique lists
        :return: list of the metadata-fields values
        """
        ret_vals = []
        for info in self.metadata.values():
            try:
                val = info[metafield]
                if unique:
                    if val not in ret_vals:
                        if allow_none:
                            ret_vals.append(val)
                        elif val is not None:
                            ret_vals.append(val)
                else:
                    ret_vals.append(val)
            except KeyError:
                if not unique:
                    ret_vals.append(undef)
        return ret_vals

    @property
    @override
    def contains_vars(self) -> list[str]:
        """List of all variables in this dataset"""
        return list(self.var_idx)

    @property
    @override
    def contains_datasets(self):
        """List of all datasets in this object"""
        return self._list_from_metadata("data_id", unique=True)

    @property
    @override
    def contains_instruments(self):
        """List of all instruments in this object"""
        return self._list_from_metadata("instrument_name", unique=True, allow_none=False)

        # instruments = []
        # for info in self.metadata.values():
        #     try:
        #         instr = info["instrument_name"]
        #         if instr is not None and instr not in instruments:
        #             instruments.append(instr)
        #     except Exception:
        #         pass
        # return instruments

    @property
    @override
    def is_empty(self):
        """Boolean specifying whether this object contains data or not"""
        return True if len(self.metadata) == 0 else False

    @property
    @override
    def is_filtered(self):
        """Boolean specifying whether this data object has been filtered

        Note
        ----
        Details about applied filtering can be found in :attr:`filter_hist`
        """
        if len(self.filter_hist) > 0:
            return True
        return False

    @property
    @override
    def longitude(self):
        """Longitudes of stations"""
        return self._list_from_metadata("longitude", undef=np.nan)

    @property
    @override
    def latitude(self):
        """Latitudes of stations"""
        return self._list_from_metadata("latitude", undef=np.nan)

    @property
    @override
    def altitude(self):
        """Altitudes of stations"""
        return self._list_from_metadata("altitude", undef=np.nan)

    @property
    @override
    def station_name(self):
        """Station-names of stations"""
        return self._list_from_metadata("station_name", undef=np.nan)

    @property
    @override
    def unique_station_names(self):
        """List of unique station names"""
        return sorted(list(set(self.station_name)))

    @property
    @override
    def available_meta_keys(self):
        """List of all available metadata keys

        Note
        ----
        This is a list of all metadata keys that exist in this dataset, but
        it does not mean that all of the keys are registered in all metadata
        blocks, especially if the data is merged from different sources with
        different metadata availability
        """
        metakeys = []
        for meta in self.metadata.values():
            for key in meta:
                if key not in metakeys:
                    metakeys.append(key)
        return metakeys

    @property
    @override
    def nonunique_station_names(self):
        """List of station names that occur more than once in metadata"""
        import collections

        lst = self.station_name
        return [item for item, count in collections.Counter(lst).items() if count > 1]

    @override
    def last_filter_applied(self):
        """Returns the last filter that was applied to this dataset

        To see all filters, check out :attr:`filter_hist`
        """
        if not self.is_filtered:
            raise AttributeError("No filters were applied so far")
        return self.filter_hist[max(self.filter_hist)]
