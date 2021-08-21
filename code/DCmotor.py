import RPi.GPIO as GPIO
from time import sleep

STOP = 0
FORWARD = 1
BACKWORD = 2

CH1 = 0

# PIN 입출력 설정
OUTPUT = 1
INPUT = 0

# PIN 설정
HIGH = 1
LOW = 0

ENA = 16
IN1 = 21
IN2 = 20

def setPinConfig(EN,INA,INB):
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(INA, GPIO.OUT)
    GPIO.setup(INB, GPIO.OUT)
    pwm = GPIO.PWM(EN,100)
    
    pwm.start(0)
    return pwm

def setMotorContorl(pwm, INA,INB, speed, stat):
    pwm.ChangeDutyCycle(speed)
    if stat == FORWARD:
        GPIO.output(INA,HIGH)
        GPIO.output(INB,LOW)
    elif stat == BACKWORD:
        GPIO.output(INA,LOW)
        GPIO.output(INB,HIGH)
    elif stat == STOP:
        GPIO.output(INA,LOW)
        GPIO.output(INB,LOW)
        
# 모터 제어함수 간단하게 사용하기 위해 한번더 래핑(감쌈)
def setMotor(ch, speed, stat):
    if ch == CH1:
        #pwmA는 핀 설정 후 pwm 핸들을 리턴 받은 값이다.
        setMotorContorl(pwmA, IN1, IN2, speed, stat)

# GPIO 모드 설정 
GPIO.setmode(GPIO.BCM)
    
#모터 핀 설정
#핀 설정후 PWM 핸들 얻어옴
pwmA = setPinConfig(ENA, IN1, IN2)

#제어 시작
# 앞으로 80프로 속도로
count = 0
while count<5:
    setMotor(CH1, 30, FORWARD)
    #5초 대기
    sleep(3)
    setMotor(CH1, 30, STOP)
    #5초 대기
    sleep(1)
    setMotor(CH1, 30, BACKWORD)
    #5초 대기
    sleep(3)
    count+=1


GPIO.cleanup()