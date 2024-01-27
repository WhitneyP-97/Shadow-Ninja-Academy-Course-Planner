import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from pyscript import document

data = {'course_name': ['Cloaking','Cloaking','Karate','Karate','Karate','Karate','Kenjutsu','Shuriken Throwing','Poisons I','Poisons II','Squad Tactics I',
                        'The Art of War','The Art of War','History of Modern Warfare','Honoring the Code of Bushido','Calculus I','Dodgeball'],
        'course_id': ['DS101-1','DS101-2','MA101-1','MA101-2','MA101-3','MA101-4','MA210-1','MA223-1','MA405-1','MA406-1','TAC101-1',
                      'STR101-1','STR101-2','STR337-1','ET101-1','GS210-1','ELE225-1'],
        'section': [1,2,1,2,3,4,1,1,1,1,1,
                    1,2,1,1,1,1],
        'capacity': [15,15,50,50,50,30,15,15,10,10,8,
                     100,50,30,100,30,25],
        'registered': [0,0,0,0,0,0,0,0,0,0,0,
                       0,0,0,0,0,0],
        'professor': ['Kageyama, Kenji','Nakashima, Ichiro','Nakashima, Ichiro','Nakashima, Ichiro','Nakashima, Ichiro','Williams, Chester M.','Kageyama, Kenji',
                      'Kageyama, Kenji','Watanabe, James','Watanabe, James','Miyazaki, Machiko',
                      'Devonshire, Wilson','Suzuki, Kotaro','Mendez, Maria L.','Suzuki, Kotaro','Iwata, Kenshin','Smith, Dan'],
        'semester': ['fall2023','fall2023','fall2023','fall2023','fall2023','fall2023','fall2023','fall2023','fall2023','fall2023','fall2023',
                     'fall2023','fall2023','fall2023','fall2023','fall2023','fall2023'],
        'department': ['disguises','disguises','martial_arts','martial_arts','martial_arts','martial_arts','martial_arts','martial_arts','martial_arts','martial_arts','tactics',
                       'strategy','strategy','strategy','ethics','general_studies','electives'],
        'location': ['tokyo','tokyo','tokyo','tokyo','kyoto','london','tokyo','tokyo','sapporo','sapporo','nyc',
                     'london','kyoto','london','kyoto','tokyo','nyc'],
        'course_type': ['in_person','in_person','in_person','in_person','in_person','in_person','in_person','in_person','hybrid','hybrid','in_person',
                        'in_person','hybrid','online','online','online','in_person'],
        'schedule': ['M 18-21','TH 14-15.5','MW 14-15.5','M 8.5-11.5','M 18-21','F 18-21','MF 16-17.5','MH 14-15.5','TW 16-17.5','H 8.5-11.5','H 12-15',
                  'MWF 12-13','MWH 16-17','TH 14-15.5','H 18-21','W 18-21','F 12-15']}
	#Thursday = H, Sunday = U

courses = pd.DataFrame.from_dict(data)
reg_courses = []

def coursesToHTML(courselist):
	#courselist is a dataframe
	line = f'<table><tr><th>Course Name</th><th>Course ID</th><th>Section</th><th>Professor</th><th>Department</th><th>Semester</th><th>Location</th><th>Schedule</th><th>Type</th></tr>'

	for i in range(len(courselist)):
		line = line+f'<tr><td>{courselist.iloc[i]["course_name"]}</td><td>{courselist.iloc[i]["course_id"]}</td><td>{str(courselist.iloc[i]["section"])}</td><td>{courselist.iloc[i]["professor"]}</td><td>{courselist.iloc[i]["department"]}</td><td>{courselist.iloc[i]["semester"]}</td><td>{courselist.iloc[i]["location"]}</td><td>{scheduleToClock(courselist.iloc[i]["schedule"])}</td><td>{courselist.iloc[i]["course_type"]}</td></tr>'

	line = line + f'</table>'
	return line

