# DocuMind Quick Start Guide

## ⚡ Quick Setup (5 minutes)

### Step 1: Install Dependencies
Open PowerShell or Command Prompt in this directory and run:

```powershell
py -m pip install streamlit google-generativeai PyPDF2 python-dotenv
```

### Step 2: Add Your Gemini API Key

1. Open the `.env` file in this directory
2. Replace `your_actual_api_key_here` with your Gemini API key
3. If you don't have one, get it free at: https://aistudio.google.com/app/apikey

Your `.env` file should look like:
```
GEMINI_API_KEY=AIzaSy...your_actual_key...
```

### Step 3: Run the Application

```powershell
py -m streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

---

## 🎯 Quick Demo

1. **Upload a PDF** - Click "Browse files" in the sidebar
2. **Get Summary** - Click the "Summary" tab and click "Generate Summary"
3. **Ask Questions** - Go to "Q&A" tab and type questions about your document
4. **View Mind Map** - Click "Mind Map" tab and click "Generate Mind Map"

---

## 📝 Test PDFs

Try with any PDF you have, or download test PDFs from:
- Academic papers: https://arxiv.org/
- Business reports: Any quarterly report or whitepaper
- Books: Any PDF book chapter

---

## ❌ Troubleshooting

### If dependencies fail to install:
Try installing one at a time:
```powershell
py -m pip install --upgrade pip
py -m pip install streamlit
py -m pip install google-generativeai
py -m pip install PyPDF2
py -m pip install python-dotenv
```

### If the app won't start:
- Make sure you added your API key to `.env` file
- Check that you're in the correct directory (`c:\learning\A5-alternate`)
- Try restarting your terminal

### If you get API errors:
- Verify your API key is correct in `.env`
- Check you haven't exceeded the free tier limits (15 requests/minute)
- Wait a few seconds and try again

---

## 📊 Assignment Deliverables

All assignment questions are answered in `README.md`:
- ✅ Value proposition
- ✅ Data/knowledge sources  
- ✅ AI tasks and methods
- ✅ Example inputs/outputs (2+ examples)
- ✅ Testing metrics with formulas and results

---

## 🚀 That's It!

You're ready to demo DocuMind. Enjoy!
