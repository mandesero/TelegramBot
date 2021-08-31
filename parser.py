import csv

from data import second, lection_lines, group_colomn, heads


def return_timetable(group):
    file_name = '2_' + str(second[group]) + '.csv'
    with open(file_name) as r_file:
        time_dict = {}
        read_file = csv.reader(r_file)
        i = group_colomn[group]
        j, count = 0, 0
        tmp = []
        for line in read_file:
            if j in heads:
                time_dict[count] = tmp
                tmp = []
                tmp.append('\t' + line[0] + '\n\n')
                count += 1
            elif j in lection_lines:
                tmp.append(line[0] + '\n' + line[1] + '\n\n')
            else:
                tmp.append(line[0] + '\n' + line[i] + '\n\n')
            j += 1
        time_dict[6] = tmp
    return time_dict

#
# if __name__ == '__main__':
#     group = int(input('Group'))
#     time_dict = return_timetable(group)
#     # day = int(input('Day'))
#     for day in range(1,7):
#         print(*time_dict[day])



