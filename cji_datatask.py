import pandas as pd

#Import client data from excel file that were saved as csv files (with dates formated to include 4 digits for the year)
client_data = pd.read_csv('rda_data_excercise_client.csv')

#Transform Date of Birth, Case Opened Date, and Closed Date to datetime
client_data['Date of Birth'] = pd.to_datetime(client_data['Date of Birth'])
client_data['Case Opened Date'] = pd.to_datetime(client_data['Case Opened Date'])
client_data['Case Closed Date'] = pd.to_datetime(client_data['Case Closed Date'])

## Determine the age of clients at the time of case opening and add it to the client data frame
for client in client_data:
    #Calculate the age of the client at the time of case opening in years rounded down the year and add it to the client data frame
    client_data['Age at Case Opening'] = (client_data['Case Opened Date'].dt.year 
                                          - client_data['Date of Birth'].dt.year).astype(int)

# Identify client id of clients with an Age at Case Opening of less than 15 years
client_age_less_than_15 = client_data[client_data['Age at Case Opening'] < 15]
#Remove clients with an Age at Case Opening of less than 15 years from the client data frame
client_data = client_data[client_data['Age at Case Opening'] >= 15]

#Import program data 
program_data = pd.read_csv('rda_data_excercise_program.csv')

#Remove rows with a client id included in the client_age_less_than_15 data frame from the program data frame
program_data = program_data[~program_data['Person ID'].isin(client_age_less_than_15['Person ID'])]

#Transform Program Start Date to datetime
program_data['Date'] = pd.to_datetime(program_data['Date'])

#Create two data frames for clients with age at case opening less than 25 and greater than or equal to 25
client_data_less_than_25 = client_data[client_data['Age at Case Opening'] < 25]
client_data_greater_than_or_equal_to_25 = client_data[client_data['Age at Case Opening'] >= 25]

###########################################################################
###########################################################################
###########################################################################

#Question 1: How many clients atteneded individual counseling in 2019?

#Create a data frame for clients who attended individual counseling in 2019 with the attended column equal to Y
individual_counseling_2019 = program_data[(program_data['Program'] == 'Individual Counseling') 
                                          & (program_data['Date'].dt.year == 2019) 
                                          & (program_data['Attended'] == 'Y')]

#Create a list of the unique client ids for clients who attended individual counseling in 2019
individual_counseling_2019_client_ids = individual_counseling_2019['Person ID'].unique()

#Identify the clients who attended individual counseling in 2019 from the client data frame
client_data_individual_counseling_2019 = client_data[client_data['Person ID'].isin(individual_counseling_2019_client_ids)]

#Print the number of clients who attended individual counseling in 2019 with an age of less than 25
print('The number of clients who attended individual counseling in 2019 with an age of less than 25 is ' + str(
    len(client_data_individual_counseling_2019[client_data_individual_counseling_2019['Age at Case Opening'] < 25])))

#Print the number of clients who attended individual counseling in 2019 with an age of greater than or equal to 25
print('The number of clients who attended individual counseling in 2019 with an age of greater than or equal to 25 is ' + 
      str(len(client_data_individual_counseling_2019[client_data_individual_counseling_2019['Age at Case Opening'] >= 25])))

###########################################################################
###########################################################################
###########################################################################

#Question 2: 2.	How many individuals attended at least one group counseling session in 2019?

#Create a data frame for clients who attended group counseling in 2019 with the attended column equal to Y
group_counseling_2019 = program_data[(program_data['Program'] == 'Group Class') & (program_data['Date'].dt.year == 2019) & (program_data['Attended'] == 'Y')]

#Create a list of the unique client ids for clients who attended group counseling in 2019
group_counseling_2019_client_ids = group_counseling_2019['Person ID'].unique()

#Identify the clients who attended group counseling in 2019 from the client data frame
client_data_group_counseling_2019 = client_data[client_data['Person ID'].isin(group_counseling_2019_client_ids)]

#Print the number of clients who attended group counseling in 2019 with an age of less than 25
print('The number of clients who attended group counseling in 2019 with an age of less than 25 is ' 
      + str(len(client_data_group_counseling_2019[client_data_group_counseling_2019['Age at Case Opening'] < 25])))
#Print the number of clients who attended group counseling in 2019 with an age of greater than or equal to 25
print('The number of clients who attended group counseling in 2019 with an age of greater than or equal to 25 is ' 
      + str(len(client_data_group_counseling_2019[client_data_group_counseling_2019['Age at Case Opening'] >= 25])))

###########################################################################
###########################################################################
###########################################################################

#Questions 3: Of the individuals who attended at least one individual counseling session, what is the average number of individual counseling sessions attended by year?

