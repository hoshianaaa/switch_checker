import RPi.GPIO as GPIO
import time

screw_pin = 14
arm_pin = 26

screw_count = 0
arm_count = 0
interval_count = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(screw_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(arm_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

f_data = open('data/data.txt', 'w')
f_zero = open('data/zero.txt', 'w')
f_many = open('data/many.txt', 'w')


def callBackArm(channel):
    global arm_count
    global interval_count
    global f_zero
    global f_many

    arm_count += 1

    if interval_count is 0 and arm_count is not 1:
        print("no")
        f_zero.write(str(arm_count) + '\n')
    if interval_count is 1:
        print("ok")
    if interval_count > 1:
        print("many")
        f_many.write(str(arm_count) + '\n')
 
    interval_count = 0
    print("arm_count", arm_count)
    
    
    
    
def callBackScrew(channel):
    global screw_count
    global interval_count

    screw_count += 1
    interval_count += 1
    print("screw_count", screw_count)
    print("interval_count", interval_count)


GPIO.add_event_detect(arm_pin, GPIO.RISING, callback=callBackArm, bouncetime=300)
GPIO.add_event_detect(screw_pin, GPIO.RISING, callback=callBackScrew, bouncetime=300)

while True:
    time.sleep(1)
    timer = time.time()
    while(GPIO.input(arm_pin)):
        print(time.time() - timer)
        if ((time.time() - timer) > 3):
            f_zero.close()
            f_many.close()
            f_data.write('arm_count:'+str(arm_count)+'\n')
            f_data.write('screw_count:'+str(screw_count)+'\n')
            f_data.close()
            exit()





        
