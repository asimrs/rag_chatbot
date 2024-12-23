# rag_chatbot
# **TekRevol HR Chatbot**

The **TekRevol HR Chatbot** is a powerful tool designed to assist TekRevol employees with quick and accurate answers about company policies, training materials, rate cards, leadership information, and more. Built with advanced AI capabilities, this chatbot serves as an intelligent assistant to streamline HR-related queries and improve employee experience.

---

## **Features**

- 💬 **HR Knowledgebase Q&A**: Ask questions about company policies, benefits, leadership, training programs, and other HR-related topics.
- 📄 **Document Summarization**: Upload HR documents (e.g., policies, training materials) to get concise summaries.
- 🌐 **Webpage Analysis**: Enter URLs of HR resources to extract and process relevant information.
- 📚 **Conversational Context**: Maintains chat history to provide context-aware answers.
- ⚡ **Quick Responses**: Powered by LangChain and OpenAI, it delivers fast and accurate results.

---

## **Tech Stack**

- **Programming Language**: Python
- **Framework**: [Streamlit](https://streamlit.io) for the interactive web interface
- **AI Components**:
  - [LangChain](https://langchain.com) for conversational AI and retrieval-based Q&A
  - [OpenAI](https://openai.com) GPT models for natural language processing
- **Vector Store**: [FAISS](https://faiss.ai) for efficient embedding storage and retrieval
- **Embeddings**: OpenAI Embeddings for semantic understanding
- **Other Libraries**:
  - `beautifulsoup4` for webpage text extraction
  - `dotenv` for managing environment variables

---

## **Setup Instructions**

### **Prerequisites**

- Python 3.8 or above
- OpenAI API Key
- Git installed on your system

### **Step 1: Clone the Repository**

```bash
git clone https://github.com/username/tekrevol-hr-chatbot.git
cd tekrevol-hr-chatbot
```

### **Step 2: Install Dependencies**

Use `pip` to install required libraries:

```bash
pip install -r requirements.txt
```

### **Step 3: Set Environment Variables**

Create a `.env` file in the project root and add your OpenAI API key:

```plaintext
OPENAI_API_KEY=your_openai_api_key
```

### **Step 4: Run the Application**

Start the Streamlit app:

```bash
streamlit run chatbot_app.py
```

The chatbot will be available in your browser at `http://localhost:8501`.

---

## **Usage**

### **1. Sidebar Options**
- **Enter OpenAI API Key**: Input your OpenAI API Key to activate the chatbot.
- **Choose Input Method**:
  - Upload HR documents (e.g., PDFs, images).
  - Enter URLs of HR resources.

### **2. Interact with the Chatbot**
- Ask questions directly in the chat window:
  - *"What is the company's leave policy?"*
  - *"Can you summarize the uploaded training document?"*
- Upload files or URLs for analysis and summarization.

### **3. Clear Embeddings**
- Use the "Clear HR Knowledgebase" option to reset the stored embeddings.

---

## **Folder Structure**

```
tekrevol-hr-chatbot/
├── src/
│   ├── document_processor.py   # Handles document processing and chunking
│   └── __init__.py             # Module initializer
├── chatbot_app.py              # Main chatbot application
├── file_processor.py           # Embedding creation and summarization logic
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── README.md                   # Project documentation
└── faiss_index/                # Directory for FAISS index storage
```

---

## **Key Functionalities**

1. **Document Upload**:
   - Upload PDFs or images to analyze and process HR-related materials.
   - Automatically splits large files into manageable chunks for efficient embeddings and summarization.

2. **Webpage Analysis**:
   - Extracts and processes text from webpages for HR-related knowledge.

3. **Conversational Q&A**:
   - Context-aware responses using chat history and the FAISS-based retriever.

4. **Summarization**:
   - Generates concise summaries of uploaded documents or extracted text from URLs.

---

## **Example Questions**

Here are some example interactions to showcase the chatbot’s capabilities:

- *"What is the company's reimbursement policy?"*
- *"Who is the head of the marketing department?"*
- *"Summarize the uploaded HR training manual."*
- *"What are the key points from the leadership development program document?"*

---

## **Contributing**

We welcome contributions to enhance the TekRevol HR Chatbot! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and test thoroughly.
4. Submit a pull request with a detailed description of your changes.

---

## **Future Enhancements**

- Integration with Slack or Microsoft Teams for real-time HR support.
- Support for additional file formats (e.g., `.docx`).
- Multilingual support for global teams.
- Advanced analytics dashboard for HR insights.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Contact**

For any questions or support, please contact the TekRevol HR team.
