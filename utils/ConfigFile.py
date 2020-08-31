
class Config:

    def __init__(self):
        self.port ="/dev/tty.usbserial-FT45BKV3"
        self.baudIndex = 0
        self.baudRates = [
            ["1000000", "1M", 1],
            ["115200", "115200", 16],
            ["57600", '57600', 34],
            ["9600", "9600", 207]
        ]

        self.FrontRightShoulderID = None
        self.FrontRightLegID = None
        self.FrontRightFemerID = None

        self.FrontLeftShoulderID = None
        self.FrontLeftFemerID = None
        self.FrontLeftLegID = None

        self.RearRightShoulderID = None
        self.RearRightFemerID = None
        self.RearRightLegID = None

        self.RearLeftShoulderID = None
        self.RearLeftFemerID = None
        self.RearLeftLegID = None

