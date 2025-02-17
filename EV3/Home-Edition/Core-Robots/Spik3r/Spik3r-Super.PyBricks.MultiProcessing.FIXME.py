#!/usr/bin/env pybricks-micropython


from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, InfraredSensor
from pybricks.hubs import EV3Brick
from pybricks.media.ev3dev import ImageFile, SoundFile
from pybricks.parameters import Button, Direction, Port, Stop

from multiprocessing import Process


class Spik3r(EV3Brick):
    def __init__(
            self,
            sting_motor_port: Port = Port.D, go_motor_port: Port = Port.B,
            claw_motor_port: Port = Port.A,
            touch_sensor_port: Port = Port.S1, color_sensor_port: Port = Port.S3,
            ir_sensor_port: Port = Port.S4, ir_beacon_channel: int = 1):
        self.sting_motor = Motor(port=sting_motor_port,
                                 positive_direction=Direction.CLOCKWISE)
        self.go_motor = Motor(port=go_motor_port,
                              positive_direction=Direction.CLOCKWISE)
        self.claw_motor = Motor(port=claw_motor_port,
                                positive_direction=Direction.CLOCKWISE)

        self.ir_sensor = InfraredSensor(port=ir_sensor_port)
        self.ir_beacon_channel = ir_beacon_channel

        self.touch_sensor = TouchSensor(port=touch_sensor_port)
        self.color_sensor = ColorSensor(port=color_sensor_port)


    def sting_by_ir_beacon(self):
        while True:
            ir_buttons_pressed = set(self.ir_sensor.buttons(channel=self.ir_beacon_channel))

            if ir_buttons_pressed == {Button.BEACON}:
                self.sting_motor.run_angle(
                    speed=-750,
                    rotation_angle=220,
                    then=Stop.HOLD,
                    wait=False)

                self.speaker.play_file(file=SoundFile.EV3)

                self.sting_motor.run_time(
                    speed=-1000,
                    time=1000,
                    then=Stop.HOLD,
                    wait=True)

                self.sting_motor.run_time(
                    speed=1000,
                    time=1000,
                    then=Stop.HOLD,
                    wait=True)

                while Button.BEACON in self.ir_sensor.buttons(channel=self.ir_beacon_channel):
                    pass


    def be_noisy_to_people(self):
        while True:
            if self.color_sensor.reflection() > 30:
                for i in range(4):
                    self.speaker.play_file(file=SoundFile.ERROR_ALARM)
                        

    def pinch_if_touched(self):
        while True:
            if self.touch_sensor.pressed():
                self.claw_motor.run_time(
                    speed=500,
                    time=1000,
                    then=Stop.HOLD,
                    wait=True)

                self.claw_motor.run_time(
                    speed=-500,
                    time=0.3 * 1000,
                    then=Stop.HOLD,
                    wait=True)


    def keep_driving_by_ir_beacon(self):
        while True: 
            ir_buttons_pressed = set(self.ir_sensor.buttons(channel=self.ir_beacon_channel))

            if ir_buttons_pressed == {Button.RIGHT_UP, Button.LEFT_UP}:
                self.go_motor.run(speed=910)

            elif ir_buttons_pressed == {Button.RIGHT_UP}:
                self.go_motor.run(speed=-1000)

            else:
                self.go_motor.stop()


    def main(self):
        self.screen.load_image(ImageFile.EVIL)
        
        # FIXME: OSError: [Errno 5] EIO: 
        # Unexpected hardware input/output error with a motor or sensor:
        # --> Try unplugging the sensor or motor and plug it back in again.
        # --> To see which sensor or motor is causing the problem,
        #     check the line in your script that matches
        #     the line number given in the 'Traceback' above.
        # --> Try rebooting the hub/brick if the problem persists.
        Process(target=self.be_noisy_to_people).start()    
        Process(target=self.sting_by_ir_beacon).start()    
        Process(target=self.pinch_if_touched).start()   
        self.keep_driving_by_ir_beacon()


if __name__ == '__main__':
    SPIK3R = Spik3r()

    SPIK3R.main()
