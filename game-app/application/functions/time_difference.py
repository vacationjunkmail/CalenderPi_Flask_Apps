import datetime
from pytz import timezone

def diff_minutes(t):
	utc = timezone('utc')
	n = datetime.datetime.now(utc)
	t = utc.localize(t)
	diff = n - t
	diff_minutes = diff.seconds/60
	return diff_minutes
