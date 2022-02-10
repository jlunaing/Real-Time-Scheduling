'''!    @file    task_encoder.py
        @brief   Runs the encoder driver to receive current encoder position
        @details Establishes encoder pin values and runs encoder frequently 
                 to provide measured values to closed loop gain.
        @author  Cade Liberty
        @author  Juan Luna
        @author  Marcus Monroe
        @date    February 10, 2022
'''
import utime
import pyb
import encoder

class Task_Encoder:
    '''! @brief     Task implementing functionality of encoder driver.
    '''
    
    def __init__(self, encoder_share, ENC1A_pin, ENC1B_pin, tim_ENC_A):
        '''! @brief      Initializes objects of the Task_Encoder class.
             @param  encoder_share  Share variable storing encoder value.
             @param  ENC1A_pin    First pin object for encoder channel.
             @param  ENC1B_pin    Second pin object for encoder channel.
             @param  tim_ENC_A   Timer object for encoder.
        ''' 
        ## @brief   Share variable storing encoder value.
        self.encoder_share = encoder_share
        ## @brief   Encoder object
        self.encoder = encoder.EncoderDriver(ENC1A_pin, ENC1B_pin, tim_ENC_A)
        
        
    def run(self):
        '''! @brief Runs the encoder driver and position to share variable
        '''
        while True:   
            self.encoder_share.put(self.encoder.read())
            yield(0)

    def zero(self):
        '''! @brief Zeros the encoder reading
        '''
        self.encoder.zero()
        