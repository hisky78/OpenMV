
#红:P5 白：GND 绿：3.3V 蓝：P1 YC  黑 P4 NU
import sensor, image, time,pyb,lcd

thresholds = [(61, 90, -31, 12, -49, -26),(34, 71, -22, 31, -67, -29)] # RED, BLUE

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.VGA)
sensor.set_windowing((((((640-180)//2)-20)), (480-180)//2, 180, 180))
#sensor.set_windowing((120,100,300, 300))
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(True) # must be turned off for color tracking
sensor.set_auto_whitebal(True) # must be turned off for color tracking
clock=time.clock()
#led=pyb.LED(3)#RED LED=1, GREEN LED=2,BLUE LED=3,IR LEDS=4.

led_R = pyb.LED(1)
led_G = pyb.LED(2)
led_B = pyb.LED(3)

led_R.off()
led_G.off()
led_B.off()

lcd.init()

from pyb import Pin

pin1 = Pin('P1', Pin.IN, Pin.PULL_DOWN)
pin4 = Pin('P4', Pin.IN, Pin.PULL_DOWN)
pin5 = Pin('P5', Pin.OUT, Pin.PULL_NONE)
pin9 = Pin('P9', Pin.OUT, Pin.PULL_NONE)



#NEW
Count_I = 0
Count_ok = 0
Count_ng =0

while(True):
   img=sensor.snapshot()
   lcd.display(img)
   value1=pin1.value()
   value4=pin4.value()


   if value1==1: #YC connector
    lcd.display(img)
    Count_I += 1
    if Count_I <= 10:
        img = sensor.snapshot()
        lcd.display(img)
        for blob in img.find_blobs([thresholds[0]],roi=(100,90,80,90), pixels_threshold=20,area_threshold=20, merge=True,margin=100): #invert=False,
                if blob.area()>300 and blob.area()<3000:
                   img.draw_rectangle(blob.rect(),color=(255,0,0))
                   img.draw_cross(blob.cx(),blob.cy())
                   img.draw_string(100,60,"OK",color=(0,0,255),scale=3,mono_space=False)
                   lcd.display(img)
                   area=blob.area()
                   print('YC OK')
                   print(area)
                   Count_ok += 1
                else:
                   img.draw_rectangle(blob.rect(),color=(255,0,0))
                   img.draw_cross(blob.cx(),blob.cy())
                   img.draw_string(100,60,"NG",color=(0,0,255),scale=3,mono_space=False)
                   lcd.display(img)
                   area=blob.area()
                   print('YC NG')
                   print(area)
                   Count_ng += 1
    else:
        if Count_ok > Count_ng:
            led_G.on()
            print('total OK')
            pin5.value(1)
            img.draw_string(100,60,"TOTAL OK",color=(0,0,255),scale=3,mono_space=False)
            Count_I = 0
            Count_ok = 0
            Count_ng = 0

        else:
            led_R.on()
            print('total ng')
            pin9.value(1)
            img.draw_string(100,60,"TOTAL NG",color=(0,0,255),scale=3,mono_space=False)
            Count_I = 0
            Count_ok = 0
            Count_ng = 0


   elif value4==1: #NU
    lcd.display(img)
    Count_I += 1
    if Count_I <= 10:
        img = sensor.snapshot()
        lcd.display(img)
        for blob in img.find_blobs([thresholds[1]],pixels_threshold=15,area_threshold=15, merge=True,margin=100):  #roi=(0,30,300,210),
             if blob.area()>1000 and blob.area()<12000:
                img.draw_rectangle(blob.rect(),color=(255,0,0))
                img.draw_cross(blob.cx(),blob.cy())
                img.draw_string(100,60,"OK",color=(0,0,255),scale=3,mono_space=False)
                lcd.display(img)
                area=blob.area()
                print('OK')
                print(area)
                Count_ok += 1
             else:
                img.draw_string(100,60,"NG",color=(0,0,255),scale=3,mono_space=False)
                img.draw_rectangle(blob.rect(),color=(255,0,0))
                lcd.display(img)
                area=blob.area()
                print('NG')
                print(area)
                Count_ng += 1
    else:
        if Count_ok > Count_ng:
            led_G.on()
            print('total OK')
            pin5.value(1)
            img.draw_string(100,60,"TOTAL OK",color=(0,0,255),scale=3,mono_space=False)
            Count_I = 0
            Count_ok = 0
            Count_ng = 0
        else:
            led_R.on()
            print('total ng')
            pin9.value(1)
            img.draw_string(100,60,"TOTAL NG",color=(0,0,255),scale=3,mono_space=False)
            Count_I = 0
            Count_ok = 0
            Count_ng = 0


   else:
    img.draw_string(40,10," NO",color=(0,0,255),scale=4,mono_space=False)
    img.draw_string(40,50," ANY",color=(0,0,255),scale=4,mono_space=False)
    img.draw_string(40,90," SKID",color=(0,0,255),scale=4,mono_space=False)
    lcd.display(img)
    print('no skid')
    pin5.value(0)
    pin9.value(0)
    Count_I = 0
    Count_ok = 0
    Count_ng = 0
    led_R.off()
    led_G.off()
    led_B.off()

