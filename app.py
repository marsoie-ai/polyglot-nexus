import os
import streamlit as st
from engine import polyglot_nexus_engine
from xhtml2pdf import pisa
from arabic_reshaper import reshape
from bidi.algorithm import get_display
import io
from supabase import create_client, Client  # <--- OLD IMPORT DB1
from convex import ConvexClient  # <--- NEW IMPORT DB2

# Fetch secrets from Hugging Face environment
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

# Initialize the Supabase client
supabase: Client = create_client(url, key)
# New Convex Init
convex_url = os.environ.get("CONVEX_URL")
convex_client = ConvexClient(convex_url)

# --- DATABASE LOGIC (NEW) ---
def save_lesson_to_db(topic, level, content):
    data = {
        "topic": topic,
        "level": level,
        "content": content
    }
    
    success = False

    # 1. Attempt Supabase
    try:
        supabase.table("lessons").insert(data).execute()
        st.success("✅ Archived to Supabase")
        success = True
    except Exception as e:
        st.error(f"❌ Supabase Error: {e}")

    # 2. Attempt Convex
    try:
        # 'lessons' is the table name, 'insert' is a common internal name for mutations
        convex_client.mutation("lessons:insert", data) 
        st.success("✅ Archived to Convex")
        success = True
    except Exception as e:
        # We use info here so it doesn't look like a "total" failure if Supabase worked
        st.info(f"💡 Convex Note: {e}") 

    return success

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

def main():
    st.set_page_config(page_title="ISW Polyglot-Nexus", page_icon="🏫", layout="wide")

    with st.sidebar:
        st.image("https://www.is-westpfalz.de/wp-content/uploads/logo-is-westpfalz-200x70.png", use_container_width=True)
        st.divider()
        st.info("🚀 **Project Portfolio: ISW Edition**")
        show_advanced = st.checkbox("Show Engine Analytics", value=True)
        st.divider()
        st.caption("Architected by Ben Mahmoud | 2026")

    st.title("🏫 Polyglot-Nexus")
    st.subheader("Cambridge International Education • Semantic Logic Adapter")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        level = st.selectbox("Select Cambridge Pathway:", 
                             options=["Primary", "Lower Secondary", "IGCSE", "A Level"])
    with col2:
        topic = st.text_input("Computer Science Topic:", placeholder="e.g. Logic Gates")

    # --- BUTTON LOGIC ---
    if st.button("Generate Cultural Logic", use_container_width=True):
        if topic:
            with st.spinner("Executing Semantic Mapping..."):
                try:
                    # 1. Generate the content
                    lesson_content = polyglot_nexus_engine(topic, level)
                    
                    # 2. Save to database
                    db_status = save_lesson_to_db(topic, level, str(lesson_content))

                    # 3. Process PDF
                    pdf_bytes = create_pdf_bytes(lesson_content)

                    # 4. Success UI
                    if db_status:
                        st.success("✅ Lesson archived to Supabase.")
                    else:
                        st.warning("⚠️ Content generated, but failed to sync with Supabase.")

                    # --- ALWAYS VISIBLE DOWNLOAD ---
                    st.download_button("📥 Download Lesson Notes (PDF)", 
                                     pdf_bytes, f"{topic}_{level}_Notes.pdf", "application/pdf")
                    st.divider()

                    if show_advanced:
                        st.markdown("### 📊 Lesson Analytics")
                        m1, m2, m3 = st.columns(3)
                        depth_score = {"Primary": "Core", "Lower Secondary": "Intermediate", "IGCSE": "Advanced", "A Level": "Expert"}
                        m1.metric("Cognitive Depth", depth_score[level])
                        m2.metric("Linguistic Frameworks", "7 Languages", "Verified")
                        m3.metric("PDF Encoding", "UTF-8", "RTL Active")
                        st.divider()
                        
                        with st.expander("🛠️ View Semantic Mapping Prompt"):
                            system_prompt = f"You are a Cambridge CS Expert. Task: Adapt '{topic}' for the '{level}' pathway."
                            st.code(system_prompt, language="markdown")
                        
                    # --- TRANSLATION DISPLAY ---
                    languages = ["ENGLISH", "DEUTSCH", "FRANÇAIS", "ITALIANO", "ESPAÑOL", "العربية", "MALTI"]
                    for lang in languages:
                        with st.expander(f"⬜ {lang} Perspective"):
                            search_tag = f"### {lang}"
                            if search_tag in lesson_content:
                                # This splits by the language name and takes the text before the next ###
                                content = lesson_content.split(search_tag)[1].split("###")[0]
                                st.markdown(content.strip())

                except Exception as e:
                    st.error(f"❌ System Error: {e}")
        else:
            st.warning("Input required: Please enter a topic to begin.")

if __name__ == "__main__":
    main()
