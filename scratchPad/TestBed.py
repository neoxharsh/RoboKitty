import arcade,tinyik,math
import numpy as np
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Radar Sweep Example"

femerAngle = 0
femerLength = 100
femerColor = arcade.color.RED
femerX = 400
femerY = 400
femerX1 = 0
femerY1 = 0

legAngle = 0
legLength = 80
legColor = arcade.color.GREEN
legX = 0
legY = 0
legY1 = 0
legX1 = 0

i = 0
arm = tinyik.Actuator(['z', [femerLength, 0., 0.], 'z', [legLength, 0., 0.]])

class MyGame(arcade.Window):
    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        pass

    def on_draw(self):
        global femerAngle,legAngle
        arcade.start_render()
        femerAngle = np.rad2deg(arm.angles)[0]
        _femerAngle = math.radians(femerAngle)
        femerX1 = math.cos(_femerAngle) * femerLength + femerX
        femerY1 = math.sin(_femerAngle) * femerLength + femerY

        legAngle = np.rad2deg(arm.angles)[1]
        # legAngle += 3
        _legAngle = math.radians(legAngle)
        legX1 = math.cos(_legAngle) * legLength + femerX1
        legY1 = math.sin(_legAngle) * legLength + femerY1
        arcade.draw_line(femerX,femerY,femerX1,femerY1,femerColor,10)
        arcade.draw_line(femerX1,femerY1,legX1,legY1,legColor,10)

    def on_mouse_motion(self, x, y, dx, dy):
        global i,arm
        print(arm.ee,np.interp(x,[400-180,400+180],[-180,180]),np.interp(y,[400-180,400+180],[-180,180]))
        # print(x-400,y)

        arm.ee = [np.interp(x,[400-180,400+180],[-180,180]),np.interp(y,[400-180,400+180],[-180,180]),0]
        # arm.angles = np.deg2rad([180,90,0])
        # print(np.rad2deg(arm.angles))
        # arm.ee = [171,-55,0]

    def on_update(self, delta_time):
        global i,arm

        # arm.ee = [100,61,0]
        # print(np.rad2deg(arm.angles))
        # arm.angles = np.deg2rad([20,0])
        # print(arm.ee)
        i += 1



if __name__ == "__main__":
    windows = MyGame()
    arcade.run()