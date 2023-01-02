"""!
@file       main.py
    Imports modules responsible for executing tasks implementing closed-loop 
    position control on a DC motor. Cooperative multi-tasking is used to run 
    tasks sequentially and share resources. This time, we integrated the code 
    developed previously in Project 0x12 into a real-time scheduler and tested 
    its performance.

@author     Juan Luna
@date       2022-02-10 Original file
@date       2022-12-30 Modified for portfolio update
"""

import gc
import pyb
import cotask
import task_share
import task_encoder
import task_motor_controller

if __name__ == "__main__":

    # Define encoder pin objects -------------------------------
    
    # ENCODER 1

    ## First pin object for encoder channel.
    ENC1A_pin_1 = pyb.Pin.cpu.C6
    ## Second pin object for encoder channel.
    ENC1B_pin_1 = pyb.Pin.cpu.C7
    ## Timer object for encoder.
    tim_ENC_A_1 = pyb.Timer(8, prescaler = 0, period = 2**16 - 1)
    
    # ENCODER 2

    ## First pin object for encoder channel.
    ENC1A_pin_2 = pyb.Pin.cpu.B6
    ## Second pin object for encoder channel.
    ENC1B_pin_2 = pyb.Pin.cpu.B7
    ## Timer object for encoder.
    tim_ENC_A_2 = pyb.Timer(4, prescaler = 0, period = 2**16 - 1)
    
    # Define motor pin objects ---------------------------------
    
    # First motor

    ## Enable pin object
    ENA_pin_1 = pyb.Pin(pyb.Pin.cpu.C1, pyb.Pin.OUT_PP)
    ## First control pin of motor
    In1_pin_1 = pyb.Pin.cpu.A0
    ## Second control pin of motor
    In2_pin_1 = pyb.Pin.cpu.A1
    ## Timer object for motor with 20-kHz frequency
    Timer_1   = pyb.Timer(5, freq = 20000)

    # Second motor

    ## Enable pin object
    ENA_pin_2 = pyb.Pin(pyb.Pin.cpu.C1, pyb.Pin.OUT_PP)
    ## First control pin of motor
    In1_pin_2 = pyb.Pin.cpu.B4
    ## Second control pin of motor
    In2_pin_2 = pyb.Pin.cpu.B5
    ## Timer object for motor with 20-kHz frequency
    Timer_2   = pyb.Timer(3, freq = 20000)
    
    # Create shared variables

    ## Encoder share variable for encoder 1
    encoder_share_1   = task_share.Share ('h', thread_protect = False, name = "Encoder_Share_1")
    ## Gain share variable for motor 1
    gain_share_1      = task_share.Share ('f', thread_protect = False, name = "Gain_Share_1")
    ## Setpoint variable for motor 1
    set_point_share_1 = task_share.Share ('f', thread_protect = False, name = "Set _Point _Share_1")
    ## Encoder share variable for encoder 2
    encoder_share_2   = task_share.Share ('h', thread_protect = False, name = "Encoder_Share_2")
    ## Gain share variable for motor 2
    gain_share_2      = task_share.Share ('f', thread_protect = False, name = "Gain_Share_2")
    ## Setpoint variable for motor 2
    set_point_share_2 = task_share.Share ('f', thread_protect = False, name = "Set_Point_Share_2")
    
    # Tracking values for debugging

    ## Counter variable
    count = 0

    ## Serial input Boolean variable flag
    serial_input = False
    
    # Define task objects

    ## Encoder 1 task object
    task_encoder1 = task_encoder.Task_Encoder(encoder_share_1, ENC1A_pin_1, ENC1B_pin_1, tim_ENC_A_1)
    ## Encoder 2 task object
    task_encoder2 = task_encoder.Task_Encoder(encoder_share_2, ENC1A_pin_2, ENC1B_pin_2, tim_ENC_A_2) 
    ## Motor Controller 1 task object
    task_motor_controller1 = task_motor_controller.Task_Motor_Controller(encoder_share_1, gain_share_1, set_point_share_1, ENA_pin_1, In1_pin_1, In2_pin_1, Timer_1)
    ## Motor Controller 2 task object
    task_motor_controller2 = task_motor_controller.Task_Motor_Controller(encoder_share_2, gain_share_2, set_point_share_2, ENA_pin_2, In1_pin_2, In2_pin_2, Timer_2)    

    ## Encoder 1 task object from cotask module     
    task_enc1 = cotask.Task (task_encoder1.run, name = 'Task_Encoder', priority = 2, 
                        period = 1, profile = True, trace = False)
    ## Encoder 2 task object from cotask module 
    task_enc2 = cotask.Task (task_encoder2.run, name = 'Task_Encoder', priority = 2, 
                        period = 1, profile = True, trace = False)
    ## Motor 1 task object from cotask module 
    task_mot1 = cotask.Task (task_motor_controller1.run, name = 'Task_Controller', priority = 2, 
                        period = 5, profile = True, trace = False)
    ## Motor 2 task object from cotask module 
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
    ## Virtual COM port object
    vcp = pyb.USB_VCP ()
    
    while True:
        
        if serial_input == False:
            ## First setpoint
            setpoint1 = input()
            ## First proportional gain
            kp1 = input()
            ## Second setpoint
            setpoint2 = input()
            ## Second proportional gain
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
                    if  set_point_share_1.get() - set_point_share_1.get()*.1 >=  encoder_share_1.get() <= set_point_share_1.get() + set_point_share_1.get()*.1 and set_point_share_2.get() - set_point_share_2.get()*.1 >=  encoder_share_2.get() <= set_point_share_2.get() + set_point_share_2.get()*.1:
        
                        serial_input = False
                        count = 0
                        print('Run Complete!')
                        task_encoder1.zero()
                        task_encoder2.zero()
                        task_motor_controller1.set_duty_cycle(0)
                        task_motor_controller2.set_duty_cycle(0)
                            
                    elif count > 1010:
                        serial_input = False
                        count = 0
                        task_encoder1.zero()
                        task_encoder2.zero()
                        task_motor_controller1.set_duty_cycle(0)
                        task_motor_controller2.set_duty_cycle(0)
                      
            except KeyboardInterrupt:
                break

    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()