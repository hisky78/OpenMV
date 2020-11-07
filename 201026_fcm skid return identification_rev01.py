


import sensor, image, time,pyb,lcd

thresholds = [(12, 39, 27, 46, 13, 33),(40, 69, 17, 86, -16, 51)]

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.VGA)
sensor.set_windowing((100,350,200,130))
sensor.skip_frames(time = 200)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking

#led=pyb.LED(3)#RED LED=1, GREEN LED=2,BLUE LED=3,IR LEDS=4.
led_R = pyb.LED(1)
led_G = pyb.LED(2)
led_B = pyb.LED(3)

led_R.off()
led_G.off()


led_B.off()

#program rebuilding start

lcd.init()

from pyb import Pin

pin4 = Pin('P4', Pin.IN, Pin.PULL_DOWN)
pin5 = Pin('P5', Pin.OUT, Pin.PULL_DOWN)
pin6 = Pin('P6', Pin.OUT, Pin.PULL_DOWN)

Count_I = 0
Count_ok = 0
Count_ng =0

while(True):

   img=sensor.snapshot()
   lcd.display(img)
   value4=pin4.value()
   if value4==1:
    lcd.display(img)
    Count_I += 1
    if Count_I <= 10:
        img = sensor.snapshot()
        lcd.display(img)
        for blob in img.find_blobs(thresholds,pixels_threshold=20,area_threshold=20, merge=True,margin=100):  #roi=(0,0,90,180),
                if blob.area()>5000 and blob.area()<28000:
                   img.draw_rectangle(blob.rect(),color=(255,0,0))
                   img.draw_cross(blob.cx(),blob.cy())
                   img.draw_string(100,60,"OK",color=(0,0,255),scale=3,mono_space=False)
                   lcd.display(img)
                   area=blob.area()
                   print('OK')
                   print(area)
                   Count_ok += 1
                else:
                   img.draw_rectangle(blob.rect(),color=(255,0,0))
                   img.draw_cross(blob.cx(),blob.cy())
                   img.draw_string(100,60,"NO",color=(0,0,255),scale=3,mono_space=False)
                   lcd.display(img)
                   area=blob.area()
                   print('NO')
                   print(area)
                   Count_ng += 1
    else:
        if Count_ok > Count_ng:
            led_G.on()
            print('totaL OK')
            pin5.value(1)
            img.draw_string(100,60,"TOTAL OK",color=(0,0,255),scale=3,mono_space=False)
        else:
            led_R.on()
            print('total NG')
            pin6.value(1)
            img.draw_string(100,60,"TOTAL NG",color=(0,0,255),scale=3,mono_space=False)

   else:
    img.draw_string(40,10,"NO",color=(0,0,255),scale=4,mono_space=False)
    img.draw_string(40,40,"SKID",color=(0,0,255),scale=4,mono_space=False)
    lcd.display(img)
    print('no skid')
    Count_I = 0
    Count_ok = 0
    Count_ng = 0
    pin5.value(0)
    pin6.value(0)
    led_R.off()
    led_G.off()
    led_B.off()
