import os, urllib, datetime, jinja2, math, re, time, py.datamodel as model

PAGE_LIMIT=10
DEFAULT_DELIMIT=","

def replace_image_html(content):
	newstring = re.sub(r'(\http[s]?://[^\s<>"]+|www\.[^\s<>"]+)', r'<a href="\1">\1</a>', content)
	content = re.sub(r'<a href="(\http[s]?://[^\s<>"]+|www\.[^\s<>"]+)">[^\s]+.jpg</a>', r'<img src="\1">', newstring)
	newstring = re.sub(r'<a href="(\http[s]?://[^\s<>"]+|www\.[^\s<>"]+)">[^\s]+.png</a>', r'<img src="\1">', content)
	content = re.sub(r'<a href="(\http[s]?://[^\s<>"]+|www\.[^\s<>"]+)">[^\s]+.gif</a>', r'<img src="\1">', newstring)
	return content

def replace_newline(content):
	content=content.replace('\n', '<br>')
	return content

def replace_content(content):
	content=replace_newline(content)
	content=replace_image_html(content)
	return content

def max_page_num(length):
	max_p = int(math.ceil(length/PAGE_LIMIT))+1
	return max_p

def split_element_by_page_num(inputlist, pagenum, pagelimit=PAGE_LIMIT):
	max_page_num =int(math.ceil(len(inputlist)/pagelimit))+1
	if pagenum >= max_page_num:
		pagenum=max_page_num
	elif pagenum <=0 :
		pagenum=1
	begin_index=pagelimit*(pagenum-1)
	end_index=pagelimit*pagenum 
	if end_index > len(inputlist):
		end_index = len(inputlist)
	return inputlist[begin_index: end_index]

def check_string_empty(content):
	return not content or content == "" or content.isspace()

def get_previous_next_page(page_num, current_page):
	previous = current_page -1
	next = current_page +1
	if previous <= 0:
		previous =1
	if next > page_num:
		next = page_num
	return [previous, next]

def tag_split(tag_string, delimit=DEFAULT_DELIMIT):
	tag_list = tag_string.replace(' ','').lower().split(delimit)
  	for x in xrange(len(tag_list)):
  		tag_list[x] = tag_list[x].strip()
		if tag_list[x] == '':
			tag_list[x] = None
	  	tag_list = filter(None, tag_list)
	  	tag_list = list(set(tag_list))
  	return tag_list

def merge_tags(tag_list):
	tags=""
	if len(tag_list) != 0:
		for t in tag_list:
			tags+=t+DEFAULT_DELIMIT+" "
		return tags[:len(tags)-2]
	else:
		return ""