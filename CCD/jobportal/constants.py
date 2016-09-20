"""
Choices for model fields
"""
SEX = (
    ('M', 'Male'),
    ('F', 'Female'),
)

CATEGORY = (
    ('GEN', 'GEN'),
    ('OBC', 'OBC'),
    ('SC', 'SC'),
    ('ST', 'ST'),
    ('PD', 'PD'),
    ('FOREIGN', 'FOREIGN'),
)

USER_TYPE = (
    ('student', 'student'),
    ('alumni', 'alumni'),
    ('admin', 'admin'),
    ('company', 'company'),
    ('verifier', 'verifier'),
)


USER_CATEGORY = (
    ('Current Student', 'Current Student'),
    ('Alumni', 'Alumni'),
    ('Company', 'Company'),
    ('Admin', 'Admin'),
)

DEPARTMENTS = (
    ('Biosciences and Bioengineering', 'Biosciences and Bioengineering'),
    ('Chemistry', 'Chemistry'),
    ('Chemical Engineering', 'Chemical Engineering'),
    ('Civil Engineering', 'Civil Engineering'),
    ('Computer Science and Engineering', 'Computer Science and Engineering'),
    ('Design', 'Design'),
    ('Electronics and Electrical Engineering',
     'Electronics and Electrical Engineering'),
    ('Electronics and Communication Engineering',
     'Electronics and Communication Engineering'),
    ('Humanities & Social Sciences', 'Humanities & Social Sciences'),
    ('Mathematics', 'Mathematics'),
    ('Mechanical Engineering', 'Mechanical Engineering'),
    ('Physics', 'Physics'),
    ('Center for Energy', 'Center for Energy'),
)

DEPARTMENTS_JOBCHOICE = DEPARTMENTS + (('ALL', 'All Departments'),)

PROGRAMMES = (
    ('BTECH', 'B.Tech.'),
    ('BDES', 'B.Des.'),
    ('MTECH', 'M.Tech.'),
    ('MDES', 'M.Des.'),
    ('PHD', 'Ph.D.'),
    ('MSC', 'M.Sc.'),
    ('MA', 'M.A.'),
)

HOSTELS = (
    ('Barak', 'Barak'),
    ('Brahmaputra', 'Brahmaputra'),
    ('Dhansiri', 'Dhansiri'),
    ('Dibang', 'Dibang'),
    ('Dihing', 'Dihing'),
    ('Kameng', 'Kameng'),
    ('Kapili', 'Kapili'),
    ('Lohit', 'Lohit'),
    ('Manas', 'Manas'),
    ("Married Scholars ", "Married Scholars"),
    ('Siang', 'Siang'),
    ('Subansiri', 'Subansiri'),
    ('Umiam', 'Umiam'),
    ('Other', 'Other'),
)

ORGANIZATION_TYPE = (
    ('Private', 'Private'),
    ('Government', 'Government'),
    ('PSU', 'PSU'),
    ('MNC(Indian Origin)', 'MNC(Indian Origin)'),
    ('MNC(Foreign Origin)', 'MNC(Foreign Origin)'),
    ('NGO', 'NGO'),
    ('Other', 'Other')

)

INDUSTRY_SECTOR = (
    ('Core Engg', 'Core Engg'),
    ('IT', 'IT'),
    ('Analytics', 'Analytics'),
    ('Management', 'Management'),
    ('Finance', 'Finance'),
    ('Education', 'Education'),
    ('Consulting', 'Consulting'),
    ('R&D', 'R&D'),
    ('Oil and Gas', 'Oil and Gas'),
    ('Ecommerce', 'Ecommerce'),
    ('FMCG', 'FMCG'),
    ('Manufacturing', 'Manufacturing'),
    ('Telecom', 'Telecom'),
    ('Other', 'Other')
)

EVENT_TYPE = (
    ('Screening Test', 'Screening Test'),
    ('Pre Placement Talk', 'Pre Placement Talk'),
    ('Workshop', 'Workshop'),
    ('Promotional Event', 'Promotional Event'),
)

SERVER_IP = (
    ('202.141.80.9', 'naambor'),
    ('202.141.80.10', 'disbang'),
    ('202.141.80.11', 'tamdil'),
    ('202.141.80.12', 'teesta'),
    ('202.141.80.13', 'dikrong'),
)
