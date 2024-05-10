import serial

uart = []

def work(): 
    global uart
    global uart_split
    try: 
        recvpacket = sr.readline().decode()
        uart_split = recvpacket.split(",")
        if uart_split[0] == '$GPRMC':
            print (uart_split[3], "N", uart_split[5], "E")
    except:
        print ("NOT CONNECTED")

try:
    sr = serial.Serial("COM3", 115200)
except:
    print("Port Not Found")
    exit()
              
while True:
    uart = ""
    uart_split = []
    work()

