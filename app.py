import streamlit as st
from engine import polyglot_nexus_engine

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Polyglot-Nexus", page_icon="🚀")

# 2. THE USER INTERFACE (UI)
st.title("🚀 Polyglot-Nexus")
st.subheader("Multilingual Semantic Logic Adapter")
st.markdown("Adapt complex CS concepts into 6 cultural frameworks.")

# 3. USER INPUT
topic = st.text_input("Enter a Computer Science topic (e.g., Recursion, Big O, Linked Lists):")

if st.button("Generate Cultural Logic"):
    if topic:
        with st.spinner("Adapting logic for 6 cultures..."):
            try:
                # Call the engine from your other file
                response = polyglot_nexus_engine(topic)
                st.markdown("---")
                st.markdown(response)
                st.success("✅ Adaptation Complete")
            except Exception as e:
                st.error(f"An error occurred. Make sure your API key is set! Error: {e}")
    else:
        st.warning("Please enter a topic first.")

# 4. FOOTER
st.sidebar.info("Developed by Ben Mahmoud | 2026")
