import json
import shutil
import argparse

# file_names is a txt file, each line is the file name
def filter_move(splitType, orig_dir, dest_dir):
    file_names = 'dataset_filter.json'
    with open(file_names, 'r') as name:
        names = json.load(name)

    names_split = names[splitType]
    for file_name in names_split:
        orig_file_name = file_name.rstrip()
        file_name = orig_file_name.split('.')[0]
        pred_name ='coco_val' + file_name + '.predictions'
        shutil.copy('{}/{}'.format(orig_dir, pred_name), dest_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--split', help='type of split, one of test, val, train')
    parser.add_argument('--orig', help='original directory')
    parser.add_argument('--to', help='destination directory')
    args = parser.parse_args()

    filter_move(args.split, args.orig, args.to)
