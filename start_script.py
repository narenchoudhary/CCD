from jobportal.models import *

y16 = Year.objects.create(current_year=2016, remark='')
cse16 = Department.objects.create(year=y16, dept='CSE', dept_code='CSE')
cse16bt = ProgrammeJobRelation(year=y16, dept=cse16, name='BTECH')
cse16btm = ProgrammeJobRelation(year=y16, dept=cse16, name='BTECH', minor_status=True)

cse16bt = ProgrammeJobRelation(year=y16, dept=cse16, name='MTECH')
cse16btm = ProgrammeJobRelation(year=y16, dept=cse16, name='MTECH', minor_status=True)


me16 = Department.objects.create(year=y16, dept='ME', dept_code='ME')
me16bt = ProgrammeJobRelation(year=y16, dept=me16, name='BTECH')
me16btm = ProgrammeJobRelation(year=y16, dept=me16, name='BTECH', minor_status=True)
