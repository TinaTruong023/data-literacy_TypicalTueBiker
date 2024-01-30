## Events/Holidays
Data should be loaded using the dedicated [Event Data Loader](LoadEventsData.py)

 - [COVID Dates](evd_covid_date.csv) contains events like lockdowns, school closures, mask requirements and other COVID related events.
 - [COVID Info](evd_covid_info.csv) supplies the necessary information to certain events.
 - [Holiday](evd_holiday.csv) all national holidays and regional holidays in Baden-Württemberg.
 - [Lecture](evd_lecture.csv) the lecture periods of the Eberhard-Karls-Universität Tübingen.
 - [Semester](evd_semester.csv) start and end dates of the semesters at the Eberhard-Karls-Universität Tübingen.
 - [Uni breaks](evd_unibreak.csv) university during-semester breakes.
 - [OEPV](evd_oepv.csv) contains the periods where special OEPV tickets were introduced in Baden-Württemberg and germany.
 - [Schoolbreaks](evd_schoolbreak.csv) periods of schoolbreaks in Baden-Württemberg.

The formats slightly differ depending on the required format of the events.
All tables contain a `start` and `end` timestamp for the given entry.
