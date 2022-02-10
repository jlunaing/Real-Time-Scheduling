'''! @file      controller.py
     @brief     A driver implementing proportional closed-loop control.
     @details   Computes the actuation value by multiplying the signal by the
                proportional controller gain, Kp. The error is found by
                calculating the difference between the setpoint (desired) value
                and measured value.
     @author    Cade Liberty
     @author    Juan Luna
     @author    Marcus Monroe
     @date      February 10, 2022
'''

class controller:
    '''! @brief     Driver class implementing proportional control.
        @details    Methods of this class set up attributes and methods
                    responsible for calculating the actuation value to be
                    sent to the motor for closed-loop control.
    '''
    def __init__(self, setpoint, gain_share):
        '''! @brief  Initializes objects of the EncoderDriver class.
             @param  setpoint  Chosen motor position value
             @param  gain      Kp, proportional gain value
        '''  
        self.setpoint = setpoint.get()
        self.gain_share = gain_share
    
    def run(self, measured):
        '''! @brief Runs closed loop control calculation
             @param measured  measured position value from encoder
        '''
        print('Measured: ', measured)
        self.error = float(self.setpoint) - float(measured)
        self.gain = float(self.gain_share.get())
        return (self.error*self.gain)
    
    def setpoint(self, setpoint):        
        '''! @brief  Establishes new reference value
             @param setpoint  reference value selected by user
        '''
        self.setpoint = setpoint
        
    def set_gain(self, gain):
        '''! @brief Establishes new Kp value
             @param gain  Kp value, the proportional gain
        '''
        self.gain = gain
    