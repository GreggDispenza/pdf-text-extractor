import streamlit as st
import pymupdf
from io import BytesIO

st.set_page_config(page_title="PDF Text Extractor", page_icon="📄")
st.title("📄 PDF Text Extractor")
st.write("Upload any PDF and extract text, count words, or download results!")

st.sidebar.header("About")
st.sidebar.info("This app extracts text from PDFs using PyMuPDF. Upload a PDF to get started!")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    pdf_bytes = uploaded_file.read()
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    
    st.success(f"✓ Successfully loaded: **{uploaded_file.name}**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Pages", len(doc))
    
    all_text = ""
    for page_num, page in enumerate(doc):
        all_text += f"\n--- Page {page_num + 1} ---\n"
        all_text += page.get_text()
    
    word_count = len(all_text.split())
    char_count = len(all_text)
    
    with col2:
        st.metric("Total Words", f"{word_count:,}")
    
    tab1, tab2, tab3 = st.tabs(["📝 Full Text", "📊 Statistics", "⚙️ Options"])
    
    with tab1:
        st.subheader("Extracted Text")
        st.text_area("Full content:", all_text, height=400)
    
    with tab2:
        st.subheader("Document Statistics")
        st.write(f"**Total Pages:** {len(doc)}")
        st.write(f"**Total Words:** {word_count:,}")
        st.write(f"**Total Characters:** {char_count:,}")
        st.write(f"**Average Words per Page:** {word_count // len(doc)}")
    
    with tab3:
        st.subheader("Extract Specific Pages")
        page_range = st.slider(
            "Select page range:",
            1, len(doc), (1, min(3, len(doc)))
        )
        
        if st.button("Extract Selected Pages"):
            selected_text = ""
            for page_num in range(page_range[0] - 1, page_range[1]):
                page = doc[page_num]
                selected_text += f"\n--- Page {page_num + 1} ---\n"
                selected_text += page.get_text()
            
            st.text_area("Selected pages text:", selected_text, height=300)
            
            st.download_button(
                label="💾 Download Selected Pages",
                data=selected_text,
                file_name=f"{uploaded_file.name}_pages_{page_range[0]}-{page_range[1]}.txt",
                mime="text/plain"
            )
    
    st.divider()
    st.download_button(
        label="💾 Download Full Text File",
        data=all_text,
        file_name=f"{uploaded_file.name}_extracted.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    doc.close()

else:
    st.info("👆 Upload a PDF file to get started!")
    
    with st.expander("ℹ️ How to use this app"):
        st.write("""
        1. Click 'Browse files' above
        2. Select any PDF from your computer
        3. View extracted text in the tabs
        4. Download results as a .txt file
        """)
