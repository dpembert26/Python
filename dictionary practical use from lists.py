name_list = ["Shawn","Darin","Glen","Peter","Larry"]
age_list = [22,42,33,45,54]
job_list = ["Administrator","Automation Engineer","Accountant","Banker","Painter"]

info_dict = {}

info_dict = dict((g[0],list(g[1:])) for g in zip(name_list,age_list,job_list))

for key,value in info_dict.items():
    print("\nName: %s" % key + "\nAge: %s" % value[0] + "\nJob: %s" % value[1])