def scheduleToClock(schedule):
	#changes a schedule format from something like MW 18-21 meaning Monday and Wednesday from 6pm to 9pm to MW 6:00PM-9:00PM for laymen to understand, also replaces H with Th (for Thursday) and U for Su (for Sunday)
	days, time = schedule.split(' ')
	days = days.replace('H','Th')
	days = days.replace('U','Su')
	times = time.split('-')
	for i in range(len(times)):
		if '.' not in times[i]:
			times[i] = times[i]+'.0'
		hours, minutes = times[i].split('.')
		ampm = 'AM'
		if (int)(hours) <=12:
			ampm = 'AM'
		else:
			hours = (int)(hours)-12
			ampm = 'PM'
		minutes = (float)('0.'+minutes)
		minutes = (str((int)(60*(float)(minutes)))).zfill(2)
		times[i] = (str)(hours)+':'+(str)(minutes)+ampm
	return days + ' ' + (str)(times[0]) + '-' + (str)(times[1])

def parseSchedule(schedule):
	#schedule is in the format of something like MW 18-21 meaning Monday and Wednesday from 6pm to 9pm
	days, time = schedule.split(' ')
	begin, end = time.split('-')
	sched = []

	for i in days:
		sched.append([i])
	for i in range(len(sched)):
		sched[i].append((float)(begin))
		sched[i].append((float)(end))
	return sched

def displayRegistered():
	courselist = courses.copy()
	courselist = courselist[courselist['course_id'].isin(reg_courses)]
	return coursesToHTML(courselist)

def checkSchedule(schedule, registered, courses):
	courselist = courses[courses['course_id'].isin(registered)]
	sched = parseSchedule(schedule)

	for i in range(len(courselist)):
		sched2 = parseSchedule(courselist.iloc[i]['schedule'])
		for j in sched:
			#midnight classes detector
			if (float)(j[2]) < (float)(j[1]):
				j[2] = j[2]+24
			for k in sched2:
				if (float)(k[2]) < (float)(k[1]):
					k[2] = k[2]+24
				if j[1]>=k[1] and j[1]<=k[2]:
					return False;
				elif j[2]>=k[1] and j[2]<=k[2]:
					return False;
				elif k[1]>=j[1] and k[1]<=j[2]:
					return False
				elif k[2]>=j[1] and k[2]<=j[2]:
					return False
	return True

def plotSchedule(registered, courselist):
	#to-do: label bars
	courselist2 = courselist.copy()
	courselist2 = courselist2[courselist['course_id'].isin(registered)]
	scheds = []
	print(scheds)
	print(courselist2)

	if len(registered) > 1:
		for i in range(len(courselist2)):
			scheds.append([courselist2['course_id'].iloc[i] , parseSchedule(courselist2['schedule'].iloc[i])])

	else:
		scheds.append([courselist2['course_id'].iloc[0] , parseSchedule(courselist2['schedule'].iloc[0])])

	
	for i in range(len(scheds)):
		for j in range(len(scheds[i][1])):
			if (float)(scheds[i][1][j][2]) < (float)(scheds[i][1][j][1]):
				#midnight detector, splits midnight classes into two sections
				i1 = [scheds[i][1][j][0],scheds[i][1][j][1],24]
				i2 = [scheds[i][1][j][0],0,scheds[i][1][j][2]]
				scheds[i][1][j] = i1
				scheds[i][1].append(i2)
				j = j-1

	print(scheds)

	def convertBar(sched, registered):
		#sched in the form of [courseid, [[day, begin, end], [day, begin, end]]]
		#returns array of [courseid, [heights array],[bottoms array]]
		results = []
		for i in sched:
			for j in i[1]:
				print(j[0])
				heights = [0,0,0,0,0,0,0]
				bottoms = [0,0,0,0,0,0,0]
				if j[0] == 'M':
					heights[0] = (float)(j[2])-(float)(j[1])
					bottoms[0] = (float)(j[1])
				elif j[0] == 'T':
					heights[1] = (float)(j[2])-(float)(j[1])
					bottoms[1] = (float)(j[1])
				elif j[0] == 'W':
					heights[2] = (float)(j[2])-(float)(j[1])
					bottoms[2] = (float)(j[1])
				elif j[0] == 'H':
					heights[3] = (float)(j[2])-(float)(j[1])
					bottoms[3] = (float)(j[1])
				elif j[0] == 'F':
					heights[4] = (float)(j[2])-(float)(j[1])
					bottoms[4] = (float)(j[1])
				elif j[0] == 'S':
					heights[5] = (float)(j[2])-(float)(j[1])
					bottoms[5] = (float)(j[1])
				elif j[0] == 'U':
					heights[6] = (float)(j[2])-(float)(j[1])
					bottoms[6] = (float)(j[1])
				results.append([i[0],heights,bottoms])
		return results

	bars = convertBar(scheds,registered)

	def plotBars(b):
		for i in b:
			plt.bar(['M','T','W','Th','F','S','Su'],i[1],bottom=i[2], label = i[0])
	plotBars(bars)
	plt.show()
	print(bars)
	return

