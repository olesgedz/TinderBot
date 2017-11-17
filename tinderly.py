# -*- coding: utf-8 -*-
#! /usr/bin/env python                                                                                                                                      1,1           Top# encoding: utf8
import argparse
from datetime import datetime
import json
from random import randint
import requests
import sys
from time import sleep
import config
import datetime
import pynder
from messages import messages
from messagesbot import messagesbot
from messagesfake import messagesfake
from messagesreal import messagesreal


requests.packages.urllib3.disable_warnings()  # Find way around this...

session = pynder.Session(config.FACEBOOK_AUTH_TOKEN) #config.FACEBOOK_ID, facebook_id=BID, facebook_token=FBTOKEN




def log(msg):
    print '[' + str(datetime.datetime.now()) + ']' + ' ' + msg

def like_or_nope():
    if randint(1, 100) == 31:
        return 'nope'
    else:
        return 'like'

def check_swipes():
    swipes_remaining = session.likes_remaining
    if swipes_remaining == 0:
        return 'Send messages'

def handle_likes():
    users = session.nearby_users()
    for u in users:
        try:
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
    for mb in messagesbot[message_no_bot]:
        session._api._post('/user/matches/' + match['id'],
                            {"message": mb})
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
        elif 'bot' in m['message'].lower():
            count = 0
            saidbot = True
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
    log(str(len(session._api.matches())) + ' matches')
    matches = session._api.matches()
    x = True
    for m in reversed(matches):
        message(m)

def sendAll(text):
    flag = 1
    if flag:
        matches = session._api.matches()
        for i in reversed(matches):
            session._api._post('/user/matches/' + i['id'],
                                {"message": text})
        print "sent"
        flag = 0;
    else:

        print "already sent"



while True:
    text = "Привет, пошли сегодня на киноночь Хаяо Миядзаки в антикафе?"
    ##sendAll(text)
    handle_likes()
    handle_matches()
    log('Resting for a few minutes...')
    sleep(randint(30,60))
    
