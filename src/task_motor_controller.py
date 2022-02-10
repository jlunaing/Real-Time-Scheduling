''' @file    task_motor_controller.py
    @brief   Runs the motor and controller together  
    @details 
    @author  Marcus Monroe
    @author  Cade Liberty
    @author  Juan Luna
    @date    January 31, 2022
'''
import controller
import motor
import utime
import print_task
import array

class Task_Motor_Controller:
     def __init__(self, encoder_share, gain_share, set_point_share, ENA_pin, In1_pin, In2_pin, Timer):         
         ''' @brief Sets
             @param  encoder_share  Passes the present valeu from the encoder
             @param  motor_share    Shared variable to set new duty cycle
         '''
         # Define share variables
         self.encoder_share = encoder_share
         self.gain_share = gain_share
         self.set_point_share = set_point_share
         
         # Define controller
         self.controller = controller.controller(self.set_point_share, self.gain_share)
        
         # Define motor-related pin objects
         self.ENA = ENA_pin
         self.IN1A_pin = In1_pin
         self.IN2A_pin = In2_pin
         self.tim_MOT_A = Timer
        
         # Define motor object
         self.motor = motor.MotorDriver(self.ENA, self.IN1A_pin, self.IN2A_pin, self.tim_MOT_A)
         
         self.start_time = utime.ticks_ms()
         self.record_time = self.start_time
         self.record_period = 20
         self.time_list = array.array('i', [1000]*0)
         self.position_list = array.array('f', [1000]*0)
        
     def run(self):
         ''' @brief Runs the controller task and sets new duty cycle 
         '''
         
         while True:
             
             true_position = float(self.encoder_share.get())
             
             self.calc_error = self.controller.run(true_position)
             self.motor.set_duty_cycle(float(self.calc_error))
             
             self.current_time = utime.ticks_diff(utime.ticks_ms(), self.start_time)
             
             #if utime.ticks_diff(self.current_time,self.record_time) >=0: 
             self.time_list.append(self.current_time)
             self.position_list.append(true_position)
            #print(position_list)
                #self.record_time = utime.ticks_add(self.current_time, self.record_period)
             
            #print_task.put(str(self.current_time))
            # could use a string that is a dot format
            # example is    "it is: {:.3f}".format (1.23)
            # "one: {:d}, two: {:d}".format (1, 2)

             print_task.put(str(true_position))
            
             yield (0)
             
     def prints(self):
                  
         for k in range(len(self.time_list)):
             
             self.time = utime.ticks_diff(self.time_list[k], self.time_list[0])
             print('t: ', self.time  ,', x: ', self.position_list[k])
             
         self.motor.set_duty_cycle(0)     
         self.time_list = array.array('i', [1000]*0)
         self.position_list = array.array('f', [1000]*0)