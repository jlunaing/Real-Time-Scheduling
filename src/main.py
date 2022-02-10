"""!
@file main.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author Marcus Monroe
@author Cade Liberty
@author Juan Luna
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share
import task_encoder
import task_motor_controller
import print_task

if __name__ == "__main__":
        
    # Define encoder pin objects -------------------------------
    
    # First encoder
    ENC1A_pin_1 = pyb.Pin.cpu.C6
    ENC1B_pin_1 = pyb.Pin.cpu.C7
    tim_ENC_A_1 = pyb.Timer(8, prescaler = 0, period = 2**16 - 1)
    # Second encoder
    ENC1A_pin_2 = pyb.Pin.cpu.B6
    ENC1B_pin_2 = pyb.Pin.cpu.B7
    tim_ENC_A_2 = pyb.Timer(4, prescaler = 0, period = 2**16 - 1)
    
    # Define motor pin objects ---------------------------------
    
    # First motor
    ENA_pin_1 = pyb.Pin(pyb.Pin.cpu.C1, pyb.Pin.OUT_PP)
    In1_pin_1 = pyb.Pin.cpu.A0
    In2_pin_1 = pyb.Pin.cpu.A1
    Timer_1   = pyb.Timer(5, freq = 20000)
    # Second motor
    ENA_pin_2 = pyb.Pin(pyb.Pin.cpu.C1, pyb.Pin.OUT_PP)
    In1_pin_2 = pyb.Pin.cpu.B4
    In2_pin_2 = pyb.Pin.cpu.B5
    Timer_2   = pyb.Timer(3, freq = 20000)
    
    # Create shared variables
    encoder_share_1   = task_share.Share ('h', thread_protect = False, name = "Encoder Share 1")
    gain_share_1      = task_share.Share ('f', thread_protect = False, name = "Gain Share 1")
    set_point_share_1 = task_share.Share ('f', thread_protect = False, name = "Set Point Share 1")
    encoder_share_2   = task_share.Share ('h', thread_protect = False, name = "Encoder Share 2")
    gain_share_2      = task_share.Share ('f', thread_protect = False, name = "Gain Share 2")
    set_point_share_2 = task_share.Share ('f', thread_protect = False, name = "Set Point Share 2")
    
    # Tracking values for debugging
    count = 0
    serial_input = False
        
    # Define task objects
    task_encoder1 = task_encoder.Task_Encoder(encoder_share_1, ENC1A_pin_1, ENC1B_pin_1, tim_ENC_A_1)
    task_encoder2 = task_encoder.Task_Encoder(encoder_share_2, ENC1A_pin_2, ENC1B_pin_2, tim_ENC_A_2)

    task_motor_controller1 = task_motor_controller.Task_Motor_Controller(encoder_share_1, gain_share_1,
                                                                         set_point_share_1, ENA_pin_1,
                                                                         In1_pin_1, In2_pin_1, Timer_1)
    
    task_motor_controller2 = task_motor_controller.Task_Motor_Controller(encoder_share_2, gain_share_2,
                                                                         set_point_share_2, ENA_pin_2,
                                                                         In1_pin_2, In2_pin_2, Timer_2)    
    # Define objects of the Task class from cotask.py module
        
    task_enc1 = cotask.Task (task_encoder1.run, name = 'Task_Encoder', priority = 2, 
                                 period = 1, profile = True, trace = False)
    task_enc2 = cotask.Task (task_encoder2.run, name = 'Task_Encoder', priority = 2, 
                                 period = 1, profile = True, trace = False)
    task_mot1 = cotask.Task (task_motor_controller1.run, name = 'Task_Controller', priority = 2, 
                                 period = 5, profile = True, trace = False)
    task_mot2 = cotask.Task (task_motor_controller2.run, name = 'Task_Controller', priority = 2, 
                                 period = 5, profile = True, trace = False)
    
    cotask.task_list.append (task_enc1)
    cotask.task_list.append (task_enc2)
    cotask.task_list.append (task_mot1)
    cotask.task_list.append (task_mot2)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is received through the serial port
    vcp = pyb.USB_VCP ()
    
    while True:
        
        if serial_input == False:
            setpoint1 = input()
            kp1 = input()
            setpoint2 = input()
            kp2 = input()
            
            set_point_share_1.put(float(setpoint1))
            print('The setpoint you entered for Motor 1 is ', set_point_share_1.get())
            gain_share_1.put(float(kp1))
            print('The gain you entered for Motor 1 is ', gain_share_1.get())
            set_point_share_2.put(float(setpoint2))
            print('The setpoint you entered for Motor 2 is ', set_point_share_2.get())
            gain_share_2.put(float(kp2))
            print('The gain you entered is for Motor 2 ', gain_share_2.get())
            
            serial_input = True
            
        elif serial_input == True:
            try:
                
                cotask.task_list.pri_sched ()
                
                count +=1
                
                if count >= 1000:
                    if  16380 >=  encoder_share_1.get() <= 16390:
        
                        serial_input = False
                        count = 0
                        task_motor_controller1.prints()
                        task_encoder1.zero()
                            
                    elif count > 1010:
                        serial_input = False
                        count = 0
                        task_motor_controller1.prints()
                        task_encoder1.zero()
                                  
            except KeyboardInterrupt:
                break

    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()