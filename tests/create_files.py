import os
import zipfile
import shutil

# Create a directory named 'nested_dir'
os.makedirs('nested_dir', exist_ok=True)

# Create 'test.csv' and write "some,text" to it
with open('test.csv', 'w') as file:
    file.write('some,text')

# Create 'test.json' and write "some text" to it
with open('test.json', 'w') as file:
    file.write('some text')

# Create 'test1.txt' and write "some text" to it
with open('file1.txt', 'w') as file:
    file.write('some text')

# Create 'file2.csv' and write "some text" to it
with open('file2.csv', 'w') as file:
    file.write('some,text')

# Create 'file3.txt' inside 'nested_dir' and write "some text" to it
with open('nested_dir/file3.txt', 'w') as file:
    file.write('some text')

# Create 'file4.csv' and write "some, text" to it
with open('nested_dir/file4.csv', 'w') as file:
    file.write('some,text')

# Case 1 - Create a zip file 
with zipfile.ZipFile('tests/files_json_and_csv.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write('test.csv')
    zipf.write('test.json')

# Case 2 - Create a zip file containing 'test1.txt', test2.csv and 'subdir/test2.txt'
with zipfile.ZipFile('tests/files_with_nested.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write('file1.txt')
    zipf.write('file2.csv')
    zipf.write('nested_dir/file3.txt')
    zipf.write('nested_dir/file4.csv')

# Case 3 - Create an empty zip file
with zipfile.ZipFile('tests/empty_test.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    pass

# Clean up the files and directories created
test_files = ['test.csv', 'test.json', 'file1.txt', 'file2.csv']
for file in test_files:
    if os.path.exists(file):
        os.remove(file)
if os.path.exists("nested_dir"):
    shutil.rmtree("nested_dir")