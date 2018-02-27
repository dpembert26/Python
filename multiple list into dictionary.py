name_list = ["Shawn","Darin","Glen","Peter","Larry"]
age_list = [22,42,33,45,54]
job_list = ["Administrator","Automation Engineer","Accountant","Banker","Painter"]

combine_dict = {}

# Combine name, age and job lists into a dictionary
combine_dict = dict((v[0],list(v[1:])) for v in zip(name_list,age_list,job_list))
print(combine_dict)