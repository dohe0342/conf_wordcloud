f = open('./asr_keyword.txt', 'r').readlines()
csv_file = open('./asr_keyword.csv', 'w')

keyword = []

#print('"weight";"word"')
csv_file.write('"weight";"word"\n')
for line in f:
    line = line.strip().split(' ')
    keyword = ' '.join(line[:-1])
    repeat_num = int(line[-1])
    #print(f'"{repeat_num}";"{keyword}"')
    csv_file.write(f'"{repeat_num}";"{keyword}"\n')
