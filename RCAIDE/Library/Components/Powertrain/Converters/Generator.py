# RCAIDE/Library/Components/Propulsors/Converters/Generator.py
# 
# 
# Created:  Jan 2025, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports  
from .Converter  import Converter
from RCAIDE.Library.Methods.Powertrain.Converters.Generator.append_generator_conditions import  append_generator_conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Generator  
# ----------------------------------------------------------------------------------------------------------------------           
class Generator(Converter):
    """
    A electric generator component model for electric propulsion systems.

    Attributes
    ----------
    tag : str
        Identifier for the generator. Default is 'generator'.
        
    resistance : float
        Internal electrical resistance of the generator [Ω]. Default is 0.0.
        
    no_load_current : float
        Current drawn by the generator with no mechanical load [A]. Default is 0.0.
        
    speed_constant : float
        generator speed constant (Kv). Default is 0.0.
        
    rotor_radius : float
        Radius of the generator's rotor [m]. Default is 0.0.
        
    rotor_Cp : float
        Specific heat capacity of the rotor [J/kg/K]. Default is 0.0.
        
    efficiency : float
        Overall generator efficiency. Default is 1.0.
        
    gear_ratio : float
        Ratio of output shaft speed to generator speed. Default is 1.0.
        
    gearbox_efficiency : float
        Efficiency of the gearbox. Default is 1.0.
        
    expected_current : float
        Expected operating current [A]. Default is 0.0.
        
    power_split_ratio : float
        Ratio of power distribution when generator drives multiple loads. Default is 0.0.
        
    design_torque : float
        Design point torque output [N·m]. Default is 0.0.
        
    interpolated_func : callable
        Function for interpolating generator performance. Default is None.

    Notes
    -----
    The DC_generator class models a direct current electric generator's performance
    characteristics. It accounts for electrical, mechanical, and thermal effects
    including:
    * Internal resistance losses
    * No-load current losses
    * Gearbox losses
    * Speed-torque relationships
    * Power distribution for multiple loads

    **Definitions**

    'Kv'
        generator velocity constant, relating voltage to unloaded generator speed

    'No-load Current'
        Current drawn by generator to overcome internal friction when unloaded
        
    'Power Split Ratio'
        Fraction of total power delivered to primary load in multi-load applications

    See Also
    --------
    RCAIDE.Library.Methods.Powertrain.Converters.generator
    """      
    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """           
        self.tag                = 'generator' 
        self.resistance         = 0.0
        self.no_load_current    = 0.0
        self.speed_constant     = 0.0 
        self.efficiency         = 1.0
        self.gear_ratio         = 1.0
        self.gearbox_efficiency = 1.0
        self.expected_current   = 0.0 
        self.design_torque      = 0.0 
        self.interpolated_func  = None
        
    def append_operating_conditions(self,segment,propulsor):
        propulsor_conditions =  segment.state.conditions.energy[propulsor.tag]
        append_generator_conditions(self,segment,propulsor_conditions)
        return
    