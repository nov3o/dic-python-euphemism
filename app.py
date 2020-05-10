#!/usr/bin/env python3

"""
['french word', 'other language word', test_priority: int, next_test: Date()]
"""

import csv
from datetime import datetime
import re
import bisect

now = datetime.now
timestamp = datetime.timestamp
strftime = datetime.strftime
fromtimestamp = datetime.fromtimestamp


FILE_NAME = 'dictionarydata'


def read(filename):
	data = []
	try:
		with open(filename, newline='') as csvfile:
		    data = list(csv.reader(csvfile, delimiter=',', quotechar='|'))
		for r in data:
			r[2] = int(r[2])
			r[3] = int(r[3])
	except FileNotFoundError:
		data = None

	return data


def save(data, filename):
	if not data:
		return
	with open(filename, 'w', newline='') as csvfile:
	    writer = csv.writer(
	    	csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL
	    	)
	    for row in data:
	    	writer.writerow(row)


def print_test(data):
	if not data:
		return
	istest = 0
	for i in range(len(data)):
		row = data[i]
		if row[3] > now().timestamp():
			print(" These words are waiting for test:")
			istest = 1
			break

	if not istest:
		return
	
	for_test = []
	for j in range(i, len(data)):
		row = data[i]
		if row[3] > now().timestamp():
			for_test.append(j)
			print(row[0])

	print()
	return for_test


def test(data, ls):
	if not ls:
		return
	print()
	right = 0
	total = len(ls)
	for i in ls:
		row = data[i]
		print(f'{row[0]}: ', end='')
		transl = input().strip().lower()
		while not transl:
			print()
			print("Empty input. Type again")
			print(f'{row[0]}: ', end='')
			transl = input().strip().lower()
		if transl == row[1]:
			print("Correct!")
			print()
			right += 1
			row[2] += 1
		else:
			print(f"Wrong. The right answer is {row[1]}")
			print()1
			if row[2] != 1:
				row[2] -= 1
		row[3] = int(now().timestamp()) + 2**row[2] * (60*60*24)
		del ls[i]

	print(f"Your score: {round(right*10 / total)}/10")
	print()

	return data


def add_text(data):
	if not data:
		data = []
	print("Enter text")
	lines = []
	while True:
	    line = input()
	    if line:
	        lines.append(line)
	    else:
	        break

	known = sorted([r[0] for r in data])
	words = []
	new_words = []
	for l in lines:
		l = l.lower()
		words = re.findall(r'[a-z]+', l)
		for w in words:
			ip = bisect.bisect_left(known, w)
			if ip < len(known) and known[ip] == w:
				continue
			new_words.append(w)
		words = []	

	print("Enter words' translations")
	print("Еype '-' if you don't want add the word")
	for w in new_words:
		print(f"{w}: ", end='')
		tr = input().strip().lower()
		while not tr:
			print()
			print("Empty input. Type again")
			print(f"{w}: ", end='')
			tr = input().strip().lower()
		if tr == '-':
			continue
		data.append([w, tr, 1, int(now().timestamp()) + (60*60*24)])

	print(f"You have added new {len(new_words)} words")
	print()
	return data


def change(data):
	if not data:
		return
	print()
	print("What word want to change(type it in your new lang)")
	word = input().strip()
	while not word:
		print()
		print("Empty input. Type again")
		word = input().strip().lower()

	prev = ''
	found = 0
	for r in data:
		if r[0] == word:
			print(f"Current translation is {w[1]}. What's new translation?")
			tr = input().strip()
			while not tr:
				print()
				print("Empty input. Type again")
				tr = input().strip().lower()
			prev = r[1]
			r[1] = tr
			found = 1
			break

	if found:
		print()
		print(f"You changed translation of '{w[0]}' from {prev} to {r[1]}")
		print()
	else:
		print()
		print("The word wasn't found")
		print()

	return data


def get_next_tests(data):
	if not data:
		return
	srt = sorted([r[3] for r in data])
	if srt[0] <= now().timestamp():
		print()
		print("You have test to pass")
		print()
	for i in range(len(srt)):
		if srt[i] > now().timestamp():
			break
	next_tests = [ 
		fromtimestamp(i).strftime("%Y-%m-%d %H:%M") for i in srt[i:i+3]
		]
	if next_tests:
		print(f"Next {len(next_tests)} tests will be {', '.join(next_tests)}")


def show(data):
	if not data:
		return
	for r in data:
		print(r[0], r[1], sep=' - ')

	print()


def main():
	data = read(FILE_NAME)
	test_rows = []
	if data != None:
		test_rows = print_test(data)
	while 1:
		cmd = input().strip()
		if cmd == 'exit':
			save(data, FILE_NAME)
			exit(0)
		elif cmd == 'add':
			data = add_text(data)
		elif cmd == 'test':
			if test_rows:
				data = test(data, test_rows)
		elif cmd == 'change':
			data = change(data)
		elif cmd == 'next':
			get_next_tests(data)
		elif cmd == 'help':
			print('exit add test change next help')
			print()
		elif cmd == 'save':
			save(data, FILE_NAME)
		elif cmd == 'show':
			show(data)
		else:
			print("Wrong command")
			print()


if __name__ == '__main__':
	main()