from openai import OpenAI
import streamlit as st
import pandas as pd
import numpy as np
import time
from io import StringIO
from utils.logo import add_logo


st.set_page_config(page_title="Calculate", page_icon="https://co2freight-calculator.com/wp-content/uploads/2024/02/EcoFreightCalculator_logo-Charlotte-Waltregny.png")

client = OpenAI()

# Function to load uploaded CSV file
#@st.cache(allow_output_mutation=True)
def load_uploaded_file(uploaded_file):
    return pd.read_csv(uploaded_file)

def inject_css():
    css = """
    <style>
        /* General body styling */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #F0F2F5;
        }
        
        /* Custom banner style */
        .custom-banner {
            background-color: white; 
            padding: 10px 0;
            color: black;
            text-align: left;
            margin-bottom: 10px;
            font-size: 25px;
        }

        .custom-banner img {
            height: 80px; /* Adjust based on your logo's size */
            margin: 0 20px;
            vertical-align: middle;
        }

        .stButton>button {
            border: 2px solid #4CAF50;
            background-color: #4CAF50;
            color: white;
            padding: 10px 24px;
            cursor: pointer;
            border-radius: 4px;
        }

        .stButton>button:hover {
            background-color: #45a049;
        }

        .stFileUploader {
            border: 2px dashed #4CAF50;
            border-radius: 5px;
            background-color: #ffffff;
        }

        h1 {
            color: #333;
        }

        /* Add more custom styles as needed */
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def wait_for_run_completion(client, thread_id, run_id, sleep_interval=1):
    """
    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                print(f"Run completed in {formatted_elapsed_time}")
                break
        except Exception as e:
            print(f"An error occurred while retrieving the run: {e}")
            break
        print("Waiting for run to complete...")
        time.sleep(sleep_interval)
inject_css()
st.markdown("""
        <div class="custom-banner">
            <img src="https://co2freight-calculator.com/wp-content/uploads/2024/02/EcoFreightCalculator_logo-Charlotte-Waltregny.png" alt="Logo">
            CO2 Freight Calculator
        </div>
    """, unsafe_allow_html=True)
#st.write("## CO2 Freight Calculator")

uploaded_file = st.file_uploader("Upload your freight activity file (CSV format)", type="csv")
if uploaded_file is not None:
    #data = load_uploaded_file(uploaded_file)
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)
    user_input = "Compute the CO2 emissions associated to these activities: " + str(dataframe)

if st.button("Compute"):
    try:
        if user_input:
            with st.spinner('Computing based on emission factors... This can take up to several minutes.'):
                run = client.beta.threads.create_and_run(
                    assistant_id="asst_lsdJjY2H9ksFVkgUJou1P0bz",
                    thread={
                        "messages": [
                        {"role": "user", "content": user_input}
                        ]
                    },
                    instructions = "You are NOT an assistant. Never ask questions to the user. Never provide example computations. Compute all of the routes asked by the user. First step is always to find the distance between the origin and destination for each row. Second step is always to find the correct emission factors. Third step is always to compute the total CO2 emission for each row based on these 2 elements. Provide straight answers to the best of your knowledge. Always output a table with your calculations for each row at the end of your answer."
                    )
                wait_for_run_completion(client, run.thread_id, run.id)

                messages = client.beta.threads.messages.list(
                        thread_id=run.thread_id
                        )
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                if response:
                    st.write(response)
                    try:
                        print(response)
                        # Split the text into lines
                        lines = response.split('\n')

                        # Find the start and end of the table
                        # Assuming the table starts with '| Origin' and ends before an empty line
                        table_start = None
                        table_end = None

                        for i, line in enumerate(lines):
                            if '| Origin' in line:  # This finds the header row
                                table_start = i
                            elif table_start is not None and line.strip() == '':
                                table_end = i
                                break

                        # If the table doesn't explicitly end with an empty line, assume it's at the end of the text
                        if table_end is None and table_start is not None:
                            table_end = len(lines)

                        # Extract the table lines and convert them into a single string
                        table_lines = '\n'.join(lines[table_start:table_end])

                        # Convert the markdown table to a CSV format by replacing "|" with ","
                        table_csv = table_lines.replace('|', ',')

                        # Use StringIO to simulate a file for pandas
                        table_io = StringIO(table_csv)

                        # Load into a pandas DataFrame
                        df = pd.read_csv(table_io, sep=',', skipinitialspace=True)

                        # Read the data into a DataFrame, specifying the delimiter if needed
                        #df = pd.read_table(data, sep="\s+")
                        #df = pd.DataFrame(response)
                        def convert_df_to_csv(df):
                            csv_buffer = StringIO()
                            df.to_csv(csv_buffer, index=False)
                            return csv_buffer.getvalue()

                        csv = convert_df_to_csv(df)

                        # Streamlit download button
                        st.download_button(
                            label="Download table as CSV",
                            data=csv,
                            file_name='routes_with_co2eq.csv',
                            mime='text/csv',
                        )
                    except Exception as e:
                        st.download_button(
                            label="Download complete answer",
                            data=response,
                            file_name='co2freight_calculator.txt',
                            mime='text/plain',
                        )
                        #st.write("Could not extract dataframe only, downloading the total answer.")
                    if st.button("Suggest another answer"):
                        main()
        else:
            st.error("Enter a request to the calculator.")
    except Exception as e:
        st.warning("Please enter a request to the calculator.")