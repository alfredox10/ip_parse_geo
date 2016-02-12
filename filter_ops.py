import MySQLdb
import time
import operator


def parse_params(user_input):
    params = []
    for part in user_input.split('-'):
        if part:
            field = part.split('[')[0]
            values = part.split('[')[1].split(']')[0].split(',')

            new_values = []
            for v in values:
                new_values.append(v.lstrip().rstrip())
            condition = ''
            if len(part.split('[')[1].split(']')) > 1:
                condition = part.split('[')[1].split(']')[1].replace(' ','')
            params.append((field, new_values, condition))
    return params


def build_query(parsed_cmd):
    command = "SELECT * FROM ip2location.ip2location_db5 WHERE "
    for entry in parsed_cmd:
        command += "{} IN ".format(entry[0])
        for val in entry[1]:
            command += "({},".format(val)
        command = command[:-1] + ") {} ".format(entry[2].upper())
        # print command
    command = command.rstrip() + ';'
    return command


def filter_str_fields( data_dict, command, save_indexes ):
    field, filter_values = command
    for row in data_dict:
        if row[0][field] in filter_values:
            if data_dict.index(row) not in save_indexes:
                save_indexes.append(data_dict.index(row))


def filter_num_fields( data_dict, command, save_indexes ):
    field, cmd_values = command
    contains_conditions = False

    # Check if conditions exist
    for cmd_val in cmd_values:
        if '<' in cmd_val or '>' in cmd_val:
            contains_conditions = True
            break

    if contains_conditions:
        # Condition filtering
        filter_num_field_range(data_dict, command, save_indexes)
    else:
        # Normal filtering
        for row in data_dict:
            if row[0][field] in cmd_values:
                if data_dict.index(row) not in save_indexes:
                    save_indexes.append(data_dict.index(row))


def filter_num_field_range( data_dict, command, save_indexes ):
    field, cmd_values = command

    # Separate condition and value
    cond_idx = 0
    conditions = []
    values = []
    for cmd_val in cmd_values:
        for ch in cmd_val:
            if ch.isdigit():
                break
            cond_idx += 1
        condition = cmd_val[:cond_idx]
        value = float(cmd_val[cond_idx:])

        # Apply single value condition and value
        for row in data_dict:
            data_val = row[0][field]
            match = False
            if condition   == '>' and data_val > value:
                match = True
            elif condition == '<' and data_val < value:
                match = True
            elif condition == '>=' and data_val >= value:
                match = True
            elif condition == '<=' and data_val <= value:
                match = True

            # Save matching values
            if match:
                if data_dict.index(row) not in save_indexes:
                    save_indexes.append(data_dict.index(row))



def summarize_by_string_field( data_dict, field, save_indexes ):
    count_dict = {}
    longest_col = 0
    print "---- Summarizing for field [{}]".format(field)

    for row in data_dict:
        if row[0][field] in count_dict.keys():
            count_dict[row[0][field]] += 1
        else:
            count_dict[row[0][field]] = 1
        longest_col = len(row[0][field]) if len(row[0][field]) > longest_col else longest_col

    # if '-' in count_dict.keys():
    #     count_dict["No Country"] = count_dict.pop('-')

    # Choose how to sort values
    type_sort = ''
    while (type_sort not in [0,1]):
        type_sort = int(raw_input("Sort alphabetically[0] or by count[1]?: "))

    # Print metrics
    print "Unique {}s: {}\n".format(field, len(count_dict))

    # Print results
    # if longest_col < len("No Country"): longest_col = len("No Country")
    if longest_col < len(field): longest_col = len(field)
    template = "{0:>" + str(longest_col) + "} | {1:5}" # column widths
    print template.format(field, 'count') # header
    separator = ''
    for i in xrange(longest_col + 3 + 5):
        separator += '-' if i != longest_col+1 else '+'
    print separator

    # If type_sort == 1 --> numeric sort, type_sort == 0 --> alphabetic sort
    sorted_d = sorted(count_dict.items(), key=operator.itemgetter(type_sort), reverse=type_sort)
    for key, count in sorted_d:
        print template.format(key, count)
    print ''


if __name__ == '__main__':
    # Debug
    # cnx, cursor = db_connect()
    print "\n"

    command = "-country_name[MY] and -city_name[Bukit Tinggi, New York] and -longitude[101.25,3.1255]"
    prs_params = parse_params(command)
    print prs_params
    # print build_query(prs_params)


    # qd = find_single_ip_geo( ip2num([221, 58, 181, 228]) )
    # geo_infoprettyprint_many_rows(qd, DB_COLUMNS, DB_COLUMNS)

    # td = { '221.58.181.228': [221, 58, 181, 228], '1.1.1.228': [1, 1, 1, 228],
    #        '100.58.0.5': [100, 58, 0, 5] }
    # find_many_ips_geo(td)
