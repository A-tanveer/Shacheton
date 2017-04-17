import re
import datetime


def find_date(url, dateStr):
    if url.startswith('http://sylhetsangbad24'):
        dateStr = dateStr.replace('ইং', '')
        if len(dateStr) == 0:
            return None
    if url.startswith('http://www.bhorerkagoj') or url.startswith('http://bangla.samakal') or url.startswith('jugantor') or url.startswith('kaler'):
        return get_date(url, 1)
    elif url.startswith('http://www.sylhetnews24'):
        return get_date(dateStr, 2)
    elif url.startswith('http://dailysylhet') or url.startswith('http://www.prothom-alo') or url.startswith('http://sylhetsangbad24'):
        return get_date_bangla(url, dateStr)


# extract date from url.
# x = line no (starts from zero) and y = date separation character 1 for '/' and 2 for '-'
def get_date(data, y):
    if y == 1:
        match = re.search(r'\d{4}/\d{2}/\d{2}', data)
        x = match.group().split('/')
        date = datetime.datetime(int(x[0]),int(x[1]),int(x[2]))
        # date = datetime.datetime.strptime(match.group(), '%Y/%m/%d').date()
        # print(date)
    elif y == 2:
        match = re.search(r'\d{4}-\d{2}-\d{2}', data)
        x = match.group().split('-')
        date = datetime.datetime(int(x[0]), int(x[1]), int(x[2]))
        # date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
    return date


# extract date from bangla text. if date is like জানুয়ারি ০৫, ২০১৫ or something else... #hardest one, took days to figure out.
def get_date_bangla(url, data):

    months = [' ', 'জানুয়ারি', 'ফেব্রুয়ারি', 'মার্চ', 'এপ্রিল', 'মে', 'জুন', 'জুলাই', 'আগস্ট', 'সেপ্টেম্বর',
              'অক্টোবর', 'নভেম্বর', 'ডিসেম্বর']

    bang = '০১২৩৪৫৬৭৮৯'
    eng = '0123456789'
    if data.startswith(' '):
        data = data[1:]
    date_data = data.replace(',', '').replace('.', '').replace('  ', ' ').translate({ord(x): y for (x, y) in zip(bang, eng)})  # stackoverflow rocks ;)

    if url.startswith('http://sylhetsangbad24'):
        date_data = data.replace(',', '').replace('.', '').replace(':','').replace('  ', ' ').translate({ord(x): y for (x, y) in zip(bang, eng)})

    x = date_data.split()

    for i in months:
        if i in x:
            month = months.index(i)
            break
    try:
        if url.startswith('http://dailysylhet'):
            day = int(x[9])
            year = int(x[10])
        elif url.startswith('http://www.prothom-alo') and data.startswith('আপডেট'):
            day = int(x[3])
            year = int(x[4])
        elif url.startswith('http://www.prothom-alo'):
            day = int(x[2])
            year = int(x[3])
        elif url.startswith('http://sylhetsangbad24'):
            day = int(x[0])
            year = int(x[2])
    except Exception:
        print(data)
        return
    try:
        date = datetime.datetime(year,month,day)
    except UnboundLocalError:
        print(data)
        return
    # datestr = year + '-' + month + '-' + day
    # date = datetime.datetime.strptime(datestr, '%Y-%m-%d').date()
    return date


# extract date from url if url is in the sixth line date separated by / #not needed anymore
def get_date2():
    f = open('content.txt', encoding="utf8")
    text = f.readlines()
    x = 0
    for line in text:
        x += 1
        if x == 6:
            data = repr(line)
            match = re.search(r'\d{4}-\d{2}-\d{2}', data)
            date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
            break
    return date


# extract date from url if url is in the third line date separated by - #not needed anymore
def get_date_bn():
    f = open('content.txt', encoding="utf8")
    text = f.readlines()
    x = 0
    for line in text:
        x += 1
        if x == 3:
            data = repr(line)
            match = re.search(r'\d{4}-\d{2}-\d{2}', data)
            date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
            break
    return date


# extract date from text. if date is in bangla numeric form and separated by '-' #can be used
# just a few line needed to make it useful like 1st method. hint - arguments
def get_date3():
    f = open('content.txt', encoding="utf8")
    text = f.readlines()
    x = 0
    for line in text:
        x += 1
        if x == 6:
            data = repr(line)
            bang = '০১২৩৪৫৬৭৮৯'
            eng = '0123456789'
            # http://stackoverflow.com/questions/3031045/how-come-string-maketrans-does-not-work-in-python-3-1
            ddata = data.translate({ord(x): y for (x, y) in zip(bang, eng)})
            # print(ddata)
            match = re.search(r'\d{4}-\d{2}-\d{2}', ddata)

            date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
            break
    return date


# name says it all......
def get_date_of_incident(date):
    f = open('content.txt', encoding='utf8')
    lines = f.readlines()
    x = 0
    content = lines[6].split('।')
    for line in content:
        for word in line.split():
            if 'পরশু' in repr(word):
                x = 2
                break
            elif 'কালকে' in repr(word):
                x = 1
                break
            elif 'গতকাল' in repr(word):
                x = 1
                break
            elif 'আজ' in repr(word):
                x = 0
                break

    # date = datetime.datetime.strptime(datestr, '%Y/%m/%d')
    incident_date = date - datetime.timedelta(days=x)
    return incident_date

