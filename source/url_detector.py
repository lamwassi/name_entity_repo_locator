import json
from openpyxl import load_workbook
import re



def cleanStrValue(value):
    """sumary_line: format strings from cells by removing unnecessary characters 
    
    Keyword arguments: value
    argument -- description: string input

    Return: formated str

    """    
    if value:
        value = str(value).strip()
        value = value.replace(u'\u00a0', ' ')
        value = re.sub(r'[^\x00-\x7F]+', ' ', ' ' + str(value) + ' ').strip()
    else:
        value = ''
        
    return value

def load_data(inputexcel):
    """
    Keyword arguments: 
    argument -- 
    Return: JSON file containing entity as key and urls as value (if exist)
    """
    if not inputexcel:
        return None

    sheet = load_workbook(filename = inputexcel)
    sheet_data = sheet['dockerimages']
    max_row = sheet_data.max_row
    containers = {}
    for xint in range(2, max_row+1):
        row_num = str(xint)    
        container_name = cleanStrValue(value = sheet_data['A' + row_num].value)
        url = cleanStrValue(value = sheet_data['K' + row_num].value)
        containers[container_name] = url
       
    return containers



if __name__ == "__main__":

    file_pth = "kb/ACA_KG_0.0.2.0.xlsx"
    entities = load_data(file_pth)

    
    