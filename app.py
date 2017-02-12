from bottle import route, run, template, static_file, request, default_app, get, response
import pymysql
import random
import json
from sys import argv
import os
from os import environ as env

connection = pymysql.connect(host='sql9.freesqldatabase.com', user='sql9157851', password='nfeyJlT6Yl',db='sql9157851', charset='utf8', cursorclass = pymysql.cursors.DictCursor)
adv1 = [1,2,3,4,5,6,7]
adv2 = [8,9,10,11,12,13,14]
adv3 = [15,16,17,18,19,20,21]

@route("/", method="GET")
def index():
    return template("adventure.html")


@route("/start", method="POST")
def start():
    try:
        with connection.cursor() as cursor:
            username = request.POST.get("name")
            current_adv_id = int(request.POST.get("adventure_id"))
            determine_next_steps = determine_next_step(current_adv_id)
            current_score = 50
            current_story_id = 1

            #ADD USER IF NOT IN DB OR GET CURRENT_STEP IF USER EXISTS IN ADVENTURE
            get_all_userinfo = "SELECT name, id, current_step, adventure_id, score FROM userinfo"
            cursor.execute(get_all_userinfo)
            result = cursor.fetchall()

            for item in result:
                print("item",item)
                print("result",result)
                if item["name"] == username: #if the user already exists...

                    get_user_adventures = "SELECT adventure_id FROM userinfo WHERE name = '{}'".format(username)
                    cursor.execute(get_user_adventures)
                    user_adventures = cursor.fetchall()
                    print("user_adventures",user_adventures)

                    if {"adventure_id": current_adv_id} not in user_adventures: #and the user has not played this adventure yet, then add them
                        add_new_adventure = "INSERT INTO userinfo (name, current_step, adventure_id) VALUES ('{0}', '{1}', '{2}')".format(username, current_story_id, current_adv_id)
                        cursor.execute(add_new_adventure)
                        connection.commit()

                    else: #and the user has already played this adventure, then get the last step they played to continue from there
                        get_last_step = "SELECT adventure_id, current_step, score FROM userinfo WHERE name = '{}'".format(username)
                        cursor.execute(get_last_step)
                        adventure_info = cursor.fetchall()
                        print("adventure_info",adventure_info)

                        for info in adventure_info:
                            if info["adventure_id"] == current_adv_id:
                                current_score = item["score"]
                                print("current_score",current_score)
                                current_story_id = int(item["current_step"])

                else: #if this is a new user, add them
                    add_user = "INSERT INTO userinfo (name, current_step, adventure_id, score) VALUES ('{0}', '{1}', '{2}','{3}')".format(username, current_story_id, current_adv_id, current_score)
                    cursor.execute(add_user)
                    connection.commit()

            # GET THE QUESTION FOR THE NEXT STEP FROM DB
            get_question = "SELECT question, image FROM questions INNER JOIN userinfo ON userinfo.current_step = questions.question_number WHERE name ='{0}' and userinfo.adventure_id='{1}'".format(
                username, current_adv_id)
            cursor.execute(get_question)
            current_question_and_image = cursor.fetchone()
            print("current_question_and_image",current_question_and_image)

            #TODO does fetchone only return a dictionary, or do we have to loop through a list?
            current_question = current_question_and_image["question"]
            current_image = current_question_and_image["image"]

            # GET THE QUESTION OPTIONS FOR THE NEXT STEP FROM DB
            get_question_options = "SELECT question_options, options.score FROM options INNER JOIN questions ON options.question_number = questions.question_number INNER JOIN userinfo ON userinfo.current_step = questions.question_number AND questions.adventure_id = userinfo.adventure_id WHERE name = '{0}' and current_step = '{1}' and userinfo.adventure_id = '{2}'".format(username, current_story_id, current_adv_id)
            cursor.execute(get_question_options)
            current_question_options = cursor.fetchall()
            print("current_question_options",current_question_options)

            return json.dumps({"user": username,
                               "adventure": current_adv_id,
                               "current": current_story_id,
                               "score": current_score,
                               "text": current_question,
                               "image": current_image,
                               "options": current_question_options
                               })
    except Exception as e:
        print(repr(e))


@route("/story", method="POST")
def story():
    try:
        with connection.cursor() as cursor:
            username = request.POST.get("user")
            print("username",username)
            current_adv_id = int(request.POST.get("adventure"))
            print("current_adv_id",current_adv_id)
            current_score = int(request.POST.get("currentScore"))
            print("current_score",current_score)
            next_step_id = int(request.POST.get("nextStep"))
            print("next_step_id",next_step_id)

            #UPDATING SCORE
            update_score = "UPDATE userinfo SET score = '{0}' WHERE name ='{1}' and adventure_id ='{2}'".format(current_score,username,current_adv_id)
            cursor.execute(update_score)
            connection.commit()

            #UPDATING STEP
            update_step ="UPDATE userinfo SET current_step ='{0}' WHERE name ='{1}' and adventure_id ='{2}'".format(next_step_id,username,current_adv_id)
            cursor.execute(update_step)
            connection.commit()

            # GET THE QUESTION FOR THE NEXT STEP FROM DB
            get_question = "SELECT question, image FROM questions INNER JOIN userinfo ON userinfo.current_step = questions.question_number WHERE name ='{0}' and userinfo.adventure_id='{1}' and current_step='{2}'".format(
                username, current_adv_id, next_step_id)
            cursor.execute(get_question)
            current_question_and_image = cursor.fetchone()
            print("current_question_and_image",current_question_and_image)

            # TODO does fetchone only return a dictionary, or do we have to loop through a list?
            current_question = current_question_and_image["question"]
            current_image = current_question_and_image["image"]

            # GET THE QUESTION OPTIONS FOR THE NEXT STEP FROM DB
            get_question_options = "SELECT question_options, options.score FROM options INNER JOIN questions ON options.question_number = questions.question_number INNER JOIN userinfo ON userinfo.current_step = questions.question_number AND questions.adventure_id = userinfo.adventure_id WHERE name = '{0}' and current_step = '{1}' and userinfo.adventure_id = '{2}'".format(username, next_step_id, current_adv_id)
            cursor.execute(get_question_options)
            current_question_options = cursor.fetchall()
            print("current_question_options",current_question_options)

        return json.dumps({"user": username,
                           "adventure": current_adv_id,
                           "current": next_step_id,
                           "text": current_question,
                           "image": current_image,
                           "options": current_question_options,
                           })
    except Exception as e:
        print(repr(e))

@route('/js/<filename:re:.*\.js$>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|jpeg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')

def determine_next_step(current_adv_id):
    if current_adv_id == 1:
        nextStep = adv1.pop(random.randrange(len(adv1)))
        return nextStep
    elif current_adv_id == 2:
        nextStep = adv2.pop(random.randrange(len(adv2)))
        return nextStep
    else:
        nextStep = adv3.pop(random.randrange(len(adv3)))
        return nextStep

def main():
    #run(host='0.0.0.0',port=argv[1])
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()

