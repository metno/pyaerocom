from scipy.constants import Avogadro
import numpy as np

def mass_to_nr_molecules(mass, mm):
    """ Calculating the number of molecules form mass and molarmass.

    Mass, Molar mass need to be in the same unit, either both g and g/mol
    or kg and kg/mol.

    Parameters
    ---------------------------
    mass : float
        mass of all compounds.

    mm : float
        molar mass of compounds.

    Returns
    -----------------
    nr_molecules : float
        number of molecules
    """
    nr_molecules = mass/mm*Avogadro
    return nr_molecules

def nr_molecules_to_mass(nr_molecules, mm):
    """ Calculates the mass from the number of molecules and molar mass.

    Parameters
    ---------------
    nr_molecules : int
        Number of molecules

    mm : float
        Molar mass [g/mol]

    Returns
    ---------------------
    mass : float
        mass in grams
    """
    mass = mm*nr_molecules/Avogadro
    return mass

def unitconv_sfc_conc_bck(data, x = 2):
    """ Converting: ugSOx/m3 to  ugS/ m3.

    Parameters
    ------------------
    data: ndarray
        Contains the data in units of ugSoX/m3.

    x: int
        The number of oxygen atoms, O in you desired SOx compound.

    Returns
    ------------
    data : ndarray
        in units of ugS/ m3.

    Notes
    -----------
    micro grams to kilos is 10**6
    """

    mmO = 15.9999 # molar mass oxygen
    mmS = 32.065  # molar mass sulphur
    mm_compound =  (mmS + x*mmO)*10**3 # *10**3 gives molar mass in micrograms

    nr_molecules = mass_to_nr_molecules(data, mm_compound)
    weight_s = nr_molecules_to_mass(nr_molecules, mmS*10**3) # weigth in ug
    return weight_s

def unitconv_sfc_conc(data, nr_of_O = 2):
    """ Unitconverting:  ugS/m3 to ugSOx/m3

    Parameters
    ------------------
    data : array_like
        Contains the data in units of ugS/m3.

    nr_of_O: int
        The number of O's in you desired SOx compound.

    Returns
    ------------
    data : ndarray
        data in units of ug SOx/m3

    """

    mm_s = 32.065*10**6 # in units of ug/mol
    mm_o = nr_of_O*15.9999*10**6 ## in units of ug/mol
    nr_molecules = mass_to_nr_molecules(data, mm_s) # 32.065*10**6) [ug/mol]
    added_weight_oksygen = nr_molecules_to_mass(nr_molecules, mm_o) # ug
    # added weights in micrograms
    mass = data + added_weight_oksygen # in micrograms
    return mass

def unitconv_wet_depo_bck(data, time, ts_type = "monthly"):
    """ The unitconversion kg SO4 m-2 s-1 to kgS/ha.

    Removing the weight of oxygen.

    Parameters
    ------------------
    data: ndarray
        Sulphur data you wish to convert.

    time : pd.Seires[numpy.datetime64]
         Array of datetime64 timesteps.

    ts_type: str
       The timeseries type. Default monthly.

    Returns
    ------------------
    data : ndarray
       Sulphur data in units of ugSOx m-3 s-1.

    """
    # kg SO4 m-2 s-1 to kg S/ha
    mm_so4 = 0.001*32.065 + 0.001*15.999*4 # kg/mol
    mm_s = 32.065*0.001 # kg/mol
    mm_o = 0.001*15.999*4 # kg/mol

    days_in_month = time.dt.daysinmonth
    monthly_to_sec = days_in_month*24*60*60 # Seconds in each
    nr_molecules = data*Avogadro/mm_so4 # [1]
    mass_S       = nr_molecules*mm_s/Avogadro # mass in kg
    # Mulitply by seconds in one month
    mass_pr_ha = mass_S*monthly_to_sec*10000
    return mass_pr_ha

def unitconv_wet_depo(data, time, ts_type = "monthly"):
    """ Unitconversion kg S/ha to kg SOx m-2 s-1.

    Adding mass of oksygen.

    Parameters
    ------------------
    data: ndarray
        data in unit kg S/ha = kg S/(1000 m2)

    time : pd.Seires[numpy.datetime64]
        Array of datetime64 timesteps.

    ts_type : str
        The timeseries type. Default "monthly".

    Returns
    ------------------
    data : ndarray
        data in units of ugSOx/m3

    """
    mmSO4 = 0.001*32.065 + 0.001*15.999*4 # in kg/mol
    mm_s = 32.065*0.001 # kg/mol
    #print('uses new updated version, in that case fix conversion')
    nr_molecules = data*Avogadro/mm_s # [1]
    mass_SO4 = nr_molecules*mmSO4/Avogadro # mass in kl
    days_in_month = time.dt.daysinmonth
    monthly_to_sec = days_in_month*24*60*60
    #print('includes new changes')
    mass_pr_square_m_pr_sek = mass_SO4/(10000*monthly_to_sec)
    return mass_pr_square_m_pr_sek

def unitconv_wet_depo_from_emep(data, time, ts_type = "monthly"):
    """ Unitconversion mgS m-2 to kg SO4 m-2 s-1.

    Milligram to kilos is 10-6.

    Adding mass of oksygen.

    Parameters
    ------------------
    data: ndarray
        data in unit mg S m-2.

    time : pd.Seires[numpy.datetime64]
        Array of datetime64 timesteps.

    ts_type : str
        The timeseries type. Default "monthly".

    Returns
    ------------------
    data : ndarray
        data in units of ugSOx/m3

    """
    # TODO add if time is not of correct pandas series convert
    # numpy ndarray to pandas series. Much better than having to remeber that
    #the only thing thats a åandas seies.
    # If time

    mm_so4 = 0.001*32.065 + 0.001*15.999*4 # in kg/mol
    mm_s  = 0.001*32.065 # kg/mol
    data_in_kilos = data*10**(-9)
    nr_molecules = data_in_kilos*Avogadro/mm_s  # [1]
    mass_SO4     = nr_molecules*mm_so4/Avogadro # mass in kg
    days_in_month  = time.dt.daysinmonth
    monthly_to_sec = days_in_month*24*60*60
    mass_pr_square_m_pr_sek = mass_SO4*10000/monthly_to_sec
    return mass_pr_square_m_pr_sek
