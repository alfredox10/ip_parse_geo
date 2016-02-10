command = "country[MY] city[Ampang]"


params = {}
for st in command.split(' '):
    params[st.split('[')[0]] = st[st.find('[')+1:st.find(']')]

commands = ["countrycode[MY,USA,MX]",
            "countrycode[M%,%SA,mx]",
            "country[japan]",
            "country[japan] city[O%]",
            "country[japan] city[%ma, %ya%]",
            "lat[3.1588]",
            "long[>100]",
            "long[>100] lat[<=10]",
            "ip[155.55.12.9, 155.55.12.99]",
            "ip[>155.55.12.9]",
            "ip[155.55.12.%]",
            "ip[155.%.12.10]",
            "ip[155.100.5%.10]",
            "ip[155.100.%5.10]",
            "ip[>155.55.12.9, <155.55.12.50]"]