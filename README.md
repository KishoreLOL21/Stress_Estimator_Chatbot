# 🤖 ARCA – Smart Healthcare Chatbot using Few-Shot Learning

ARCA (AI for Real-time Care & Assistance) is a personalized smart healthcare assistant that converses with users in natural speech and actively monitors their health when commanded. It uses a few-shot learning technique to predict user stress levels based on sensor data.

---

## 🧠 Features

- **Conversational AI**: Voice-based chatbot interaction using speech recognition and text-to-speech.
- **Health Tracking Mode**: Real-time monitoring of heart rate and SpO2 via Arduino sensors.
- **Stress Detection**: Uses a Prototypical Network (Few-Shot Learning) model to classify stress levels.
- **Friendly Personalization**: Learns your name and interacts naturally like a companion.
- **Offline Voice Processing**: Uses local speech synthesis (pyttsx3) and recognition (SpeechRecognition + Google API).
- **Arduino Integration**: Real-time serial communication for sensor data capture.

---

## 📁 Project Structure

```
├── main.py # Entry script for conversational interaction
├── Arduino_Python_Tracker.py# Handles serial data from Arduino and stress prediction
├── Predict_Stress.py # Few-shot learning model using Prototypical Networks
├── BPM_Data_Final.csv # Sample sensor data (heart rate, SpO2, etc.)
├── scaler.pkl # Scaler used for normalizing input data
├── X_train.npy # Training feature data for the prototype network
├── y_train.npy # Corresponding labels for training data
├── best_protonet_model.pth # Pretrained model weights
```


---

## 🧪 Technique Used – Few-Shot Learning

The core of the prediction system uses a **Prototypical Network (ProtoNet)**, a type of few-shot learning model. It encodes physiological data into embeddings and compares against class prototypes using Euclidean distance to classify the stress level:

- Inputs: `[Systolic BP, Diastolic BP, Heart Rate, SpO2]`
- Outputs: `"Normal"` or `"Stress High"`

Few-shot learning allows accurate prediction with limited labeled data — a crucial benefit for personalized healthcare applications.

---

## 🛠️ Requirements

Install the following Python packages:

```bash
pip install pyttsx3 speechrecognition torch joblib numpy serial

```

🚀 How It Works
Conversation Starts: ARCA introduces itself and greets the user.

Command Activation: On saying “Activate Command Mode”, user can:

🩺 Check current body conditions

📊 Track & analyze historical trends

Voice Trigger: Saying “Track” starts sensor monitoring.

Sensor Reading: Heart rate and SpO₂ data are collected from the Arduino.

Prediction: ARCA uses a trained ProtoNet model to predict stress level.

Response: The chatbot speaks out the result: "Stress Level: Normal" or "Stress Level: Stress High".

🧠 Sample Use Case
👤: Hello ARCA
🤖: Hello sir, I’m ARCA... How are you?
👤: I’m fine. What about you?
🤖: I’m good. Please tell your name.
👤: Kishore
🤖: Hello Kishore. How can I help you today?
👤: Activate command mode
🤖: Activating... say command mode one or two.
👤: mode one
🤖: Please say Track.
👤: Track
🤖: Stress Level: Normal ✅

📌 Future Enhancements
🧬 Expand dataset for more diverse stress indicators

🌐 Cloud integration for health data logging

📲 Mobile app companion for continuous tracking

🗣️ Emotion-aware conversation dynamics
