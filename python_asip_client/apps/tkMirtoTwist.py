
# tkInter test harness for low level mirto ROS code

import math
from mirto_twist import MirtoTwist

if __name__ == '__main__':
    mirto=MirtoTwist()

    import tkinter as tk
    SENSOR_UPDATE_INTERVAL = 25
    
    root=tk.Tk()
    root.title(string='Mirto test')
    root.geometry("300x175")
    
    frame1=tk.Frame(root)
    frame1.pack(side=tk.TOP,fill=tk.X)

    frame2=tk.Frame(root)
    frame2.pack(expand=1, side=tk.TOP, fill=tk.X)

    linear_var=tk.StringVar()
    angular_var=tk.StringVar()
    duration_var=tk.StringVar()
    encoders_var=tk.StringVar()
    ir_sensors_var=tk.StringVar()
    bump_sensors_var=tk.StringVar()
     
    def twist():    
        linear=float(linear_var.get())
        angular=float(angular_var.get())
        duration=float(duration_var.get())
        mirto.twist(linear, math.radians(angular), duration)

    def stop():
        mirto.twist(0, 0, 0)  
    
    def update_sensors():
        encoders = mirto.get_encoder_counts()
        s = [str(value) for value in encoders]
        encoders_var.set(','.join(s)) 
        ir = mirto.get_ir_sensors()
        s = [str(value) for value in ir]
        ir_sensors_var.set(','.join(s))
        b = mirto.get_bump_sensors()
        bump_sensors_var.set("L bump {},  R bump {}".format(str(b[0]), str(b[1])))
        root.after(SENSOR_UPDATE_INTERVAL, update_sensors)

        
    linear_label=tk.Label(frame1, text='Linear velocity m/s')      
    linear_entry=tk.Entry(frame1,textvariable=linear_var, )      

    angular_label=tk.Label(frame1, text='Angular velocity D/s')      
    angular_entry=tk.Entry(frame1, textvariable=angular_var)
    
    duration_label=tk.Label(frame1, text='Duration seconds')      
    duration_entry=tk.Entry(frame1, textvariable=duration_var)
      
    stop_btn=tk.Button(frame1,text='Stop', command=stop)
    twist_btn=tk.Button(frame1,text='Twist', command=twist)

    encoders_label=tk.Label(frame2, textvariable=encoders_var)
    ir_sensors_label=tk.Label(frame2, textvariable=ir_sensors_var)
    bump_sensors_label=tk.Label(frame2, textvariable=bump_sensors_var)

    linear_label.grid(row=0,column=0)
    linear_entry.grid(row=0,column=1)
    angular_label.grid(row=1,column=0)
    angular_entry.grid(row=1,column=1)
    duration_label.grid(row=2,column=0)
    duration_entry.grid(row=2,column=1)
    stop_btn.grid(row=3,column=0) 
    twist_btn.grid(row=3,column=1)
    encoders_label.pack()
    ir_sensors_label.pack()
    bump_sensors_label.pack()
    root.after(SENSOR_UPDATE_INTERVAL, update_sensors)
    root.mainloop()
    mirto.abort()