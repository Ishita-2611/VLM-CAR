# Vision-Language Model Robotic Car Control System

This project implements a vision-based control system for a robotic car using the CLIP vision-language model. The system analyzes the environment through a camera and generates appropriate control commands for the car.

## Features

- Real-time visual scene analysis using CLIP model
- Automatic obstacle detection and avoidance
- Traffic signal and stop sign recognition
- Path analysis and navigation
- Safety-first command generation
- Real-time feedback display

## Hardware Requirements

### Computer/Laptop
- CPU: Intel i5/AMD Ryzen 5 or better
- RAM: 8GB minimum (16GB recommended)
- GPU: NVIDIA GPU with 4GB VRAM minimum (for better performance)
- Storage: 20GB free space
- USB ports: At least 2 USB ports

### Camera System
- HD webcam (720p minimum, 1080p recommended)
- USB interface
- Wide-angle lens (90°+ field of view)

### Robotic Car Components

1. **Chassis**
   - Base frame
   - 4 wheels
   - Mounting brackets

2. **Motors**
   - 4 DC motors (12V)
   - Motor drivers (L298N or similar)
   - Encoders for feedback

3. **Control Electronics**
   - Arduino board (Arduino Mega recommended)
   - Motor driver board
   - Power supply (12V battery)
   - USB-to-Serial converter

4. **Additional Sensors** (Optional but recommended)
   - Ultrasonic sensors
   - Infrared sensors
   - IMU sensor

## Hardware Setup

### 1. Car Assembly
1. Mount the motors to the chassis
2. Connect the wheels to the motors
3. Mount the Arduino board
4. Connect motor drivers to Arduino
5. Mount the camera on the front
6. Add optional sensors

### 2. Arduino Wiring
```
Arduino Mega Pin Connections:
- Motor 1: Pins 2, 3
- Motor 2: Pins 4, 5
- Motor 3: Pins 6, 7
- Motor 4: Pins 8, 9
- Camera: USB to Computer
- Optional Sensors: Analog pins
```

### 3. Arduino Code
Upload the following code to your Arduino board:

```cpp
// motor_control.ino
#include <Servo.h>

// Motor pins
const int MOTOR_LEFT_FRONT = 2;
const int MOTOR_LEFT_BACK = 3;
const int MOTOR_RIGHT_FRONT = 4;
const int MOTOR_RIGHT_BACK = 5;

void setup() {
  // Initialize motor pins
  pinMode(MOTOR_LEFT_FRONT, OUTPUT);
  pinMode(MOTOR_LEFT_BACK, OUTPUT);
  pinMode(MOTOR_RIGHT_FRONT, OUTPUT);
  pinMode(MOTOR_RIGHT_BACK, OUTPUT);
  
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    executeCommand(command);
  }
}

void executeCommand(String cmd) {
  // Parse command format: "speed,steering,brake"
  // Example: "0.5,-0.3,0.0"
  int firstComma = cmd.indexOf(',');
  int secondComma = cmd.indexOf(',', firstComma + 1);
  
  float speed = cmd.substring(0, firstComma).toFloat();
  float steering = cmd.substring(firstComma + 1, secondComma).toFloat();
  float brake = cmd.substring(secondComma + 1).toFloat();
  
  // Convert to motor commands
  if (brake > 0.5) {
    stopMotors();
    return;
  }
  
  // Calculate left and right motor speeds
  float leftSpeed = speed * (1.0 - steering);
  float rightSpeed = speed * (1.0 + steering);
  
  // Apply motor commands
  setMotorSpeed(MOTOR_LEFT_FRONT, MOTOR_LEFT_BACK, leftSpeed);
  setMotorSpeed(MOTOR_RIGHT_FRONT, MOTOR_RIGHT_BACK, rightSpeed);
}

void setMotorSpeed(int pin1, int pin2, float speed) {
  if (speed > 0) {
    analogWrite(pin1, speed * 255);
    analogWrite(pin2, 0);
  } else {
    analogWrite(pin1, 0);
    analogWrite(pin2, -speed * 255);
  }
}

void stopMotors() {
  analogWrite(MOTOR_LEFT_FRONT, 0);
  analogWrite(MOTOR_LEFT_BACK, 0);
  analogWrite(MOTOR_RIGHT_FRONT, 0);
  analogWrite(MOTOR_RIGHT_BACK, 0);
}
```

## Software Setup

### 1. Install Dependencies
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Project Structure
```
VLM-CAR/
├── laptop/
│   ├── main.py                    # Main entry point
│   ├── vision_control_system.py   # Core control system
│   └── requirements.txt           # Dependencies
└── arduino/
    └── motor_control.ino         # Arduino control code
```

## Running the System

1. **Connect Hardware**
   - Connect Arduino to computer via USB
   - Connect camera to computer
   - Ensure all motors are properly connected

2. **Upload Arduino Code**
   - Open Arduino IDE
   - Select correct board and port
   - Upload motor_control.ino

3. **Run the System**
```bash
# Navigate to project directory
cd VLM-CAR/laptop

# Run the system
python main.py

# For debug mode
python main.py --debug
```

## System Operation

The system operates in a continuous loop:

1. **Visual Processing**
   - Captures frame from camera
   - Analyzes scene using CLIP model
   - Detects obstacles and hazards

2. **Command Generation**
   - Determines appropriate command
   - Validates safety conditions
   - Generates motor commands

3. **Command Execution**
   - Sends commands to Arduino
   - Controls motors
   - Updates system state

4. **Feedback Loop**
   - Displays camera feed
   - Shows command information
   - Updates status

## Safety Features

1. **Automatic Safety Checks**
   - Obstacle detection
   - Speed limiting
   - Emergency stop capability
   - Path validation

2. **Manual Override**
   - Emergency stop button
   - Manual control option
   - System status monitoring

## Troubleshooting

### Common Issues

1. **Camera Not Detected**
   - Check USB connection
   - Verify camera permissions
   - Try different USB port

2. **Motor Control Issues**
   - Check Arduino connections
   - Verify power supply
   - Test motor drivers

3. **Performance Issues**
   - Reduce frame rate
   - Lower resolution
   - Use GPU acceleration

## Maintenance

Regular Maintenance Tasks:
1. Check battery level
2. Clean camera lens
3. Verify motor connections
4. Update software
5. Test safety features

## Future Improvements

Potential Enhancements:
1. Add more sensors
2. Implement SLAM
3. Add GPS navigation
4. Improve obstacle detection
5. Add wireless control

## Cost Estimation

Approximate Costs:
- Computer/Laptop: $500-1000
- Camera: $30-100
- Arduino + Components: $50-100
- Motors + Drivers: $40-80
- Chassis + Wheels: $30-50
- Optional Sensors: $20-50 each

Total Estimated Cost: $670-1430

## License

This project is licensed under the MIT License - see the LICENSE file for details.
