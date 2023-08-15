import re
import codecs

position_dict = {1: (0.15, 0.15), 2: (0.45, 0.15), 3: (0.75, 0.15), 4: (1.05, 0.15), 5: (1.05, 0.45), 6: (0.75, 0.45), 7: (0.45, 0.45), 8: (0.15, 0.45), 9: (0.15, 0.75), 10:(0.45, 0.75), 11:(0.75, 0.75), 12:(1.05, 0.75), 13:(1.05, 1.15), 14:(0.75, 1.05), 15:(0.45, 1.05), 16:(0.15, 1.05)}
# Open the file "myfile.txt" in utf-8 encoding mode and read its contents
with codecs.open('myfile.txt', "r", encoding="utf-8") as f:
     code = f.read()

# Define an IP address as a string variable
ip_address= "192.168.167.158"

# Check if the script is being run as the main module
if __name__ == '__main__':
    
    
        # Define a regular expression to extract code blocks enclosed in triple backticks (```)
        run_regex = re.compile(r"'''(.*?)'''", re.DOTALL)
         # Define a function to extract Python code from a given content using the regular expression
        def CODE(content):
            code_blocks = run_regex.findall(content)
            if code_blocks:
                full_code = "\n".join(code_blocks)
                return full_code
        print(CODE(code)) # Print the extracted Python code from the "myfile.txt" file
        print("Please wait while I run the code ....")
        exec(CODE(code)) # Execute the extracted Python code using the exec() function
        print("Done!\n")

   
