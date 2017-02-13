from bottle import route, run, template, static_file, request, default_app, get, response
import pymysql
import random
import json
from sys import argv
import os
from os import environ as env

connection = pymysql.connect(host='sql9.freesqldatabase.com', user='sql9157851', password='nfeyJlT6Yl',db='sql9157851', charset='utf8', cursorclass = pymysql.cursors.DictCursor)
adv1 = [1,2,3,4,5]
adv2 = [6,7,8,9,10]
adv3 = [11,12,13,14,15]

@route("/", method="GET")
def index():
    return template("adventure.html")


@route("/start", method="POST")
def start():
    try:
        with connection.cursor() as cursor:
            username = request.POST.get("name")
            print("username",username)
            current_adv_id = int(request.POST.get("adventure_id"))
            current_score = 50
            current_story_id = 1

            #ADD USER IF NOT IN DB OR GET CURRENT_STEP IF USER EXISTS IN ADVENTURE
            get_all_userinfo = "SELECT name, id, current_step, adventure_id, score, past_questions FROM userinfo"
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

                    if {"adventure_id": current_adv_id} in user_adventures: #and the user has already played this adventure, then get the last step they played to continue from there
                        get_last_step = "SELECT adventure_id, past_questions, score FROM userinfo WHERE name = '{}'".format(
                            username)
                        cursor.execute(get_last_step)
                        adventure_info = cursor.fetchall()
                        print("adventure_info", adventure_info)

                        for info in adventure_info:
                            if info["adventure_id"] == current_adv_id:
                                current_score = info["score"]  # or is it item["score"]?
                                print("current_score", current_score)
                                questions_asked = get_list_of_past_questions(username, current_adv_id)

                                # DETERMINE NEXT QUESTION
                                current_story_id = determine_next_step(current_adv_id)

                                # STORE THAT QUESTION IN THE DATABASE
                                store_random_question_in_DB(questions_asked, current_story_id, username, current_adv_id)

                    else: #and the user has not played this adventure yet, then add them
                        # DETERMINE NEXT QUESTION
                        current_story_id = determine_next_step(current_adv_id)

                        add_new_adventure = "INSERT INTO userinfo (name, current_step, adventure_id, score, past_questions) VALUES ('{0}', '{1}', '{2}','{3}', '{4}')".format(
                            username, current_story_id, current_adv_id, 50, str(current_story_id))
                        cursor.execute(add_new_adventure)
                        connection.commit()

                else: #if this is a new user, add them

                    # DETERMINE NEXT QUESTION
                    current_story_id = determine_next_step(current_adv_id)

                    add_user = "INSERT INTO userinfo (name, current_step, past_questions, adventure_id, score) VALUES ('{0}', '{1}', '{2}', '{3}','{4}')".format(username, current_story_id, str(current_story_id), current_adv_id, current_score)
                    cursor.execute(add_user)
                    connection.commit()

                # GET THE QUESTIONS FOR THE NEXT STEP FROM DB
                current_question_and_image = retrieve_question_info(username, current_adv_id)

                current_question = current_question_and_image["question"]
                current_image = current_question_and_image["image"]

                # GET THE QUESTION OPTIONS FOR THE NEXT STEP FROM DB
                current_question_options = get_question_options_info(username, current_story_id, current_adv_id)
                print("current_question_options in start", current_question_options)
                break


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

            if current_score >= 100:
                # UPDATING SCORE
                update_score = "UPDATE userinfo SET score = '{0}' and past_questions = '{1}' WHERE name ='{2}' and adventure_id ='{3}'".format(0, "0", username, current_adv_id)
                cursor.execute(update_score)
                connection.commit()
            elif current_score <=0:
                # UPDATING SCORE
                update_score = "UPDATE userinfo SET score = '{0}' and past_questions = '{1}' WHERE name ='{2}' and adventure_id ='{3}'".format(0, "0", username, current_adv_id)
                cursor.execute(update_score)
                connection.commit()
            else:
                # UPDATING SCORE
                update_score = "UPDATE userinfo SET score = '{0}' WHERE name ='{1}' and adventure_id ='{2}'".format(current_score, username, current_adv_id)
                cursor.execute(update_score)
                connection.commit()

            #TODO if we want to do it later, we can transition between the adventures by automatically advancing the user after a certain score to the next adventure

            #QUERY PAST QUESTIONS
            questions_asked = get_list_of_past_questions(username, current_adv_id)

            # DETERMINE NEXT QUESTION
            current_story_id = determine_next_step(current_adv_id)

            if current_story_id == 0:
                print("losing", current_story_id)
                # UPDATING SCORE
                update_score = "UPDATE userinfo SET past_questions = '{0}' WHERE name ='{1}' and adventure_id ='{2}'".format("0", username, current_adv_id)
                cursor.execute(update_score)
                connection.commit()
                return json.dumps({"user": username,
                                   "adventure": current_adv_id,
                                   "current": current_story_id,
                                   "score": 0
                                   })
            else:
                # STORE THAT QUESTION IN THE DATABASE
                store_random_question_in_DB(questions_asked, current_story_id, username, current_adv_id)

                # GET THE QUESTION FOR THE NEXT STEP FROM DB
                current_question_and_image = retrieve_question_info(username, current_adv_id)

                current_question = current_question_and_image["question"]
                current_image = current_question_and_image["image"]

                # GET THE QUESTION OPTIONS FOR THE NEXT STEP FROM DB
                current_question_options = get_question_options_info(username, current_story_id, current_adv_id)


                return json.dumps({"user": username,
                               "adventure": current_adv_id,
                               "current": current_story_id,
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


def get_question_options_info(username, current_story_id, current_adv_id):
    try:
        with connection.cursor() as cursor:
            print("current)story_id",current_story_id)
            get_question_options = "SELECT question_options, options.score FROM options INNER JOIN questions ON options.question_number = questions.question_number INNER JOIN userinfo ON userinfo.current_step = questions.question_number AND questions.adventure_id = userinfo.adventure_id WHERE name = '{0}' and current_step = '{1}' and userinfo.adventure_id = '{2}'".format(username, current_story_id, current_adv_id)
            cursor.execute(get_question_options)
            current_question_options = cursor.fetchall()
            print("current_question_options",current_question_options)
            return current_question_options
    except Exception as e:
        print(repr(e))


def retrieve_question_info(username, current_adv_id):
    try:
        with connection.cursor() as cursor:
            print("username",username)
            print("current_adv_id",current_adv_id)
            # GET THE QUESTION FOR THE NEXT STEP FROM DB
            get_question = "SELECT question, image FROM questions INNER JOIN userinfo ON userinfo.current_step = questions.question_number WHERE name ='{0}' and userinfo.adventure_id='{1}'".format(
                username, current_adv_id)
            cursor.execute(get_question)
            current_question_and_image = cursor.fetchone()
            print("current_question_and_image", current_question_and_image)

            return current_question_and_image
    except Exception as e:
        print(repr(e))


def determine_next_step(current_adv_id):
    if current_adv_id == 1:
        print("current_adv_id1", current_adv_id)
        print("adv1",adv1)
        if adv1 == []:
            print("you lose!")
            return 0
        else:
            nextStep = adv1.pop(random.randrange(len(adv1)))
            print("adv1 after pop", adv1)
            print("nextStep1", nextStep)
            return nextStep
    elif current_adv_id == 2:
        if adv2 == []:
            print("you lose!")
            return 0
        else:
            nextStep = adv2.pop(random.randrange(len(adv2)))
            return nextStep
    else:
        if adv3 == []:
            print("you lose!")
            return 0
        else:
            nextStep = adv3.pop(random.randrange(len(adv3)))
            return nextStep


def get_list_of_past_questions(username, current_adv_id):
    try:
        with connection.cursor() as cursor:
            get_questions = "SELECT past_questions FROM userinfo WHERE name ='{0}' and adventure_id='{1}'".format(
                username, current_adv_id)
            cursor.execute(get_questions)
            past_questions = cursor.fetchone()
            print("past_questions in function",past_questions)
            questions_asked_list = past_questions["past_questions"].split()
            print("questions_asked_list in function", questions_asked_list)
            for question in questions_asked_list:
                if int(question) in adv1:
                    adv1.remove(int(question))
                elif int(question) in adv2:
                    adv2.remove(int(question))
                elif int(question) in adv3:
                    adv3.remove(int(question))
            return str(past_questions["past_questions"])
    except Exception as e:
        print(repr(e))

def store_random_question_in_DB(questions_asked, current_story_id, username, current_adv_id):
    try:
        with connection.cursor() as cursor:
            questions_asked += " "+str(current_story_id)
            print("questions_asked TOTAL", questions_asked)
            update_questions = "UPDATE userinfo SET past_questions ='{0}' WHERE name ='{1}' and adventure_id ='{2}'".format(
                questions_asked, username, current_adv_id)
            cursor.execute(update_questions)
            connection.commit()
            update_current_step = "UPDATE userinfo SET current_step ='{0}' WHERE name ='{1}' and adventure_id ='{2}'".format(
                current_story_id, username, current_adv_id)
            cursor.execute(update_current_step)
            connection.commit()
    except Exception as e:
        print(repr(e))


def main():
    #run(host='0.0.0.0',port=argv[1])
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()

