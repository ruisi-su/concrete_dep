import shutil
import argparse

# # move
# def move(file_name, orig_dir, dest_dir):
#     # file_name = 'COCO_val2014_000000458401'
#     # full_name = '{}.jpg'.format(file_name)
#     # orig_dir = '/Users/sisi/Downloads/{}'.format(orig_dir)
#     # dest_dir = '/Users/sisi/Downloads/{}'.format(dest_dir)


# file_names is a txt file, each line is the file name
def filter_move(splitType, orig_dir, dest_dir):
    file_names = 'data2014/{}_name.txt'.format(splitType)
    with open(file_names, 'r') as name:
        for file_name in name:
            orig_file_name = file_name.rstrip()
            file_name = orig_file_name.split('.')[0]
            pred_name ='coco_val' + file_name + '.predictions'
            # print(file_name)
            # print(orig_dir)
            # print(dest_dir)
            shutil.copy('{}/{}'.format(orig_dir, pred_name), dest_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--split', help='type of split, one of test, val, train')
    parser.add_argument('--orig', help='original directory')
    parser.add_argument('--to', help='destination directory')
    args = parser.parse_args()


    # print('split is ' + args.split)
    # print('from ' + args.orig)
    # print('to ' + args.to)
    filter_move(args.split, args.orig, args.to)
