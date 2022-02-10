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

COM_num = "COM6"       
        
def send(command):

    port.write((command+"\r\n").encode('utf-8'))
        
def read():
    data = port.readline().decode('utf-8')
                
if __name__ == '__main__':
    
    print_flag = False
    Kp_flag = False
    record_flag = False
    time_list = []
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
                    start_time = time.time()
                else:

                    try:
                        data = port.readline().decode('utf-8')
                        current_data = [idx for idx in data.replace('r\n', '').split(',')]
                        
                        time_list.append(float(current_data[0]))
                        position.append(float(current_data[1]))
                    except:
                        pass
                    
                    if (time.time()- start_time) > 2:
                        print_flag = True
                        
                       
                
            elif print_flag == True:
                print('Im printing a plot')
                time_list.pop(-1)
                fig, ax = plt.subplots()

                # Scatter plot of first and second columns of CSV data.
                ax.scatter(time_list, position)

                # Plot labels: title, x-label, and y-label
                ax.set_title("Response Plot")
                ax.set_xlabel("Time, ms")
                ax.set_ylabel("Position, ticks")
                    
                # Display the figure
                plt.show()
                plt.savefig("response1.png")
                print_flag = False
                
            
                    