## Events/Holidays
Data should be loaded using the dedicated [Event Data Loader](../../src/LoadEventsData.py)

 - [COVID Dates](evd_covid_date.csv) Contains events like lockdowns, school closures, mask requirements and other COVID related events.
 - [COVID Info](evd_covid_info.csv) Supplies the necessary information to certain events.
 - [Holiday](evd_holiday.csv) All national holidays and regional holidays in Baden-Württemberg.
 - [Lecture](evd_lecture.csv) The lecture periods of the Eberhard-Karls-Universität Tübingen.
 - [Semester](evd_semester.csv) Start and end dates of the semesters at the Eberhard-Karls-Universität Tübingen.
 - [Uni breaks](evd_unibreak.csv) University during-semester breakes.
 - [OEPV](evd_oepv.csv) Contains the periods where special OEPV tickets were introduced in Baden-Württemberg and germany.
 - [Schoolbreaks](evd_schoolbreak.csv) Periods of schoolbreaks in Baden-Württemberg.

The formats slightly differ depending on the required format of the events.
All tables contain a `start` and `end` timestamp for the given entry.
