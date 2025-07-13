# 📝 Studysheet Composer Bot

Studysheet Composer Bot is a smart Streamlit app that transforms long technical blogs or tutorials into clean, compact one-page study sheets — ideal for quick revision and focused learning. Powered by [Agno](https://github.com/agno-agi/agno) and OpenAI, it supports customizable tone and focus types to fit your personal study needs.



## Folder Structure

```
Studysheet-Composer-Bot/
├── studysheet-composer-bot.py
├── README.md
└── requirements.txt
```

* **studysheet-composer-bot.py**: The main Streamlit application.
* **requirements.txt**: Required Python packages.
* **README.md**: This documentation file.



## Features

* **Paste Any Blog or Tutorial URL**
  Quickly summarize any technical blog or tutorial into a dense, single-page learning resource.

* **Choose Focus & Tone**
  Customize the study sheet to emphasize key concepts, step-by-step instructions, or summary points — in a formal, friendly, or neutral tone.

* **Compact, Markdown-Formatted Output**
  Each sheet follows a strict layout policy:

  * No filler or fluff
  * No diagrams or closing lines
  * Dense bullet points, numbered steps, or quick reference tables
  * Designed for \~600–800 words

* **Download as Markdown File**
  Instantly download the generated study sheet for offline revision or sharing.

* **Clean Streamlit UI**
  Simple layout with two columns — one for link input and one for your preferences.



## Prerequisites

* Python 3.11 or higher
* An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))



## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/akash301191/Studysheet-Composer-Bot.git
   cd Studysheet-Composer-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:

   ```bash
   streamlit run studysheet-composer-bot.py
   ```

2. **In your browser**:

   * Add your OpenAI API key in the sidebar.
   * Paste the blog/tutorial URL.
   * Choose your study preferences (focus + tone).
   * Click **📝 Generate Study Sheet**.
   * Download the output as a `.md` file.



## Code Overview

* **`render_sidebar()`**:
  Stores and manages the OpenAI API key in Streamlit session state.

* **`render_studysheet_preferences()`**:
  Captures the blog or tutorial link and user preferences (focus area and tone).

* **`generate_study_sheet()`**:

  * Creates a `Studysheet Generator` agent using the OpenAI `o3-mini` model via Agno.
  * Summarizes the blog content into a dense, structured, Markdown-formatted one-page study sheet based on user preferences.
  * Applies strict constraints: no diagrams, no summaries, no sign-offs, and no meta-description.

* **`main()`**:
  Handles layout, renders UI components, captures inputs, manages session state, triggers study sheet generation, and enables Markdown file download.



## Contributions

Contributions are welcome!
Feel free to fork the repo, suggest features, report bugs, or open a pull request. Please ensure your changes are clean, tested, and in line with the app’s minimal and educational goals.