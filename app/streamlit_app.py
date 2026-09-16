# import streamlit as st
# import pandas as pd
# from llm import generate_sql,check_clarification
# from database import execute_query
# st.title("Intelligent Text-to-SQL Assistant")
# st.write("Ask a question about your database.")
# if "pending_question" not in st.session_state:
#     st.session_state.pending_question=None
# if "clarification_question" not in st.session_state:
#     st.session_state.clarification_question=None
# question=st.text_input("Enter your question: ")
# if st.button("Generate SQL"):
#     if question:
#         try:
#             clarification=check_clarification(question)
#             if clarification.needs_clarification:
#                 st.session_state.pending_question=question
#                 st.session_state.clarification_question=clarification.question
#                 st.rerun();

#                 if st.button("Continue"):
#                     if clarification_answer:
#                         final_question=question+ " "+clarification_answer
#                         sql=generate_sql(final_question)
#                         st.subheader("Generated SQL")
#                         st.code(sql,language="sql")
#                         columns,results=execute_query(sql)
#                         st.subheader("Query Result")
#                         df=pd.DataFrame(results,columns=columns)
#                         if df.empty:
#                             st.info("No result found")
#                         else:
#                             st.dataframe(df,use_container_width=True)
#                     else:
#                         st.warning("Please provide an answer.")
        

    

                        

#             else:
#                 sql=generate_sql(question)
#                 st.subheader("Generated SQL")
                
#                 st.code(sql,language="sql")
                
#                 columns,results=execute_query(sql)
#                 st.subheader("Query Result")
                
#                 df=pd.DataFrame(results,columns=columns)
#                 if df.empty:
#                     st.info("No result found.")
#                 else:
#                     st.dataframe(df,use_container_width=True)
                
                
#         except Exception as e:
            
#             st.error("Something went wrong.")
#             st.write(str(e))

#     else:
#         st.warning("Please enter a question.")


import streamlit as st
import pandas as pd

from llm import generate_sql, check_clarification
from database import load_csv_to_mysql,get_table_schema
from database import execute_query
st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(135deg, #e8c4d8 0%, #d8c8e6 100%);
}

/* Main title */
.main-title {
    font-size: 38px;
    font-weight: 700;
    text-align: center;
    color: #5b3158;
    margin-bottom: 5px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 17px;
    color: #7b6b78;
    margin-bottom: 30px;
}

/* Input box */
.stTextInput > div > div > input {
    border: 2px solid #f3c6d8;
    border-radius: 12px;
    padding: 12px;
    background-color: #ffffff;
}

/* Input focus */
.stTextInput > div > div > input:focus {
    border-color: #d98caf;
    box-shadow: 0 0 8px rgba(217, 140, 175, 0.25);
}

/* Buttons */
.stButton > button {
    background-color:  #d46a9a;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 24px;
    font-weight: 600;
}

/* Button hover */
.stButton > button:hover {
    background-color: #d98caf;
    color: white;
}

/* Code block */
.stCodeBlock {
    border-radius: 12px;
}

/* Warning / clarification */
.stAlert {
    border-radius: 12px;
}
.choose-title {
    font-size: 20px;
    font-weight: 600;
    color: #5b3158;
    text-align: center;
    margin-top: 10px;
    margin-bottom: 18px;
    width: 100%;
}

