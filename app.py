"""
DocuMind - AI Document Intelligence Platform
A mini NotebookLM-style application for PDF analysis

Features:
- Document Summarization using Gemini LLM
- Question Answering with context retrieval
- Mind map generation with D3.js visualization
"""

import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="DocuMind - AI Document Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure Gemini API with validation
API_KEY = os.getenv('GEMINI_API_KEY')
if not API_KEY or API_KEY == 'your_actual_api_key_here':
    st.error("⚠️ GEMINI_API_KEY not configured! Please set it in the .env file.")
    st.info("Get your free API key at: https://aistudio.google.com/app/apikey")
    st.stop()

try:
    genai.configure(api_key=API_KEY)
    MODEL_NAME = 'gemini-2.5-flash'  # Using Gemini 2.5 Flash for optimal performance
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    st.error(f"❌ Error configuring Gemini API: {str(e)}")
    st.stop()

# Custom CSS for polished, modern UI
# Custom CSS for polished, modern UI
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("styles.css")

# Initialize session state
if 'pdf_text' not in st.session_state:
    st.session_state.pdf_text = None
if 'filename' not in st.session_state:
    st.session_state.filename = None
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'mindmap_data' not in st.session_state:
    st.session_state.mindmap_data = None


def extract_text_from_pdf(pdf_file):
    """
    Extract text content from uploaded PDF file.
    
    Args:
        pdf_file: Uploaded PDF file object from Streamlit file_uploader
        
    Returns:
        str: Extracted text content from all pages, or None if extraction fails
    """
    try:
        pdf_reader = PdfReader(pdf_file)
        text = ""
        total_pages = len(pdf_reader.pages)
        
        if total_pages == 0:
            st.warning("⚠️ PDF appears to be empty.")
            return None
            
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
                
        if not text.strip():
            st.warning("⚠️ Could not extract text from PDF. It may be image-based or encrypted.")
            return None
            
        return text
    except Exception as e:
        st.error(f"❌ Error extracting text from PDF: {str(e)}")
        return None


def generate_summary(text):
    """
    Generate comprehensive document summary using Gemini LLM.
    
    AI Task: Text Summarization
    AI Method: Large Language Models (Gemini 2.5 Flash)
    
    Args:
        text (str): Full document text to summarize
        
    Returns:
        str: Generated summary with main topic and key points, or None if generation fails
    """
    try:
        # Limit text to ~8000 characters to stay within token limits
        text_chunk = text[:8000] if len(text) > 8000 else text
        
        prompt = f"""
        You are an expert document analyst. Please provide a comprehensive summary of the following document.
        
        Instructions:
        - Identify the main topic/theme
        - List 5-8 key points with detailed explanations
        - Keep it comprehensive and informative (500-700 words)
        - Use bullet points for clarity
        
        Document:
        {text_chunk}
        
        Summary:
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"❌ Error generating summary: {str(e)}")
        return None


def answer_question(text, question):
    """
    Answer user questions about document content using Gemini LLM.
    
    AI Task: Question Answering with Information Extraction
    AI Method: Large Language Models (Gemini 2.5 Flash)
    
    Args:
        text (str): Document text to query
        question (str): User's question about the document
        
    Returns:
        str: Generated answer based on document content, or None if generation fails
    """
    try:
        # Limit text to ~8000 characters for context window
        text_chunk = text[:8000] if len(text) > 8000 else text
        
        prompt = f"""
        You are an expert document analyst. Answer the following question based ONLY on the document content below.
        
        Instructions:
        - Provide accurate, factual answers
        - Quote relevant parts if helpful
        - If the answer is not in the document, say "I cannot find this information in the document."
        - Be concise but complete
        
        Document:
        {text_chunk}
        
        Question: {question}
        
        Answer:
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"❌ Error answering question: {str(e)}")
        return None


