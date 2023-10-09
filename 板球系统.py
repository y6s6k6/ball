#报错记得更换固件
#报错记得更换固件
#报错记得更换固件
import sensor, lcd, time
import sensor, time
from machine import UART,Timer
from fpioa_manager import fm
from Maix import GPIO
from fpioa_manager import fm
fm.register(12, fm.fpioa.GPIO0)
LED_B = GPIO(GPIO.GPIO0, GPIO.OUT) #构建LED对象
LED_B.value(0) #点亮LED
#摄像头初始化
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224,224))
sensor.set_vflip(1) #后置模式，所见即所得
sensor.run(1)
sensor.skip_frames(30)
from machine import UART,Timer
from fpioa_manager import fm

#映射串口引脚
fm.register(6 , fm.fpioa.UART1_RX, force=True)
fm.register(7 , fm.fpioa.UART1_TX, force=True)
fm.register(9 , fm.fpioa.UART2_RX, force=True)
fm.register(10, fm.fpioa.UART2_TX, force=True)

#初始化串口
uart1 = UART(UART.UART1, 115200, read_buf_len=4096)
uart2 = UART(UART.UART2, 115200, read_buf_len=4096)
#lcd初始化
lcd.init()

clock=time.clock()


color_threshold = (((57, 80, -3, 35, 9, 47)))
size_threshold = 2000
max_Size = 10
def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
    return max_blob

LED_B.value(0) #点亮LED
while(1):
    clock.tick()
    img= sensor.snapshot()
    blobs = img.find_blobs([color_threshold],area_threshold=50,pixels_threshold=50)
    if blobs:
      #for b in blobs:
          b = find_max(blobs)
          img.draw_rectangle(b[0:4])  # circle
          img.draw_cross(b[5], b[6], color=(0, 0, 255))
          x_pos = b[5]#中心位置x坐标
          y_pos = b[6]#中心位置y坐标
          Size = b.area()
          X = '%03d' % x_pos
          Y = '%03d' % y_pos
          DATA1 = 'F' + X +'E'
          DATA2 = 'F' + Y +'E'
          img.draw_string(2,2, ("X:%03d" %(b[5])), color=(255,255,255), scale=2)
          img.draw_string(2,25, ("Y:%03d" %(b[6])), color=(255,255,255), scale=2)
          img.draw_string(2,50, ("S:%04d" %(b.area())), color=(255,255,255), scale=2)
          uart1.write(DATA1)
          uart2.write(DATA2)
          print(DATA1)
          print(DATA2)
    else:
          uart1.write('000')
          uart2.write('000')
          img.draw_string(2,2, ("X:%03d" %(000)), color=(255,255,255), scale=2)
          img.draw_string(2,25, ("Y:%03d" %(000)), color=(255,255,255), scale=2)
          img.draw_string(2,50, ("S:%04d" %(000)), color=(255,255,255), scale=2)
    lcd.display(img)     #LCD显示图片
