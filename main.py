import pandas as pd

# Delimters to find values for commands
delim = ('[', ']')

# DB Info: http://lite.ip2location.com/faqs#ipv6-csharp
# Database of ip addresses in csv format
db_columns = ['ip_from', 'ip_to', 'country_code', 'country_name', 'region_name', 'city_name', 'latitude', 'longitude']
ip_df = pd.read_csv( 'IP2LOCATION-LITE-DB5.CSV', names=db_columns, header=None )

def find_single_ip_geo(ipnum):
    geo_data = ip_df.loc[(ip_df.ip_from <= ipnum) & (ip_df.ip_to >= ipnum)]
    return geo_data


# Total ip count was 4998, ips that began with dots may have been missed.
def parse_ips_from_file( file_path ):
    ip_dict = {}
    dots3_words = []
    dots4_words = []
    raw_ips = []
    digits = ('1', '2', '3' ,'4' ,'5' ,'6' ,'7' ,'8' ,'9')
    with open(file_path) as f:
        lines = f.readlines()
        # Collecting all IPs even if they start with 0 or 255
    for line in lines:
        for word in line.split(' '):
            if word.count('.') == 3: dots3_words.append(word)
            if word.count('.') == 4: dots4_words.append(word)
            # Counting 3 periods to catch ips at end of sentence
            if word.count('.') <= 4:
                # Remove starting and trailing non-digit chars
                ip = word if word.startswith(digits) else word[1:]
                ip = word if word.endswith(digits)   else word[:-1]
                octets = []
                for i, octet in enumerate( ip.split( '.' ) ):
                    try:
                        octets.append(int(octet))
                        if octets[i] >= 0 and octets[i] <= 255:
                            if i == 3:
                                ip = ip.rstrip('\n')
                                ip = ip[:-1] if ip.endswith('.') else ip
                                ip_dict[ip] = octets
                                raw_ips.append(word)
                        else:
                            break
                    except:
                        break
    # For verification
    # print "3 dotted items: {}".format(len(dots3_words))
    # print "4 dotted items: {}".format(len(dots4_words))
    # missing_ips = [x for x in dots3_words + dots4_words if x not in raw_ips]
    # print "Missing IP count: {}, {}".format(len(missing_ips), missing_ips)
    print "Parsed IP Count: {}".format(len(ip_dict.keys()))
    return ip_dict


# Convert ip to numeric format in db for faster querying
# Formula = (ip[0]*256*256*256) + (ip[1]*256*256) + (ip[2]*256) + ip[3]
def ip2num(ip):
    return (ip[0]*16777216) + (ip[1]*65536) + (ip[2]*256) + ip[3]


def parse_params(user_input):
    params = {}
    for st in user_input.split(' '):
        params[st.split( delim[0] )[0]] = st[st.find( delim[0] ) + 1:st.find( delim[1] )]
    return params


def filtering(command):
    do = True


print '/n'

# ------ IP Parsing
# fpath = 'tiny.txt'
fpath = 'list_of_ips.txt'
ip_address_dict = parse_ips_from_file( fpath )
# print "First 4 IPs: {}".format(ip_address_list[:4])
# print " Last 4 IPs: {}".format(ip_address_list[-4:])
# print "IPs: {}".format(ip_address_list)

# ------ IP 2 Num Conversion
d = {}
d['202.186.13.4'] = [202, 186, 13, 4]
# d['55.16.13.1'] = [55, 16, 13, 1]
ipn = ip2num(d['202.186.13.4'])
print ipn

# ------ IP Geo retrieval
print find_single_ip_geo(ipn)