file_path = 'name.txt'

with open(file_path, 'r') as file:
    name = file.read()

print('First name: ', name.split()[0])
print('Middle name: ', name.split()[1])
print('Last name: ', name.split()[2])
print('Full name: ', name.strip())