import csv

input_file_path = 'orig_tb.csv'
output_file_path = 'bug_trigger_input.txt'
error_cycle = 775

with open(input_file_path, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    header = next(reader)

    processed_data = []

    cnt = 0
    for row in reader:
        row = ['0' if value == 'x' else value.strip() for value in row]
        row = [value.strip() for i, value in enumerate(row) if i not in [0, 1, 7, 8]]
        for i in range(len(row)):
            if row[i].isdigit():  
                row[i] = bin(int(row[i]))[2:]  
        processed_data.append(row)

        cnt = cnt + 1
        if cnt > error_cycle + 10:
            break

with open(output_file_path, mode='w', newline='', encoding='utf-8') as outfile:
    for i, row in enumerate(processed_data):
        outfile.write(','.join(map(str, row))) 
        if i < len(processed_data) - 1:
            outfile.write('\n')
