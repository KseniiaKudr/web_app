import io
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, clear_output

# Interface for file upload
upload = widgets.FileUpload(accept='.csv, .xlsx', multiple=False)
display(upload)

# Global list to store both label and dropdown widgets
widgets_pairs = []

def create_dropdowns_from_file(change):
    global widgets_pairs
    # Read the uploaded file into a DataFrame
    uploaded_filename = next(iter(upload.value))
    content = upload.value[uploaded_filename]['content']
    if uploaded_filename.endswith('.csv'):
        df = pd.read_csv(io.BytesIO(content))
    else:
        df = pd.read_excel(io.BytesIO(content))

    df.set_index('Item', inplace=True)

    # Clear previous output
    clear_output()
    display(upload)  # Redisplay the upload button
    widgets_pairs.clear()  # Clear previous pairs
    
    # Create dropdowns for each item in the pivot table
    item_widgets = []
    for item in df.index:
        matched_prices = df.loc[item].dropna().values
        item_label = widgets.Label(value=f'{item}:', layout=widgets.Layout(width='40%'))
        dropdown = widgets.Dropdown(
            options=matched_prices,
            description='',  # No description to avoid duplication
            disabled=False,
            layout=widgets.Layout(width='60%')
        )

        # Store the label and dropdown together
        widgets_pairs.append((item_label, dropdown))
        
        hbox = widgets.HBox([item_label, dropdown])
        item_widgets.append(hbox)

    container = widgets.VBox(item_widgets)
    display(container)
    display(save_button)  # Display the save button

upload.observe(create_dropdowns_from_file, names='value')

def save_selections(button):
    data = {'Item': [], 'Matched_Item_ReportedPrice': []}
    for label, dropdown in widgets_pairs:
        item_name = label.value.rstrip(':')
        data['Item'].append(item_name)
        data['Matched_Item_ReportedPrice'].append(dropdown.value)

    # Create DataFrame
    selected_df = pd.DataFrame(data)
    
    # Save the DataFrame to CSV
    try:
        selected_df.to_csv('selected_prices.csv', index=False)
        print("Selections saved to 'selected_prices.csv'")
    except Exception as e:
        print(f"Failed to save CSV: {e}")

# Button for saving the selections
save_button = widgets.Button(description="Save Selections")
save_button.on_click(save_selections)  # Link the button click to the save function
