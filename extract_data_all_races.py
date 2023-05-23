import shutil
import random
import os


DRY_RUN = False


def split_array(array):
    total_length = len(array)
    split_point = int(total_length * 0.8)
    random.shuffle(array)  # Shuffle the array randomly
    return array[:split_point], array[split_point:]


def copy(src, dst):
    if DRY_RUN:
        print(src, ' -> ', dst)
    else:
        shutil.copyfile(src, dst)


def get_class(string):
    last_digit_index = len(string) - 1
    while last_digit_index >= 0 and string[last_digit_index].isdigit():
        last_digit_index -= 1

    string = string[:last_digit_index+1]
    string = string.rstrip('_')

    return string


def main():
    dirs = []
    with open('Dataset/annotations/list.txt', 'r') as file:
        for line in file.readlines():
            if line[0] == '#':
                continue
            cls = get_class(line.split(' ')[0])
            train_dir = f'Dataset/all_races/train/{cls}'
            val_dir = f'Dataset/all_races/val/{cls}'
            test_dir = f'Dataset/all_races/test/{cls}'

            if train_dir not in dirs:
                dirs.append(train_dir)
            if val_dir not in dirs:
                dirs.append(val_dir)
            if test_dir not in dirs:
                dirs.append(test_dir)

    for dir in dirs:
        if not DRY_RUN:
            if not os.path.exists(dir):
                os.makedirs(dir)
        else:
            print('mkdir ', dir)

    # Train validation
    with open('Dataset/annotations/trainval.txt', 'r') as file:
        files_per_class = {}
        for line in file.readlines():
            name = line.split(' ')[0]
            cls = get_class(name)
            if cls not in files_per_class:
                files_per_class[cls] = []

            files_per_class[cls].append(f'{name}.jpg')

        for cls in files_per_class:
            cls_train, cls_val = split_array(files_per_class[cls])
            print(f'  - {cls} train', len(cls_train))
            print(f'  - {cls} val', len(cls_val))

            for img in cls_train:
                out_name = img.split('/')[-1]
                copy('Dataset/images/' + img, f'Dataset/all_races/train/{cls}/{out_name}')

            for img in cls_val:
                out_name = img.split('/')[-1]
                copy('Dataset/images/' + img, f'Dataset/all_races/val/{cls}/{out_name}')

    with open('Dataset/annotations/test.txt', 'r') as file:
        files_per_class = {}
        for line in file.readlines():
            name = line.split(' ')[0]
            cls = get_class(name)
            if cls not in files_per_class:
                files_per_class[cls] = []

            files_per_class[cls].append(f'{name}.jpg')

        for cls in files_per_class:
            cls_test = files_per_class[cls]
            print(f'  - {cls} test', len(cls_test))

            for img in cls_test:
                out_name = img.split('/')[-1]
                copy('Dataset/images/' + img, f'Dataset/all_races/test/{cls}/{out_name}')


if __name__ == '__main__':
    main()
