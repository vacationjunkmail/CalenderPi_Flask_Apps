import datetime,re
from pytz import timezone

def diff_minutes(t):
	utc = timezone('utc')
	n = datetime.datetime.now(utc)
	t = utc.localize(t)
	diff = n - t
	diff_minutes = diff.seconds/60
	return diff_minutes

def host_regex(a,h):
	h = re.sub(r':\d{1,}','',h)
	h = re.sub(r'\d{1,}\.\d{1,}\.\d{1,}\.\d{1,}',a,h)
	h = re.sub(r':\d{1,}','',h)
	return h 
