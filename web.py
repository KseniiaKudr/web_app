import streamlit as st
import pandas as pd
import base64
from io import BytesIO


# Function to generate download link for the DataFrame
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data


st.title('Pivot Table to Dropdown Application')

# File uploader allows user to add their own CSV or Excel
uploaded_file = st.file_uploader("Upload your pivot table file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Read and display the file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.write('Pivot Table:')
    st.dataframe(df)

    # Process the DataFrame to create dropdowns (a simplified example)
    options = df.iloc[0, 1:].dropna().tolist()
    selections = {}
    for item in df['Item']:
        selections[item] = st.selectbox(f'Select price for {item}', options)

    if st.button('Save Selections'):
        # Save the selected options
        selected_df = pd.DataFrame(list(selections.items()), columns=['Item', 'Selected_Price'])
        st.write('Selected Prices:')
        st.dataframe(selected_df)

        # Generate a link to download the new DataFrame as Excel
        val = to_excel(selected_df)
        b64 = base64.b64encode(val)  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="selected_prices.xlsx">Download selected prices as Excel</a>'
        st.markdown(href, unsafe_allow_html=True)