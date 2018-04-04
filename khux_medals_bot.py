import praw
import config
import os

def bot_login():
	r = praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = "Daibaken's khux medal bot")

	return r

def run_bot(r, comments_replied):

	for comment in r.subreddit('test').comments(limit=25):
		if comment.body.startswith('[[') and comment.body.endswith(']]') and comment.id not in comments_replied:
			print ("String with \"khux\" found" + comment.id) 
			comment.reply("I will able to show khux medals soon!")
			print ("Replied to comment" + comment.id)

			comments_replied.append(comment.id)
			with open ("comments_replied.txt", "a") as f:
				f.write(comment.id + "\n")

def get_saveds_comments():
	if not os.path.isfile("comments_replied.txt"):
		comments_replied = []
	else:
		with open("comments_replied.txt", "r") as f:
			comments_replied = f.read()
			comments_replied = comments_replied.split("\n")
			comments_replied = list(filter(None, comments_replied))
	
	return comments_replied 

r = bot_login()

#gets the comment id of all comments replied to by bot from a text file
comments_replied = get_saveds_comments()

while True:
	run_bot(r, comments_replied)
