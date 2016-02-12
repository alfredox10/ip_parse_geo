# ---------------- IP PARSING --------------
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
    print "\n---- Begin parsing ----"
    print "Parsed IP Count: {}".format(len(ip_dict.keys()))
    print "From file: {}".format(file_path)
    print "First 4 IPs: {}".format(ip_dict.keys()[:4])
    print " Last 4 IPs: {}".format(ip_dict.keys()[-4:])
    print "---- End parsing ------"
    return ip_dict