</style>
""", unsafe_allow_html=True)
st.markdown(
    '<div class="main-title">🤖 Intelligent Text-to-SQL Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Ask questions in natural language and get SQL results instantly.</div>',
    unsafe_allow_html=True
)

# Session state
if "mode" not in st.session_state:
    st.session_state.mode = None
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

if "clarification_question" not in st.session_state:
    st.session_state.clarification_question = None

if "uploaded_schema" not in st.session_state:
    st.session_state.uploaded_schema = None

# question = st.text_input(
#     "Ask your question",
#     placeholder="e.g. Which customer spent the most?"
# )
# =========================
# HOME SCREEN
# =========================

if st.session_state.mode is None:

    st.markdown(
    """
    <div class="choose-title">
        Choose how you want to use the assistant
    </div>
    """,
    unsafe_allow_html=True
)
  

    st.write("")

    # Center the cards
    left_space, col1, col2, right_space = st.columns(
        [1.2, 2.8, 2.8, 1.2],
        gap="medium"
    )

    # =========================
    # DEMO CARD
    # =========================

    with col1:

        with st.container(border=True):

            st.markdown(
                """
                <div style="
                    text-align:center;
                    font-size:38px;
                    margin-bottom:10px;
                ">
                    🗄️
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div style="
                    text-align:center;
                    font-size:22px;
                    font-weight:700;
                    color:#5b3158;
                    margin-bottom:8px;
                ">
                    Try Demo Database
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div style="
                    text-align:center;
                    color:#756875;
                    font-size:14px;
                    line-height:1.5;
                    min-height:55px;
                ">
                    Explore customers, products and orders
                    using our ready-to-use sample database.
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")

            if st.button(
                "Explore Demo →",
                key="demo_button",
                use_container_width=True
            ):
                st.session_state.mode = "demo"
                st.rerun()

    # =========================
    # UPLOAD CARD
    # =========================

    with col2:

        with st.container(border=True):

            st.markdown(
                """
                <div style="
                    text-align:center;
                    font-size:38px;
                    margin-bottom:10px;
                ">
                    📁
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div style="
                    text-align:center;
                    font-size:22px;
                    font-weight:700;
                    color:#5b3158;
                    margin-bottom:8px;
                ">
                    Upload Your Data
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div style="
                    text-align:center;
                    color:#756875;
                    font-size:14px;
                    line-height:1.5;
                    min-height:55px;
                ">
                    Upload your CSV file and ask questions
                    about your own dataset.
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")

            if st.button(
                "Upload CSV →",
                key="upload_button",
                use_container_width=True
            ):
                st.session_state.mode = "upload"
                st.rerun()
    # =========================
# DEMO MODE
# =========================

if st.session_state.mode == "demo":

    st.subheader("🗄️ Demo Database")

    st.write("Ask questions about customers, products and orders.")

    question = st.text_input(
        "Ask your question",
        placeholder="e.g. Which customer spent the most?"
    )

    if st.button("Generate SQL", key="demo_generate"):

        if question:

            try:

                clarification = check_clarification(question)

                if clarification.needs_clarification:

                    st.session_state.pending_question = question
                    st.session_state.clarification_question = clarification.question

                    st.rerun()

                else:

                    sql = generate_sql(question)

                    st.subheader("Generated SQL")
                    st.code(sql, language="sql")

                    columns, results = execute_query(sql)

                    st.subheader("Query Result")

                    df = pd.DataFrame(results, columns=columns)

                    if df.empty:
                        st.info("No result found.")
                    else:
                        st.dataframe(df, use_container_width=True)

            except Exception as e:

                st.error("Something went wrong.")
                st.write(str(e))

        else:

            st.warning("Please enter a question.")

    if st.button("← Back to Home", key="demo_back"):

        st.session_state.mode = None
        st.session_state.pending_question = None
        st.session_state.clarification_question = None

        st.rerun()


# =========================
# UPLOAD MODE
# =========================

if st.session_state.mode == "upload":

    st.subheader("📁 Upload Your Data")

    uploaded_file = st.file_uploader(
        "Upload your CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        st.success("CSV uploaded successfully!")

        st.subheader("📊 Data Preview")

        st.dataframe(
            df.head(),
            use_container_width=True
        )

        load_csv_to_mysql(df)

        st.success(
            "Your data has been loaded into MySQL successfully!"
        )

        columns = get_table_schema()

        st.session_state.uploaded_schema = columns

        st.subheader("📋 Uploaded Data Schema")

        st.write(columns)
        question = st.text_input(
        "Ask your question",
        placeholder="e.g. How many patients have COVID?"
    )

    if st.button("Generate SQL", key="upload_generate"):

        if question:

            try:

                clarification = check_clarification(
                    question,
                    st.session_state.uploaded_schema
                )

                if clarification.needs_clarification:

                    st.session_state.pending_question = question
                    st.session_state.clarification_question = clarification.question

                    st.rerun()

                else:

                    sql = generate_sql(
                        question,
                        st.session_state.uploaded_schema
                    )

                    st.subheader("Generated SQL")
                    st.code(sql, language="sql")

                    columns, results = execute_query(sql)

                    st.subheader("Query Result")

                    df = pd.DataFrame(
                        results,
                        columns=columns
                    )

                    if df.empty:
                        st.info("No result found.")
                    else:
                        st.dataframe(
                            df,
                            use_container_width=True
                        )

            except Exception as e:

                st.error("Something went wrong.")
                st.write(str(e))

        else:

            st.warning("Please enter a question.")

    if st.button("← Back to Home", key="upload_back"):

        st.session_state.mode = None
        st.session_state.pending_question = None
        st.session_state.clarification_question = None
        st.session_state.uploaded_schema = None

        st.rerun()
# st.subheader("📁 Upload Your Data")

# uploaded_file = st.file_uploader(
#     "Upload your CSV file",
#     type=["csv"]
# )

# if uploaded_file is not None:
#         df = pd.read_csv(uploaded_file)

#         st.success("CSV uploaded successfully!")

#         st.subheader("📊 Data Preview")
#         st.dataframe(df.head(), use_container_width=True)

#         load_csv_to_mysql(df)

#         st.success("Your data has been loaded into MySQL successfully!")
#         columns = get_table_schema()
#         st.session_state.uploaded_schema=columns
#         st.subheader("📋 Uploaded Data Schema")
#         st.write(columns)
# # Generate SQL
# if st.button("Generate SQL"):

#     if question:

#         try:
#             clarification = check_clarification(question, st.session_state.uploaded_schema)

#             if clarification.needs_clarification:

#                 # Save question
#                 st.session_state.pending_question = question
#                 st.session_state.clarification_question = clarification.question

#                 st.rerun()

#             else:

#                 sql = generate_sql(
#                     question,
#                     st.session_state.uploaded_schema)

#                 st.subheader("Generated SQL")
#                 st.code(sql, language="sql")

#                 columns, results = execute_query(sql)

#                 st.subheader("Query Result")

#                 df = pd.DataFrame(results, columns=columns)

#                 if df.empty:
#                     st.info("No result found.")
#                 else:
#                     st.dataframe(df, use_container_width=True)

#         except Exception as e:

#             st.error("Something went wrong.")
#             st.write(str(e))

#     else:

#         st.warning("Please enter a question.")


# =========================
# CLARIFICATION SECTION
# =========================

if st.session_state.pending_question:

    st.warning("Could you clarify:")

    st.write(
        st.session_state.clarification_question
    )

    clarification_answer = st.text_input(
        "Your answer:",
        key="clarification_answer"
    )

    if st.button("Continue", key="continue_button"):

        if clarification_answer:

            try:

                final_question = (
                    st.session_state.pending_question
                    + " "
                    + clarification_answer
                )

                if st.session_state.mode == "demo":

                    sql = generate_sql(final_question)

                else:

                    sql = generate_sql(
                        final_question,
                        st.session_state.uploaded_schema
                    )

                st.subheader("Generated SQL")

                st.code(
                    sql,
                    language="sql"
                )

                columns, results = execute_query(sql)

                st.subheader("Query Result")

                df = pd.DataFrame(
                    results,
                    columns=columns
                )

                if df.empty:

                    st.info("No result found.")

                else:

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                st.session_state.pending_question = None
                st.session_state.clarification_question = None

            except Exception as e:

                st.error("Something went wrong.")
                st.write(str(e))

        else:

            st.warning("Please provide an answer.")