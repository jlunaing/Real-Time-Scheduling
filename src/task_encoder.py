''' @file    task_encoder.py
    @brief   Runs the encoder driver to receive current encoder position
    @details Establishes encoder pin values and runs encoder frequently 
             to provide measured values to closed loop gain
    @author  Marcus Monroe
    @author  Cade Liberty
    @author  Juan Luna
    @date    January 31, 2022
'''
import utime
import pyb
import encoder

class Task_Encoder:
    
    def __init__(self, encoder_share,ENC1A_pin,ENC1B_pin,tim_ENC_A):
        '''! @brief      Initializes objects of the EncoderDriver class.
             @param  encoder_share  Shared variable storing encoder value  
        '''  
        self.encoder_share = encoder_share
        
        self.encoder = encoder.EncoderDriver(ENC1A_pin, ENC1B_pin, tim_ENC_A)
        
        
    def run(self):
        ''' @brief Runs the encoder driver and position to shared variable
        '''
        while True:   
            self.encoder_share.put(self.encoder.read())
            yield(0)

    def zero(self):
        ''' @brief Zeros the encoder reading
        '''
        self.encoder.zero()
        