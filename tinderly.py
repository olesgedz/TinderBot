# -*- coding: utf-8 -*-
#! /usr/bin/env python                                                                                                                                      1,1           Top# encoding: utf8
import argparse
import configparser
from datetime import datetime
import json
from random import randint
import requests
import sys
from time import sleep
import config
import datetime
import pynder
import robobrowser
import re
from messages import messages
#from messagesbot import messagesbot
from messagesfake import messagesfake
from messagesreal import messagesreal

MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; U; en-gb; KFTHWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.16 Safari/535.19"
FB_AUTH = "https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&display=touch&state=%7B%22challenge%22%3A%22IUUkEUqIGud332lfu%252BMJhxL4Wlc%253D%22%2C%220_auth_logger_id%22%3A%2230F06532-A1B9-4B10-BB28-B29956C71AB1%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=464891386855067&ret=login&sdk=ios&logger_id=30F06532-A1B9-4B10-BB28-B29956C71AB1&ext=1470840777&hash=AeZqkIcf-NEW6vBd"







requests.packages.urllib3.disable_warnings()  # Find way around this...
##FBTOKEN=config.FACEBOOK_AUTH_TOKEN
##BID= "100000904101013"
##session = pynder.Session(facebook_id="",facebook_token=FBTOKEN) #config.FACEBOOK_ID, facebook_id=BID, facebook_token=FBTOKEN
print("we are in")
ID = "100021479961277"
##ID = "316458302288682"
##FB_TOKEN = config.FACEBOOK_AUTH_TOKEN
FB_TOKEN = "EAAGm0PX4ZCpsBAIC7sXmi2Ajo1TYEvSzPMXioYaeWZBcLvR0DHIez76UWymDYZASoS3kZBYlHyGpcZBViojZB1Qbr3pBpG4OcuDLUlSOtZAsZBCj4BkNOc77H3Q6ZCOZBepSx9RSZB2B2KJ14NOZBMJNY9qAVlVzTR5cM5ZBWEUyYXEl0wZCOh9A3joWHZAwZB31XurMRl42BxRyiNDAB1sS135RBZCkYcZA54WpZBmZCo0vVKzERdSSU6h03C5Q0YIOZB0bkinFvf0kh1ZBB7BUZAPaQZDZD"





session = pynder.Session(facebook_id=ID, facebook_token=FB_TOKEN)











def log(msg):
    print ( '[' + str(datetime.datetime.now()).encode('utf-8') +']' + ' ' + msg.encode('utf-8')) ##+ str(datetime.datetime.now()) +

def like_or_nope():
    if randint(1, 100) == 31:
        return 'nope'
    else:
        return 'like'

def check_swipes():
    swipes_remaining = session.likes_remaining
    print(swipes_remaining)
    if swipes_remaining == 0:
        return 'Send messages'
def handle_ass():
    print("likes2")
    users = session.nearby_users()
    next(users).like()

def handle_likes_two():
    global session
    if session is not None:
        users = session.nearby_users()
        ##log(str(len(users)) + ' users to swipe')
        for u in users:
            try:
                log('Checking swipes remaining.')
                status = check_swipes()
                if status == 'Send messages':
                    log('Out of swipes. Moving along to send messages.')
                    break
                else:
                    try:
                        action = like_or_nope()
                        if action == 'like':
                            u.like()
                            log('Liked ' + u.name)
                            sleep(randint(2,3))
                        else:
                            u.dislike()
                            log('Disliked ' + u.name)
                            sleep(randint(3,5))
                    except ValueError:
                        log("ValueError")
                        break
                    except pynder.errors.RequestError:
                        log("Pynder Error. Trying to get new auth.")
                        auth = get_access_token(str(config['DEFAULT']['FB_EMAIL']), str(config['DEFAULT']['FB_PASSWORD']), str(config['DEFAULT']['MOBILE_USER_AGENT']), str(config['DEFAULT']['FB_AUTH']))
                        config['DEFAULT']['FACEBOOK_AUTH_TOKEN'] = auth
                        with open('config.ini', 'w') as configfile:
                            config.write(configfile)
                        config.read('config.ini')
                        try:
                            session = pynder.Session(str(config['DEFAULT']['FACEBOOK_ID']), auth)
                        except pynder.errors.RequestError:
                            log("Pynder Error. New auth did NOT work.")
                            break
                        continue
                    except:
                        log("Generic Exception. Don't know what issue is....")
                        break
            except ValueError:
                log("ValueError")
                break
            except pynder.errors.RequestError:
                log("Pynder Error. Trying to get new auth.")
                auth = get_access_token(str(config['DEFAULT']['FB_EMAIL']), str(config['DEFAULT']['FB_PASSWORD']), str(config['DEFAULT']['MOBILE_USER_AGENT']), str(config['DEFAULT']['FB_AUTH']))
                config['DEFAULT']['FACEBOOK_AUTH_TOKEN'] = auth
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                config.read('config.ini')
                try:
                    session = pynder.Session(str(config['DEFAULT']['FACEBOOK_ID']), auth)
                except pynder.errors.RequestError:
                    log("Pynder Error. New auth did NOT work.")
                    break
                continue
            except:
                log("Generic Exception. Don't know what issue is....")
                break
    else:
        log("Sessions is None.")
        quit()

