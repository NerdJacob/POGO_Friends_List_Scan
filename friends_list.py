import os
from pathlib import Path
os.chdir(Path(__file__).parents[0])
import subprocess
import re
from PIL import Image, ImageEnhance

count, contrast_shift = 1, 0.5
trainer_string, distance_string, victories_string, catches_string = "^(.*?)\s", "Walked (\d.*?)\s", "Battles Won (\d.*?)\s", "Caught (\d.*?)\s"
file = open("output\list.txt",'a')
file.writelines('Trainer\tVictories\tDistance\tCatches\tFile Name\n')

# OCR choise
decision = input(f'Would we like to read these files using 1) pytesseract or 2) easyOCR?\nAs of 04/05/25 pytesseract is having reliability issues.')
if int(decision) == 1:
    import pytesseract    
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'    
else:
    decision = 2
    import easyocr
    reader = easyocr.Reader(['en'])

def pull_screenshots():
    input_file_list = []
    for input_file in os.listdir('inputs'):
        input_file_list.append(input_file)
    return(input_file_list)

input_file_list = pull_screenshots()

def convert_to_grayscale():
    count = 1
    for input_picture in input_file_list:
        converting = Image.open(f'inputs/{input_picture}').convert('L')
        converted = ImageEnhance.Contrast(converting).enhance(contrast_shift)
        converted.save(f'processing/{count:03}.jpg')
        count += 1
convert_to_grayscale()

def get_list_of_converted_files():
    grey_files_list = []
    for processed_picture in os.listdir('processing'):
        grey_files_list.append(processed_picture)
    return(grey_files_list)
grey_files_list = get_list_of_converted_files()

def using_pytesseract(grey_files_list):
    print('Using pyterra-thing?')
    count = 1    
    for screenshot in grey_files_list:
        converted_image = Image.open(f'processing/{screenshot}')
        raw_text = pytesseract.image_to_string(converted_image)
        combined_text = re.sub("\n"," ", raw_text)
        print(combined_text)
        try:
            trainer = re.findall(trainer_string,combined_text)[0]
            try:
                victories = re.findall(victories_string,combined_text)[0]
            except:
                victories = "???"
            try:
                distance = re.findall(distance_string,combined_text)[0]
            except:
                distance = "???"
            try:
                catches = re.findall(catches_string, combined_text)[0]
            except:
                catches = "???"
        except:
            print(f'Couldn\'t read it.')
        try:
            print(f'{trainer}\t{victories}\t{distance}\t{screenshot}')
            file.writelines(f'{trainer}\t{victories}\t{distance}\t{catches}\t{screenshot}\n')
        except:
           print(f'Couldn\'t read it.')
        count += 1
    file.close()

def using_easyocr(grey_files_list):
    print('Using easyocr')
    count = 1
    for screenshot in grey_files_list:
        converted_image = Image.open(f'processing/{screenshot}')
        text = reader.readtext(converted_image, detail = 0)
        combined_text = ""
        
        for part in text:
            combined_text = combined_text + part + " "

        try:
            trainer = re.findall(trainer_string,combined_text)[0]
            try:
                victories = re.findall(victories_string,combined_text)[0]
            except:
                victories = "???"
            try:
                distance = re.findall(distance_string,combined_text)[0]
            except:
                distance = "???"
            try:
                catches = re.findall(catches_string,combined_text)[0]
            except:
                catches = "???"
            try:
                print(f'{trainer}\t{victories}\t{distance}\t{screenshot}')
                file.writelines(f'{trainer}\t{victories}\t{distance}\t{catches}\t{screenshot}\n')
            except:
                pass
        except:
            print(f'Couldn\'t read it.')
        count += 1
    file.close()

if decision == 1: # ← Fix this, it doesn't ... reader not defined?
    using_pytesseract(grey_files_list)
else:
    using_easyocr(grey_files_list)

print('We have pulled the data from the screenshots.  Drop it into a spreadsheet with lookups using\n\n=IFERROR(index(\'old-sheet\'!B:B,match(A93,\'old-sheet\'!A:A,0)),"No match")\n')