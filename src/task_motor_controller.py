'''!    @file    task_motor_controller.py
        @brief   Runs the motor and controller tasks together.  
        @details Implements closed-loop position control on a motor
                 using a task defined as a generator.
        @author  Cade Liberty
        @author  Juan Luna
        @author  Marcus Monroe
        @date    February 10, 2022
'''
import controller
import motor
import utime
import print_task
import array

class Task_Motor_Controller:
     def __init__(self, encoder_share, gain_share, set_point_share, ENA_pin, In1_pin, In2_pin, Timer):
        '''! @brief    Instantiates objects of the Task_Motor_Controller class.
             @param  encoder_share  Passes the present value from the encoder
             @param  gain_share    Share variable for proportional gain value.
             @param  set_point_share   Share variable for setpoint value.
             @param  ENA_pin            Enable pin object for the motor.
             @param  In1A_pin       Control pin 1 associated with motor.
             @param  In2A_pin       Control pin 2 associated with motor.
             @param  Timer          Timer object for motor.
        '''
        # Define shares for motor and encoder 1
        self.encoder_share = encoder_share
        self.gain_share = gain_share
        self.set_point_share = set_point_share
        
        # Define motor-related pin objects
        self.ENA = ENA_pin
        self.IN1A_pin = In1_pin
        self.IN2A_pin = In2_pin
        self.tim_MOT_A = Timer
        
        ## @brief  Motor object
        self.motor = motor.MotorDriver(self.ENA, self.IN1A_pin, self.IN2A_pin, self.tim_MOT_A)
         
        ## @brief  Timing variable for tracking starting time.
        self.start_time = utime.ticks_ms()
        ## @brief  Timing variable for recording time.
        self.record_time = self.start_time
        ## @brief  Timing variabe for recording period.
        self.record_period = 20
        ## @brief  Array of time data point values for plotting.
        self.time_list = array.array('i', [1000]*0)
        ## @brief  Array of position values for plotting.
        self.position_list = array.array('f', [1000]*0)
        
     def run(self):
         '''! @brief Runs the controller task and sets new duty cycle 
         '''
         ## @brief  Controller object
         self.controller = controller.controller(self.set_point_share.get(), self.gain_share.get())
         
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

             print_task.put(str(true_position))
            
             yield (0)
             
     def prints(self):
         '''! @brief    Prints time and position data for plotting.
         '''
         for k in range(len(self.time_list)):

             self.time = utime.ticks_diff(self.time_list[k], self.time_list[0])
             print(self.time  ,',', self.position_list[k])

         self.motor.set_duty_cycle(0)     
         self.time_list = array.array('i', [1000]*0)
         self.position_list = array.array('f', [1000]*0)