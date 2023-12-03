import random


def generate_dataset(filename, num_items):
    with open(filename, 'w') as file:
        file.write("weight,value\n")
        for _ in range(num_items):
            weight = random.randint(1, num_items)
            value = random.randint(1, num_items*2)
            file.write(f"{weight},{value}\n")

filename = "dataset_kecil.txt"
generate_dataset(filename, 100)
