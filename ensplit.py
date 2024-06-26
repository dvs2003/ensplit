from cryptography.fernet import Fernet
import os
import tarfile


def folderchooser():
    file_counter = 0
    file_list = os.listdir()
    for i in file_list:
        print(f'{file_counter} : {file_list[file_counter]}')
        file_counter += 1
        
    chosen_one = int(input('Choose a file/folder : '))
    return file_list[chosen_one]

def generate_key(name_of_key):
    # Name the encrypted files in accordance with keys
    
    key = Fernet.generate_key()
    
    print('Key will be generated in ->')
    print(f'{print(os.getcwd())} -> {name_of_key}.key')
    
    with open(f'{name_of_key}.key', 'wb') as filekey:
        filekey.write(key)
    return key
        
#Add the hash of the file to it also to make sure its stiched correctly watchout for memory size
#This function has been AI generated by Google Gemini Advanced on 15th May 2024, and then modified by me.
def split_file(input_file, max_bytes=1024 * 1024 * 100):  # 100 MB default 
    """Splits a large input file into smaller chunks."""

    chunk_number = 1
    output_file = None
    current_size = 0
    
    with open(input_file, 'rb') as f_in:  # Open in binary mode (optional)
        folder_name = f'folder_{input_file}'
        os.mkdir(folder_name)
        
        for line in f_in:
            if output_file is None or current_size >= max_bytes:
                if output_file:
                    output_file.close()
                output_file = open(f'./{folder_name}/part{chunk_number}.part', 'wb')
                chunk_number += 1
                current_size = 0
            
            output_file.write(line)
            current_size += len(line)

    if output_file:
        output_file.close()
    with open(f'./{folder_name}/ensplit.cfg', 'w') as ensplit_cfg:
        ensplit_cfg.writelines(f'{input_file}')
    return 1
def stitching(output_file = ""):
    
    all_files = os.listdir()
    file_number = 0
    for i in all_files:
        if os.path.isdir(i):
            print(f'{file_number} : {i}')
        file_number += 1

    for i in all_files:
        if i[-3:] == 'key':
            keyname = i
        elif i == all_files[-1]:
            print('Keyfile not found')
            return 0
        
    chosen_folder = int(input("Enter Folder Number : "))
    
    if 'ensplit.cfg' not in os.listdir(f'./{all_files[chosen_folder]}'):
        print('ensplit.cfg not found.')
        return 0
    else:
        with open(f'./{all_files[chosen_folder]}/ensplit.cfg', 'r') as ensplit_cfg:
            output_file = ensplit_cfg.readlines()[0]
    to_stitch = {}
    all_to_stitch = os.listdir(f'./{all_files[chosen_folder]}')
    for each_file in all_to_stitch:
        if each_file[:4] == 'part':
            #to_stitch.append(each_file)
            to_stitch[int(f'{each_file.split('.')[0][4:]}')] = each_file
    #print(to_stitch)
    to_stitch_sorted =[]
    for i in range(len(to_stitch)):
        to_stitch_sorted.append(to_stitch[i + 1])
    #print(to_stitch_sorted)
    #Create Output File
    with open(f'{output_file}', 'wb'):
        print(f'{output_file} Created.')
    #Append each part to it
    for __file in to_stitch_sorted:
        with open(output_file, 'ab') as output_to:
            with open(f'./{all_files[chosen_folder]}/{__file}', 'rb') as current_chunk:
                
                output_to.write(current_chunk.read())
    return 1
def make_tarfile(output_filename="", source_dir = ""):
        
    chosen_one = folderchooser()
    source_dir = chosen_one
    output_filename = f"{source_dir}.archive"
    
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    return 1
def recover_tarfile():
    chosen_one = folderchooser()
    fileee = tarfile.open(chosen_one)
    fileee.extractall(f'./extracted_{chosen_one}')
    return 1



def start():
    print('1. Convert to archive')
    print('2. Split and encrypt file')
    print('3. Decrypt and Merge to archive')
    print('4. Recover files from archive')
    
    print('Any other integer to exit.')
    user_choice = int(input('>> '))
    
    if user_choice == 1:
        make_tarfile()
        return 1
    if user_choice == 2:
        inputfile = folderchooser()
        split_file(inputfile)
        return 1
    if user_choice == 3:
        stitching()
        return 1
    if user_choice == 4:
        recover_tarfile()
        return 1
    else:
        return 'done'

while True:
    if start() == 'done':
        break
    else:
        continue