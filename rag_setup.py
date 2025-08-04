"""
Basic RAG Setup for HR Handbook
This script sets up a Retrieval-Augmented Generation system for the HR handbook.
"""

import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI
from langchain.chains import RetrievalQA
from config import OPENAI_API_KEY, CHUNK_SIZE, CHUNK_OVERLAP, TOP_K_RETRIEVAL, LLM_TEMPERATURE

def setup_rag():
    """
    Set up the complete RAG pipeline for the HR handbook
    """
    print("Setting up RAG system for HR Handbook...")
    
    # Check if OpenAI API key is set
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
        print("Error: OpenAI API key not found!")
        print("   Please set your OPENAI_API_KEY in a .env file")
        print("   See env_example.txt for reference")
        return None, None
    
    # Step 1: Load documents from the handbook directory
    print("\nStep 1: Loading documents from handbook/ directory...")
    loader = DirectoryLoader(
        path="./handbook",
        glob="**/*.md",  # Load all markdown files
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    
    documents = loader.load()
    print(f"   Loaded {len(documents)} documents")
    
    # Step 2: Split documents into chunks
    print("\nStep 2: Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,  # Each chunk will be ~1000 characters
        chunk_overlap=CHUNK_OVERLAP,  # 200 character overlap between chunks
        length_function=len,
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"   Created {len(chunks)} chunks from {len(documents)} documents")
    
    # Step 3: Create embeddings and vector store
    print("\nStep 3: Creating embeddings and vector store...")
    embeddings = OpenAIEmbeddings()
    
    # Create FAISS vector store
    vectorstore = FAISS.from_documents(chunks, embeddings)
    print("   Vector store created successfully")
    
    # Step 4: Set up the retrieval chain
    print("\nStep 4: Setting up retrieval chain...")
    llm = OpenAI(temperature=LLM_TEMPERATURE)  # Low temperature for more consistent answers
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # Simple chain that stuffs all retrieved docs into prompt
        retriever=vectorstore.as_retriever(search_kwargs={"k": TOP_K_RETRIEVAL}),  # Retrieve top 3 most relevant chunks
        return_source_documents=True,  # Return source documents for transparency
    )
    
    print("   RAG system setup complete!")
    
    return qa_chain, vectorstore

def ask_question(qa_chain, question):
    """
    Ask a question to the RAG system
    """
    print(f"\nQuestion: {question}")
    print("Searching for relevant information...")
    
    result = qa_chain({"query": question})
    
    print(f"\nAnswer: {result['result']}")
    print(f"\nSources:")
    for i, doc in enumerate(result['source_documents'], 1):
        print(f"   {i}. {doc.metadata.get('source', 'Unknown source')}")
    
    return result

if __name__ == "__main__":
    # Set up the RAG system
    qa_chain, vectorstore = setup_rag()
    
    # Test the system with a sample question
    print("\n" + "="*50)
    print("Testing the RAG system...")
    print("="*50)
    
    test_question = "What is the company's vacation policy?"
    ask_question(qa_chain, test_question) 