def generate_mindmap_data(text):
    """Generate mind map data structure using Gemini LLM"""
    try:
        prompt = f"""
        You are an expert at extracting knowledge structures from documents.
        
        Analyze the following document and extract a hierarchical mind map structure.
        
        Return ONLY valid JSON in this exact format (Tree Structure):
        {{
            "name": "Central Topic",
            "children": [
                {{
                    "name": "Main Concept 1",
                    "children": [
                        {{"name": "Sub-concept A"}},
                        {{"name": "Sub-concept B"}}
                    ]
                }},
                {{
                    "name": "Main Concept 2",
                    "children": [
                        {{"name": "Sub-concept C"}}
                    ]
                }}
            ]
        }}
        
        Rules:
        - Root node should be the main document title or central theme
        - Create 3-5 main branches (level 1)
        - Each main branch should have 2-4 sub-branches (level 2)
        - Keep labels concise (2-5 words max)
        
        Document:
        {text[:6000]}
        
        JSON:
        """
        
        response = model.generate_content(prompt)
        
        # Extract JSON from response
        response_text = response.text.strip()
        
        # Try to find JSON in the response
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            json_str = response_text[json_start:json_end].strip()
        elif "```" in response_text:
            json_start = response_text.find("```") + 3
            json_end = response_text.find("```", json_start)
            json_str = response_text[json_start:json_end].strip()
        else:
            json_str = response_text
        
        mindmap_data = json.loads(json_str)
        return mindmap_data
        
    except json.JSONDecodeError as e:
        st.error(f"Error parsing mind map data: {str(e)}")
        st.error(f"Response was: {response_text}")
        return None
    except Exception as e:
        st.error(f"Error generating mind map: {str(e)}")
        return None


