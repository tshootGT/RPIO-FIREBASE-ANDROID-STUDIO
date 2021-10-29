import sys
from time import sleep
import signal
import RPi.GPIO as gpio
from gpiozero import LED, Button, PWMLED, LightSensor, MotionSensor
from signal import pause
from threading import Thread
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

gpio.setmode(gpio.BOARD)

gpio.setup(11, gpio.OUT)

MOTOR = gpio.PWM(11, 50)
MOTOR.start(12)

SALA = LED(4) #pin 7
 
COCINA = LED(18) #pin 12

CUARTO = LED(27) #pin 13

PUERTA = Button(24) #pin 18

ALARMA = LED(25) # PIN 22

SENSORLUZ = LightSensor(22) # PIN 15

FOCO = LED(23) #PIN 16

SENSORMOV = MotionSensor(20) #pin 11

BUZZER = LED(21) # PIN 40

BOMBA = LED(16) # PIN 36






PAHT_CRED = '/home/pi/Documents/FINAL/prueba.json'

URL_DB = 'https://prueba10iot-default-rtdb.firebaseio.com'

REF_HOME = 'home'

REF_LUCES = 'luces'

REF_ACTUADORES = 'actuadores'

REF_BOTONES = 'botones'

REF_LUZ_SALA = 'luz_sala'

REF_LUZ_COCINA = 'luz_cocina'

REF_LUZ_CUARTO = 'luz_cuarto'

REF_LUZ_CALLE = 'luz_calle'

REF_SENSOR_PUERTA = 'sensor_puerta'

REF_SENSOR_MOVIMIENTO = 'sensor_movimiento'

REF_MOTOR = 'motor'

REF_BOMBA = 'bomba'



