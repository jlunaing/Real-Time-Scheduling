''' @file    controller.py
    @brief   Runs proportional closed loop control
    @details Multiplies difference between setpoint location and 
             measured location with value Kp to get new dutycycle
    @author  Marcus Monroe
    @author  Cade Liberty
    @author  Juan Luna
    @date    January 31, 2022
'''

class controller:
    def __init__(self, setpoint, gain_share):
        '''! @brief  Initializes objects of the EncoderDriver class.
             @param  setpoint  Chosen motor position value
             @param  gain      Kp, proportional gain value
        '''  
        self.setpoint = setpoint.get()
        self.gain_share = gain_share
    
    def run(self, measured):
        ''' @brief Runs closed loop control calculation
            @param measured  measured position value from encoder
        '''
        print('Measured: ', measured)
        self.error = float(self.setpoint) - float(measured)
        self.gain = float(self.gain_share.get())
        return (self.error*self.gain)
    
    def setpoint(self, setpoint):        
        ''' @brief  Establishes new reference value
            @param setpoint  reference value selected by user
        '''
        self.setpoint = setpoint
        
    def set_gain(self, gain):
        ''' @brief Establishes new Kp value
            @param gain  Kp value, the proportional gain
        '''
        self.gain = gain
    