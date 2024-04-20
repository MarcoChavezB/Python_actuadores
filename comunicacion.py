import serial
import platform

class comunicacion:

    def __init__(self):
        self.port = self.find_port()
        self.ser = serial.Serial(self.port, 9600)
        
    dataRecived = []
        
    def find_port(self):
      os = platform.system()
      initPort = "/dev/ttyUSB"
      
      if(os == "Windows"):
         initPort = "COM"
      
      for number in range(5):
         try:
            with serial.Serial(initPort + str(number), 19200) as ser:
               return initPort + str(number)
         except:
            pass
         
    def read_serial(self, port="", baud=19200):
        port = self.find_port()
        with serial.Serial(port, baud) as ser:
            try:
                while True:
                    self.dataRecived = ser.readline().decode().strip()
                    if(self.dataRecived[0] == 'A' or self.dataRecived[0] == 'D' or self.dataRecived[0] == 'L'):
                        yield self.format_data_serial(self.dataRecived)
            except KeyboardInterrupt:
                pass

    def print_serial_data(self):
        for data in self.read_serial():
            print(data)
            
    def get_alarm_value(self):
        for data in self.read_serial():
            if(self.dataRecived[0] == 'A'):
                return data[3]
            
    def get_luz_value(self):
        for data in self.read_serial():
            if(self.dataRecived[0] == 'L'):
                return data[3]
            
    def get_distance_value(self):
        for data in self.read_serial():
            if(self.dataRecived[0] == 'D'):
                return  float(data[3])
            

        
    def format_data_serial(self, data):
       return data.split("|")
            
