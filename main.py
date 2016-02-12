import filter_ops
import ip_parsing
import geo_info


# -------------- Global Settings -----------
# Delimters to find values for commands
delim = ('[', ']')
fpath = 'list_of_ips.txt'
keep_running = True
ip_address_dict = {}
ip_geo_values = []

if __name__ == '__main__':
    # Functionality
    # Metrics:
    # + Total IPs by country
    # + Total IPs by city in country
    # + Total IPs by region in country

    # Queries:
    # + longitude/latitude range
    # + countries, city, region
    print '\n'
    while keep_running:
        while not ip_address_dict:
            print "Load default csv: {}".format(fpath)
            var = raw_input("y/n: ")
            if var in ['y', 'Y']:
                ip_address_dict = ip_parsing.parse_ips_from_file( fpath )
            else:
                var = raw_input("Input full file path: ")
                try:
                    ip_address_dict = ip_parsing.parse_ips_from_file(var)
                except:
                    print "Error: Incorrect path!"

        if not ip_geo_values:
            ip_geo_values = geo_info.find_many_ips_geo_opt( ip_address_dict, False )

        print "Filter data retrieved for pased IPs."
        print "Available fields: ip, country_code, country_name, region_name, city_name, latitude, longitude"
        print "Can have multiple comma-separated values per field."
        print "Every field must be delimited with a dash '-'"
        print "Conditions allowed .. '<' and '<=: less/equal than, '>' and '>=': greater/equal than"
        print "                      and, or"
        print "NOTE: Numeric queries can only take 1 value/condition"
        print "Sample queries (case sensitive):"
        print "Ex 1: -country_code[MY, MX]"
        print "Ex 1: -country_code[JP] and -latitude[>37]"
        print "Ex 1: -country_code[MY] or -city_name[Tsu, Fukuoka]\n"

        option = ''
        params = ''
        idx = 0
        dict_of_lists = {}

        while option not in ['s', 'q']:
            option = raw_input("Summarize(s) metrics or query(q) parsed IPs: ")

        if option == 's':
            print "Options: {}".format( geo_info.DB_COLUMNS[2:6] )
            while params not in geo_info.DB_COLUMNS[2:6]:
                params = raw_input("Field to group by: ")
            list_idx = []
            filter_ops.summarize_by_string_field( ip_geo_values, params, list_idx )
        elif option == 'q':
            params = raw_input("Input query parameters: ")
            parsed_params = filter_ops.parse_params( params )
            print "Parsed parameters: {}".format(parsed_params)
            # Query values
            for pp in parsed_params:
                list_idx = []
                if pp[0] in ['country_code', 'country_name', 'region_name', 'city_name']:
                    filter_ops.filter_str_fields( ip_geo_values, pp[:2], list_idx )
                    dict_of_lists[idx] = list_idx
                elif pp[0] in ['longitude', 'latitude']:
                    filter_ops.filter_num_fields( ip_geo_values, pp[:2], list_idx )
                    dict_of_lists[idx] = list_idx
                idx += 1

            # Apply list combinations
            final_list = []
            if len(parsed_params) > 1:
                for i, pp in enumerate(parsed_params):
                    if pp[2].lower() == 'and':
                        if i == 0:
                            final_list = list(set(dict_of_lists[i]).intersection(dict_of_lists[i+1]))
                        else:
                            final_list = list(set(final_list).intersection(dict_of_lists[i+1]))
                    elif pp[2].lower() == 'or':
                        if i == 0:
                            final_list = set(dict_of_lists[i] + dict_of_lists[i+1])
                        else:
                            final_list = set(final_list + dict_of_lists[i+1])
            else:
                final_list = dict_of_lists[0]

            # Print resulting combined query list
            print "Query values count: {}".format(len(final_list))
            usr_input = ''
            print "Options: {}".format( geo_info.DB_COLUMNS )
            while usr_input not in geo_info.DB_COLUMNS:
                usr_input = raw_input("Sort rows by column (none defaults to [ip_from]): ")
                if usr_input == '':
                    usr_input = 'ip_from'
                    break
                elif usr_input not in geo_info.DB_COLUMNS:
                    print "Incorrect input, please try again.\n"

            filtered_geo_list = []
            for i in final_list:
                filtered_geo_list.append( ip_geo_values[i] )
            geo_info.prettyprint_many_rows( filtered_geo_list, geo_info.DB_COLUMNS, geo_info.DB_COLUMNS, usr_input )


        var = ''
        while var.lower() not in ['y', 'n']:
            var = raw_input("Perform another operation (y/n): ")
            if var.lower() != 'y':
                keep_running = False
            print "Incorrect input, please try again.\n"




# == DEBUG ==
    # ------ IP Parsing
    # fpath = 'tiny.txt'
    # ip_address_dict = ip_parsing.parse_ips_from_file( fpath )

    # ------ IP 2 Num Conversion
    # d = {}
    # d['202.186.13.4'] = [202, 186, 13, 4]
    # d['55.16.13.1'] = [55, 16, 13, 1]
    # ipn = ip2num(d['202.186.13.4'])
    # print ipn

    # ------ IP Geo retrieval
    # Retrieve all IP Geo info from DB
    # ip_geo_values = geo_info.parse_ips_from_file(ip_address_dict, False)
    # filtering.prettyprint_many_rows(ip_geo_values[:5], filtering.DB_COLUMNS, filtering.DB_COLUMNS)

    # Filter some values
    # list_idx = []
    # filtering.filter_str_fields( ip_geo_values, ('country_code', ['MY']), list_idx )
    # filtering.filter_num_fields( ip_geo_values, ('latitude', ['>65']), list_idx )
    # print "Query values count: {}".format(len(list_idx))
    # filtered_list = []
    # for i in list_idx:
    #     filtered_list.append(ip_geo_values[i])
    # usr_input = ''
    # print "Options: {}".format(filtering.DB_COLUMNS)
    # while usr_input not in filtering.DB_COLUMNS:
    #     usr_input = raw_input("Column to sort rows: ")
    # filtering.prettyprint_many_rows(filtered_list, filtering.DB_COLUMNS, filtering.DB_COLUMNS, usr_input)

    # Summarize values
    # print "Options: {}".format(filtering.DB_COLUMNS[2:6])
    # while usr_input not in filtering.DB_COLUMNS[2:6]:
    #     usr_input = raw_input("Field to group by: ")
    # filtering.summarize_by_string_field( ip_geo_values, usr_input, list_idx )
# == /DEBUG/ ==