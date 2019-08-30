# INSTRUCTIONS
# this code works only for multiple choice questions

## prepare key answer & student answer with the format:
### A1: text "Number" for key answer file and text "NAME" for student answer files;
### B1: text "key_answer" for key answer file and text the name of the student for student answer file;
### A2 and below: the question numbers;
### B2 and below: the answer key according to each question numbers;

## put the .py file in the same folder with key_answer 

## put all the student files in a new folder under current directory
### example: dir / current_key_files_folder / student_files_folder
## make sure all of the student files is correctly formatted

# run the python script with this command
# python <space> checker.py <space> answer_key_filename <space> answer_files_folder_name
# example: "python checker.py answerkey studentfiles"

# import libary
import os
import sys
import glob
import pandas as pd

# get the file directory
dirpath = os.getcwd()

#set up files
answer_key = pd.read_excel(sys.argv[1])
answer_key.columns = ["No", "answer_key"]
nama_folder = sys.argv[2]
files = glob.glob(dirpath + "/" + nama_folder + "/*.xl*")

# new dataframe
df = pd.DataFrame()
all_data = pd.DataFrame() 

# 2. open student files
for file in files:
    answer = pd.read_excel(file)
    answer.rename(columns={answer.columns[0]:"NO"}, inplace=True)
    
    # 3. concat file key answer & answers
    df = pd.concat([answer_key, answer], axis=1)
    df = df.drop("NO",1)
    
    # 4. check the right/wrong answer (0,1) -> new column "result"_"student name"
    df['result_'+df.columns[-1]] = df[df.columns[-1]].copy()
    df[df.columns[-1]][df[df.columns[-1]]!=df['answer_key']] = 0
    df[df.columns[-1]][df[df.columns[-1]]==df['answer_key']] = 1
    
    # 5. concat to the new dataframe
    all_data = pd.concat([all_data, df[df.columns[-1]]], axis=1)

# 6. no of correct answer per student
result = pd.DataFrame(all_data.sum(axis = 0, skipna = True))
result.rename(columns={result.columns[0]:"correct_answer"}, inplace=True)
result['score'] = result[result.columns[0]]/answer_key.shape[0]*100
result['score'] = result.score.astype(int)
result.to_excel("Result of "+nama_folder+".xlsx")

# 7. no of correct answer per question
evaluation = pd.DataFrame(all_data.sum(axis = 1, skipna = True))
evaluation.rename(columns={evaluation.columns[0]:"correct_answer"}, inplace=True)
evaluation.to_excel("Evaluation of "+nama_folder+".xlsx")
