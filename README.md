# 🚗 Vision-Language Model Autonomous Car Control

## 🛠️ End-to-End Workflow

### 1. Sensors on Car → Perception
- **Camera** captures the road environment.
- (Optional) **LiDAR** and **IMU** provide depth and motion data.

### 2. Raspberry Pi 5 → Data Aggregation and Communication
- Collects and preprocesses sensor data.
- Sends data to Laptop over Wi-Fi/Ethernet.

### 3. Laptop (Running Vision-Language Model) → Scene Understanding
- VLM processes visual input.
- Generates driving commands (`forward`, `left`, `right`, `stop`).

### 4. Raspberry Pi 5 → Command Execution
- Receives commands from Laptop.
- Controls motor driver (L298N / H-Bridge) to actuate the car.

### 5. Feedback Loop
- Sensors continuously update the system.
- IMU and Camera ensure accurate control and corrections.

---

## ⚙️ Technologies Used
| Component           | Tech                                 |
|---------------------|--------------------------------------|
| Sensors             | Camera, LiDAR (optional), IMU        |
| Edge Processor      | Raspberry Pi 5                       |
| VLM Processor       | Laptop (BLIP-2 / LLaVA / GPT-4V)     |
| Actuation           | Motor driver (L298N / H-Bridge)      |
| Communication       | Wi-Fi, Ethernet, ROS (optional)      |
