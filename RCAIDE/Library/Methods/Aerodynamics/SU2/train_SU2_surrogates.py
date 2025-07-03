# RCAIDE/Library/Methods/Aerodynamics/Vortex_Lattice_Method/train_SU2_surrogates.py
#  
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
import RCAIDE 
from RCAIDE.Framework.Core import  Data 
from RCAIDE.Library.Methods.Aerodynamics.SU2.SU2   import SU2 
from copy import deepcopy

# package imports
import numpy  as np

# ----------------------------------------------------------------------------------------------------------------------
#  Vortex_Lattice
# ---------------------------------------------------------------------------------------------------------------------- 
def train_SU2_surrogates(aerodynamics):
    """  
    """
 
    Mach           = aerodynamics.training.Mach   
    vehicle        = deepcopy(aerodynamics.vehicle)
    settings       = aerodynamics.settings
    AoA            = aerodynamics.training.angle_of_attack  
    training       = aerodynamics.training        
    training.Mach  = Mach 
     
    len_Mach       = len(Mach)        
    len_AoA        = len(AoA)   
    
    # --------------------------------------------------------------------------------------------------------------
    # Alpha
    # --------------------------------------------------------------------------------------------------------------
    
    # Setup new array shapes for vectorization  
    AoAs       = np.atleast_2d(np.tile(AoA,len_Mach).T.flatten()).T 
    Machs      = np.atleast_2d(np.repeat(Mach,len_AoA)).T        
     
    conditions                                      = RCAIDE.Framework.Mission.Common.Results()
    conditions.freestream.mach_number               = Machs
    conditions.aerodynamics.angles.alpha            = np.ones_like(Machs)*AoAs 
    
    # Call SU2 
    SU2_results      = SU2(conditions,settings,vehicle)
    Clift_res        = SU2_results.CLift
    Cdrag_res        = SU2_results.CDrag_induced 
    S_ref            = SU2_results.S_ref
    b_ref            = SU2_results.b_ref
    c_ref            = SU2_results.c_ref
    X_ref            = SU2_results.X_ref
    Y_ref            = SU2_results.Y_ref
    Z_ref            = SU2_results.Z_ref        
    
    Clift_alpha   = np.reshape(Clift_res,(len_Mach,len_AoA)).T 
    Cdrag_alpha   = np.reshape(Cdrag_res,(len_Mach,len_AoA)).T  

    aerodynamics.reference_values.S_ref = S_ref
    aerodynamics.reference_values.b_ref = b_ref
    aerodynamics.reference_values.c_ref = c_ref
    aerodynamics.reference_values.X_ref = X_ref
    aerodynamics.reference_values.Y_ref = Y_ref
    aerodynamics.reference_values.Z_ref = Z_ref
    aerodynamics.reference_values.aspect_ratio = (b_ref ** 2) / S_ref
    
    Clift_wing_alpha = Data()
    Cdrag_wing_alpha = Data() 
    for wing in vehicle.wings: 
        Clift_wing_alpha[wing.tag] = np.reshape(SU2_results.CLift_wings[wing.tag],(len_Mach,len_AoA)).T    
        Cdrag_wing_alpha[wing.tag] = np.reshape(SU2_results.CDrag_induced_wings[wing.tag],(len_Mach,len_AoA)).T  
   
        
    # STABILITY COEFFICIENTS  
    training.Clift_alpha       = Clift_alpha  
    training.Cdrag_alpha       = Cdrag_alpha   
    training.Cdrag_wing_alpha  = Cdrag_wing_alpha     
      
    # STABILITY DERIVATIVES 
    training.dClift_dalpha = (Clift_alpha[0,:] - Clift_alpha[1,:]) / (AoA[0] - AoA[1])     
    
    return training
        
        
