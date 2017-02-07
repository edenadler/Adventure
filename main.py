from bottle import route, run, template, static_file, request
import pymysql
import random
import json

connection = pymysql.connect(host='localhost', user='root', password='root',db='adventure', charset='utf8', cursorclass = pymysql.cursors.DictCursor)


@route("/", method="GET")
def index():
    return template("adventure.html")


@route("/start", method="POST")
def start():
    try:
        with connection.cursor() as cursor:
            username = request.POST.get("name")
            current_adv_id = request.POST.get("adventure_id")
            user_id = 0
            current_story_id = 0

            sql = "SELECT name, id, current_step, adventure_id FROM userinfo"
            cursor.execute(sql)
            result = cursor.fetchall()
            print("cursor result:", result)

            for item in result:
                print("into for loop")
                print("item[name]:",item["name"],"username:",username)
                if item["name"] == username:
                    #todo will this start over and try to find a new name??
                    if item["adventure_id"] == current_adv_id:
                        user_id = item["id"]
                        current_story_id = int(item["current_step"])
                    else:
                        add_new_adventure = "INSERT INTO userinfo (name, current_step, adventure_id) VALUES ('{0}', '{1}', '{2}')".format(username, current_story_id, current_adv_id)
                        cursor.execute(add_new_adventure)
                        connection.commit()
                else:
                    print("else, no username")
                    add_user = "INSERT INTO userinfo (name, current_step, adventure_id) VALUES ('{0}', '{1}', '{2}')".format(username, current_story_id, current_adv_id)
                    cursor.execute(add_user)
                    connection.commit()

            next_steps_results = [
                {"id": 1, "option_text": "I fight it"},
                {"id": 2, "option_text": "I give him 10 coins"},
                {"id": 3, "option_text": "I tell it that I just want to go home"},
                {"id": 4, "option_text": "I run away quickly"}
                ]

            #todo add the next step based on db
            return json.dumps({"user": user_id,
                               "adventure": current_adv_id,
                               "current": current_story_id,
                               "next": current_story_id + 1, #is this right?????
                               "text": "You meet a mysterious creature in the woods, what do you do?",
                               "image": "troll.png",
                               "options": next_steps_results
                               })
    except Exception as e:
        print(repr(e))


@route("/story", method="POST")
def story():
    user_id = request.POST.get("user")
    current_adv_id = request.POST.get("adventure")
    next_story_id = request.POST.get("next") #this is what the user chose - use it!
    next_steps_results = [
        {"id": 1, "option_text": "I run!"},
        {"id": 2, "option_text": "I hide!"},
        {"id": 3, "option_text": "I sleep!"},
        {"id": 4, "option_text": "I fight!"}
        ]
    random.shuffle(next_steps_results) #todo change - used only for demonstration purpouses

    #todo add the next step based on db
    return json.dumps({"user": user_id,
                       "adventure": current_adv_id,
                       "next": next_story_id,
                       "text": "New scenario! What would you do?",
                       "image": "choice.jpg",
                       "options": next_steps_results
                       })

@route('/js/<filename:re:.*\.js$>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')

def main():
    run(host='localhost', port=9000)

if __name__ == '__main__':
    main()

