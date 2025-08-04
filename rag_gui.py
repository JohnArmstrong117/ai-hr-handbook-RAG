"""
HR Handbook RAG GUI
A simple desktop interface for the RAG system using tkinter.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from rag_setup import setup_rag, ask_question

class RAGGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HR Handbook RAG System")
        self.root.geometry("800x600")
        
        # Initialize RAG system
        self.qa_chain = None
        self.vectorstore = None
        self.setup_rag_system()
        
        # Create GUI components
        self.create_widgets()
        
    def setup_rag_system(self):
        """Initialize the RAG system in a separate thread"""
        def init_rag():
            try:
                self.qa_chain, self.vectorstore = setup_rag()
                if self.qa_chain is None:
                    self.root.after(0, self.show_setup_error)
                else:
                    self.root.after(0, self.show_ready_message)
            except Exception as e:
                self.root.after(0, lambda: self.show_error(f"Setup error: {e}"))
        
        # Run setup in background thread
        thread = threading.Thread(target=init_rag, daemon=True)
        thread.start()
    
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="HR Handbook RAG System", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Initializing RAG system...", 
                                     foreground="blue")
        self.status_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # Question input
        question_frame = ttk.LabelFrame(main_frame, text="Ask a Question", padding="10")
        question_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        question_frame.columnconfigure(0, weight=1)
        
        # Question entry
        self.question_var = tk.StringVar()
        self.question_entry = ttk.Entry(question_frame, textvariable=self.question_var, 
                                       font=("Arial", 11))
        self.question_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.question_entry.bind('<Return>', self.ask_question)
        
        # Ask button
        self.ask_button = ttk.Button(question_frame, text="Ask", command=self.ask_question)
        self.ask_button.grid(row=0, column=1)
        
        # Answer display
        answer_frame = ttk.LabelFrame(main_frame, text="Answer", padding="10")
        answer_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        answer_frame.columnconfigure(0, weight=1)
        answer_frame.rowconfigure(0, weight=1)
        
        # Answer text area
        self.answer_text = scrolledtext.ScrolledText(answer_frame, wrap=tk.WORD, 
                                                    height=10, font=("Arial", 10))
        self.answer_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Sources display
        sources_frame = ttk.LabelFrame(main_frame, text="Sources", padding="10")
        sources_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        sources_frame.columnconfigure(0, weight=1)
        
        # Sources text area
        self.sources_text = scrolledtext.ScrolledText(sources_frame, wrap=tk.WORD, 
                                                     height=4, font=("Arial", 9))
        self.sources_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Example questions
        examples_frame = ttk.LabelFrame(main_frame, text="Example Questions", padding="10")
        examples_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))
        examples_frame.columnconfigure(0, weight=1)
        
        examples = [
            "What is our vacation policy?",
            "How do I request time off?",
            "What benefits do we offer?",
            "What are the career development opportunities?",
            "What's the policy on work devices?"
        ]
        
        for i, example in enumerate(examples):
            btn = ttk.Button(examples_frame, text=example, 
                           command=lambda q=example: self.load_example_question(q))
            btn.grid(row=i//2, column=i%2, sticky=(tk.W, tk.E), padx=5, pady=2)
            examples_frame.columnconfigure(i%2, weight=1)
        
        # Clear button
        clear_button = ttk.Button(main_frame, text="Clear", command=self.clear_display)
        clear_button.grid(row=6, column=0, columnspan=2, pady=(10, 0))
    
    def show_setup_error(self):
        """Show error message when RAG setup fails"""
        self.status_label.config(text="Error: OpenAI API key not found!", foreground="red")
        self.answer_text.insert(tk.END, 
            "To use this system:\n"
            "1. Get an OpenAI API key from https://platform.openai.com/api-keys\n"
            "2. Create a .env file with: OPENAI_API_KEY=your_key_here\n"
            "3. Restart this application\n")
        self.ask_button.config(state="disabled")
    
    def show_ready_message(self):
        """Show ready message when RAG system is initialized"""
        self.status_label.config(text="RAG system ready! Ask a question.", foreground="green")
        self.ask_button.config(state="normal")
        self.question_entry.focus()
    
    def show_error(self, message):
        """Show error message"""
        self.status_label.config(text=message, foreground="red")
        messagebox.showerror("Error", message)
    
    def ask_question(self, event=None):
        """Ask a question to the RAG system"""
        if self.qa_chain is None:
            messagebox.showwarning("Warning", "RAG system not ready. Please check your API key.")
            return
        
        question = self.question_var.get().strip()
        if not question:
            messagebox.showwarning("Warning", "Please enter a question.")
            return
        
        # Clear previous results
        self.answer_text.delete(1.0, tk.END)
        self.sources_text.delete(1.0, tk.END)
        
        # Disable input during processing
        self.ask_button.config(state="disabled")
        self.question_entry.config(state="disabled")
        self.status_label.config(text="Searching for answer...", foreground="blue")
        
        # Process question in background thread
        def process_question():
            try:
                result = self.qa_chain({"query": question})
                
                # Update GUI in main thread
                self.root.after(0, lambda: self.display_result(result))
            except Exception as e:
                self.root.after(0, lambda: self.show_error(f"Error processing question: {e}"))
            finally:
                # Re-enable input
                self.root.after(0, self.enable_input)
        
        thread = threading.Thread(target=process_question, daemon=True)
        thread.start()
    
    def display_result(self, result):
        """Display the RAG result"""
        # Display answer
        self.answer_text.insert(tk.END, result['result'])
        
        # Display sources
        sources = []
        for i, doc in enumerate(result['source_documents'], 1):
            source = doc.metadata.get('source', 'Unknown source')
            # Extract just the filename from the path
            filename = source.split('/')[-1] if '/' in source else source
            sources.append(f"{i}. {filename}")
        
        self.sources_text.insert(tk.END, "\n".join(sources))
        
        # Update status
        self.status_label.config(text="Answer ready!", foreground="green")
    
    def enable_input(self):
        """Re-enable input controls"""
        self.ask_button.config(state="normal")
        self.question_entry.config(state="normal")
    
    def load_example_question(self, question):
        """Load an example question into the input field"""
        self.question_var.set(question)
        self.question_entry.focus()
    
    def clear_display(self):
        """Clear the display areas"""
        self.answer_text.delete(1.0, tk.END)
        self.sources_text.delete(1.0, tk.END)
        self.question_var.set("")

def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = RAGGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 