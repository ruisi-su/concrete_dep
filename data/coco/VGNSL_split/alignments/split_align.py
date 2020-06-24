type = 'split_verb'
eqn_type = 'pmi'
file_name = 'traindevtest.cap-frame.{}.{}_output'.format(type, eqn_type)

file = open(file_name, 'r')
train_file = open('train.{}.{}.align'.format(type, eqn_type), 'w')
dev_file = open('dev.{}.{}.align'.format(type, eqn_type), 'w')
test_file = open('test.{}.{}.align'.format(type, eqn_type), 'w')

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
