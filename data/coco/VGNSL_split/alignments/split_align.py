type = 'split_verb'
file_name = 'traindevtest.cap-frame.{}.output'.format(type)

file = open(file_name, 'r')
train_file = open('train.{}.align'.format(type), 'w')
dev_file = open('dev.{}.align'.format(type), 'w')
test_file = open('test.{}.align'.format(type), 'w')

file = file.readlines()

for lines in file[0:413915]:
    train_file.write(lines)
for lines in file[413915:418915]:
    dev_file.write(lines)
for lines in file[418915:]:
    test_file.write(lines)

train_file.close()
dev_file.close()
test_file.close()
