"""
Interactive RAG Test Script
This script allows you to test the RAG system with your HR handbook.
"""

from rag_setup import setup_rag, ask_question

def main():
    print("HR Handbook RAG System")
    print("=" * 50)
    
    # Set up the RAG system
    qa_chain, vectorstore = setup_rag()
    
    if qa_chain is None:
        print("\nTo use this system:")
        print("   1. Get an OpenAI API key from https://platform.openai.com/api-keys")
        print("   2. Create a .env file with: OPENAI_API_KEY=your_key_here")
        print("   3. Run this script again")
        return
    
    print("\nRAG system is ready!")
    print("\nYou can ask questions about:")
    print("   - Company policies and procedures")
    print("   - Benefits and perks")
    print("   - Career development")
    print("   - Work devices and systems")
    print("   - And more from your HR handbook!")
    
    print("\n" + "=" * 50)
    
    # Interactive question loop
    while True:
        print("\nAsk a question (or type 'quit' to exit):")
        question = input("> ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not question:
            continue
            
        try:
            ask_question(qa_chain, question)
        except Exception as e:
            print(f"Error: {e}")
            print("   Please try again with a different question.")

if __name__ == "__main__":
    main() 