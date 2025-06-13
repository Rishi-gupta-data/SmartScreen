import streamlit as st  # Ensure Streamlit is imported
from backend import ATSBackend, BulkATSBackend  # Removed circular import
from dotenv import load_dotenv
import requests  # Ensure requests is imported if used
import logging  # Added for logging

# Load environment variables from .env file
load_dotenv()

# Streamlit Frontend
st.set_page_config(page_title="ATS Resume Expert", page_icon="📄", layout="wide")

# Custom styling
st.markdown("""
<style>
.stTextInput, .stTextArea, .stFileUploader, .stSelectbox {
    border-radius: 10px;
}
.stButton > button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
}
.stExpander {
    border: 1px solid #ddd;
    border-radius: 10px;
    background-color: #f9f9f9;
}
</style>
""", unsafe_allow_html=True)

class ATSFrontend:
    def __init__(self, bulk_backend, ats_backend):
        self.bulk_backend = bulk_backend
        self.ats_backend = ats_backend
        # Initialize session state
        if "uploaded_file" not in st.session_state:
            st.session_state.uploaded_file = None
        if "job_description" not in st.session_state:
            st.session_state.job_description = None
        if "mode" not in st.session_state:
            st.session_state.mode = None
        if "selected_section" not in st.session_state:
            st.session_state.selected_section = None

    def run(self):
        """Run the Streamlit application."""
        if st.session_state.mode is None:
            self.display_homepage()
        elif st.session_state.mode == "individual":
            if self.handle_file_upload():
                self.display_analysis()
        elif st.session_state.mode == "recruiter":
            self.handle_bulk_file_upload()

    def handle_file_upload(self):
        """Handle file upload and job description input with a Back to Home button."""
        col1, col2 = st.columns([8, 1])  # Align button to the right
        with col2:
            if st.button("🏠 Back to Home", key="back_home_individual"):
                st.session_state.mode = None  # Reset mode to go back to home
                st.rerun()

        st.sidebar.header("Upload Your Resume")
        uploaded_file = st.sidebar.file_uploader("Upload Resume (PDF)", type=["pdf"])

        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file
            st.sidebar.success("File uploaded successfully!")

        job_description = st.sidebar.text_area(
            "Job Description",
            placeholder="Paste the job description here...",
            height=150)
        if job_description:
            st.session_state.job_description = job_description

        if st.session_state.uploaded_file and st.session_state.job_description:
            if st.sidebar.button("Process Resume"):
                with st.spinner("Processing resume..."):
                    try:
                        # Extract text from the uploaded file correctly
                        resume_text = self.ats_backend.extract_text_from_pdf(st.session_state.uploaded_file)
                        self.ats_backend.set_job_description(st.session_state.job_description)
                        st.sidebar.success("Resume processed successfully!")
                        return True
                    except Exception as e:
                        st.sidebar.error(f"Error processing resume: {str(e)}")
        return False

    def display_analysis(self):
        """Display analysis results."""
        resume_text = self.ats_backend.extract_text_from_pdf(st.session_state.uploaded_file)
        
        # Log the extracted resume text for debugging
        logging.info(f"Extracted Resume Text: {resume_text}")  # Log the extracted text

        # Ensure resume_text is a string before passing it to analyze_resume
        if not isinstance(resume_text, str):
            st.error("Failed to extract text from the uploaded resume.")
            return

        # Now pass the extracted text to analyze_resume
        analysis = self.ats_backend.analyze_resume(resume_text, st.session_state.job_description)

        st.write("### Analysis Results:")

        # Create dropdowns for each section
        with st.expander("📊 Match Percentage"):
            st.write(f"**Match Percentage:** {analysis['Match Percentage']}")

        with st.expander("🔑 Found Keywords"):
            st.write(f"**Found Keywords:** {', '.join(analysis['Found Keywords'])}")

        with st.expander("❌ Missing Keywords"):
            st.write(f"**Missing Keywords:** {', '.join(analysis['Missing Keywords'])}")

        with st.expander("⭐ Key Strengths"):
            st.write(f"**Key Strengths:** {', '.join(analysis['Key Strengths'])}")

        with st.expander("🔍 Areas for Improvement"):
            st.write(f"**Areas for Improvement:** {', '.join(analysis['Areas for Improvement'])}")

        with st.expander("🎨 Resume Formatting & Optimization Tips"):
            st.write(f"**Resume Formatting & Optimization Tips:** {', '.join(analysis['Resume Formatting & Optimization Tips'])}")

    def display_homepage(self):
        """Display the ATS Home Page with selection buttons."""
        st.title("📑 Intelligent Applicant Tracking System (ATS)")
        st.markdown("Welcome to the ATS! Please select an option below:")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("For Individuals"):
                st.session_state.mode = "individual"
                st.rerun()

        with col2:
            if st.button("For Recruiters"):
                st.session_state.mode = "recruiter"
                st.rerun()

    def handle_bulk_file_upload(self):
        """Handle bulk file upload for recruiters with a Back to Home button."""
        col1, col2 = st.columns([8, 1])  # Align button to the right
        with col2:
            if st.button("🏠 Back to Home", key="back_home_recruiter"):
                st.session_state.mode = None  # Reset mode to go back to home
                st.rerun()

        st.sidebar.header("Upload Bulk Resumes")
        
        uploaded_file = st.sidebar.file_uploader("Upload ZIP file containing resumes", type=["zip"])

        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file
            st.sidebar.success("ZIP file uploaded successfully!")

            # Process the uploaded ZIP file
            try:
                self.bulk_backend.extract_text_from_zip(uploaded_file)
                st.success("Resumes extracted successfully!")
            except Exception as e:
                st.error(f"Error processing ZIP file: {str(e)}")

        job_description = st.sidebar.text_area(
            "Job Description",
            placeholder="Paste the job description here...",
            height=150)

        if uploaded_file and job_description:
            with st.spinner("Processing bulk resumes..."):
                try:
                    results_df = self.bulk_backend.process_bulk_resumes(job_description)  # Process resumes
                    st.write("### Results:")
                    st.dataframe(results_df)  # Display results in a table

                    # Allow users to download the report as a CSV file
                    csv = results_df.to_csv(index=False)
                    st.download_button(label="Download Report as CSV",
                                       data=csv,
                                       file_name="bulk_resume_report.csv",
                                       mime="text/csv")

                    st.sidebar.success("Bulk resumes processed successfully!")
                except Exception as e:
                    st.sidebar.error(f"Error processing bulk resumes: {str(e)}")
        return False

    def individual(self):
        """Handles individual resume analysis mode with an improved UI."""
        st.header("✨ Resume Analysis Toolkit")
        st.subheader("Unleash your potential with data-driven insights.")

        col1, col2 = st.columns([0.7, 0.3])  # Adjust ratios for layout

        with col1:
            uploaded_file = st.file_uploader(
                "📄 Upload Resume (PDF)", type=["pdf"], help="Only PDF files accepted."
            )
            job_description = st.text_area(
                "🎯 Job Description",
                placeholder="Paste the job description here...",
                height=200,
                help="Paste the job description to analyze your resume against it."
            )

        with col2:
            st.markdown("""
                ### Analysis Tips
                *   **Suitability:** How closely your resume matches the job description.
                *   **Keywords:** Words and phrases that hiring managers look for.
                *   **Formatting:** How well your resume is structured and presented.
                *   **Overall Review:** Strengths and weaknesses based on the information provided.
            """)

        if uploaded_file and job_description:
            try:
                # Set backend properties
                resume_text = self.ats_backend.extract_text_from_pdf(uploaded_file)
                self.ats_backend.resume_text = resume_text
                self.ats_backend.job_description = job_description

                # Perform analysis
                suitability_analysis = self.ats_backend.analyze_resume(resume_text, job_description)
                keyword_analysis = self.ats_backend.get_keyword_optimization()
                formatting_analysis = self.ats_backend.get_formatting_suggestions()
                resume_review = self.ats_backend.get_resume_analysis()

                st.success("✅ Analysis Complete!")
                st.subheader("🔍 Analysis Summary")
                st.info("Please review these insights carefully to improve your resume.")

                st.write(f"**Overall Match:** {suitability_analysis['Match Percentage']}")

                st.markdown(
                    f"""
                    <div style="background-color:#f0f2f6; padding:10px; border-radius:5px;">
                        **Suitability:** {suitability_analysis['Suitability']}
                        <br>
                        **Reason:** {suitability_analysis['Reason']}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                with st.expander("🔑 **Keyword Analysis - Optimize Your Content**"):
                    st.markdown(keyword_analysis)

                with st.expander("🎨 **Formatting Review - Make a Great First Impression**"):
                    st.markdown(formatting_analysis)

                with st.expander("⭐ **Overall Resume Review - Refine Your Strategy**"):
                    st.markdown(resume_review)

            except Exception as e:
                st.error(f"❌ Error processing resume: {str(e)}")

        else:
            st.info("⬆️ Please upload your resume and paste the job description to begin.")

def main():
    """Main function to run the Streamlit application."""
    try:
        # Initialize backend instances
        ats_backend = ATSBackend()
        bulk_backend = BulkATSBackend(ats_backend)
        
        # Initialize the frontend with the backend instances
        frontend = ATSFrontend(bulk_backend, ats_backend)
        
        # Run the frontend application
        frontend.run()
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")  # Handle exceptions

# Entry point of the application
if __name__ == "__main__":
    main()  # Call the main function

#    streamlit run app.py