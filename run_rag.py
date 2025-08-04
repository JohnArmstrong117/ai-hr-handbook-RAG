"""
RAG System Launcher
Choose between GUI and command-line interfaces for the HR Handbook RAG system.
"""

import sys
import os

def main():
    print("HR Handbook RAG System")
    print("=" * 40)
    print("Choose your interface:")
    print("1. GUI (Desktop Application)")
    print("2. Command Line Interface")
    print("3. Exit")
    print()
    
    while True:
        try:
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == "1":
                print("\nStarting GUI...")
                try:
                    import rag_gui
                    rag_gui.main()
                except ImportError as e:
                    print(f"Error: Could not import GUI module: {e}")
                    print("Make sure all dependencies are installed.")
                except Exception as e:
                    print(f"Error starting GUI: {e}")
                break
                
            elif choice == "2":
                print("\nStarting command-line interface...")
                try:
                    import test_rag
                    test_rag.main()
                except ImportError as e:
                    print(f"Error: Could not import CLI module: {e}")
                    print("Make sure all dependencies are installed.")
                except Exception as e:
                    print(f"Error starting CLI: {e}")
                break
                
            elif choice == "3":
                print("Goodbye!")
                break
                
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break

if __name__ == "__main__":
    main() 