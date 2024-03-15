from datetime import datetime, timedelta
from storage.cloudStorage import B2Storage

TICKET_NUMBER=0

data = B2Storage.read_pickle('classic_punk_party')

duration = data[TICKET_NUMBER]['event_duration']

# Get the current date and time, then subtract 3 hours
now = datetime.now() - timedelta(hours=3)

# Break down the components
start_year = now.year
start_month = now.month
start_day = now.day
start_hour = now.hour
start_minute = now.minute
start_second = now.second

# Get the current date and time, of the event durratio
end = datetime.now() - timedelta(hours=3) + timedelta(
                                            days=duration['days'] , 
                                            hours=duration['hours'],
                                            minutes=duration['minutes']
                                            )

# Break down the components
end_year = end.year
end_month = end.month
end_day = end.day
end_hour = end.hour
end_minute = end.minute
end_second = end.second

print()


# Target date and time for comparison
# target_date_start = datetime(2024, 3, 16)
target_date_start = datetime.strptime(data[TICKET_NUMBER]['event_date'], '%B %d %Y')

target_time_start = datetime.strptime(f"{data[TICKET_NUMBER]['event_date']} {data[TICKET_NUMBER]['event_start_time']}", 
                                      '%B %d %Y %I:%M %p')

target_time_end = target_time_start + timedelta(
                                            days=duration['days'] , 
                                            hours=duration['hours'],
                                            minutes=duration['minutes']
                                            )

print()

if now < target_date_start:
    # Calculate difference
    delta = target_date_start - now
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"BEFORE - {days} days, {hours} hours and {minutes} minutes until the start")
elif now > target_time_end:
    print("EVENT HAS HAPPENED")
else:
    if target_time_start <= now <= target_time_end:
        print("HAPPENING")
    elif now < target_time_start:
        # Calculate difference
        delta = target_time_start - now
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"{hours} hours and {minutes} minutes until the event")
    else:
        print("EVENT HAS HAPPENED")
        
print()


