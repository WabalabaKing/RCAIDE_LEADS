# RCAIDE/Methods/Noise/Correlation_Buildup/Engine/primary_noise_component.py
# 
# 
# Created:  Jul 2023, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
# Python package imports   
import numpy as np   

# ----------------------------------------------------------------------------------------------------------------------     
#  Primary Noise Component
# ----------------------------------------------------------------------------------------------------------------------          
def primary_noise_component(Velocity_primary, Temperature_primary, R_gas, theta_p, DVPS, sound_ambient, 
                            Velocity_secondary, Velocity_aircraft, Area_primary, Area_secondary, DSPL_p, EX_p, Str_p):
    """
    This function calculates the noise contribution of the primary jet component.

    Parameters
    ----------
    Velocity_primary : float
        Velocity of the primary jet [m/s].
    Temperature_primary : float
        Temperature of the primary jet [K].
    R_gas : float
        Specific gas constant [J/(kg·K)].
    theta_p : float
        Angle for the primary jet [rad].
    DVPS : float
        Design velocity parameter for the primary jet.
    sound_ambient : float
        Ambient sound level [SPL].
    Velocity_secondary : float
        Velocity of the secondary jet [m/s].
    Velocity_aircraft : float
        Velocity of the aircraft [m/s].
    Area_primary : float
        Area of the primary jet [m^2].
    Area_secondary : float
        Area of the secondary jet [m^2].
    DSPL_p : float
        Decibel Sound Pressure Level for the primary jet [SPL].
    EX_p : float
        Excess noise level for the primary jet.
    Str_p : float
        Strouhal number for the primary jet.

    Returns
    -------
    SPL_p : float
        Sound Pressure Level for the primary jet component [dB].

    Notes
    -----
    The function uses empirical methods to calculate the noise contribution of the primary jet component.

    **Definitions**

    'SPL_p'
        Sound Pressure Level for the primary jet component.

    References
    ----------
    [1] SAE ARP876D: Gas Turbine Jet Exhaust Noise Prediction (original)
    [2] de Almeida, Odenir. "Semi-empirical methods for coaxial jet noise prediction." (2008). (adapted)
    """

    # Flow parameters of the primary jet
    sound_primary    = np.sqrt(1.4*R_gas*Temperature_primary) 
    Mach_primary_jet = Velocity_primary/sound_primary  
    
    # Calculation of the velocity exponent 
    velocity_exponent = 1.5*np.exp(-10*(theta_p - 2.2)**2)
    if theta_p <= 2.2: 
        velocity_exponent = 1.56

    # Calculation of the Source Strengh Function (FV)
    FV = Mach_primary_jet*(DVPS/sound_ambient)**0.6*((Velocity_primary+Velocity_secondary)/sound_ambient)**0.4*  (np.abs(Velocity_primary-Velocity_aircraft)/Velocity_primary)**velocity_exponent

    # Determination of the noise model coefficients
    Z1 = -18*((1.8*theta_p/np.pi)-0.6)**2
    Z2 = -18-18*((1.8*theta_p/np.pi)-0.6)**2
    Z3 = 0.0
    Z4 = -0.1 - 0.75*((Velocity_primary-Velocity_secondary-Velocity_aircraft)/sound_ambient) *  ((1.8*theta_p/np.pi)-0.6)**3. + 0.8*(0.6-np.log10(1+Area_secondary/Area_primary))
    Z5 = 50 + 20*np.exp(-(theta_p-2.6)**2.)
    Z6 = 94 + 46*np.exp(-(theta_p-2.5)**2.) - 26.*(0.6-np.log10(1+Area_secondary/Area_primary))/  np.exp(5*(theta_p-2.3)**2) + DSPL_p + EX_p

    # Determination of Sound Pressure Level for the primary jet component
    SPL_p = (Z1*np.log10(FV)+Z2) * (np.log10(Str_p)-Z3*np.log10(FV)-Z4)**2 + Z5*np.log10(FV) + Z6

    return SPL_p

