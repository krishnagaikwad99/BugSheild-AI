
import streamlit as st

from analyzer import analyze_code
from feature_extractor import extract_features
from bug_predictor import predict_defect_risk
from ai_agent import analyze_code as analyze_with_ai


# -------------------- PAGE CONFIGURATION --------------------

st.set_page_config(
    page_title="BugShield AI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ BugShield AI")
st.subheader("AI-Powered Software Bug Detection and Testing")

st.write(
    "Upload a Python file to analyze code quality, estimate defect risk, "
    "and generate AI-powered testing recommendations."
)

st.divider()


# -------------------- SESSION STATE --------------------

if "code" not in st.session_state:
    st.session_state.code = None

if "filename" not in st.session_state:
    st.session_state.filename = None

if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

if "features" not in st.session_state:
    st.session_state.features = None

if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "ai_report" not in st.session_state:
    st.session_state.ai_report = None


# -------------------- FILE UPLOAD --------------------

uploaded_file = st.file_uploader(
    "📂 Upload your Python file",
    type=["py"]
)


if uploaded_file is not None:

    try:
        code = uploaded_file.getvalue().decode("utf-8")

        # Reset stored results if a different file or new content is uploaded
        if (
            code != st.session_state.code
            or uploaded_file.name != st.session_state.filename
        ):
            st.session_state.code = code
            st.session_state.filename = uploaded_file.name
            st.session_state.analysis_results = None
            st.session_state.features = None
            st.session_state.prediction = None
            st.session_state.ai_report = None

        st.subheader("📄 Uploaded File")
        st.caption(f"Filename: {uploaded_file.name}")
        st.code(code, language="python")

        # -------------------- RUN ANALYSIS --------------------

        if st.button("🔍 Analyze Code", type="primary"):

            # Clear old results before analyzing
            st.session_state.analysis_results = None
            st.session_state.features = None
            st.session_state.prediction = None
            st.session_state.ai_report = None

            with st.spinner("Analyzing your Python code..."):

                # Static analysis
                try:
                    results = analyze_code(code)
                    st.session_state.analysis_results = results
                except Exception as error:
                    st.error(f"Static analysis failed: {error}")

                # Extract code metrics and predict defect risk
                try:
                    features = extract_features(code)
                    st.session_state.features = features

                    prediction = predict_defect_risk(features)
                    st.session_state.prediction = prediction

                except SyntaxError:
                    st.warning(
                        "Code metrics and ML prediction are unavailable "
                        "because the uploaded file has syntax errors."
                    )

                except FileNotFoundError:
                    st.error(
                        "Trained ML model not found. "
                        "Run `python train_model.py` first."
                    )

                except Exception as error:
                    st.error(f"ML prediction failed: {error}")

        # -------------------- DISPLAY STATIC ANALYSIS --------------------

        if st.session_state.analysis_results is not None:

            st.divider()
            st.subheader("🔍 Static Code Analysis Results")

            results = st.session_state.analysis_results

            if not results:
                st.info("No findings were returned by the analyzer.")

            for issue in results:

                severity = issue.get("severity", "Info")
                issue_type = issue.get("type", "Code")
                message = issue.get("message", "No description available.")

                if severity.lower() == "high":
                    st.error(f"🔴 {issue_type}: {message}")

                elif severity.lower() == "medium":
                    st.warning(f"🟡 {issue_type}: {message}")

                else:
                    st.info(f"ℹ️ {issue_type}: {message}")

        # -------------------- DISPLAY CODE METRICS --------------------

        if st.session_state.features is not None:

            features = st.session_state.features

            st.divider()
            st.subheader("📊 Code Metrics")

            metric_columns = st.columns(3)

            metric_columns[0].metric(
                "Lines of Code",
                features.get("lines_of_code", 0)
            )

            metric_columns[1].metric(
                "Functions",
                features.get("function_count", 0)
            )

            metric_columns[2].metric(
                "Classes",
                features.get("class_count", 0)
            )

            metric_columns = st.columns(3)

            metric_columns[0].metric(
                "If Statements",
                features.get("if_count", 0)
            )

            metric_columns[1].metric(
                "Loops",
                features.get("loop_count", 0)
            )

            metric_columns[2].metric(
                "Function Arguments",
                features.get("function_arguments", 0)
            )

            with st.expander("View all extracted features"):
                st.json(features)

        # -------------------- ML DEFECT-RISK PREDICTION --------------------

        if st.session_state.prediction is not None:

            prediction = st.session_state.prediction

            st.divider()
            st.subheader("🤖 ML Defect-Risk Prediction")

            predicted_label = prediction.get("prediction", 0)
            risk_score = prediction.get("risk_score", 0.0)
            is_demo_model = prediction.get("demo_model", False)

            # Support either a numeric class or a text label
            if isinstance(predicted_label, str):
                is_defect_prone = (
                    predicted_label.strip().lower()
                    in {"1", "true", "defect", "defect-prone", "defect prone"}
                )
            else:
                is_defect_prone = bool(predicted_label)

            if is_defect_prone:
                st.warning("⚠️ Model classification: Potentially defect-prone")
            else:
                st.success("✅ Model classification: Not defect-prone")

            st.metric(
                "Model Defect Score",
                f"{risk_score:.2%}"
                if isinstance(risk_score, (int, float))
                else str(risk_score)
            )

            if is_demo_model:
                st.info(
                    "This model uses illustrative sample data. "
                    "Its score is a demonstration, not a validated real-world "
                    "probability of defects."
                )

        # -------------------- AGENTIC AI ASSISTANT --------------------

        if st.session_state.features is not None:

            st.divider()
            st.subheader("🧠 Agentic AI Testing Assistant")

            st.write(
                "Ask the AI agent to explain potential bugs, recommend fixes, "
                "and generate pytest test cases for your code."
            )

            if st.button("✨ Ask AI to Analyze My Code"):

                with st.spinner(
                    "AI agent is reviewing your code and preparing a report..."
                ):

                    try:
                        ai_report = analyze_with_ai(
                            code=st.session_state.code,
                            findings=st.session_state.analysis_results or [],
                            features=st.session_state.features,
                            prediction=st.session_state.prediction
                        )

                        st.session_state.ai_report = ai_report

                    except Exception as error:
                        st.error(f"AI analysis failed: {error}")

            if st.session_state.ai_report:

                st.markdown("### 📝 AI Testing Report")
                st.markdown(st.session_state.ai_report)

                st.caption(
                    "AI-generated recommendations and tests have not "
                    "necessarily been executed or verified."
                )

    except UnicodeDecodeError:
        st.error(
            "Unable to read this file as UTF-8 text. "
            "Please upload a standard UTF-8 encoded Python file."
        )

else:
    st.info("👆 Upload a `.py` file to get started.")

    st.markdown(
        """
        **What BugShield AI can do**

        - 🔍 Detect syntax errors and static-analysis issues
        - 📊 Extract code complexity indicators
        - 🤖 Estimate defect risk using a machine-learning model
        - 🧠 Explain findings and suggest potential fixes with an AI agent
        - 🧪 Generate pytest test cases for further testing
        """
    )

st.divider()
st.caption("BugShield AI | ML + Agentic AI for Software Testing")