class IOT():


    def _init_(self):

        cred = credentials.Certificate(PAHT_CRED)

        firebase_admin.initialize_app(cred, {

            'databaseURL': URL_DB

        })


        self.refHome = db.reference(REF_HOME)

       

        #self.estructuraInicialDB() # solo ejecutar la primera vez


        self.refLuces = self.refHome.child(REF_LUCES)
        self.refLuzSala = self.refLuces.child(REF_LUZ_SALA) 
        self.refLuzCocina = self.refLuces.child(REF_LUZ_COCINA)
        self.refLuzCuarto = self.refLuces.child(REF_LUZ_CUARTO)
        self.refLuzCalle = self.refLuces.child(REF_LUZ_CALLE)
        
        self.refActuadores = self.refHome.child(REF_ACTUADORES)
        self.refMotor = self.refActuadores.child(REF_MOTOR)
        self.refBomba = self.refActuadores.child(REF_BOMBA)

        self.refBotones = self.refHome.child(REF_BOTONES)
        self.refPulsadorA = self.refBotones.child(REF_SENSOR_PUERTA)
        self.refPulsadorB = self.refBotones.child(REF_SENSOR_MOVIMIENTO)


    def estructuraInicialDB(self):

        self.refHome.set({

            'luces': {

                'luz_sala':True,

                'luz_cocina':True,
                
                'luz_cuarto':True,
                
                'luz_calle':True,
                

            },

            'actuadores': {

                'motor':True,

                'bomba':True,

                

            },
            
            'puertas': {

                'sensor_puerta':True,
                'sensor_movimiento':True,

                'patio':True

            },            

            'botones':{

                'pulsador_a':True,
                'sensor_puerta':True,
                'sensor_movimiento':True,

                'pulsador_b':True

            }

        })

   

    def ledControlGPIO(self, estado):

        if estado:

            SALA.off()


            print('LUZ DE LA SALA ENCENDIDA')

        else:

            SALA.on()


            print('LUZ DE LA SALA APAGADA')


    def lucesStart(self):


        E, i = [], 0


        estado_anterior = self.refLuzSala.get()


        self.ledControlGPIO(estado_anterior)


        E.append(estado_anterior)


        while True:

          estado_actual = self.refLuzSala.get()


          E.append(estado_actual)


          if E[i] != E[-1]:

              self.ledControlGPIO(estado_actual)


          del E[0]

          i = i + i

          sleep(0.4)


    def led1ControlGPIO(self, estado):

        if estado:

            COCINA.off()


            print('LUZ DE LA COCINA ENCENDIDA')

        else:

            COCINA.on()


            print('LUZ DE LA COCINA APAGADA')

    def lucesStart1(self):


        E, i = [], 0


        estado_anterior = self.refLuzCocina.get()


        self.led1ControlGPIO(estado_anterior)


        E.append(estado_anterior)


        while True:

          estado_actual = self.refLuzCocina.get()


          E.append(estado_actual)


          if E[i] != E[-1]:

              self.led1ControlGPIO(estado_actual)


          del E[0]

          i = i + i

          sleep(0.4)

    def led2ControlGPIO(self, estado):

        if estado:

            CUARTO.off()


            print('LUZ DE LA HABITACION ENCENDIDA')

        else:

            CUARTO.on()


            print('LUZ DE LA HABITACION APAGADA')

    def lucesStart2(self):


        E, i = [], 0


        estado_anterior = self.refLuzCuarto.get()


        self.led2ControlGPIO(estado_anterior)


        E.append(estado_anterior)


        while True:

          estado_actual = self.refLuzCuarto.get()


          E.append(estado_actual)


          if E[i] != E[-1]:

              self.led2ControlGPIO(estado_actual)


          del E[0]

          i = i + i

          sleep(0.4)


    def led3ControlGPIO(self, estado):

        if estado:
            SENSORLUZ.when_dark = FOCO.off
            
       


            FOCO.off()
           


            print('LUZ DE LA CALLE ENCENDIDA')

        else:
            
            SENSORLUZ.when_light = FOCO.on
            
            FOCO.on()


            print('LUZ DE LA CALLE APAGADA')

    def lucesStart3(self):


        E, i = [], 0


        estado_anterior = self.refLuzCalle.get()


        self.led3ControlGPIO(estado_anterior)


        E.append(estado_anterior)


        while True:

          estado_actual = self.refLuzCalle.get()


          E.append(estado_actual)


          if E[i] != E[-1]:

              self.led3ControlGPIO(estado_actual)


          del E[0]

          i = i + i

          sleep(0.4)


    def motorControlGPIO(self, estado):

        if estado:
            
            MOTOR.ChangeDutyCycle(2.5)
            sleep(1)
            MOTOR.ChangeDutyCycle(0)
            
            print('MOTOR ON')

        else:
            
            MOTOR.ChangeDutyCycle(12)
            sleep(1)
            MOTOR.ChangeDutyCycle(0)
            
            print('MOTOR OFF')            
            
            
         

    def motorStart4(self):


        E, i = [], 0


        estado_anterior = self.refMotor.get()


        self.motorControlGPIO(estado_anterior)


        E.append(estado_anterior)


        while True:

          estado_actual = self.refMotor.get()


          E.append(estado_actual)


          if E[i] != E[-1]:

              self.motorControlGPIO(estado_actual)


          del E[0]

          i = i + i

          sleep(0.4)


    def bombaControlGPIO(self, estado):

        if estado:
            

            BOMBA.off()
            print('BOMBA DE RIEGO ENCENDIDA')

        else:
            
            
            BOMBA.on()
            print('BOMBA DE RIEGO APAGADA')

    def bombaStart5(self):


        E, i = [], 0


        estado_anterior = self.refBomba.get()


        self.bombaControlGPIO(estado_anterior)


        E.append(estado_anterior)


        while True:

          estado_actual = self.refBomba.get()


          E.append(estado_actual)


          if E[i] != E[-1]:

              self.bombaControlGPIO(estado_actual)


          del E[0]

          i = i + i

          sleep(0.4)
          
          
          


    def pulsador_on(self):

        print('LA PUERTA SE HA ABIERTO')

        self.refPulsadorA.set(True)
        
        ALARMA.off()
        


    def pulsador_off(self):

        print('LA PUERTA SE HA CERRADO')

        self.refPulsadorA.set(False)
        
        ALARMA.on()


    def botonesStart(self):

        print('Start btn !')

        PUERTA.when_pressed = self.pulsador_on

        PUERTA.when_released = self.pulsador_off
        
        
    def pulsadorb_on(self):

        print('SE HA DETECTADO MOVIMIENTO')

        self.refPulsadorB.set(True)
        
        BUZZER.on()    
    
    def pulsadorb_off(self):

        print('NO HAY MOVIMIENTO')

        self.refPulsadorB.set(False)
        
        BUZZER.off()

    def botonesbStart(self):

        print('Sensor Activo !')
        
        SENSORMOV.when_motion = self.pulsadorb_on
        SENSORMOV.when_no_motion = self.pulsadorb_off

  
  



print ('START !')

iot = IOT()


subproceso_led = Thread(target=iot.lucesStart)
subproceso_led.daemon = True
subproceso_led.start()

subproceso_led = Thread(target=iot.lucesStart1)
subproceso_led.daemon = True
subproceso_led.start()

subproceso_led = Thread(target=iot.lucesStart2)
subproceso_led.daemon = True
subproceso_led.start()

subproceso_led = Thread(target=iot.lucesStart3)
subproceso_led.daemon = True
subproceso_led.start()

subproceso_btn = Thread(target=iot.motorStart4)
subproceso_btn.daemon = True
subproceso_btn.start()

subproceso_btn = Thread(target=iot.bombaStart5)
subproceso_btn.daemon = True
subproceso_btn.start()

subproceso_btn = Thread(target=iot.botonesStart)
subproceso_btn.daemon = True
subproceso_btn.start()

subproceso_btn = Thread(target=iot.botonesbStart)
subproceso_btn.daemon = True
subproceso_btn.start()

signal.pause()