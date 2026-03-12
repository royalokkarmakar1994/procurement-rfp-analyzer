import streamlit as st
import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# --- Page Config ---
st.set_page_config(page_title="RFP Analyzer", page_icon="📄", layout="centered")
st.title("📄 Intelligent Procurement RFP Analyzer")
st.write("Upload a vendor Request for Proposal (RFP) to instantly extract compliance clauses and structure pricing tables.")

# --- API Key Input ---
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

# --- File Uploader ---
uploaded_file = st.file_uploader("Upload Vendor RFP (PDF)", type="pdf")

if uploaded_file and api_key:
    if st.button("Analyze RFP"):
        with st.spinner("Parsing document and extracting clauses..."):
            try:
                # 1. Save uploaded file temporarily for PyPDFLoader
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name

                # 2. Load PDF using LangChain
                loader = PyPDFLoader(tmp_file_path)
                pages = loader.load()
                document_text = "\n".join([page.page_content for page in pages])

                # 3. Setup LLM and Prompt
                os.environ["OPENAI_API_KEY"] = api_key
                llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

                prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are an expert enterprise procurement manager. Extract key information from the provided vendor RFP."),
                    ("user", """
                    Please analyze the following RFP text and provide:
                    1. **Critical SLA Risks:** A bulleted list of any Service Level Agreement risks or strict compliance clauses.
                    2. **Pricing Structure:** Extract all pricing, tiering, or cost data and format it strictly as a Markdown table.
                    3. **Summary:** A 2-sentence executive summary of the vendor's proposal.

                    RFP Text:
                    {text}
                    """)
                ])

                # 4. Execute Chain
                chain = prompt | llm
                response = chain.invoke({"text": document_text[:15000]})

                # 5. Display Results
                st.success("Analysis Complete!")
                st.markdown("### 📊 Extraction Results")
                st.markdown(response.content)

                # Cleanup temp file
                os.remove(tmp_file_path)

            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
elif uploaded_file and not api_key:
    st.warning("Please enter your OpenAI API Key in the sidebar to proceed.")
