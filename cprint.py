from termcolor import colored

def rprint(out_message):
	print(colored(out_message, 'red'))

def bprint(out_message):
	print(colored(out_message, 'blue'))

def gprint(out_message):
	print(colored(out_message, 'green'))
