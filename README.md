# 📄 DocuMind - AI Document Intelligence Platform

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)

A powerful document analysis tool built with Streamlit and Google Gemini AI that transforms how you interact with PDF documents. Get instant summaries, ask intelligent questions, and visualize document concepts through interactive mind maps.

## ✨ Features

- **📝 Smart Summarization** - Extract key insights from lengthy documents in seconds
- **💬 Interactive Q&A** - Ask questions and get accurate answers based on document content
- **🗺️ Visual Mind Maps** - See relationships between concepts with interactive D3.js visualizations
- **⚡ Fast & Efficient** - Powered by Google Gemini 2.5 Flash for rapid processing
- **🎯 User-Friendly** - Clean Streamlit interface with drag-and-drop PDF upload

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Google Gemini API key ([Get free key here](https://aistudio.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd A5-alternate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key**
   
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the app**
   - Open your browser to `http://localhost:8501`
   - Upload a PDF and start exploring!

## 📖 Usage

1. **Upload Document**: Drag and drop a PDF file in the sidebar
2. **Generate Summary**: Navigate to the Summary tab and click "Generate Smart Summary"
3. **Ask Questions**: Switch to Q&A tab and type your questions about the document
4. **Explore Concepts**: View the Mind Map tab to see an interactive visualization of key concepts

## 🛠️ Tech Stack

- **Frontend**: Streamlit, D3.js (for visualizations)
- **Backend**: Python 3.9+
- **AI/ML**: Google Gemini 2.5 Flash API
- **PDF Processing**: PyPDF2
- **Styling**: Custom CSS

## 📁 Project Structure

```
A5-alternate/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── styles.css               # Custom CSS styling
├── .env.example             # Environment variable template
├── .gitignore               # Git ignore rules
├── QUICKSTART.md            # Detailed setup guide
├── Chandrasekar-A5.md       # Assignment submission document
├── Example PDFs/            # Test PDF documents
├── image.png                # Example 1 mind map screenshot
└── image-1.png              # Example 2 mind map screenshot
```

## 🎯 Key Components

### Document Summarization
Uses advanced LLM capabilities to generate comprehensive summaries that capture:
- Main topics and themes
- Key points and insights
- Important details and relationships

### Question Answering
Intelligent Q&A system that:
- Understands context from uploaded documents
- Provides accurate, relevant answers
- Cites specific information from the source

### Mind Map Generation
Visual concept mapping that:
- Extracts key concepts automatically
- Shows relationships between ideas
- Interactive graph with drag, zoom, and pan

## 🔐 Security Notes

- **Never commit your `.env` file** - It contains your API key
- The `.gitignore` file is configured to exclude sensitive files
- Use environment variables for all secrets
- For deployment, use Streamlit Cloud's secrets management

## 🌐 Deployment

### Deploy to Streamlit Cloud (Free)

1. Push your code to GitHub (excluding `.env`)
2. Visit [share.streamlit.io](https://share.streamlit.io/)
3. Connect your GitHub repository
4. Add your `GEMINI_API_KEY` in the Secrets section
5. Deploy!

See [QUICKSTART.md](QUICKSTART.md) for detailed deployment instructions.

## 📊 Performance

- **Summary Generation**: ~4.2 seconds (10-page document)
- **Question Answering**: ~2.8 seconds per question
- **Mind Map Generation**: ~6.5 seconds
- **PDF Processing**: ~1.5 seconds (10-page PDF)

## 🤝 Contributing

This is an academic project created for an Assignment . Feel free to fork and adapt for your own use.

## 📝 License

This project is created for educational purposes .



## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Google Gemini AI](https://ai.google.dev/)
- Visualizations using [D3.js](https://d3js.org/)
- PDF processing with [PyPDF2](https://pypdf.readthedocs.io/)

## 📚 Documentation


- [Quick Start Guide](QUICKSTART.md) - Detailed setup and usage instructions
- [Google Gemini API Docs](https://ai.google.dev/gemini-api/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 🐛 Troubleshooting

**API Key Issues:**
- Ensure your `.env` file exists in the project root
- Verify your API key is correct (get it from https://aistudio.google.com/app/apikey)
- Check that python-dotenv is installed

**PDF Upload Issues:**
- Ensure PDF is not password-protected
- Check file size (large PDFs may take longer to process)
- Verify PDF contains extractable text (not just images)

**Dependencies:**
- Run `pip install --upgrade -r requirements.txt` to update all packages
- Ensure Python 3.9+ is installed

---

**⭐ If you find this project helpful, please star the repository!**
