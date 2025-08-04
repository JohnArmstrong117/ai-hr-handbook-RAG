# HR Handbook RAG System

This project implements a Retrieval-Augmented Generation (RAG) system for your HR handbook, allowing users to ask questions and get accurate answers based on your company's policies and procedures.

## How it Works

**RAG (Retrieval-Augmented Generation)** combines:
- **Document Retrieval**: Finds relevant information from your HR handbook
- **Text Generation**: Uses AI to generate accurate answers based on that information

This ensures answers are grounded in your actual company policies rather than generic information.

## Project Structure

```
├── handbook/                 # Your HR handbook markdown files
├── rag_setup.py             # Core RAG system implementation
├── test_rag.py              # Interactive testing script
├── config.py                # Configuration settings
├── env_example.txt          # Environment variables template
└── requirements.txt         # Python dependencies
```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key

### 3. Set Up Environment Variables
1. Create a `.env` file in the project root
2. Add your OpenAI API key:
```
OPENAI_API_KEY=your_actual_api_key_here
```

## Testing the System

### Quick Test (No API Key Required)
```bash
python test_rag.py
```
This will show you the setup instructions if no API key is found.

### Full Test (With API Key)
1. Set up your `.env` file with your OpenAI API key
2. Run the test script:
```bash
python test_rag.py
```
3. Ask questions like:
   - "What is our vacation policy?"
   - "How do I request time off?"
   - "What benefits do we offer?"
   - "What are the career development opportunities?"

## How It Works

### Step 1: Document Loading
- Scans the `handbook/` directory for all `.md` files
- Loads each markdown file as text

### Step 2: Text Chunking
- Splits large documents into smaller chunks (~1000 characters)
- Maintains context with overlapping chunks (200 characters)

### Step 3: Embeddings & Vector Store
- Converts text chunks into numerical vectors using OpenAI embeddings
- Stores vectors in FAISS for fast similarity search

### Step 4: Question Answering
- Converts your question to a vector
- Finds the most similar document chunks
- Generates an answer using the retrieved information

## Configuration

You can modify settings in `config.py`:

```python
CHUNK_SIZE = 1000          # Size of text chunks
CHUNK_OVERLAP = 200        # Overlap between chunks
TOP_K_RETRIEVAL = 3        # Number of chunks to retrieve
LLM_TEMPERATURE = 0        # AI response consistency (0 = most consistent)
```

## Example Questions

Try asking about:
- **Benefits**: "What health insurance options do we have?"
- **Policies**: "What's our remote work policy?"
- **Career**: "How do promotions work here?"
- **Devices**: "What's the policy on work laptops?"
- **Time Off**: "How do I request PTO?"

## Understanding the Output

When you ask a question, the system will:
1. **Search** for relevant information in your handbook
2. **Generate** an answer based on that information
3. **Show sources** - the specific files where the information was found

This transparency helps you verify the accuracy of answers.

## Troubleshooting

### "OpenAI API key not found"
- Make sure you created a `.env` file
- Check that your API key is correct
- Ensure the file is in the project root directory

### "No documents found"
- Check that your `handbook/` directory contains `.md` files
- Verify file permissions

### Slow responses
- The first run creates embeddings (can take a few minutes)
- Subsequent runs will be faster

## Updating the System

When you update your HR handbook:
1. Add new `.md` files to the `handbook/` directory
2. Run the system again - it will automatically include the new content

## Performance Tips

- **Chunk size**: Smaller chunks (500-1000 chars) work well for specific questions
- **Overlap**: 10-20% overlap prevents losing context
- **Retrieval count**: 3-5 chunks usually provide good coverage

## Contributing

To improve the system:
1. Add more handbook content to the `handbook/` directory
2. Adjust configuration parameters in `config.py`
3. Test with various question types

---

**Note**: This system uses OpenAI's API, which incurs costs based on usage. Monitor your usage at the OpenAI platform dashboard. 