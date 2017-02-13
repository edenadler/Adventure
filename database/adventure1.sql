 CREATE TABLE questions(
 	adventure_id smallint,
     question_number smallint,
     question varchar(225),
     image varchar(40)
     );
--     
 ALTER TABLE questions
 ADD PRIMARY KEY (question_number);
-- 
-- -- 
 CREATE TABLE options(
 	question_number smallint,
     question_options varchar(225),
     score int,
     FOREIGN KEY (question_number) REFERENCES questions(question_number)
     );


INSERT INTO questions  
 VALUES (1,1, 'A kid in Kindergarden calls you a name, you:', 'Image1'),
 (1,2, 'Your mom made something yucky for dinner, you:', 'Image2'),
 (1,3, 'Your parents tell you you’re going to have another sibling soon, you:', 'Image3'),
 (1,4, 'Its nap time, you:', 'Image4'),
 (1,5, 'It is your birthday and you get a present but you don’t like it, you:', 'Image5'),
 (2,6, 'It is time to do homework, you:', 'Image6'),
 (2,7, 'Your parents catch you sneaking out of the house at night, you:', 'Image7'),
 (2,8, 'Prom is coming up, you:', 'Image8'),
 (2,9, 'Your parents sit you down and want to have “the talk”, you:', 'Image9'),
 (2,10, 'There is a rumor being spread about you in school, you:', 'Image10'),
 (3,11, 'You don’t want to go into work, you:', 'Image11'),
 (3,12, 'The person you are on a first date with is horribly awkward, you:', 'Image12'),
 (3,13, 'Your roommate never helps clean the apartment, you:', 'Image13'),
 (3,14, 'You suspect that your boss is involved in a scandal at work, you:', 'Image14'),
 (3,15, 'Your significant other wants to get a pet with you, you:', 'Image15');
-- 
INSERT INTO options  
VALUES (1,'Sit there and cry ', -5),
(1,'Tell on them to the teacher', -10),
(1,'Call them a name back', 15),
(1,'Run away', 10),
(2,'Eat it because you are starving', 10),
(2,'Throw it on the floor', -5),
(2,'Feed it to the dog', 15),
(2,'Refuse to even open your mouth', 0),
(3,'Scream with excitement', 10),
(3,'Cry because you don’t want them to steal the attention from you', -10),
(3,'Okay, but only if it is a girl', 5),
(3,'Can’t wait to have another friend to play with/torture', 15),
(3,'Cry because you don’t want them to steal the attention from you', -10),
(3,'Okay, but only if it is a girl', 5),
(4,'Run and hide', 10),
(4,'Are happy, you love naptime', 5),
(4,'Cry until you fall asleep', -5),
(4,'Say, “Okay!” But then later sneak away…', -30),
(5,'Say, “Thank you!” and plan to return it later', 5),
(5,'Scream and cry', -5),
(5,'Make a face because you don’t like it', -10),
(5,'Smile because you are happy people love you', 10);,
(6,'Procrastinate, it can be done later…', 15),
(6,'Make excuses why you can’t do it now', -5),
(6,'Do it, you love homework and school and learning', 5),
(6,'Do the bare minimum to “finish” it', -10),
(7,'Pretend you don’t know what they talking about', 5),
(7,'Blame it on your sibling', -5),
(7,'Yell at them for being too overprotective ', 15),
(7,'Lie and tell them it is for a school event ', 10),
(8,'Get the courage to ask your crush ', 15),
(8,'Wait for someone to ask you', -5),
(8,'Ask your best friend, they have to go with you, right?', -10),
(8,'Decide to skip it all together, you hate dances', 5),
(9,'Stay and listen like a good kid', 5),
(9,'Pretend to listen, but are thinking of other things ', 10),
(9,'Make an excuse of why now is not a good time ', -5),
(9,'Scream at them for being embarrassing ', 15),
(10,'Do everything you can to avoid going to school  ', -5),
(10,'Cry and tell the principal', -15),
(10,'Get your friends to find out who is spreading it ', 10),
(10,'Invent a new rumor about someone else so people will stop talking about you', 5),
(11,'Take a “sick day”', 5),
(11,'Make up a crazy story about how you can’t possibly make it in today', 10),
(11,'Go anyway, you don’t want to get in trouble', -5),
(11,'Don’t show up and wonder if anyone will even notice', -10),
(12,'Make an excuse about having to leave and go', -10),
(12,'Smile and nod and plan your escape ', 10),
(12,'Order another drink, you might as well enjoy yourself ', 15),
(12,'Stay in the bathroom and call a friend to pass the time', 5),
(13,'Leave passive-aggressive notes to them', -5),
(13,'Clean it up yourself', -10),
(13,'Move to a new apartment', 10),
(13,'Yell at them when they get home from work ', 5),
(14,'Gossip about it to your co-workers', -10),
(14,'Pretend you don’t know anything about it', 10),
(14,'Confront them', 5),
(14,'Become an undercover agent and spy on them to find out', 5),
(15,'Freak out. You didn’t realize things were that serious between you', 5),
(15,'Are so happy! You’ve always wanted a pet', 10),
(15,'Say, “Yes!” But only if it is a dog…  ', -15),
(15,'Tell them, “No way!”, neither of you have time to take care of it', -5);