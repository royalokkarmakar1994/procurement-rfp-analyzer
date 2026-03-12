# 📄 Intelligent Procurement RFP Analyzer

An AI-powered web application built with Streamlit and LangChain designed to automate the review of vendor Requests for Proposals (RFPs). 

## 🏗️ System Architecture
This tool leverages **Retrieval and Extraction** techniques to solve administrative bottlenecks in B2B procurement:
* **Frontend:** Streamlit for rapid UI prototyping.
* **Document Ingestion:** `PyPDFLoader` via LangChain to parse unstructured PDF text.
* **AI Engine:** OpenAI `gpt-4o-mini` with strict few-shot prompting to isolate compliance risks and force unstructured pricing data into clean Markdown tables.

## 🚀 How to Run Locally
1. Clone the repository: `git clone https://github.com/royalokkarmakar1994/procurement-rfp-analyzer.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the Streamlit server: `streamlit run app.py`

*Note: You will need an OpenAI API key to process documents.*
