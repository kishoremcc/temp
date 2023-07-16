{\rtf1\ansi\ansicpg1252\cocoartf2639
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # Import the required libraries\
import glob\
import re\
import pytesseract\
import pandas as pd\
from pdf2image import convert_from_path\
from pytesseract import Output\
import sys\
\
\
def img_to_text(img_path, outputPath):\
    """\
    Extracts the data from the images and store the text information\
    Returns Text\
    ----------\
    img_path (str): string filename of target image\
    """\
    image_file = img_path\
    with open(image_file) as f:\
        imagePages = f.readlines()\
\
    # Path to tesseract (You must install it before using this script)\
    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'\
    outputData = pytesseract.image_to_data(image_file)\
\
    parameterFields = open(r"Parameter fields.txt", "r")\
    parameterFieldsInList = read_text(parameterFields)\
\
    textLocation = open(r"ParameterLocation.txt", "r")\
    textLocationInList = read_text(textLocation)\
    parameterValues = []\
\
\
    dataDict = \{\}\
    i = 0\
    dataDict = dataDict.fromkeys(outputData.splitlines()[0].split('\\t'))\
    print(outputData)\
    for anItem in textLocationInList:\
        print(anItem)\
        for b in outputData.splitlines()[1:]:\
            dataDict.update(zip(dataDict, b.split("\\t")))\
            if dataDict['block_num'] == anItem.split(",")[0].strip('\\t') and dataDict['line_num'] == anItem.split(",")[1].strip('\\t') and \\\
                    dataDict['word_num'] == anItem.split(",")[2].strip('\\t') and \\\
                    int(anItem.split(",")[3].strip('\\t'))-10 <= int(dataDict['left']) <= int(anItem.split(",")[3].strip('\\t'))+10 and \\\
                    int(anItem.split(",")[4].strip('\\t'))-10 <= int(dataDict['top']) <= int(anItem.split(",")[4].strip('\\t'))+10 and \\\
                    int(anItem.split(",")[5].strip('\\t'))-10 <= int(dataDict['width']) <= int(anItem.split(",")[5].strip('\\t'))+10 and \\\
                    int(anItem.split(",")[6].strip('\\n'))-10 <= int(dataDict['height']) <= int(anItem.split(",")[6].strip('\\n'))+10:\
                parameterValues.append(dataDict['text'])\
                print(parameterValues)\
                break\
\
    parameterFields = open(r"Parameter fields.txt", "r")\
    parameterFieldsInList = read_text(parameterFields)\
\
    formNumber = []\
    yearFiled = []\
    for _ in parameterFieldsInList:\
        formNumber.append(f'Form 1040')\
        yearFiled.append(parameterValues[0])\
\
    df_text = pd.DataFrame(list(zip(formNumber, yearFiled, parameterFieldsInList, parameterValues[1:])),\
                                                       columns=['Form No.', 'Year', 'Parameter Fields', 'Parameter Value'])\
\
    # Transfer it to the excel file\
    df_text.to_excel(outputPath+"form_1040.xlsx", index=False)\
\
\
def read_text(textFile):\
    textInList = []\
    count = 0\
    for line in textFile:\
        count += 1\
        line.strip()\
        textInList.append(line)\
    return textInList\
\
\
def convert_pdf_to_images(aPdfFilePath, currentDir):\
    """\
    Function to convert a pdf file into collection of images\
\
    :param aPdfFilePath: a pdf file to convert into collection of image files\
    :param currentDir: directory to save the image files\
    save the path of image collections from multiple pages in a text file\
    """\
    # Convert pdf file to images\
    images = convert_from_path(aPdfFilePath, dpi=600, fmt="jpg")\
    text_file = open("./imageFilesPath.txt", "w")\
    for i in range(len(images)):\
        # Assigned file name for each image (i.e., page_0, page_1...)\
        fileName = f"page_\{str(i)\}.jpg"\
        # Save each page in the pdf as an image\
        images[i].save(currentDir + "\\\\" + fileName, 'JPEG')\
        text_file.write(currentDir + "\\\\" + fileName)\
        text_file.write("\\n")\
\
    text_file.close()\
\
\
def main():\
    # User input, the path to your files\
    # dataFolderPath = input("Enter the path of your files: ")\
    # Please provide the correct data path\
    dataFolderPath = sys.argv[1]\
    outputPath = sys.argv[2]\
\
    # Subdirectories paths\
    userDirectories = glob.glob(dataFolderPath + '//*', recursive=True)\
\
    # Add image formats here\
    neededExt = ["pdf", "jpeg", "jpg", "png", "tif", "tiff", "bmp"]\
\
    # Loop through each user\
    for eachUserDir in userDirectories:\
        # Full file paths in a list\
        fullFilePaths = []\
        [fullFilePaths.extend(glob.glob(eachUserDir + '/*.' + ext)) for ext in neededExt]\
        # Iterate over the list and do respective process\
        for aFilePath in fullFilePaths:\
            if aFilePath.lower().endswith('.pdf'):\
                # Read pdf file\
                convert_pdf_to_images(aFilePath, eachUserDir)\
                img_to_text("./imageFilesPath.txt", outputPath)\
\
if __name__ == '__main__':\
    main()\
}