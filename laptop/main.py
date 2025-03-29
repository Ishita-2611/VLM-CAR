from vision_control_system import VisionControlSystem
import argparse

def main():
    parser = argparse.ArgumentParser(description='Vision-Language Model Robotic Car Control System')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    
    try:
        # Initialize and run the control system
        control_system = VisionControlSystem()
        print("Starting Vision Control System...")
        print("Press Ctrl+C to stop")
        control_system.run_control_loop()
        
    except Exception as e:
        print(f"Error: {str(e)}")
        if args.debug:
            import traceback
            traceback.print_exc()
    finally:
        print("System shutdown complete")

if __name__ == "__main__":
    main() 