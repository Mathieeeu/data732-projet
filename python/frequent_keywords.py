from datetime import datetime

# Test simple avec un format 'YYYY-Month'
date_str = '2021-January'
date_obj = datetime.strptime(date_str, "%Y-%B")
print(date_obj)
