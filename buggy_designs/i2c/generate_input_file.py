import csv

# input_file_path = 'orig_tb.csv'
input_file_path = 'orig_tb_sync_reset.csv'


output_file_path = 'bug_trigger_input_1.txt'
error_cycle = 1250
input_row = [2,3,4,5,6,7,8,9,10]

with open(input_file_path, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    header = next(reader)

    processed_data = []

    cnt = 0
    for row in reader:
        row = ['0' if value.strip() == 'x' else value.strip() for value in row]
        row = [value for i, value in enumerate(row) if i in input_row]
        for i in range(len(row)):
            if row[i].isdigit():  
                row[i] = bin(int(row[i]))[2:]  
        processed_data.append(row)

        cnt = cnt + 1
        if cnt > error_cycle:
            break

with open(output_file_path, mode='w', newline='', encoding='utf-8') as outfile:
    for i, row in enumerate(processed_data):
        outfile.write(','.join(map(str, row))) 
        if i < len(processed_data) - 1:
            outfile.write('\n')

output_file_path = 'bug_trigger_input_2.txt'
error_cycle = 10
input_row = [2,3,4,5,6,7,8,9,10]

with open(input_file_path, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    header = next(reader)

    processed_data = []

    cnt = 0
    for row in reader:
        row = ['0' if value.strip() == 'x' else value.strip() for value in row]
        row = [value for i, value in enumerate(row) if i in input_row]
        for i in range(len(row)):
            if row[i].isdigit():  
                row[i] = bin(int(row[i]))[2:]  
        processed_data.append(row)

        cnt = cnt + 1
        if cnt > error_cycle:
            break

with open(output_file_path, mode='w', newline='', encoding='utf-8') as outfile:
    for i, row in enumerate(processed_data):
        outfile.write(','.join(map(str, row))) 
        if i < len(processed_data) - 1:
            outfile.write('\n')

output_file_path = 'bug_trigger_input_3.txt'
error_cycle = 30
input_row = [2,3,4,5,6,7,8,9,10]

with open(input_file_path, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    header = next(reader)

    processed_data = []

    cnt = 0
    for row in reader:
        row = ['0' if value.strip() == 'x' else value.strip() for value in row]
        row = [value for i, value in enumerate(row) if i in input_row]
        for i in range(len(row)):
            if row[i].isdigit():  
                row[i] = bin(int(row[i]))[2:]  
        processed_data.append(row)

        cnt = cnt + 1
        if cnt > error_cycle:
            break

with open(output_file_path, mode='w', newline='', encoding='utf-8') as outfile:
    for i, row in enumerate(processed_data):
        outfile.write(','.join(map(str, row))) 
        if i < len(processed_data) - 1:
            outfile.write('\n')

output_file_path = 'bug_trigger_input_4.txt'
error_cycle = 650
input_row = [2,3,4,5,6,7,8,9,10]

with open(input_file_path, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    header = next(reader)

    processed_data = []

    cnt = 0
    for row in reader:
        row = ['0' if value.strip() == 'x' else value.strip() for value in row]
        row = [value for i, value in enumerate(row) if i in input_row]
        for i in range(len(row)):
            if row[i].isdigit():  
                row[i] = bin(int(row[i]))[2:]  
        processed_data.append(row)

        cnt = cnt + 1
        if cnt > error_cycle:
            break

with open(output_file_path, mode='w', newline='', encoding='utf-8') as outfile:
    for i, row in enumerate(processed_data):
        outfile.write(','.join(map(str, row))) 
        if i < len(processed_data) - 1:
            outfile.write('\n')

output_file_path = 'bug_trigger_input_5.txt'
error_cycle = 1650
input_row = [2,3,4,5,6,7,8,9,10]

with open(input_file_path, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    header = next(reader)

    processed_data = []

    cnt = 0
    for row in reader:
        row = ['0' if value.strip() == 'x' else value.strip() for value in row]
        row = [value for i, value in enumerate(row) if i in input_row]
        for i in range(len(row)):
            if row[i].isdigit():  
                row[i] = bin(int(row[i]))[2:]  
        processed_data.append(row)

        cnt = cnt + 1
        if cnt > error_cycle:
            break

with open(output_file_path, mode='w', newline='', encoding='utf-8') as outfile:
    for i, row in enumerate(processed_data):
        outfile.write(','.join(map(str, row))) 
        if i < len(processed_data) - 1:
            outfile.write('\n')