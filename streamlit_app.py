import os
import streamlit as st
from engine import polyglot_nexus_engine
from xhtml2pdf import pisa
from arabic_reshaper import reshape
from bidi.algorithm import get_display
import io
from supabase import create_client, Client
from convex import ConvexClient

# --- DATABASE INITIALIZATION ---
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
convex_url = os.environ.get("CONVEX_URL")

# Initialize Supabase
supabase = None
if url and key:
    try:
        supabase = create_client(url, key)
    except:
        supabase = None

# Initialize Convex
convex_client = None
if convex_url:
    try:
        # FIXED: Removed the 'mutation' call from here. 
        # You can't run a mutation during initialization because 'title/content' don't exist yet.
        convex_client = ConvexClient(convex_url) 
    except:
        convex_client = None

def save_lesson_to_db(topic, level, content):
    """Syncs data with granular status tracking."""
    data = {"topic": topic, "level": level, "content": str(content)}
    s_ok, c_ok = False, False
    
    # 1. Attempt Supabase Sync
    if supabase:
        try:
            supabase.table("lessons").insert(data).execute()
            s_ok = True
        except Exception as e:
            st.sidebar.error(f"Supabase Sync Error: {e}")
            
    # 2. Attempt Convex Sync
    if convex_client:
        try:
            # FIXED: Changed 'lessons:insert' to 'lessons:createLesson' to match your schema
            convex_client.mutation("lessons:createLesson", {
                "title": topic,
                "cultural_logic": level,
                "content": str(content)
            })
            c_ok = True
        except Exception as e:
            st.sidebar.warning(f"Convex Sync Note: {e}")
            
    return s_ok, c_ok

# --- PDF GENERATION ---
def create_pdf_bytes(raw_text):
    # 1. Prepare Text
    reshaped_text = reshape(raw_text)
    bidi_text = get_display(reshaped_text)
    sections = bidi_text.split("###")
    
    # 2. Build HTML with Page Breaks
    formatted_html = ""
    for s in sections:
        if s.strip():
            # 'page-break-after' ensures each language starts on a new page
            formatted_html += f'<div style="page-break-after:always; margin-top: 20px;">'
            formatted_html += f'{s.strip()}</div>'
    
    # 3. The "Magic" Font CSS
    # This tells the PDF to look for the files you have in your GitHub/HuggingFace folder
    style = """
    <style>
        @font-face {
            font-family: 'ArabicFont';
            src: url('NotoSansArabic-Regular.ttf');
        }
        @font-face {
            font-family: 'MalteseFont';
            src: url('NotoSansMaltese-Regular.ttf');
        }
        @page { size: A4; margin: 2cm; }
        body { 
            font-family: 'ArabicFont', 'MalteseFont', sans-serif; 
            font-size: 11pt; 
            line-height: 1.6; 
        }
    </style>
    """
    
    html_template = f"<html><head>{style}</head><body>{formatted_html}</body></html>"
    result = io.BytesIO()
    pisa.CreatePDF(io.BytesIO(html_template.encode("UTF-8")), dest=result)
    return result.getvalue()

# --- MAIN APP ---
def main():
    st.set_page_config(page_title="ISW Polyglot-Nexus", page_icon="🏫", layout="wide")
    
    with st.sidebar:
        st.image("https://www.is-westpfalz.de/wp-content/uploads/logo-is-westpfalz-200x70.png", use_container_width=True)
        st.info("🚀 **Project Portfolio: ISW Edition**")
        show_advanced = st.checkbox("Show Engine Analytics", value=True)
        st.caption("Architected by Ben Mahmoud | 2026")

    st.title("🏫 Polyglot-Nexus")
    st.subheader("Cambridge International Education • Semantic Logic Adapter")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        level = st.selectbox("Select Cambridge Pathway:", ["Primary", "Lower Secondary", "IGCSE", "A Level"])
    with col2:
        topic = st.text_input("Computer Science Topic:", placeholder="e.g. Logic Gates")

    if st.button("Generate Cultural Logic", use_container_width=True):
        if topic:
            with st.spinner("Executing Semantic Mapping..."):
                try:
                    # 1. AI Generation
                    lesson_content = polyglot_nexus_engine(topic, level)
                    
                    # 2. TRAFFIC LIGHT CLOUD SYNC
                    with st.status("Initiating Dual-Database Sync...", expanded=True) as status:
                        st.write("Handshaking with Supabase & Convex...")
                        s_ok, c_ok = save_lesson_to_db(topic, level, lesson_content)
                        
                        if s_ok and c_ok:
                            status.update(label="✅ Full Success: Supabase & Convex Synced", state="complete")
                        elif s_ok and not c_ok:
                            status.update(label="⚠️ Partial Success: Saved to Supabase (Convex Failed)", state="complete")
                        elif c_ok and not s_ok:
                            status.update(label="⚠️ Partial Success: Saved to Convex (Supabase Failed)", state="complete")
                        else:
                            status.update(label="❌ Sync Failed: Both Databases Offline", state="error")

                    # 3. PDF Preparation
                    pdf_bytes = create_pdf_bytes(str(lesson_content))
                    st.download_button("📥 Download Lesson Notes (PDF)", pdf_bytes, f"{topic}_Notes.pdf", "application/pdf")

                    # 4. Content Display
                    if show_advanced:
                        st.markdown("### 📊 Lesson Analytics")
                        m1, m2, m3 = st.columns(3)
                        m1.metric("Cognitive Depth", "Expert" if level == "A Level" else "Standard")
                        m2.metric("Linguistic Frameworks", "7 Languages", "Verified")
                        m3.metric("PDF Encoding", "UTF-8", "RTL Active")

                    languages = ["ENGLISH", "DEUTSCH", "FRANÇAIS", "ITALIANO", "ESPAÑOL", "العربية", "MALTI"]
                    for lang in languages:
                        with st.expander(f"⬜ {lang} Perspective"):
                            search_tag = f"### {lang}"
                            if search_tag in str(lesson_content):
                                content_slice = str(lesson_content).split(search_tag)[1].split("###")[0]
                                st.markdown(content_slice.strip())

                except Exception as e:
                    st.error(f"❌ System Error: {e}")
        else:
            st.warning("Input required: Please enter a topic to begin.")

if __name__ == "__main__":
    main()
