''' @file    task_user.py
    @brief   Implements a user interface for Lab 03.
    @author  Marcus Monroe
    @author  Cade Liberty
    @author  Juan Luna
    @date    January 30, 2022
'''
import serial
import matplotlib.pyplot as plt
import time

## @brief   Communication port number for task user
COM_num = "COM6"       
        
def send(command):
    '''!    @brief  Sends the proportional gain value over serial.
    '''
    port.write((command+"\r\n").encode('utf-8'))
        
def read():
    '''!    @brief  Reads data from the serial port sent by the Nucleo.
    '''
    ## @brief   Data from serial port
    data = port.readline().decode('utf-8')
                
if __name__ == '__main__':
    ## Boolean variable for triggering plotting of the data.
    print_flag = False
    ## Boolean variable that tells program whether Kp is already sent over serial.
    Kp_flag = False
    ## Boolean variable that tells program if recording has started.
    record_flag = False
    ## List of time stamps for each encoder reading value.
    time_list = []
    ## List of encoder position values in step response.
    position = []

    with serial.Serial(str(COM_num), 115200) as port:
    
        while True:
            if print_flag == False:
                if Kp_flag == False:
                    print('Please enter the set point value for Motor 1: ')
                    send(input())
                    print('Please enter a Kp value for Motor 1: ')
                    send(input())
                    print('Please enter the set point value for Motor 2: ')
                    send(input())
                    print('Please enter a Kp value for Motor 2: ')
                    send(input())
                    
                    Kp_flag = True
                    ## @brief   Timing variable keeping track of starting time.
                    start_time = time.time()
                else:

                    try:
                        ## @brief   Data from serial port
                        data = port.readline().decode('utf-8')
                        ## @brief   Current data from serial port
                        current_data = [idx for idx in data.replace('r\n', '').split(',')]
                        
                        time_list.append(float(current_data[0]))
                        position.append(float(current_data[1]))
                    except:
                        pass
                    
                    if (time.time()- start_time) > 2:
                        print_flag = True
                                 
            elif print_flag == True:
                print('Printing a plot...')
                time_list.pop(-1)

                ## @brief   fig     Figure on which plot will be shown.

                ## @brief   ax      Axis for the plot
                fig, ax = plt.subplots()

                # Scatter plot of time and position data.
                ax.scatter(time_list, position)

                # Plot labels: title, x-label, and y-label
                ax.set_title("Response Plot")
                ax.set_xlabel("Time, ms")
                ax.set_ylabel("Position, ticks")
                    
                # Display the figure
                plt.show()

                print_flag = False
                
            
                    