#Create a data frame for clients who attended individual counseling with the attended column equal to Y
individual_counseling = program_data[(program_data['Program'] == 'Individual Counseling') & (program_data['Attended'] == 'Y')]

#Print the average number of individual counseling sessions attended per individual per year for those aged 25 or older
print('Of the individuals who attended at least one individual counseling session, the average number of individual counseling sessions attended by year for those aged 25 or older\n' 
      + str(individual_counseling[individual_counseling['Person ID'].
                                  isin(client_data_greater_than_or_equal_to_25['Person ID'])].
                                  groupby([individual_counseling['Date'].dt.year, 'Person ID']).size().groupby(level=0).mean()))

#Print the average number of individual counseling sessions attended per individual per year for those aged less than 25
print('Of the individuals who attended at least one individual counseling session, the average number of individual counseling sessions attended by year for those aged less than 25\n' 
      + str(individual_counseling[individual_counseling['Person ID'].
                                  isin(client_data_less_than_25['Person ID'])].
                                  groupby([individual_counseling['Date'].dt.year, 'Person ID']).size().groupby(level=0).mean()))

###########################################################################
###########################################################################
###########################################################################

#Question 5: Among closed cases, which individual had the highest group counseling session attendance rate, excluding cancelled sessions?

#Create a data frame of clients with closed cases
closed_cases = client_data[client_data['Case Closed Date'].notnull()]

#Create a data frame for clients who attended group counseling with the attended column equal to Y
group_counseling = program_data[(program_data['Program'] == 'Group Class') & (program_data['Attended'] == 'Y')]

#Print the first name, last name, and client id of the client with the highest group counseling session attendance rate with an age 25 or older, only among clients with close dates. 
print('Excluding cancelled sessions and open cases, this client had the highest group counseling session attendance rate with an age of 25 or older\n' 
      + str(closed_cases[closed_cases['Person ID'].
                 isin(group_counseling[group_counseling['Person ID'].
                                       isin(client_data_greater_than_or_equal_to_25['Person ID'])].
                                       groupby('Person ID').size().sort_values(ascending=False).head(1).index)]
                                       [['First Name', 'Last Name', 'Person ID']]))

#Print the first name, last name, and client id of the client with the highest group counseling session attendance rate with an age of less than 25, only among clients with close dates.
print('Excluding cancelled sessions and open cases, this client had the highest group counseling session attendance rate with an age of less than 25\n' + 
      str(closed_cases[closed_cases['Person ID'].
                 isin(group_counseling[group_counseling['Person ID'].
                                       isin(client_data_less_than_25['Person ID'])].
                                       groupby('Person ID').size().sort_values(ascending=False).head(1).index)]
                                       [['First Name', 'Last Name', 'Person ID']]))

###########################################################################
###########################################################################
###########################################################################

#Question 6: Among closed cases, identify the individual(s) that had an individual counseling session attendance rate (excluding cancelled sessions) in the bottom quartile.

#Print the first name, last name and client id of the clients in the bottom quartile of individual counseling session attendance rate with an age of 25 or older, only among clients with close dates.
print('Excluding cancelled sessions and open cases, these clients aged >=25 had individual counseling session attendance rates in the bottom quartile\n' 
      + str(closed_cases[closed_cases['Person ID'].
                 isin(individual_counseling[individual_counseling['Person ID'].
                                            isin(client_data_greater_than_or_equal_to_25['Person ID'])].
                                            groupby('Person ID').size().sort_values(ascending=True).
                                            head(round(len(individual_counseling[individual_counseling['Person ID'].
                                                                                 isin(client_data_greater_than_or_equal_to_25['Person ID'])].
                                                                                 groupby('Person ID').size()) / 4)).index)]
                                                                                 [['First Name', 'Last Name', 'Person ID']]))

#Print the first name, last name and client id of the clients in the bottom quartile of individual counseling session attendance rate with an age of less than 25, only among clients with close dates.
print('Excluding cancelled sessions and open cases, these clients aged <25 had individual counseling session attendance rates in the bottom quartile\n' 
      + str(closed_cases[closed_cases['Person ID'].
                 isin(individual_counseling[individual_counseling['Person ID'].
                                            isin(client_data_less_than_25['Person ID'])].
                                            groupby('Person ID').size().sort_values(ascending=True).
                                            head(round(len(individual_counseling[individual_counseling['Person ID'].
                                                                                 isin(client_data_less_than_25['Person ID'])].
                                                                                 groupby('Person ID').size()) / 4)).index)]
                                                                                 [['First Name', 'Last Name', 'Person ID']]))

###########################################################################
###########################################################################
###########################################################################