import sys
from story_generator import run_story_generator
from plot_checker import run_plot_checker
from creative_explorer import run_creative_explorer
from style_transformer import run_style_transformer
from llm_interface import start_chat_session, end_chat_session

def display_menu():
    """Displays the main menu options."""
    print("\n===== 🖋️ AI Story Assistant ======")
    print("Choose an option:")
    print("  1. Generate a New Story")
    print("  2. Check Story for Plot Holes & Inconsistencies")
    print("  3. Creative Story Exploration (Alternate Endings, What Ifs)")
    print("  4. Transform Story Style")
    print("  0. Exit")
    print("===================================")

def main():
    """Main application loop."""
    print("Initializing session...")
    chat_session = start_chat_session()
    if not chat_session:
        print("Failed to start session. Exiting.")
        sys.exit(1)

    try:
        while True:
            display_menu()
            choice = input("Enter your choice (0-4): ")

            if choice == '1':
                run_story_generator(chat_session)
            elif choice == '2':
                run_plot_checker(chat_session)
            elif choice == '3':
                run_creative_explorer(chat_session)
            elif choice == '4':
                run_style_transformer(chat_session)
            elif choice == '0':
                print("Goodbye! 👋")
                break
            else:
                print("Invalid choice. Please enter a number between 0 and 4.")

            input("\nPress Enter to return to the main menu...")  # Pause before showing menu again
    finally:
        print("Ending session...")
        end_chat_session(chat_session)

if __name__ == "__main__":
    main()