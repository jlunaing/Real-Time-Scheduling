# Lab 03: Real-Time Scheduler
 This repository contains the source code and documentation for Lab 3 of ME 405 (Mechatronics) course at California Polytechnic State University.
 
 In this laboratory exercise, we integrated the code developed in the previous week, a closed-loop motor position control system, into a real-time scheduler and tested its performance. 
 
 First, we started running the controller task at a 10-ms period and with a proportional gain value of 0.03. The step response plot is shown below (**Figure 1**). Then, we gradually increased the period to watch for changes in the step response plot.
 
 ![Step response with Kp = 0.3, period = 10 ms](https://github.com/jdlu97/Lab-3/blob/main/src/figure_1.png?raw=true)
 
 **Figure 1:** Motor step response with a proportional gain value of **Kp = 0.3** and with its motor control task running at a period of **10 ms**.
 
 ![Step response with Kp = 0.3, period = 20 ms](https://github.com/jdlu97/Lab-3/blob/main/src/figure_2.png?raw=true)
 
 **Figure 2:** Motor step response with a proportional gain value of **Kp = 0.3** and with its motor control task running at a period of **20 ms**.
 
 ![Step response with Kp = 0.3, period = 40 ms](https://github.com/jdlu97/Lab-3/blob/main/src/figure_3.png?raw=true)
 
 **Figure 3:** Motor step response with a proportional gain value of **Kp = 0.3** and with its motor control task running at a period of **40 ms**.

![Step response with Kp = 0.3, period = 60 ms](https://github.com/jdlu97/Lab-3/blob/main/src/figure_4.png?raw=true)
 
 **Figure 4:** Motor step response with a proportional gain value of **Kp = 0.3** and with its motor control task running at a period of **60 ms**.
 
 As we can see from the plots, at around a 80-ms period, the response is still relatively the same. Ideally, we would have shown further plots at higher periods that displayed different responses showing a less accurate controller. Above 50 ms, our code breaks and will not record data. After two hours of trouble-shooting this problem, we are still unsure of why this large period causes an error in the data collection. However, with this, we can still conclude that the large periods causes undesirable effects in our system. 
If we had proper plots, we would have seen the oscillations grow as the motor would go past the setpoint much easier with improper input to control it. With a period large enough, the plot would have become an oscillation that never converged near the setpoint. 