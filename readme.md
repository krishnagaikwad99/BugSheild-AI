# 🛡️ BugShield AI — AI-Powered Software Bug Detection and Testing

BugShield AI is a Python-based software testing application that combines **static code analysis, machine learning, and Agentic AI** to help developers identify potential bugs, understand code issues, and generate test cases.

The project provides an interactive Streamlit interface where users can upload Python files and receive code analysis, defect-risk estimates, AI-generated recommendations, and pytest test suggestions.

## 🚀 Features

- **Static Code Analysis:** Checks Python syntax and identifies code-quality issues using Python AST and Ruff.
- **Code Metrics:** Extracts lines of code, function count, class count, conditional statements, loops, and function arguments.
- **ML Defect-Risk Prediction:** Uses a Random Forest classifier to demonstrate defect-risk classification from extracted code features.
- **Agentic AI Assistant:** Uses Agno and Groq to explain potential bugs, recommend fixes, and generate pytest test cases.
- **Interactive Dashboard:** Displays findings and metrics through a Streamlit web interface.

## 🏗️ Technology Stack

- Python
- Streamlit
- Abstract Syntax Trees (AST)
- Ruff
- Pandas
- Scikit-learn
- Random Forest Classifier
- Agno
- Groq API
- Pytest (for generated test cases)

## 📂 Project Structure

```text
BugShield-AI/
├── app.py
├── analyzer.py
├── feature_extractor.py
├── train_model.py
├── bug_predictor.py
├── ai_agent.py
├── datasets/
│   └── defects.csv
├── models/
│   └── bug_model.pkl
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/BugShield-AI.git
cd BugShield-AI
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure the Groq API key

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key
```

Obtain your API key from [Groq Console](https://console.groq.com/keys).

**Never commit your `.env` file or publish your API key.**

### 5. Prepare the ML model

If the trained model file is not included in the repository, generate it using:

```bash
python train_model.py
```

Ensure `datasets/defects.csv` exists before running the training script.

### 6. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal.

## 🔍 How It Works

1. Upload a Python source file.
2. Run static code analysis to identify syntax and code-quality issues.
3. Extract code metrics using Python AST.
4. Estimate defect risk using the trained machine-learning model.
5. Request an AI-generated report with potential bugs, suggested fixes, and pytest test cases.

## ⚠️ Limitations

- The current ML dataset contains illustrative sample data. Its predictions and scores are not validated measures of real-world defect probability or model accuracy.
- AI-generated findings and test cases may be incorrect and require human review.
- Generated tests are suggestions; they are not automatically executed or guaranteed to pass.
- Uploaded code should be treated as untrusted input.

## 🔮 Future Enhancements

- Automated test execution in a secure, isolated environment.
- Downloadable testing reports.
- Improved defect prediction using verified, real-world datasets.
- AI-assisted code fixes with before-and-after comparisons.
- Support for additional programming languages.

## 👨‍💻 Author

**Krishna Gaikwad**

GitHub: https://github.com/krishnagaikwad99

---

*BugShield AI is an educational software testing project demonstrating the integration of static analysis, machine learning, and Agentic AI.*
