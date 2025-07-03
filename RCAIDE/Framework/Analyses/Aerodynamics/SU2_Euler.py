# RCAIDE/Framework/Analyses/Aerodynamics/SU2_Euler.py
#  
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports   
from RCAIDE.Framework.Core                                           import Data, Units
from RCAIDE.Framework.Analyses                                       import Process 
from RCAIDE.Library.Methods.Aerodynamics                             import Common
from .Aerodynamics                                                   import Aerodynamics 
from RCAIDE.Framework.Analyses.Common.Process_Geometry               import Process_Geometry  
from RCAIDE.Library.Methods.Aerodynamics.SU2                         import *   
from RCAIDE.Framework.External_Interfaces.OpenVSP.export_vsp_vehicle import export_vsp_vehicle 
from RCAIDE.Framework.External_Interfaces.OpenVSP.run_cfd_mesh       import run_vsp_mesh 
from RCAIDE.Framework.External_Interfaces.GMSH.write_SU2_file        import write_SU2_file

# package imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Vortex_Lattice_Method
# ---------------------------------------------------------------------------------------------------------------------- 
class SU2_Euler(Aerodynamics):
    """This is a

     Assumptions:
     Stall effects are negligible 
 
     Source:
     N/A
 
     Inputs:
     None
 
     Outputs:
     None
 
     Properties Used:
     N/A 
    """      
    
    def __defaults__(self):
        """This sets the default values and methods for the analysis.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """          
        self.tag                                                    = 'Vortex_Lattice_Method'
        self.vehicle                                                = Data()  
        self.process                                                = Process()
        self.process.initialize                                     = Process()

        self.settings.vsp_filename                                  = None
        self.settings.stl_filename                                  = None
        self.settings.SU2_filename                                  = None
        self.settings.SU2_config_filename                           = None
        self.settings.half_mesh_flag                                = False
        self.settings.number_of_processors                          = 8
        self.settings.vsp_mesh_growth_ratio                         = False
        self.settings.vsp_mesh_growth_limiting_flag                 = False
    
        # conditions table, used for surrogate model training
        self.training                                               = Data()
        self.training.angle_of_attack                               = np.array([-5., -2. , 1E-20 , 2.0, 5.0, 8.0, 12., ]) * Units.deg 
        self.training.Mach                                          = np.array([0.1  ,0.3,  0.5,  0.65 , 0.85 ])             
           
        self.reference_values                                       = Data()
        self.reference_values.S_ref                                 = 0
        self.reference_values.c_ref                                 = 0
        self.reference_values.b_ref                                 = 0
        self.reference_values.X_ref                                 = 0
        self.reference_values.Y_ref                                 = 0
        self.reference_values.Z_ref                                 = 0 
                          
        # surrogoate models                 
        self.surrogates                                             = Data() 

        # build the evaluation process
        compute                                                     = Process() 
        compute.lift                                                = Process()  
        compute.lift.inviscid_wings                                 = evaluate_surrogate
        compute.lift.fuselage                                       = Common.Lift.fuselage_correction 
        #compute.LIFT.spoiler                  
        compute.drag                                                = Process()
        compute.drag.parasite                                       = Process()
        compute.drag.parasite.wings                                 = Process_Geometry('wings')
        compute.drag.parasite.wings.wing                            = Common.Drag.parasite_drag_wing 
        compute.drag.parasite.fuselages                             = Process_Geometry('fuselages')
        compute.drag.parasite.fuselages.fuselage                    = Common.Drag.parasite_drag_fuselage
        compute.drag.parasite.booms                                 = Process_Geometry('booms')
        compute.drag.parasite.booms.boom                            = Common.Drag.parasite_drag_fuselage 
        compute.drag.parasite.nacelles                              = Common.Drag.parasite_drag_nacelle
        compute.drag.parasite.pylons                                = Common.Drag.parasite_drag_pylon
        compute.drag.parasite.total                                 = Common.Drag.parasite_total
        compute.drag.induced                                        = Common.Drag.induced_drag
        compute.drag.cooling                                        = Process()
        compute.drag.cooling.total                                  = Common.Drag.cooling_drag        
        compute.drag.compressibility                                = Process() 
        compute.drag.compressibility.total                          = Common.Drag.compressibility_drag
        compute.drag.miscellaneous                                  = Common.Drag.miscellaneous_drag 
        compute.drag.spoiler                                        = Common.Drag.spoiler_drag
        compute.drag.total                                          = Common.Drag.total_drag
        compute.stability                                           = Process()
        compute.stability.dynamic_modes                             = RCAIDE.Library.Methods.Stability.compute_dynamic_flight_modes  
        self.process.compute                                        = compute
        

    def initialize(self):
        vehicle = self.vehicle
        export_vsp_vehicle(vehicle, vehicle.tag)
        
        vsp_filename        =  vehicle.tag +  '.vsp3'
        stl_filename        =  vehicle.tag +  '.stl'  
        SU2_filename        =  vehicle.tag +  '.su2'  
        SU2_config_filename =  vehicle.tag +  '.cfg'       
        run_vsp_mesh(vehicle,vsp_filename, 0.25/20,0.25, sym=False,farfield_scale=25.0,farfield=True,source=False)
        write_SU2_file(stl_filename, SU2_filename)
        
        self.settings.vsp_filename        = vsp_filename
        self.settings.stl_filename        = stl_filename
        self.settings.SU2_filename        = SU2_filename
        self.settings.SU2_config_filename = SU2_config_filename
        
        # sample training data
        train_SU2_surrogates(self)

        # build surrogate
        build_SU2_surrogates(self)
            
        return 
    
         
    def evaluate(self,state):
        """The default evaluate function.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        results   <RCAIDE data class>

        Properties Used:
        self.settings
        self.vehicle
        """          
        settings = self.settings
        vehicle  = self.vehicle 
        results  = self.process.compute(state,settings,vehicle)
        
        return results