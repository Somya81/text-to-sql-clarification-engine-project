import streamlit as st
import pandas as pd
from llm import generate_sql,check_clarification
from database import execute_query
st.title("Intelligent Text-to-SQL Assistant")
st.write("Ask a question about your database.")
question=st.text_input("Enter your question: ")
if st.button("Generate SQL"):
    if question:
        try:
            clarification=check_clarification(question)
            if clarification.needs_clarification:
                st.warning("Could you clarify:")
                st.write(clarification.question)
            else:
                sql=generate_sql(question)
                st.subheader("Generated SQL")
                
                st.code(sql,language="sql")
                
                columns,results=execute_query(sql)
                st.subheader("Query Result")
                
                df=pd.DataFrame(results,columns=columns)
                if df.empty:
                    st.info("No result found.")
                else:
                    st.dataframe(df,use_container_width=True)
                
        except Exception as e:
            
            st.error("Something went wrong.")
            st.write(str(e))

    else:
        st.warning("Please enter a question.")
