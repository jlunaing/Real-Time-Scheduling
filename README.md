# Real-Time Scheduling
 
 In this project, we integrated the code developed in the previous week, a closed-loop motor position control system, into a real-time scheduler and tested its performance. 
 
 First, the controller algorithm was executed at a 10-ms period, with a proportional gain value of 0.03. Then, we gradually increased the period to watch for changes in the step response plot. The step response plots for the various gain values are shown below.
 
 <p align="center">
    <img src="https://github.com/jdlu97/Real-Time-Scheduling/blob/main/img/figure_1.png?raw=true" alt="Step response with Kp = 0.3, period = 10 ms"/>
 </p>
 
 <p align="center">Motor step response with a proportional gain value of **Kp = 0.3** and with its motor control task running at a period of **10 ms**.</p><br/>
 
 <p align="center">
    <img src="https://github.com/jdlu97/Real-Time-Scheduling/blob/main/img/figure_2.png?raw=true" alt="Step response with Kp = 0.3, period = 20 ms"/>
 </p>
 
 <p align="center">Motor step response with a proportional gain value of **Kp = 0.3** and with its motor control task running at a period of **20 ms**.</p><br/>

 <p align="center">
    <img src="https://github.com/jdlu97/Real-Time-Scheduling/blob/main/img/figure_3.png?raw=true" alt="Step response with Kp = 0.3, period = 40 ms"/>
 </p>
 
 <p align="center">Motor step response with a proportional gain value of **Kp = 0.3** and with its motor control task running at a period of **40 ms**.</p><br/>

 <p align="center">
    <img src="https://github.com/jdlu97/Real-Time-Scheduling/blob/main/img/figure_4.png?raw=true" alt="Step response with Kp = 0.3, period = 60 ms"/>
 </p>
 
 <p align="center">Motor step response with a proportional gain value of **Kp = 0.3** and with its motor control task running at a period of **60 ms**.</p><br/>
 
 The plots indicate that, at around a 80-ms period, the response is still relatively the same. Ideally, we would have shown further plots at higher periods that displayed different responses showing a less accurate controller. Above 50 ms, our code breaks and will not record data. After two hours of trouble-shooting this problem, we are still unsure of why this large period causes an error in the data collection. However, with this, we can still conclude that the large periods causes undesirable effects in our system. 

 With more accurate plots, we would see oscillations grow as the motor would go past the setpoint much easier with improper input to control it. With a period large enough, the plot would become an oscillation that never converges near the setpoint. 