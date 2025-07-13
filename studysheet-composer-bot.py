import tempfile
import streamlit as st

from agno.agent import Agent
from agno.models.openai import OpenAIChat

from textwrap import dedent

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    st.sidebar.markdown("---")

def render_studysheet_preferences():
    st.markdown("---")
    col1, col2 = st.columns(2)

    # Column 1: Blog or Tutorial Link
    with col1:
        st.subheader("🔗 Paste Blog or Tutorial Link")
        blog_link = st.text_input(
            "Enter the URL of the blog or tutorial you'd like to summarize",
            placeholder="https://example.com/your-blog-post"
        )

    # Column 2: User Preferences
    with col2:
        st.subheader("⚙️ Sheet Preferences")

        focus_type = st.selectbox(
            "What should the study sheet emphasize?",
            [
                "Key Concepts & Definitions",
                "Step-by-Step Instructions",
                "Summary + Key Points"
            ]
        )

        tone = st.selectbox(
            "Choose your preferred tone",
            [
                "Formal & Academic",
                "Friendly & Conversational",
                "Neutral & Balanced"
            ]
        )

    return {
        "blog_link": blog_link,
        "focus_type": focus_type,
        "tone": tone
    }

def generate_study_sheet(user_studysheet_preferences):
    blog_link = user_studysheet_preferences["blog_link"]
    focus_type = user_studysheet_preferences["focus_type"]
    tone = user_studysheet_preferences["tone"]

    study_sheet_generator = Agent(
        name="Studysheet Generator",
        model=OpenAIChat(id="o3-mini", api_key=st.session_state.openai_api_key),
        role="Generates a compact, high-density, one-page study sheet from a blog or tutorial, tailored to the user's learning focus and tone preference.",
        description=dedent("""
            You are a study sheet generator. You are given:
            1. A blog or tutorial URL that the user wants summarized.
            2. The user’s chosen focus (e.g., key concepts, steps, or summary).
            3. The desired tone (e.g., academic, friendly, or neutral).

            Your task is to generate a structured, markdown-formatted study sheet that condenses all essential information into a tight, efficient format.
        """),
        instructions=[
            "Start the document with: ## 📝 Study Sheet",
            "",
            "- Immediately begin with content. **Do not include introductions, overviews, or descriptions of the study sheet itself.**",
            "",
            "- Dynamically decide appropriate section headings based on the content. Use only what’s relevant from the source blog/tutorial.",
            "- Use space-efficient formatting:",
            "   - Bullet points",
            "   - Numbered steps",
            "   - Markdown tables (if useful)",
            "   - Blockquotes for definitions",
            "   - Use markdown icons (✅ ⚠️ 💡 etc.) to enhance scannability",
            "",
            "- **Be concise**: Use short phrases or sentence fragments where possible. Avoid long paragraphs.",
            "",
            "- If including code or formulas, keep them brief and directly relevant.",
            "",
            "- Match the tone to the user’s request (academic, friendly, or neutral), but do not label the tone or describe it.",
            "",
            "- Strictly prohibit any reference to diagrams or visuals of any kind. Do NOT:",
            "   - Mention diagrams, images, visualizations, or illustrations.",
            "   - Include headers like '📌 Diagram Suggestion'.",
            "   - Describe what a diagram would show.",
            "   - Suggest the reader visualize or imagine a diagram.",
            "",
            "- Also prohibit:",
            "   - Closing remarks, summaries, or motivational lines.",
            "   - Any statements about what was covered in the study sheet.",
            "",
            "- Limit the sheet to one page (~600–800 words). Prioritize density, clarity, and compact structure.",
            "",
            "Output only the **final Markdown-formatted study sheet**. Do not explain your process or include helper content."
        ],
        markdown=True,
        add_datetime_to_instructions=True
    ) 

    final_prompt = f"""
    Blog or Tutorial Link: {blog_link}
    Focus Preference: {focus_type}
    Tone Preference: {tone}

    Generate a markdown-formatted study sheet from the blog content using the above preferences. If helpful, suggest locations for appropriate diagrams.
    """

    final_study_sheet = study_sheet_generator.run(final_prompt).content

    return final_study_sheet
    
def main() -> None:
    # Page config
    st.set_page_config(page_title="Studysheet Composer Bot", page_icon="📝", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>📝 Studysheet Composer Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to Studysheet Composer Bot — a smart Streamlit application that transforms blog or tutorial links into concise, one-page study sheets, helping you grasp key concepts quickly and revise with ease.",
        unsafe_allow_html=True
    )

    render_sidebar()
    user_studysheet_preferences = render_studysheet_preferences()

    st.markdown("---")

    if st.button("📝 Generate Study Sheet"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not user_studysheet_preferences["blog_link"]:
            st.error("Please paste a blog or tutorial URL.")
        else:
            with st.spinner("Generating your study sheet ..."):
                study_sheet = generate_study_sheet(user_studysheet_preferences)
                st.session_state.study_sheet = study_sheet

    if "study_sheet" in st.session_state:
        st.markdown(st.session_state.study_sheet, unsafe_allow_html=True)
        st.markdown("---")

        st.download_button(
            label="📥 Download Study Sheet",
            data=st.session_state.study_sheet,
            file_name="study_sheet.md",
            mime="text/markdown"
        )




if __name__ == "__main__":
    main()

