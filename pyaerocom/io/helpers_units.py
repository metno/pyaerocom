def mass_to_nr_molecules(mass, mm):
    """ Calculating the number of molecules form mass and molarmass.

    Mass, Molar mass need to be in the same unit, either both g and g/mol 
    or kg and kg/mol.
    
    Parameters
    ---------------------------
    mass : float
        mass of all compounds.
        
    mm : float
        molar mass of compound.
    
    Returns 
    -----------------
    nr_molecules : float
        number of molecules     
    """
    A = 6.022*10**23
    nr_molecules = mass/mm*A
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
    A = 6.022*10**23 # avogadros number
    mass = mm*nr_molecules/A
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
    mmS = 32.065 # molar mass sulphur
    mm_compound =  (mmS + x*mmO)*10**3 
    # since data is in micrograms we should have the 
    
    nr_molecules = mass_to_nr_molecules(data, mm_compound)
    weight_s = nr_molecules_to_mass(nr_molecules, mmS*10**3) # weight in kilos
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

    
def unitconv_wet_depo_bck(data, ts_type = "monthly"):
    """ The unitconversion kgS/ha to kg S/m-2 s-1.
    
    NOT INCLUDED THE SECONDS PART YET.

    Removing the weight of oxygen.

    Parameters
    ------------------
    data: ndarray
        Sulphur data you wish to convert.
        
    ts_type: str    
       The timeseries type. Default monthly.
    
    Returns
    ------------------
    data : ndarray
       Sulphur data in units of ugSOx/m3.
    """
    mm_compund = 0.001*32.065 + 0.001*15.999*4 # in kg/mol
    mm_s = 32.065   # g/mol
    nr_molecules = mass_to_nr_molecules(data, mm_compund) # in the order of 10**27 
    mass_S = nr_molecules_to_mass(nr_molecules, mm_s)*0.001
    return mass_S/10000 # to be divid by days in month

def unitconv_wet_depo(data, ts_type = "monthly"):
    """ Unitconversion kg S/ha to kg SOx/m2.

    Adding mass of oksygen.
    
    Parameters
    ------------------
    data: ndarray
        data in unit kg S/ha = kg S/(1000 m2)

    ts_type : str
        The timeseries type. Default "monthly".


    Returns
    ------------------
    data : ndarray
        data in units of ugSOx/m3

    """

    mm_s = 0.001*32.065 # in kilos pr mol
    mm_o = 4*15.9999 # molar mass of four okygen atom in kilo
    #mm_compound = mm_s + mm_o
    
    nr_molecules = mass_to_nr_molecules(data, mm_s) # in the order of 10**27 
    added_weight_oksygen = nr_molecules_to_mass(nr_molecules, mm_o)*0.001 
    # added_weight_oksygen [ mass in kg ]
    
    mass = data + added_weight_oksygen
    return mass*10000
