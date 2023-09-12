import pandas as pd
import json

# Load the Excel file into a Pandas DataFrame
df = pd.read_excel('testjson.xlsx', header=None)

# Extract titles and sub-titles from the first three rows
titles = df.iloc[0, :].fillna(method='ffill').tolist()
subtitles = df.iloc[1, :].fillna(method='ffill').tolist()
subsubtitles = df.iloc[2, :].fillna(method='ffill').tolist()

# Create a dictionary to store the data
data = {}

# Iterate through the columns and create the JSON structure
for col in range(df.shape[1]):
    title = titles[col]
    subtitle = subtitles[col]
    subsubtitle = subsubtitles[col]

    # Filter out NaN values and convert to list
    values = df.iloc[3:, col].dropna().tolist()

    if title not in data:
        data[title] = {}

    if pd.notna(subtitle):
        if subtitle not in data[title]:
            data[title][subtitle] = {}

        # Use a default value for subsubtitle if it's NaN
        subsubtitle = subsubtitle if pd.notna(subsubtitle) else "__default_subsubtitle__"

        if subsubtitle not in data[title][subtitle]:
            data[title][subtitle][subsubtitle] = []

        data[title][subtitle][subsubtitle].extend(values)
    elif pd.notna(title):
        # When there is just a title (no subtitle or subsubtitle)
        data[title] = values

# Convert the dictionary to JSON
json_data = json.dumps(data, indent=4, ensure_ascii=False)

# Save the JSON data to a file
with open('output.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)
