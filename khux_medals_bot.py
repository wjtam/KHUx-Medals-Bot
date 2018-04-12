import praw
import config
import os
import requests

URL = 'https://www.khuxbot.com/api/v1/medal?q=data&filter='

def bot_login():
	r = praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = "Daibaken's khux medal bot")

	return r

def getMedal(str):
	newStr = str.lower()
	if newStr == 'xex' or newStr == 'ixex':
		newStr = "illustrated xion (ex)"
	if newStr == 'kex' or newStr == 'ikex':
		newStr = "illustrated kh kairi (ex)"
	if ' and ' in newStr:
		newStr = newStr.replace(" and "," %26 ")
	if '&' in newStr:
		newStr = newStr.replace("&","%26")
	if '[ex]' in newStr:
		newStr = newStr.replace("[ex]","(ex)")
	elif ' ex' in newStr:	
		newStr = newStr.replace(" ex"," (ex)")

	print('{\"name\":\"' + newStr + '\",\"rarity\":\"6\"}')

	return '{\"name\":\"' + newStr + '\",\"rarity\":\"6\"}'

def run_bot(r, comments_replied):
	comment_found = False
	for comment in r.subreddit('khux').comments(limit=25):
		comment_body = comment.body.split()
		for comment_word in comment_body:
			if comment_word.startswith('{') and comment_word.endswith('}') and comment.id not in comments_replied:
				comment_found = True
				print ("String with \"{\" and \"}\" found" + comment.id) 
				medalURL = getMedal(comment_word[1:-1])
				data = requests.get(URL+medalURL).json()['medal']['0'] #medal json data
				comment.reply('[**' + data['name'] + '**](https://www.khuxbot.com' + data['image_link'] + ') ' + data['direction'] 
					+ ' ' + data['element'] + ' ' + str(data['tier']) + ' ' + data['targets'] 
					+ '\n\n STR: ' + str(data['strength']) + ' DEF: ' + str(data['defence']) + ' MULT: ' + str(data['multiplier']) 
					+ ' HITS: ' + str(data['hits']) + '\n\n'+ str(data['notes']))
	
	if comment_found:
		print("Replied to comment" + comment.id)
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
