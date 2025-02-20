# RCAIDE/Methods/Energy/Propulsors/Constant_Speed_ICE_Propulsor/compute_cs_ice_performance.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Framework.Core import Units  
from RCAIDE.Library.Methods.Powertrain.Converters.Engine import compute_throttle_from_power
from RCAIDE.Library.Methods.Powertrain.Converters.Rotor.compute_rotor_performance import  compute_rotor_performance
 
# pacakge imports  
from copy import deepcopy
import numpy as np  

# ----------------------------------------------------------------------------------------------------------------------
# compute_constant_speed_internal_combustion_engine_performance
# ----------------------------------------------------------------------------------------------------------------------  
def compute_constant_speed_internal_combustion_engine_performance(propulsor,state,fuel_line=None,bus=None,center_of_gravity= [[0.0, 0.0,0.0]]):  
    ''' Computes the perfomrance of one propulsor
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    conditions           - operating conditions data structure           [-]  
    fuel_line            - fuelline                                      [-] 
    propulsor        - propulsor data structure            [-] 
    total_thrust         - thrust of propulsor group              [N]
    total_power          - power of propulsor group               [W] 

    Outputs:  
    total_thrust         - thrust of propulsor group              [N]
    total_power          - power of propulsor group               [W] 
    stored_results_flag  - boolean for stored results                    [-]     
    stored_propulsor_tag - name of propulsor with stored results  [-]
    
    Properties Used: 
    N.A.        
    '''  
    conditions              = state.conditions  
    ice_cs_conditions       = conditions.energy[propulsor.tag] 
    engine                  = propulsor.engine 
    propeller               = propulsor.propeller
    engine_conditions       = ice_cs_conditions[engine.tag]
    engine_conditions.rpm   = conditions.energy[propulsor.tag].rpm 

    # Run the propeller to get the power
    propeller_conditions                = ice_cs_conditions[propeller.tag]
    propeller_conditions.omega          = engine_conditions.rpm * Units.rpm
    propeller_conditions.pitch_command  = ice_cs_conditions.throttle - 0.5
    propeller_conditions.throttle       = ice_cs_conditions.throttle
    compute_rotor_performance(propulsor,state,center_of_gravity)

    # Run the engine to calculate the throttle setting and the fuel burn
    engine_conditions.power        = conditions.energy[propulsor.tag][propeller.tag].power 
    compute_throttle_from_power(engine,engine_conditions,conditions) 
    
    # Create the outputs
    ice_cs_conditions.fuel_flow_rate         = engine_conditions.fuel_flow_rate  
    stored_results_flag                      = True
    stored_propulsor_tag                     = propulsor.tag  

    # compute total forces and moments from propulsor (future work would be to add moments from motors)
    conditions.energy[propulsor.tag].thrust      = conditions.energy[propulsor.tag][propeller.tag].thrust 
    conditions.energy[propulsor.tag].moment      = conditions.energy[propulsor.tag][propeller.tag].moment
    conditions.energy[propulsor.tag].power       = conditions.energy[propulsor.tag][propeller.tag].power 
    thrust_vector  = conditions.energy[propulsor.tag].thrust 
    moment  = conditions.energy[propulsor.tag].moment 
    power  = conditions.energy[propulsor.tag].power 
    

    # ADD CODE FOR SHAFT OFFTAKE AND MOTORS
    power_elec =  0*state.ones_row(3)
    
    return thrust_vector,moment,power,power_elec,stored_results_flag,stored_propulsor_tag 
    
def reuse_stored_constant_speed_internal_combustion_engine_data(propulsor,state,network,fuel_line,bus,stored_propulsor_tag,center_of_gravity= [[0.0, 0.0,0.0]]):
    '''Reuses results from one propulsor for identical propulsors
    
    Assumptions: 
    N/A

    Source:
    N/A

    Inputs:  
    conditions           - operating conditions data structure    [-]  
    fuel_line            - fuel_line                              [-] 
    propulsor        - propulsor data structure     [-] 
    total_thrust         - thrust of propulsor group       [N]
    total_power          - power of propulsor group        [W] 
     
    Outputs:      
    total_thrust         - thrust of propulsor group       [N]
    total_power          - power of propulsor group        [W] 
    
    Properties Used: 
    N.A.        
    ''' 
    conditions                 = state.conditions
    engine                     = propulsor.engine
    propeller                  = propulsor.propeller 
    engine_0                   = network.propulsors[stored_propulsor_tag].engine
    propeller_0                = network.propulsors[stored_propulsor_tag].propeller

    conditions.energy[propulsor.tag][engine.tag]        = deepcopy(conditions.energy[stored_propulsor_tag][engine_0.tag])
    conditions.energy[propulsor.tag][propeller.tag]     = deepcopy(conditions.energy[stored_propulsor_tag][propeller_0.tag])    
  
    thrust_vector           = conditions.energy[propulsor.tag][propeller.tag].thrust 
    power                   = conditions.energy[propulsor.tag][propeller.tag].power 
    
    moment_vector           = 0*state.ones_row(3) 
    moment_vector[:,0]      = propeller.origin[0][0]  -  center_of_gravity[0][0] 
    moment_vector[:,1]      = propeller.origin[0][1]  -  center_of_gravity[0][1] 
    moment_vector[:,2]      = propeller.origin[0][2]  -  center_of_gravity[0][2]
    moment                  =  np.cross(moment_vector, thrust_vector)
    
    conditions.energy[propulsor.tag][propeller.tag].moment = moment  
    conditions.energy[propulsor.tag].thrust            = thrust_vector   
    conditions.energy[propulsor.tag].moment            = moment  
    conditions.energy[propulsor.tag].power             = power

    power_elec =  0*state.ones_row(3)
    
    return thrust_vector,moment,power, power_elec
 