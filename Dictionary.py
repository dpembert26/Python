# Create a simple dictionary from two lists
import itertools

name_list = ["Shawn", "Marty", "Tim", "Darin", "Kelly", "Aaron", "Peter", "Eden", "larry", "Gary"]
job_list = ["Carpenter", "Barber", "Construction worker", "Automation Engineer", "Nurse", "Special Ops Solution Architect", "Plumber", "Professional Soccer Player"]


name_job_dict = dict(itertools.zip_longest(name_list, job_list))

print(name_job_dict)