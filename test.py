import csv
import pandas as pd
import os



# with open('data/prompt_data.csv', 'r') as csvfile:

#     # Read the CSV file into a DataFrame
#     df = pd.read_csv('data/prompt_data.csv')

#     # Access the data as a NumPy array
#     array = df.values
#     images = os.listdir('static/images')
#     for img in images:
#         for row in array:
#             if str(row[0]) == str(img):
#                 print(row[1])   
# text = 'DAT'
# a = [f'ádsadsadas{text}',f'ádasdsadsa{text}']
# b = f'{text},{a[0]}'
# print(b)
images = os.listdir('static/images')
print(len(images))