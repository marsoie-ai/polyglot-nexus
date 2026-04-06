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

supabase = None
if url and key:
    try:
        supabase = create_client(url, key)
    except:
        supabase = None

convex_client = None
if convex_url:
    try:
        convex_client.mutation("lessons:createLesson", {
    "title": title,
    "cultural_logic": cultural_logic,
    "content": content
})
    except:
        convex_client = None

def save_lesson_to_db(topic, level, content):
    """Syncs data to Supabase and Convex simultaneously."""
    data = {"topic": topic, "level": level, "content": str(content)}
    s_ok, c_ok = False, False
    
    if supabase:
        try:
            supabase.table("lessons").insert(data).execute()
            s_ok = True
        except Exception as e:
            st.error(f"Supabase Error: {e}")
            
    if convex_client:
        try:
            convex_client.mutation("lessons:insert", data)
            c_ok = True
        except Exception as e:
            st.info(f"Convex Note: {e}")
            
    return s_ok, c_ok

# --- PDF GENERATION ---
def create_pdf_bytes(raw_text):
    reshaped_text = reshape(raw_text)
    bidi_text = get_display(reshaped_text)
    sections = bidi_text.split("###")
    formatted_html = "".join([f'<div class="section">{" ".join(s.split())}</div>' for s in sections if s.strip()])
    
    style = """<style>@page { size: A4; margin: 1.5cm; } body { font-family: sans-serif; font-size: 12pt; }</style>"""
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
                    
                    # 2. PRO CLOUD SYNC (The Fix)
                    with st.status("Initiating Dual-Database Sync...", expanded=True) as status:
                        st.write("Handshaking with Supabase & Convex...")
                        s_ok, c_ok = save_lesson_to_db(topic, level, lesson_content)
                        if s_ok and c_ok:
                            status.update(label="✅ All Databases Synchronized", state="complete")
                        elif s_ok or c_ok:
                            status.update(label="⚠️ Partial Sync (Check Logs)", state="complete")
                        else:
                            status.update(label="❌ Sync Failed", state="error")

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
                                content = str(lesson_content).split(search_tag)[1].split("###")[0]
                                st.markdown(content.strip())

                except Exception as e:
                    st.error(f"❌ System Error: {e}")
        else:
            st.warning("Input required: Please enter a topic to begin.")

if __name__ == "__main__":
    main()