def handle_likes():
    print("likes")
    users = session.nearby_users()
    for u in users:
        u.self._session._api.like(self.id)['match']
        log('Liked ' + u.name)
        try:
            status = check_swipes()
            print(status)
            if status == 'Send messages':
                log('Out of swipes. Moving along to send messages.')
                break
            else:
                try:
                    print("loko")
                    action = like_or_nope()
                    if action == True:
                        u.like()
                        log('Liked ' + u.name)
                        sleep(randint(1,5))
                    else:
                        u.dislike()
                        log('Disliked ' + u.name)
                        sleep(randint(1,5))
                except ValueError:
                    break
                except pynder.errors.RequestError:
                    break
        except ValueError:
            break
        except pynder.errors.RequestError:
            break

def send(match, message_no):
    for m in messages[message_no]:

        session._api._post('/user/matches/' + match['id'],
                         {"message": m})  #!!!

        sleep(randint(3,10))
    log('Sent message ' + str(message_no) + ' to ' + match['person']['name'])

def sendbot(match, message_no_bot):

    session._api._post('/user/matches/' + match['id'],
                         {"message": "Нет, я не бот, я настоящbq vfkmxbr бип-бу1001000100010110011001010000"})

    #print(match['messages'])

    sleep(randint(3,10))
    log('Sent message ' + str(message_no_bot) + ' to ' + match['person']['name'])

def sendfake(match, message_no_fake):
    for mf in messagesfake[message_no_fake]:
        session._api._post('/user/matches/' + match['id'],
                            {"message": mf})
        sleep(randint(3,10))
    log('Sent message ' + str(message_no_fake) + ' to ' + match['person']['name'])

def sendreal(match, message_no_real):
    for mr in messagesreal[message_no_real]:
        session._api._post('/user/matches/' + match['id'],
                            {"message": mr})
        sleep(randint(3,10))
    log('Sent message ' + str(message_no_real) + ' to ' + match['person']['name'])


def dataSave(match):
        file = open("testfile.txt","w")

        file.write(str(match))
        file.close()





def message(match):
    ms = match['messages']
    myself = session.profile.id
    if not ms:
        send(match, 0)
        return
    said = False
    saidbot = False
    saidfake = False
    saidreal = False
    count = 0
    name = match['person']['name']

    for m in ms:
        if m['from'] == myself:
            count += 1
            said = False
        #elif  ('бот ' in m['message'].lower()) and (m['from'] != myself):
        #    count = 0
        #    saidbot = True
        elif 'fake' in m['message'].lower():
            count = 0
            saidfake = True
        elif 'real person' in m['message'].lower():
            count = 0
            saidreal = True
        else:
                said = True
    if count >= len(messages):
        log('Finished conversation with ' + name)
        return
    if said:
        dataSave(match) ## HERE
        send(match,count)
    elif saidbot:
        sendbot(match,count)
    elif saidbot:
        sendfake(match,count)
    elif saidbot:
        sendreal(match,count)
    else:
        log('No new messages from ' + name)

def handle_matches():
    log(str(len(session._api.matches(0))) + ' matches')
    matches = session._api.matches(0)
    x = True
    for m in reversed(matches):
        message(m)

def sendAll(text):
    flag = 1
    num = 544
    if flag:
        matches = session._api.matches(0)
        for i in (matches):
            if(i['person']['name'] != "Yi"):
                session._api._post('/user/matches/' + i['id'],
                 {"message": text + i['person']['name'] + "?"})
        print ("sent")
        flag = 0;
    else:

        print ("already sent")

def Stats():
    matches = session._api.matches(0)
    print(len(matches))
    for match in matches:
        print(match['person']['name'] + "  gender:  " + str(match['person']['gender']) )
    log('Finished')



while True:
    text = 'Что на счет кофейка сегодня, '
    print(session.likes_remaining)
    #matches = session._api.matches(0)
    #print(matches)
    ##sendAll(text)
    if session.likes_remaining > 0 :
        ##handle_likes()
        handle_likes_two()

    ##handle_ass()
    handle_matches()
    log('Resting for a few minutes...')
    sleep(randint(3,4))
