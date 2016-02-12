command = "ip[>155.55.12.9,<155.55.12.50] country[MY] city[Ampang]"
comd = "country[MY] city[Ampang]"


params = {}
for st in t.split(' '):
    field = st.split('[')[0]
    params[field] = []
    values = st.split('[')[1].split(',')
    for i, val in enumerate(values):
        params[field].append(val[:-1] if i == len(values)-1 else val)


commands = ["countrycode[MY,USA,MX]",
            "countrycode[M%,%SA,mx]",
            "country[japan]",
            "country[japan] city[O%]",
            "country[japan] city[%ma, %ya%]",
            "lat[3.1588]",
            "long[>100]",
            "longitude[>100] latitude[<=10]",
            "ip[155.55.12.9, 155.55.12.99]",
            "ip[>155.55.12.9]",
            "ip[155.55.12.%]",
            "ip[155.%.12.10]",
            "ip[155.100.5%.10]",
            "ip[155.100.%5.10]",
            "ip[>155.55.12.9,<155.55.12.50]"]



#    -country_code[JP] and -latitude[>37]