def add(event):
	return

def add_manual(event):
	input = document.querySelector("#courseID")
	courseID = input.value

	output = document.querySelector("#adddd")

	if courseID not in courses['course_id'].to_list():
		output.innerHTML = f'<p>Invalid Course</p>'
		return

	#should be only one course as course_id should be unique, but iloc[0] to prevent a bug just in case somehow theres more than one
	course = courses[courses['course_id']==courseID].iloc[0]

	courseID1 = courseID.split('-')[0]

	reg_courses2 = reg_courses.copy()
	for i in range(len(reg_courses2)):
		reg_courses2[i] = reg_courses2[i].split('-')[0]

	if courseID1 in reg_courses2:
		output.innerHTML = f'<p>Course: "{course["course_name"]}" already added. Please remove other sections of the course to register.</p>'
		return

	if checkSchedule(course['schedule'], reg_courses, courses):
		reg_courses.append(courseID)
		output.innerHTML = f'<p>Added.</p>'
		output = document.querySelector("#schedule")
		output.innerHTML = displayRegistered()
		plotSchedule(reg_courses,courses)
	else:
		output.innerHTML = f'<p>Time conflict error. Not added.</p>'
	return

def search_search(event):
	courselist = courses.copy()

	input = document.querySelector("#course_name")
	course_name = input.value
	input = document.querySelector("#course_id")
	course_id = input.value
	input = document.querySelector("#section")
	section = input.value
	input = document.querySelector("#professor")
	professor = input.value
	input = document.querySelector("#department")
	department = input.value
	input = document.querySelector("#semester")
	semester = input.value
	input = document.querySelector("#location")
	location = input.value
	input = document.querySelector("#in_person")
	in_person = input.value
	input = document.querySelector("#online")
	online = input.value
	input = document.querySelector("#hybrid")
	hybrid = input.value

	if course_name != '':
		courselist = courselist[courselist['course_name'].str.contains(course_name)]
	if course_id != '':
		courselist = courselist[courselist['course_id'].str.contains(course_id)]
	if section != '':
		courselist = courselist[courselist['section']==section]
	if professor != '':
		courselist = courselist[courselist['professor'].str.contains(professor)]
	if department != 'all':
		courselist = courselist[courselist['department']==department]
	if semester != 'all':
		courselist = courselist[courselist['semester']==semester]
	if location != 'all':
		courselist = courselist[courselist['location']==location]
	if in_person != 'in_person':
		courselist = courselist[courselist['course_type']!='in_person']
	if online != 'online':
		courselist = courselist[courselist['course_type']!='online']
	if hybrid != 'hybrid':
		courselist = courselist[courselist['course_type']!='hybrid']
		

	output = document.querySelector("#results")
	line = f'<table><tr><th>Course Name</th><th>Course ID</th><th>Section</th><th>Professor</th><th>Department</th><th>Semester</th><th>Location</th><th>Schedule</th><th>Type</th><th>Add</th></tr>'

	for i in range(len(courselist)):
		line = line+f'<tr><td>{courselist.iloc[i]["course_name"]}</td><td>{courselist.iloc[i]["course_id"]}</td><td>{str(courselist.iloc[i]["section"])}</td><td>{courselist.iloc[i]["professor"]}</td><td>{courselist.iloc[i]["department"]}</td><td>{courselist.iloc[i]["semester"]}</td><td>{courselist.iloc[i]["location"]}</td><td>{scheduleToClock(courselist.iloc[i]["schedule"])}</td><td>{courselist.iloc[i]["course_type"]}</td><td><button py-click="add" class="add_button">Add</button></td></tr>'

	line = line + f'</table>'
	output.innerHTML = line

	return
