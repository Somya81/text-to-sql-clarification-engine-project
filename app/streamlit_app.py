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
from database import execute_query
st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(135deg, #fff7fb 0%, #f8f5ff 100%);
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
    background-color: #e8a8c2;
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
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

if "clarification_question" not in st.session_state:
    st.session_state.clarification_question = None


question = st.text_input(
    "Ask your question",
    placeholder="e.g. Which customer spent the most?"
)

# Generate SQL
if st.button("Generate SQL"):

    if question:

        try:
            clarification = check_clarification(question)

            if clarification.needs_clarification:

                # Save question
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


# Clarification section
if st.session_state.pending_question:

    st.warning("Could you clarify:")

    st.write(st.session_state.clarification_question)

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

                sql = generate_sql(final_question)

                st.subheader("Generated SQL")
                st.code(sql, language="sql")

                columns, results = execute_query(sql)

                st.subheader("Query Result")

                df = pd.DataFrame(results, columns=columns)

                if df.empty:
                    st.info("No result found.")
                else:
                    st.dataframe(df, use_container_width=True)

                # Clear old clarification
                st.session_state.pending_question = None
                st.session_state.clarification_question = None

            except Exception as e:

                st.error("Something went wrong.")
                st.write(str(e))

        else:

            st.warning("Please provide an answer.")