# SU2.py
#     
# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# package imports 
import numpy as np 
from RCAIDE.Framework.Core import Data

# ----------------------------------------------------------------------
#  Vortex Lattice
# ----------------------------------------------------------------------
def SU2(conditions,settings,geometry):
  
    # unpack settings---------------------------------------------------------------- 
    Sref       = geometry.reference_area              

    # unpack geometry----------------------------------------------------------------
    # define point about which moment coefficient is computed
    if 'main_wing' in geometry.wings:
        c_bar      = geometry.wings['main_wing'].chords.mean_aerodynamic
        x_mac      = geometry.wings['main_wing'].aerodynamic_center[0] + geometry.wings['main_wing'].origin[0][0]
        z_mac      = geometry.wings['main_wing'].aerodynamic_center[2] + geometry.wings['main_wing'].origin[0][2]
        b_ref      = geometry.wings['main_wing'].spans.projected
    else:
        c_bar  = 0.
        x_mac  = 0.
        b_ref = 0.
        for wing in geometry.wings:
            if wing.vertical == False:
                if c_bar <= wing.chords.mean_aerodynamic:
                    c_bar  = wing.chords.mean_aerodynamic
                    x_mac  = wing.aerodynamic_center[0] + wing.origin[0][0]
                    z_mac  = wing.aerodynamic_center[2] + wing.origin[0][2]
                    b_ref  = wing.spans.projected

    x_cg       = geometry.mass_properties.center_of_gravity[0][0]
    z_cg       = geometry.mass_properties.center_of_gravity[0][2]
    if x_cg == 0.0:
        x_m = x_mac 
        z_m = z_mac
    else:
        x_m = x_cg
        z_m = z_cg
        
    # unpack conditions--------------------------------------------------------------
    aoa  = conditions.aerodynamics.angles.alpha      # angle of attack  
    mach = conditions.freestream.mach_number         # mach number
    ones = np.atleast_2d(np.ones_like(mach)) 
    len_mach = len(mach)
    
  
    # ---------------------------------------------------------------------------------------
    # STEP 13: Pack outputs
    # ------------------ --------------------------------------------------------------------    
    
    results =  Data()
    # force coefficients
    results.S_ref             = 0
    results.b_ref             = 0
    results.c_ref             = 0
    results.X_ref             = 0
    results.Y_ref             = 0
    results.Z_ref             = 0
    results.CLift             = 0
    results.CX                = 0
    results.CY                = 0
    results.CZ                = 0
    results.CL                = 0
    results.CM                = 0
    results.CN                = 0
    results.chord_sections    = 0
    results.spanwise_stations = 0
    results.CLift_wing        = 0
    results.sectional_CLift   = 0
    results.CP                = 0
    results.gamma             = 0
    results.VD                = 0
    results.V_distribution    = 0
    results.V_x               = 0
    results.V_z               = 0
    
    return 
    
 