import sys
import time
from pathlib import Path

# 1. Handle the Python Path (The 'npm' search path equivalent)
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

# 2. Use your existing abstractions
from src.io import send_keys, Key

def input_loop():
    print("Logic: UP -> 2s Wait -> DOWN -> 2s Wait (Looping)")
    print("This uses your modular src/io system.")
    print("Press Ctrl+C in this terminal to stop.")

    # We pass a list of tuples: (Key, delay_after_press)
    # Your send_keys implementation handles the HWND lookup and timing
    test_sequence = [
        (Key.UP, 2.0),
        (Key.DOWN, 2.0)
    ]

    try:
        while True:
            print(f"Executing sequence: {test_sequence}")
            success = send_keys(test_sequence)
            
            if not success:
                print("Failed to send keys. Is the game running?")
                break
                
    except KeyboardInterrupt:
        print("\nInput test terminated.")

if __name__ == "__main__":
    input_loop()