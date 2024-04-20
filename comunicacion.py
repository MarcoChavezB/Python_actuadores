import serial
import platform
class comunicacion:
          
    def __init__(self):
        self.port = self.find_port()
        self.ser = serial.Serial(self.port, 9600)
        
    def find_port(self):
      os = platform.system()
      initPort = "/dev/ttyUSB"
      
      if(os == "Windows"):
         initPort = "COM"
      
      for number in range(5):
         try:
            with serial.Serial(initPort + str(number), 9600) as ser:
               return initPort + str(number)
         except:
            pass
         
    def read_serial(self, port="", baud=9600):
        port = self.find_port()
        with serial.Serial(port, baud) as ser:
            try:
                while True:
                    data = ser.readline().decode().strip()
                    yield self.format_data_serial(data)
            except KeyboardInterrupt:
                pass
            
