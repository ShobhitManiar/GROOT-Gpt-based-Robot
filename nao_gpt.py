import openai
import os
import subprocess
import asyncio
import nest_asyncio
import argparse
import recorder as r
import sys
nest_asyncio.apply()

openai.api_key = "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"  # Set the OpenAI API key

# Set the paths to different versions of Python and script files
python27_path = r'D:\Python27\python.exe'
python27_script = r'D:\Thesis\nao_test.py' 

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--prompt", type=str, default="D:\Thesis\prompts.txt")
parser.add_argument("--sysprompt", type=str, default="D:\Thesis\system_prompts.txt")
parser.add_argument("--game", type=str, default="D:\Thesis\game.txt")
parser.add_argument("--stt", type=str, default=r"D:\Thesis\transcriptions_transcript_1.txt") # Parse another command-line argument for the speech-to-text transcript file
args = parser.parse_args()

# Read system prompts and game instructions from files
with open(args.sysprompt, "r",encoding="utf-8") as f:
    sysprompt = f.read()

with open(args.prompt, "r", encoding="utf-8") as f:
     prompt = f.read()

with open(args.game, "r",encoding="utf-8") as f:
    game = f.read()

# Initialize chat history with system prompt
conversation_history = [
    {
        "role": "system",
        "content": sysprompt
    }]

def ask(prompt):
    conversation_history.append(
        {
            "role": "user",
            "content": prompt,
        }
    )
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
        temperature=0
    )
    conversation_history.append(
        {
            "role": "assistant",
            "content": completion.choices[0].message.content,
        }
    )
    return conversation_history[-1]["content"] 

ask(game)  # Ask the game instruction prompt
ask(prompt)  # Start the conversation by asking the initial prompt
# Function to generate GPT-3 response using the provided prompts
def GPT(prompts):
    question = str(prompts) # input()
    response = ask(question)
    print(response)
    file1 = open('myfile.txt', 'w')
    file1.writelines(response)
    file1.close()
    result = subprocess.Popen([python27_path, python27_script], shell=True)
    result.wait()
    

last_occurrence = -1
COMMAND_WORD="whisper"
# Function to check the transcript periodically            
async def check_transcript():
    global last_occurrence
    with open(args.stt,"r",encoding="utf-8") as f:
        text = f.read()
        occurrence= text.lower().rfind(COMMAND_WORD)
        if occurrence != last_occurrence:

            # get command starting at occurrence of command word
            command = text[occurrence:]
            if command.endswith("."):
                command=command[:-1]
           
            # store last occurrence so we don't repeat the same command
            last_occurrence = occurrence

            # Generate GPT response based on the command as a prompt
            global prompt 
            print("ready")
            prompts= f"""{command}"""  
            if prompts.strip().lower() == "whisper exit" or prompts.strip().lower() == "whisper, exit":
                print("Exiting the program...")
                sys.exit(0)
            else:
                GPT(prompts)

         
# Function to run the check_transcript() function periodically
async def run_periodically(interval, periodic_function):
    while True:
        print("say something using command word Whisper")
        r.STT()
        await asyncio.gather(asyncio.sleep(interval), periodic_function())

# Run the check_transcript() function periodically every 1 second
asyncio.run(run_periodically(1, check_transcript))

