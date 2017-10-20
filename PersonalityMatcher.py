import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights
def dataAnalysis(twitterHandle):


    twitter_consumer_key = 'YOUR CONSUMER KEY'
    twitter_consumer_secret = 'YOUR CONSUMER SECRET KEY'
    twitter_access_token = 'YOUR ACCESS TOKEN'
    twitter_access_secret = 'YOUR ACCESS SECRET TOKEN'

    twitter_api = twitter.Api(consumer_key=twitter_consumer_key, consumer_secret=twitter_consumer_secret, access_token_key=twitter_access_token, access_token_secret=twitter_access_secret)

    #Getting the last 200 tweets
    tweets = twitter_api.GetUserTimeline(screen_name=twitterHandle, count=200, include_rts=False)

    #Looping to only get the text part of the tweet and not the metadata part

    counter=1
    for tweet in tweets:
        print (counter),
        print(tweet.text)
        counter+=1

    #Merging all the tweets into one single string

    complete_text = ""

    for tweet in tweets:
            complete_text += tweet.text

    #Using username and platform from cloud platform Bluemix

    pi_username = 'YOUR USERAME'
    pi_password = 'YOUR PASSWORD'

    #It contains the details sent by PeronalityInsights api after analysis

    personality_insights = PersonalityInsights(username=pi_username, password=pi_password)

    #dataAnalysis function: It returns the personality insights in json format; it creates a tree structure for various categories;These categories are broken into personality,values,needs;
    
 
    pi_result = personality_insights.profile(complete_text)
    return pi_result

#The flatten() function below will flatten the JSON structure that the dataAnalysis() function returns from PI.

def flatten(original):
    data = {}
    for c in original['tree']['children']:
        if 'children' in c:
            for c2 in c['children']:
                if 'children' in c2:
                    for c3 in c2['children']:
                        if 'children' in c3:
                            for c4 in c3['children']:
                                if (c4['category'] == 'personality'):
                                    data[c4['id']] = c4['percentage']
                                    if 'children' not in c3:
                                        if (c3['category'] == 'personality'):
                                                data[c3['id']] = c3['percentage']
    return data
#The flatten() function flattens the results from a user and store the results in a dictionary.

#The next step is to write a function that can compare two dictionaries (the user1's and the user2's).

user1_handle = "@narendramodi"
user2_handle = "@ArvindKejriwal"

def compare(dict1, dict2):
    compared_data = {}
    for keys in dict1:
        if dict1[keys] != dict2[keys]:
                compared_data[keys]=abs(dict1[keys] - dict2[keys])
    return compared_data

#dataAnalysis() is used to analyse the data from twitter

user1_result = dataAnalysis(user1_handle)
print("===============================================================================================")
user2_result = dataAnalysis(user2_handle)
print("===============================================================================================")

#Flatten() flattens the JSON structure as returned by the dataAnalysis() function

user1 = flatten(user1_result)
user2 = flatten(user2_result)

#Calculating the difference between traits so as to sort them in order to get top 10 most common traits
compared_results = compare(user1,user2)

#Sorting the diff in traits to get the top 10 most common traits
sorted_result = sorted(compared_results.items(), key=operator.itemgetter(1))

#Getting top 10 most common traits for the two users
print("===============================================================================================")
print('\n\n\n')
print(user1_handle)
print('\n\n')
print(user2_handle)
print('\n\n')

for keys, value in sorted_result[:10]:
    print (keys,":",user1[keys],'->  ',user2[keys],'->  ',compared_results[keys])
    print('\n')