# Main App Logic
if st.session_state.pdf_text:
    # ------------------------------------------------------------------------
    # APPLICATION VIEW (File Loaded)
    # ------------------------------------------------------------------------
    
    # Sidebar
    with st.sidebar:
        st.title("🧠 DocuMind")
        st.markdown("### Document Intelligence")
        st.markdown("---")
        
        st.success(f"📄 **Active:** {st.session_state.filename}")
        st.caption(f"Size: {len(st.session_state.pdf_text):,} chars")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("📤 Upload New Document", use_container_width=True):
            # Reset state to go back to landing page
            st.session_state.pdf_text = None
            st.session_state.filename = None
            st.session_state.summary = None
            st.session_state.chat_history = []
            st.session_state.mindmap_data = None
            st.rerun()
            
        st.markdown("---")
        st.markdown("### Features")
        st.markdown("- 📝 **Smart Summary**")
        st.markdown("- 💬 **Interactive Q&A**")
        st.markdown("- 🗺️ **Visual Mind Map**")
        
        st.markdown("---")
        st.caption(f"Powered by {MODEL_NAME}")

    # Main Area
    st.markdown(f"""
    <div class="app-header">
        <div class="app-header-icon">&#128196;</div>
        <div class="app-header-content">
            <div class="app-header-subtitle">Document Analysis</div>
            <div class="app-header-title">{st.session_state.filename}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📝 Summary", "💬 Q&A", "🗺️ Mind Map"])
    
    # Tab 1: Summary
    with tab1:
        st.markdown("### Document Abstract")
        
        if st.button("✨ Generate Smart Summary", type="primary"):
            with st.spinner("🤖 Analyzing document structure and key points..."):
                summary = generate_summary(st.session_state.pdf_text)
                if summary:
                    st.session_state.summary = summary
        
        if st.session_state.summary:
            st.markdown("---")
            st.markdown(st.session_state.summary)
            
            # Download option
            st.download_button(
                label="💾 Download Summary",
                data=st.session_state.summary,
                file_name=f"{st.session_state.filename}_summary.txt",
                mime="text/plain"
            )
    
    # Tab 2: Q&A
    with tab2:
        st.markdown("### 💬 Ask Questions")
        st.markdown("Chat with your document using AI")
        st.markdown("")
        
        # Chat container with scrollable area
        chat_container = st.container()
        
        # Display chat history
        with chat_container:
            if st.session_state.chat_history:
                for i, qa in enumerate(st.session_state.chat_history):
                    # Escape HTML in messages to prevent injection
                    import html
                    safe_question = html.escape(qa['question']).replace('\n', '<br>')
                    safe_answer = html.escape(qa['answer']).replace('\n', '<br>')
                    
                    # User message (question) on the right
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <div class="message-bubble user-bubble">
                            {safe_question}
                        </div>
                        <div class="message-avatar user-avatar">👤</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # AI message (answer) on the left
                    st.markdown(f"""
                    <div class="chat-message ai-message">
                        <div class="message-avatar ai-avatar">🤖</div>
                        <div class="message-bubble ai-bubble">
                            {safe_answer}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("💡 Ask a question about your document to start the conversation!")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Placeholder for spinner at the top of the input area
        spinner_placeholder = st.empty()
        
        # Question input section at the bottom with form for Enter key support
        with st.form(key="question_form", clear_on_submit=True):
            # Custom layout for "merged" look
            col_input, col_btn = st.columns([8, 1])
            
            with col_input:
                question = st.text_input(
                    "Ask a question",
                    placeholder="Type your question here...",
                    label_visibility="collapsed",
                    key="question_input"
                )
            
            with col_btn:
                # Use a specific label or icon to make it fit slightly better
                ask_button = st.form_submit_button("➤", type="primary", use_container_width=True)
        
        # Clear history button
        if st.session_state.chat_history:
            if st.button("🗑️ Clear Chat", use_container_width=False):
                st.session_state.chat_history = []
                st.rerun()
        
        # Handle question submission
        if ask_button and question:
            with spinner_placeholder:
                with st.spinner("Thinking..."):
                    answer = answer_question(st.session_state.pdf_text, question)
                    if answer:
                        st.session_state.chat_history.append({
                            "question": question,
                            "answer": answer
                        })
                        st.rerun()

    # Tab 3: Mind Map
    with tab3:
        st.header("Concept Knowledge Graph")
        
        if st.button("🗺️ Generate Visual Graph", type="primary"):
            with st.spinner("🧠 Extracting concepts and relationships..."):
                mindmap_data = generate_mindmap_data(st.session_state.pdf_text)
                if mindmap_data:
                    st.session_state.mindmap_data = mindmap_data
        
        if st.session_state.mindmap_data:
            st.markdown("### 🎨 Interactive Mind Map")
            
            # D3.js visualization (Same code as before)
            import streamlit.components.v1 as components
            
            # Split HTML into parts to avoid f-string brace escaping issues with CSS/JS
            d3_html_head = '''
            <!DOCTYPE html>
            <html>
            <head>
                <script src="https://d3js.org/d3.v7.min.js"></script>
                <style>
                    body { margin: 0; overflow: hidden; }
                    svg { background-color: #ffffff; width: 100vw; height: 100vh; }
                    .node rect {
                        stroke: #fff;
                        stroke-width: 2px;
                        cursor: pointer;
                        filter: drop-shadow(0 3px 3px rgba(0,0,0,0.1));
                        transition: all 0.3s;
                    }
                    .node:hover rect {
                        filter: drop-shadow(0 5px 8px rgba(0,0,0,0.2));
                        transform: scale(1.02);
                    }
                    .node text {
                        font-family: 'Inter', sans-serif;
                        font-size: 12px;
                        pointer-events: none;
                        alignment-baseline: middle;
                        font-weight: 500;
                        fill: #333;
                    }
                    .link {
                        fill: none;
                        stroke: #cbd5e1;
                        stroke-width: 1.5px;
                    }
                </style>
            </head>
            <body>
                <svg id="mindmap"></svg>
                <script>
            '''
            
            # Inject data using f-string or formatting
            d3_data_script = f"const data = {json.dumps(st.session_state.mindmap_data)};"
            
            d3_html_body = '''
                    const width = window.innerWidth;
                    
                    // Pastel Color Scale
                    const colors = ["#e0f2fe", "#f0fdf4", "#fef3c7", "#fce7f3", "#ede9fe"];

                    // Process Data for Hierarchy
                    const root = d3.hierarchy(data);
                    
                    // Dynamic Height Calculation based on leaf nodes
                    const leaves = root.leaves().length;
                    const nodeHeight = 60;
                    const height = Math.max(600, leaves * nodeHeight);
                    
                    const svg = d3.select("#mindmap")
                        .attr("width", width)
                        .attr("height", height);
                        
                    const g = svg.append("g");
                    
                    // Zoom behavior
                    const zoom = d3.zoom()
                        .scaleExtent([0.1, 4])
                        .on("zoom", (event) => {
                            g.attr("transform", event.transform);
                        });
                        
                    svg.call(zoom);
                    
                    // Tree Layout
                    const tree = d3.tree()
                        .size([height - 100, width - 400]); // Increased horizontal padding
                        
                    tree(root);
                    
                    // Links
                    const link = g.selectAll(".link")
                        .data(root.links())
                        .join("path")
                        .attr("class", "link")
                        .attr("d", d3.linkHorizontal()
                            .x(d => d.y)
                            .y(d => d.x));
                            
                    // Nodes
                    const node = g.selectAll(".node")
                        .data(root.descendants())
                        .join("g")
                        .attr("class", "node")
                        .attr("transform", d => `translate(${d.y},${d.x})`);
                        
                    // Node Rectangles
                    node.append("rect")
                        .attr("rx", 6)
                        .attr("ry", 6)
                        .attr("width", d => Math.max(120, d.data.name.length * 8))
                        .attr("height", 36)
                        .attr("y", -18)
                        .attr("fill", d => {
                            if (!d.depth) return "#e0e7ff"; // Root
                            return colors[d.depth % colors.length];
                        });
                        
                    // Node Text
                    node.append("text")
                        .attr("dy", 1)
                        .attr("x", 10)
                        .text(d => d.data.name);
                        
                    // Center the tree initially
                    const initialScale = 0.8;
                    const bbox = g.node().getBBox();
                    const initialTranslate = [
                        50,
                        (height - bbox.height * initialScale) / 2 - bbox.y * initialScale
                    ];
                    
                    svg.call(zoom.transform, d3.zoomIdentity
                        .translate(initialTranslate[0], initialTranslate[1])
                        .scale(initialScale));
                        
                </script>
            </body>
            </html>
            '''
            
            # Combine parts
            d3_html = d3_html_head + d3_data_script + d3_html_body
            
            components.html(d3_html, height=600)
            
            # Show raw data
            with st.expander("📊 View Tree Data"):
                st.json(st.session_state.mindmap_data)

else:
    # ------------------------------------------------------------------------
    # LANDING PAGE VIEW (No File)
    # ------------------------------------------------------------------------
    
    # Removed extra br tags for top whitespace reduction
    
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <div class="hero-tag">✨ Master your materials with AI Intelligence</div>
        <div class="hero-title">
            <span class="hero-logo-img">🧠</span> DocuMind
        </div>
        <div class="hero-description">
            Upload your documents to create summaries, get answers, and visualize concepts instantly.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Removed extra br tag for spacing reduction
    
    # Centered File Uploader
    uploaded_file = st.file_uploader(
        "Click to upload or drag & drop (PDF)",
        type=['pdf'],
        key="landing_uploader"
    )
    
    # Handle File Upload
    if uploaded_file:
        if st.session_state.filename != uploaded_file.name:
            with st.spinner("📖 Processing Document..."):
                text = extract_text_from_pdf(uploaded_file)
                if text:
                    st.session_state.pdf_text = text
                    st.session_state.filename = uploaded_file.name
                    st.session_state.summary = None
                    st.session_state.chat_history = []
                    st.session_state.mindmap_data = None
                    st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Feature Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon icon-orange">📝</div>
            <div class="feature-title">Smart Summary</div>
            <div class="feature-desc">Instantly transform lengthy documents into concise, actionable insights.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon icon-blue">💬</div>
            <div class="feature-title">Interactive Q&A</div>
            <div class="feature-desc">Chat directly with your files to extract answers and citations in seconds.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon icon-purple">🗺️</div>
            <div class="feature-title">Visual Mind Map</div>
            <div class="feature-desc">Visualize complex connections with automatically generated knowledge graphs.</div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit, Google Gemini 2.5 Flash, and D3.js | AI Assignment A5 | Disclaimer: This is an academic project for educational purposes only")

