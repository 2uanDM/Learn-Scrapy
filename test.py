import calendar 
from datetime import datetime

# print(list(calendar.month_name).index('January'))

born_year: str = '1980'
born_month: str = 'January'
born_day: str = '1'

dob: datetime.date = datetime.strptime(f'{born_year} {born_month} {born_day}', '%Y %B %d').date()

print(datetime.strftime(dob, '%d/%m/%Y'))