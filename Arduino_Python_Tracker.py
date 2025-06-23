import serial
import serial.tools.list_ports
import pyttsx3 as sp
import speech_recognition as sr
import Predict_Stress as p 

bot = sp.init()

bot.setProperty('rate', 175)
bot.setProperty('voice', bot.getProperty('voices')[1].id)

def speaking(text):
    bot.say(text)
    bot.runAndWait()

def arduino():
    ports = serial.tools.list_ports.comports()    
    using = None

    for port in ports:
        print(port)
        if "Arduino" in port.description or "SERIAL" in port.description:
            using = port.device
            print(using)

    if using:
        with serial.Serial(using, 115200) as serialinst:
            r = sr.Recognizer() 
            try:
                with sr.Microphone() as source:
                    r.energy_threshold = 10000  
                    r.adjust_for_ambient_noise(source, 1.2)
                    print("Listening...")

                    audio = r.listen(source)  
                    message = r.recognize_google(audio)  
                    print("You said:", message)

                    if "track" in message.lower():
                        serialinst.write("on\n".encode('utf-8'))  
                    else:
                        speaking("Keyword 'track' not detected.")
                
                while True:
                    response = serialinst.readline().decode('utf-8').strip()
                    print(response)
                    vals = response.split(",")
                    
                    nums = []
                    for i in vals:
                        nums.append(float(i))

                        # Extract sensor values
                    try:
                        sys_bp = 70
                        dia_bp = 120
                        heart_rate = nums[0]
                        spo2 = nums[1]

                        # Call the prediction function
                        prediction = p.predict_stress(sys_bp, dia_bp, heart_rate, spo2)
                        print("Predicted Stress Level:", prediction)
                        speaking(f"Stress Level: {prediction}")

                    except Exception as e:
                        print("Error in processing sensor data:", e)
                        speaking("Error processing sensor values.")

            except KeyboardInterrupt:
                print("\nTerminating script...")
                serialinst.write("TERMINATE\n".encode('utf-8'))
    else:
        print("Selected port not found.")
        speaking("No Sensor Found!")

#arduino()

# import serial
# import serial.tools.list_ports
# import pyttsx3 as sp
# import speech_recognition as sr

# bot = sp.init()

# property1 = bot.getProperty('rate')  # Rate of dictation
# bot.setProperty('rate', 175)  # Rate set to 175

# property2 = bot.getProperty('voices')  # Voice type
# bot.setProperty('voice', property2[1].id)  # Voice check

# def speaking(text):
#     bot.say(text)
#     bot.runAndWait()

# def arduino():
#     ports = serial.tools.list_ports.comports()    
#     using = None

#     # Find the selected port in the list of available ports
#     for port in ports:
#         print(port)
#         if "Arduino" in port.description or "SERIAL" in port.description:
#             using = port.device
#             print(using)

#     # If the selected port is found, configure and open the serial connection
#     if using:
#         with serial.Serial(using, 9600) as serialinst:
#             r = sr.Recognizer() 
#             try:
#                 with sr.Microphone() as source:
#                     # Background noise adjustments        
#                     r.energy_threshold = 10000  # Prevent very low voices
#                     r.adjust_for_ambient_noise(source, 1.2)
#                     print("Listening...")
                    
#                     # Listening
#                     audio = r.listen(source)  # Listen from user
#                     message = r.recognize_google(audio)  # Utilizing the Google API to get the text from the voice input
#                     print("You said:", message)
                    
#                     if "track" in message.lower():
#                         # Sending "on" message to Arduino to activate sensor tracking
#                         serialinst.write("on\n".encode('utf-8'))  # Send "on" message with a newline character
#                     else:
#                         speaking("Keyword 'track' not detected.")
                    
#                 # Receiving and printing sensor data from Arduino
                
#                 while True:
#                     response = serialinst.readline().decode('utf-8').strip()
#                     if response.startswith("BPM:"):
#                         print("Arduino:", response)
#                         speaking(response)
                    
#             except KeyboardInterrupt:  # Catch Ctrl+C termination
#                 print("\nTerminating script...")
#                 serialinst.write("TERMINATE\n".encode('utf-8'))  # Send termination signal
#     else:
#         print("Selected port not found.")
#         resp = "No Sensor Found!"
#         speaking(resp)

# #arduino()
