import re

def extract_names(file_path):
    males =[] 
    females=[]

    with open(file_path, 'r') as file:
        names = file.readlines()

    pattern = r'<td>([^<]+)</td><td>([^<]+)</td>$'

    for i in names[47:2047]:
        if i.strip() == '</tr>':
            pass
        name = re.search(pattern, i)
    
        if name:
            males.append(name.group(1).strip())
            females.append(name.group(2).strip())

    return males, females

if __name__ == "__main__":
    file_path = './Assignments/Beginner/Assignment_2/baby2008.html'
    males, females = extract_names(file_path)
    print(f'Number of male names = {len(males)}, And number of female names = {len(females)}')