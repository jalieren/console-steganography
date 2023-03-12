import numpy as np
from PIL import Image
from art import *
from colorama import init
from colorama import Fore
from time import sleep
from tqdm import tqdm

init(autoreset=True)

tprint('jalieren')

def Encode(src, message, dest, key):
    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size // n

    message += key
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)

    if req_pixels > total_pixels:
        print(Fore.RED + 'ERROR: Need larger file size')
    else:
        index = 0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
                    index += 1
        
        array = array.reshape(height, width, n)
        enc_image = Image.fromarray(array.astype('uint8'), img.mode)
        enc_image.save(dest)
        print(Fore.GREEN + 'Image encoded succesfully')


def Decode(src, key):
    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size // n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    for i in range(len(hidden_bits)):
        if message[-len(key):] == key:
            break
        else:
            message += chr(int(hidden_bits[i], 2))

    if key in message:
        print(Fore.GREEN + "Hidden Message:", message[:-len(key)])
    else:
        print(Fore.RED + 'No hidden message found')

def main():
    print("-----Welcome!-----")
    print("1: Encode")
    print("2: Decode")
    print("3: Exit")

    func = input('What do you want to do: ')

    if func == '1':
        print("Enter Source Image Path: ")
        src = input()

        print("Enter Message to Hide: ")
        message = input()

        print("Enter encryption key: ")
        key = str(input())

        print("Enter Destination Image Path: ")
        dest = input()

        print("Encoding...")
        for i in tqdm(range(10)):
            sleep(0.3)

        Encode(src, message, dest, key)

    elif func == '2':
        print("Enter Source Image Path: ")
        src = input()

        print("Enter encryption key: ")
        key = str(input())

        print("Decoding...")
        for i in tqdm(range(10)):
            sleep(0.3)
        Decode(src, key)

    elif func == '3':
        exit()

    else:
        print(Fore.RED + "ERROR: Invalid option chosen")

while(True):
    main()