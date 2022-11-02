import datetime as dt


HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(7, 18)]

DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
)
places=(
    ('Nairobi-CBD', 'Nairobi-CBD'),
    ('Nairobi-Ngong Road', 'Nairobi-Ngong Road'),
    ('Nairobi-Thika Road', 'Nairobi-Thika Road'),
    ('Nairobi-Waiyaki Way', 'Nairobi-Waiyaki Way'),
    ('Nairobi-Outering Road', 'Nairobi-Outering Road'),
    ('Nairobi-Jogoo Road', 'Nairobi-Jogoo Road'),
    ('Nairobi-Kiambu Road', 'Nairobi-Kiambu Road'),
    ('Nairobi-Westlands', 'Nairobi-Westlands'),
    ('Kiambu', 'Kiambu'),
    ('Kisii', 'Kisii'),
    ('Kikuyu', 'Kikuyu'),
    ('Nakuru', 'Nakuru'),
    ('Eldoret', 'Eldoret'),
    ('Kakamega', 'Kakamega'),
    ('Kisumu', 'Kisumu'),
    ('Mombasa', 'Mombasa'),      
)
gender=(
    ('male', 'male'),
    ('female', 'female'),
)
services=(
    ('Obedience Training', 'Obedience Training'),
    ('Trick Skill Training', 'Trick Skill Training'),
    ('Behavior Modification', 'Behavior Modification'),
    ('Puppy Training', 'Puppy Training'),
    ('Security Program', 'Security Program'),
    ('Separation Anxiety', 'Separation Anxiety')
)