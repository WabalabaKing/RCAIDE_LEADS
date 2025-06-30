# RCAIDE/Library/Methods/Aerodynamics/Vortex_Lattice_Method/build_SU2_surrogates.py
#  
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from RCAIDE.Framework.Core import  Data 

# package imports 
from scipy.interpolate    import RegularGridInterpolator 

# ----------------------------------------------------------------------------------------------------------------------
#  Vortex_Lattice
# ----------------------------------------------------------------------------------------------------------------------   
def build_SU2_surrogates(aerodynamics):
    """Build a surrogate using sample evaluation results.
    
    Assumptions:
        None
        
    Source:
        None

    Args:
        aerodynamics       : SU2 analysis          [unitless] 
        
    Returns: 
        None  
    """
    surrogates = aerodynamics.surrogates
    training   = aerodynamics.training    
    
    # unpack data
    surrogates     = Data()
    mach_data      = training.Mach 
    AoA_data       = aerodynamics.training.angle_of_attack
    
    # Pack the outputs     
    surrogates.Clift_alpha       = RegularGridInterpolator((AoA_data,mach_data),training.Clift_alpha        ,method = 'linear',   bounds_error=False, fill_value=None)     
    surrogates.Cdrag_alpha       = RegularGridInterpolator((AoA_data,mach_data),training.Cdrag_alpha         ,method = 'linear',   bounds_error=False, fill_value=None)          
      
    return surrogates
 
 
