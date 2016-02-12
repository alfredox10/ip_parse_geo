import MySQLdb
import time
from prettytable import PrettyTable
# import pandas as pd

# NOTE: Pandas was too slow and memory consuming
# DB Info: http://lite.ip2location.com/faqs#ipv6-csharp
# Database of ip addresses in csv format
# db_columns = ['ip_from', 'ip_to', 'country_code', 'country_name', 'region_name', 'city_name', 'latitude', 'longitude']
# ip_df = pd.read_csv( 'IP2LOCATION-LITE-DB5.CSV', names=db_columns, header=None )
#
# def find_single_ip_geo_pandas(ipnum):
#     geo_data = ip_df.loc[(ip_df.ip_to >= ipnum)][:1]
#     # geo_data = ip_df.loc[(ip_df.ip_from <= ipnum) & (ip_df.ip_to >= ipnum)]
#     return geo_data
#
# def find_many_ip_geo_pandas(ipdict):
#     start = time.time()
#     geo_ip_dict = {}
#     count = 0
#     for key in ipdict.keys()[:1000]:
#         geo_ip = find_single_ip_geo_pandas(ip2num(ipdict[key]))
#         geo_ip_dict[key] = {'country_code': geo_ip.country_code, 'country_name': geo_ip.country_name,
#                             'region_name': geo_ip.region_name, 'city_name': geo_ip.city_name,
#                             'latitude': geo_ip.latitude, 'longitude': geo_ip.longitude}
#         count += 1
#         if not count % 1000 and count > 0:
#             print "{} Records retrieved".format(count)
#     print "Runtime: {}".format(time.time() - start)
#     print "len(geo_ip_list): {}".format(len(geo_ip_dict.keys()))
#     return geo_ip_dict


DB_COLUMNS = ('ip_from',
              'ip_to',
              'country_code',
              'country_name',
              'region_name',
              'city_name',
              'latitude',
              'longitude')


# DB Info: http://lite.ip2location.com/faqs#ipv6-csharp
def db_connect():
    db_host = 'localhost'
    db_user = 'client'
    db_pass = 'simple'
    db_name = 'ip2location'
    db_cnx = MySQLdb.connect( host=db_host, user=db_user, passwd=db_pass, db=db_name )
    cursor = db_cnx.cursor( cursorclass=MySQLdb.cursors.DictCursor )
    return db_cnx, cursor

def find_many_ips_geo_opt(ip_dict, print_status=True):
    start = time.time()
    ip_geo_vals = []
    count = 0
    for ip in ip_dict.keys():
        # num = ip2num(ip)
        ip_geo_vals.append(find_single_ip_geo(ip, print_status))
        count += 1
        # if not count % 1000 and count > 0:
            # print "{} Geo IP records loaded".format(count)
    print "\n---- Begin Geo IP retrieval ----"
    print "Runtime: {:.3} s".format(time.time()-start)
    print "Geo IP Values count: {}".format(len(ip_geo_vals))
    print "First value: {}".format(ip_geo_vals[-1:])
    print " Last value: {}".format(ip_geo_vals[:1])
    print "---- End Geo IP retrieval ------\n"
    return ip_geo_vals


# PERFORMANCE for query of 5000 IPs went from 50 s to 0.14 s with these changes:
#   1. Index ip_to and ip_from
#   2. Comparing only to (ip_to >= num) instead of (ip_to >= num and ip_from <= num)
#   3. Letting db do ip conversion with INET_ATON()
#   4. Adding ORDER BY ip_to ASC
#   5. Adding LIMIT 1
#   Note: If the ip is not defined exactly well inside another range, it will return the next closest match.
#         The client can choose to have these gaps filled in with [No Country] labels or handle them
#         a different way of their choosing.
#   The biggest performance enhancements came from 2, 4, and 5.
def find_single_ip_geo(ip, print_status = True):
    command = "SELECT * FROM ip2location.ip2location_db5 " \
              "WHERE ip_to >= INET_ATON('{0}') " \
              "ORDER BY ip_to ASC LIMIT 1".format(ip)
    if print_status: print command
    geo_data = try_cursor_select(CNX, CURSOR, command, print_status)
    return geo_data


def try_cursor_select( cnx, curs, cmd, printStatus = True ):
    db_data = None
    try:
        if printStatus: print "Execute SQL: {0}".format(cmd)
        curs.execute( cmd )
        # if not is_multi_row:
        #     if printStatus: print "Retrieving 1 record"
        #     db_data = curs.fetchone()
        # else:
        if printStatus: print "Retrieving multiple records"
        db_data = curs.fetchall()
    except MySQLdb.OperationalError as err:
        print( "Error: {0}".format(err))
        raise err
    finally:
        return db_data


# Convert ip to numeric format in db for faster querying
# Formula = (ip[0]*256*256*256) + (ip[1]*256*256) + (ip[2]*256) + ip[3]
def ip2num(ipint):
    return (ipint[0]*16777216) + (ipint[1]*65536) + (ipint[2]*256) + ipint[3]

def num2ip(num):
    o1 = int(num/ 16777216 ) % 256
    o2 = int(num/ 65536    ) % 256
    o3 = int(num/ 256      ) % 256
    o4 = int(num/ 16777216 ) % 256
    return "{}.{}.{}.{}".format(o1,o2,o3,o4)


def prettyprint_many_rows( list_dicts, align_cols, columns, sort_col = '' ):
    x = PrettyTable(columns)
    # x.get_string(sortby='city_name')
    if sort_col:
        x.sortby = sort_col
    # x.reversesort = True
    for a_col in align_cols:
        x.align[a_col] = 'l' # left align this column
    x.padding_width = 1
    for row in list_dicts:
        row_vals = []
        for col in columns:
            # print row[0][col]
            val = num2ip(row[0][col]) if col in ['ip_to', 'ip_from'] else row[0][col]
            row_vals.append(val)
        x.add_row(row_vals)
    print "{}\n".format(x)


CNX, CURSOR = db_connect()