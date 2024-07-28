import csv
import re

# Input and output file paths
input_file = 'output1.csv'
output_file = 'modified_drug_data.csv'

# Words to replace (old_word: new_word)
replace_dict = {
    'various': 'feel',
    # Add more replacements as needed
}

# Words to delete
delete_words = ['Used', 'to', 'treat']

# Compile a regex pattern for words to delete
delete_pattern = re.compile(r'\b(?:{})\b'.format('|'.join(map(re.escape, delete_words))), flags=re.IGNORECASE)

# Read input CSV and write to output CSV
with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Process each row
    for row in reader:
        modified_row = []
        for field in row:
            # Replace words
            for old_word, new_word in replace_dict.items():
                field = re.sub(r'\b{}\b'.format(re.escape(old_word)), new_word, field, flags=re.IGNORECASE)
            
            # Delete words
            field = delete_pattern.sub('', field)
            
            # Remove extra spaces
            field = ' '.join(field.split())
            
            modified_row.append(field)
        
        writer.writerow(modified_row)

print(f"Modified data has been saved to {output_file}")