import os

# this is the extension you want to detect
extension = '.csv'

for root, dirs_list, files_list in os.walk("./"):
    for file_name in files_list:
        if os.path.splitext(file_name)[-1] == extension:
            arr = []
            print(file_name)
            with open(file_name) as f:
                num = 0
                start = 0
                for index, line in enumerate(f):
                    if line[:-1].split(",")[2] == "Passing":
                        if start == 0: 
                            start = index
                        num += 1
                stop = start + num*2
                print(num)
                f.seek(0)
                for index, line in enumerate(f):
                    if index >= (start-num-30) and index < stop:
                        arr.append(line[:-1])

                with open('./final_data/'+file_name, 'w') as f:
                    for item in arr:
                        f.write("%s\n" % item)