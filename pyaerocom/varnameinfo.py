import fnmatch
import re

from pyaerocom.exceptions import VariableDefinitionError


class VarNameInfo(object):
    """This class can be used to retrieve information from variable names"""

    #: valid number range for retrieval of wavelengths from variable name
    _VALID_WVL_RANGE = [0.1, 10000] #nm

    #: valid variable families for wavelength retrievals
    _VALID_WVL_IDS = ['od', 'abs', 'ec', 'sc', 'ac', 'bsc', 'ssa']

    PATTERNS = {'od' : r'od\d+aer'}
    DEFAULT_VERT_CODE_PATTERNS = {
        'abs*'  :   'Column',
        'od*'   :   'Column',
        'ang*'  :   'Column',
        'load*' :   'Column',
        'wet*'  :   'Surface',
        'dry*'  :   'Surface',
        'emi*'  :   'Surface'}

    def __init__(self, var_name):
        self.var_name = var_name
        self._nums = []
        try:
            self._nums = self._numbers_in_string(var_name)
        except Exception:
            pass

    def get_default_vert_code(self):
        """Get default vertical code for variable name"""
        for pattern, code in self.DEFAULT_VERT_CODE_PATTERNS.items():
            if fnmatch.fnmatch(self.var_name, pattern):
                return code
        raise ValueError('No default vertical code could be found for {}'
                         .format(self.var_name))

    @staticmethod
    def _numbers_in_string(input_str):
        """Get list of all numbers in input str

        Parameters
        ----------
        input_str : str
            string to be checked

        Returns
        -------
        list
            list of numbers that were found in input string
        """
        return [int(x) for x in re.findall(r'\d+', input_str)]

    @property
    def contains_numbers(self):
        """Boolean specifying whether this variable name contains numbers"""
        if len(self._nums) > 0:
            return True
        return False

    @property
    def is_wavelength_dependent(self):
        """Boolean specifying whether this variable name is wavelength dependent"""
        for item in self._VALID_WVL_IDS:
            if self.var_name.startswith(item):
                return True
        return False

    @property
    def contains_wavelength_nm(self):
        """Boolean specifying whether this variable contains a certain wavelength"""
        if not self.contains_numbers:
            return False
        low, high = self._VALID_WVL_RANGE
        if self._nums and low <= self._nums[0] <= high:
            return True
        return False

    @property
    def wavelength_nm(self):
        """Wavelength in nm (if appliable)"""
        if not self.is_wavelength_dependent:
            raise VariableDefinitionError('Variable {} is not wavelength '
                                          'dependent (does not start with '
                                          'either of {})'.format(self.var_name,
                                                     self._VALID_WVL_IDS))

        elif not self.contains_wavelength_nm:
            raise VariableDefinitionError('Wavelength could not be extracted '
                                          'from variable name')
        return self._nums[0]

    def in_wavelength_range(self, low, high):
        """Boolean specifying whether variable is within wavelength range

        Parameters
        ----------
        low : float
            lower end of wavelength range to be tested
        high : float
            upper end of wavelength range to be tested

        Returns
        -------
        bool
            True, if this variable is wavelength dependent and if the
            wavelength that is inferred from the filename is within the
            specified input range
        """
        return low <= self.wavelength <= high

    def translate_to_wavelength(self, to_wavelength):
        """Create new variable name at a different wavelength

        Parameters
        ----------
        to_wavelength : float
            new wavelength in nm

        Returns
        -------
        VarNameInfo
            new variable name
        """
        if not self.contains_wavelength_nm:
            raise ValueError('Variable {} is not wavelength dependent'.format(self.var_name))
        name = self.var_name.replace(str(self.wavelength_nm),
                                     str(to_wavelength))
        return VarNameInfo(name)

    def __str__(self):
        s = ('\nVariable {}\n'
             'is_wavelength_dependent: {}\n'
             'is_optical_density: {}'.format(self.var_name,
                                                self.is_wavelength_dependent,
                                                self.is_optical_density))
        if self.is_wavelength_dependent:
            s += '\nwavelength_nm: {}'.format(self.wavelength_nm)
        return s