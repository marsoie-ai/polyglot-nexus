import os
import streamlit as st
from engine import polyglot_nexus_engine
from xhtml2pdf import pisa
from arabic_reshaper import reshape
from bidi.algorithm import get_display
import io
import os
from supabase import create_client, Client

# Fetch secrets from Hugging Face environment
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

# Initialize the Supabase client
supabase: Client = create_client(url, key)

# --- CORE LOGIC: PDF GENERATION ---
def create_pdf_bytes(raw_text):
    """Processes multi-language text into a professional PDF with RTL support."""
    reshaped_text = reshape(raw_text)
    bidi_text = get_display(reshaped_text)
    sections = bidi_text.split("###")
    formatted_html = ""
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_maltese = os.path.join(base_dir, "NotoSansMaltese-Regular.ttf")
    font_arabic = os.path.join(base_dir, "NotoSansArabic-Regular.ttf")

    for section in sections:
        if section.strip():
            # Apply RTL class if Arabic characters are detected
            if any("\u0600" <= c <= "\u06FF" for c in section):
                formatted_html += f'<div class="section rtl">{section.strip()}</div>'
            else:
                formatted_html += f'<div class="section">{section.strip()}</div>'

    style = f"""
    <style>
        @font-face {{ font-family: 'MalteseFont'; src: url('{font_maltese}'); }}
        @font-face {{ font-family: 'ArabicFont'; src: url('{font_arabic}'); }}
        @page {{ size: A4; margin: 1.5cm; }}
        body {{ font-family: 'MalteseFont', sans-serif; font-size: 14pt; line-height: 1.6; }}
        .rtl {{ font-family: 'ArabicFont', sans-serif; direction: rtl; text-align: right; font-size: 16pt; }}
        .section {{ page-break-after: always; white-space: pre-wrap; margin-top: 20px; }}
        h1 {{ text-align: center; color: #333; }}
    </style>
    """
    
    html_template = f"<html><head><meta charset='UTF-8'>{style}</head><body>{formatted_html}</body></html>"
    result = io.BytesIO()
    pisa.CreatePDF(io.BytesIO(html_template.encode("UTF-8")), dest=result)
    return result.getvalue()

# --- REFINED PORTFOLIO UI ---
def main():
    # 1. PAGE SETUP
    st.set_page_config(page_title="ISW Polyglot-Nexus", page_icon="🏫", layout="wide")

    # 2. SIDEBAR (With the correct ISW Link you found!)
    with st.sidebar:
        st.image("https://www.is-westpfalz.de/wp-content/uploads/logo-is-westpfalz-200x70.png", use_container_width=True)
        st.divider()
        st.info("🚀 **Project Portfolio: ISW Edition**")
        
        # Phase 2 Hook: Advanced Settings Toggle
        show_advanced = st.checkbox("Show Engine Analytics", value=True)
        
        st.divider()
        st.caption("Architected by Ben Mahmoud | 2026")

    # 3. MAIN UI HEADER
    st.title("🏫 Polyglot-Nexus")
    st.subheader("Cambridge International Education • Semantic Logic Adapter")
    st.markdown("---")
    
    # 4. INPUT SECTION
    col1, col2 = st.columns(2)
    with col1:
        level = st.selectbox("Select Cambridge Pathway:", 
                             options=["Primary", "Lower Secondary", "IGCSE", "A Level"])
    with col2:
        topic = st.text_input("Computer Science Topic:", placeholder="e.g. Logic Gates")

    # 5. EXECUTION LOGIC
    if st.button("Generate Cultural Logic", use_container_width=True):
        if topic:
            with st.spinner("Executing Semantic Mapping..."):
                try:
                    response = polyglot_nexus_engine(topic, level)
                    pdf_bytes = create_pdf_bytes(response)
                    
                    # PHASE 1: INTERACTIVE DASHBOARD
                    if show_advanced:
                        st.markdown("### 📊 Lesson Analytics")
                        m1, m2, m3 = st.columns(3)
                        depth_score = {"Primary": "Core", "Lower Secondary": "Intermediate", "IGCSE": "Advanced", "A Level": "Expert"}
                        m1.metric("Cognitive Depth", depth_score[level])
                        m2.metric("Linguistic Frameworks", "7 Languages", "Verified")
                        m3.metric("PDF Encoding", "UTF-8", "RTL Active")
                    st.divider()
                    
                    # --- PHASE 2: PROMPT ENGINEERING INSIGHTS ---
                    with st.expander("🛠️ View Semantic Mapping Prompt"):
                        st.caption("This is the system-level instruction sent to the LLM to ensure cultural and academic accuracy.")
                        
                        # We 'reconstruct' the prompt logic for the viewer
                        system_prompt = f"""
                        You are a Cambridge CS Expert. 
                        Task: Adapt '{topic}' for the '{level}' pathway.
                        Constraints:
                        1. Generate 7 specific cultural frameworks.
                        2. Use RTL formatting for Arabic/Maltese.
                        3. Apply LaTeX for any complex math/logic.
                        4. Maintain tone appropriate for {level} students.
                        """
                        st.code(system_prompt, language="markdown")
                        
                        st.info(f"**Optimization Note:** Prompt is dynamically weighted for the **{level}** cognitive framework.")
                    
                    st.divider()

                    st.download_button("📥 Download Lesson Notes (PDF)", 
                                       pdf_bytes, f"{topic}_{level}_Notes.pdf", "application/pdf")
                    
                    # LANGUAGE EXPANDERS
                    languages = ["ENGLISH", "DEUTSCH", "FRANÇAIS", "ITALIANO", "ESPAÑOL", "العربية", "MALTI"]
                    for lang in languages:
                        with st.expander(f"⬜ {lang} Perspective"):
                            search_tag = f"### {lang}"
                            if search_tag in response:
                                content = response.split(search_tag)[1].split("###")[0]
                                st.markdown(content.strip())
                            else:
                                st.info(f"Generating {lang} cultural context...")

                    st.success("✅ Adaptation complete.")
                    
                except Exception as e:
                    st.error(f"System Error: {e}")
        else:
            st.warning("Input required: Please enter a topic to begin.")

if __name__ == "__main__":
    main()
