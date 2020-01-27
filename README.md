# ActiveUsersModule
Find the active users per day from the event logs

Problem statement:

We have multiple apps emitting different kinds of events, such as when a push notification has
been received, when a certain screen was viewed, or the app has been updated. We also get
an event called “user_engagement” for each session of use, with the time the user was active in
the app.
We would like to be able to plot the number of active users per day. Our analytics database is
an SQL database, so the data from the event should bre loaded in the following table:
active_user_table

Field name Type Mode Description

date DATE REQUIRED

active_user_count INTEGER REQUIRED

1. Using the data in the attached json file, create a script to load the data from the events
into the table above. You can use python, or any language you feel familiar with. Please
provide instructions on how to run the script:

Solution:

I have created a pyspark script to extract data from json file, apply the transformations and load the data in MYSQL database.

As I have access to limited resources,I used the below technologies or resources to complete the task.

Cloudera quickstart VM-5.13.0
Python-2.6.6
spark -1.6
MySQL 


create a table in MySql named active_user_table.

create table active_user_table(date DATE NOT NULL,active_user_count INTEGER NOT NULL);

change the environment parameters in the activeusers.properties file.

# Spark job will be running in the below execution mode local or yarn-client(code supports only these two modes)
execution.mode = local 
# inpurt json file name moved to hdfs location by using (hadoop fs -copyFromLocal ./bq-results-sample-data.json /user/inputfiles/bq-results-sample-data.json)
file.name = /user/inputfiles/bq-results-sample-data.json
# jdbc url to connect to mysql (jdbc:mysql://hostname:port/dbname?user=username&password=password
jdbc.url = jdbc:mysql://localhost:3306/events?user=root&password=******
# table name
table.name = active_user_table
# spark write mode append or overwrite
write.mode = append

move both python script .py file and .properties file into one location.

and run the below command:

spark-submit activeusers.py <env>
  
Ex:spark-submit activeusers.py dev 

I have initiated the logger but didn't get time to complete it properly.

2. How would you design the ETL process for it to automatically update daily?
How would you scale this process if we got tens or hundreds of millions of events per
day?

Solution:

The script I have given can be run as a scheduled script with minor changes. I have to add the proper logging and I have to create
different modules for each extract, transform and loading steps to get more clear idea of what we are doing in the script.

Even though this script will take much time for less number of records It will give the best results on huge data if you add some of the 
configuration settings like resource allocation or by increasing the parallelism.

3. Suggest any target architecture to cater for this growth.

Solution:

I would suggest using pyspark as the ETL tool to work on these type of scenarios.As It works as a replacement to traditional ETL tools.
If you are concern about building a cluster, allocating resources and maintaining the cluster. I would suggest to go with a cloud service.


Notes:

1.event_date is UTC. Our users are based in the US.

event_date is UTC which is a date format(yyyyMMdd).I am not clear on which UTC region I have to consider. As I used  the date for 
group by condition,I assume there won't be any issue for time being.

2. We say a user is active if the engagement time is at least 3 seconds and any valuable
events occurred at least once.

I have filtered the user_engagement events out of all the events and fetched all the user ids having engagement_time_msec >=3000, I did
not understand much about any valuable events occured atleast once condition.As per my understanding all the events from json file
occured atleast once.I am clear about this bit of requirement.
