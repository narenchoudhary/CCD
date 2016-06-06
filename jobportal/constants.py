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
    ('PH', 'PH'),
    ('Foreign', 'Foreign')
)

USER_TYPE = (
    ('student', 'student'),
    ('alumni', 'alumni'),
    ('admin', 'admin'),
    ('company', 'company'),
)


USER_CATEGORY = (
    ('Current Student', 'Current Student'),
    ('Alumni', 'Alumni'),
    ('Company', 'Company'),
    ('Admin', 'Admin')
)

DEPARTMENTS = (
    ('BT', 'Biotechnology[BT]'),
    ('CL', 'Chemical[CL]'),
    ('CHE', 'Chemistry[CHE]'),
    ('CE', 'Civil[CE]'),
    ('CSE', 'Computer Science[CSE]'),
    ('DD', 'Design[DD]'),
    ('EEE', 'Electrical[EEE]'),
    ('ECE', 'Electronics[ECE]'),
    ('HSS', 'Humanities & Social Sciences[HSS]'),
    ('MA', 'Mathematics[MA]'),
    ('ME', 'Mechanical[ME]'),
    ('EP', 'Physics[EP]'),
)

DEPARTMENTS_JOBCHOICE = DEPARTMENTS + (('ALL', 'All Departments'),)

PROGRAMMES = (
    ('BTECH', 'B.Tech.'),
    ('MTECH', 'M.Tech.'),
    ('PHD', 'Ph.D.'),
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
    ("Married Scholars Hostel", "Married Scholars Hostel"),
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
