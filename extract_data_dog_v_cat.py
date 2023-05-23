import shutil
import random
import os


DRY_RUN = False


def split_array(array):
    total_length = len(array)
    split_point = int(total_length * 0.7)
    random.shuffle(array)  # Shuffle the array randomly
    return array[:split_point], array[split_point:]


def copy(src, dst):
    if DRY_RUN:
        print(src, ' -> ', dst)
    else:
        shutil.copyfile(src, dst)


def main():
    dirs = [
        'Dataset/dog_v_cat/train/dog',
        'Dataset/dog_v_cat/train/cat',
        'Dataset/dog_v_cat/val/dog',
        'Dataset/dog_v_cat/val/cat',
        'Dataset/dog_v_cat/test/dog',
        'Dataset/dog_v_cat/test/cat',
    ]

    if not DRY_RUN:
        for dir in dirs:
            if not os.path.exists(dir):
                os.makedirs(dir)

    # Train validation
    with open('Dataset/annotations/trainval.txt', 'r') as file:
        dog_files = []
        cat_files = []
        for line in file.readlines():
            is_cat = False
            is_dog = False

            if line[0] == '#':
                continue
            if line[0].isupper():
                is_cat = True
            elif line[0].islower():
                is_dog = True

            filename = line.split(' ')[0] + '.jpg'
            if is_dog:
                dog_files.append('Dataset/images/' + filename)
            elif is_cat:
                cat_files.append('Dataset/images/' + filename)

        cat_train, cat_val = split_array(cat_files)
        print('cat train', len(cat_train))
        print('cat val', len(cat_val))

        dog_train, dog_val = split_array(dog_files)
        print('dog train', len(dog_train))
        print('dog val', len(dog_val))

        for img in dog_train:
            out_name = img.split('/')[-1]
            copy(img, f'Dataset/dog_v_cat/train/dog/{out_name}')

        for img in dog_val:
            out_name = img.split('/')[-1]
            copy(img, f'Dataset/dog_v_cat/val/dog/{out_name}')

        for img in cat_train:
            out_name = img.split('/')[-1]
            copy(img, f'Dataset/dog_v_cat/train/cat/{out_name}')

        for img in cat_val:
            out_name = img.split('/')[-1]
            copy(img, f'Dataset/dog_v_cat/val/cat/{out_name}')

    with open('Dataset/annotations/test.txt', 'r') as file:
        dog_files = []
        cat_files = []
        for line in file.readlines():
            is_cat = False
            is_dog = False

            if line[0] == '#':
                continue
            if line[0].isupper():
                is_cat = True
            elif line[0].islower():
                is_dog = True

            filename = line.split(' ')[0] + '.jpg'
            if is_dog:
                dog_files.append('Dataset/images/' + filename)
            elif is_cat:
                cat_files.append('Dataset/images/' + filename)

        print('dog test', len(dog_files))
        print('cat test', len(cat_files))

        for img in dog_files:
            out_name = img.split('/')[-1]
            copy(img, f'Dataset/dog_v_cat/test/dog/{out_name}')

        for img in cat_files:
            out_name = img.split('/')[-1]
            copy(img, f'Dataset/dog_v_cat/test/cat/{out_name}')


if __name__ == '__main__':
    main()
