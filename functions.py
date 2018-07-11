import json
import urllib.request
from bs4 import BeautifulSoup

md = json.load(open('data.json'))

def check_subject(subj):
    for i in range(len(md["subjects"])):
        if subj.lower() in md["subjects"][i]["names"]:
            return [True, md["subjects"][i]["code_name"], i, md["subjects"][i]["book"]["book_code"], md["subjects"][i]["isLong"]] #5 items
        if i == len(md["subjects"])-1:
            return [False, 'ERROR']

def analyze_book(subject_code):
    u = md["subjects"][subject_code]["book"]["units"]
    depth = 1
    if len(u) > 1: depth += 1
    if len(u[0]) > 1: depth += 1
    return depth


def check_lesson(subject_code, unit, lesson): #unit is int, lesson is str
    l = md["subjects"][subject_code]["book"]["units"][unit]
    if lesson.isdigit():
        if int(lesson) > 0 and int(lesson) < (len(l) + 1):
            return [True]
        else:
            return [False]
    else:
        return [False]

def check_task(subject_code, unit, lesson, task):
    t = md["subjects"][subject_code]["book"]["units"][unit][lesson]
    if task.isdigit():
        if int(task) > 0 and int(task) < t:
            return [True]
        else:
            return [False]
    else:
        return [False]

def getImgLinks(subject, author, unit, lesson, task, depth, isLong = True): #STUB
    page_link = ''
    print(subject, author, unit, lesson, task, depth, isLong)
    if depth == 1 and isLong == True:
        page_link = 'https://resheba.com/gdz/' + subject + '/11-klass/' + author + '/e:0-a:' + str(task-1)
    elif depth == 1 and isLong == False:
        page_link = 'https://resheba.com/gdz/' + subject + '/11-klass/' + author + '/' + str(task)
    elif depth == 2 and isLong == True:
        page_link = 'https://resheba.com/gdz/' + subject + '/11-klass/' + author + '/e:' + str(lesson) + '-a:' + str(task-1)
    elif depth == 2 and isLong == False:
        page_link = 'https://resheba.com/gdz/' + subject + '/11-klass/' + author + '/' + str(lesson+1) + '-' + str(task)
    elif depth == 3:
        page_link = 'https://resheba.com/gdz/' + subject + '/11-klass/' + author + '/e:' + str(unit) + '-t:'+ str(lesson) + '-a:' + str(task-1)
    print(page_link)
    html = urllib.request.urlopen(page_link).read()
    soup = BeautifulSoup(html, 'html.parser')
    imgTags = soup.select('img[src^="//resheba.com/attachments/images/tasks/"]')
    links = []
    for i in range(len(imgTags)):
        links.append(str(imgTags[i]['src'])[2:])
    print(links)
    return links
