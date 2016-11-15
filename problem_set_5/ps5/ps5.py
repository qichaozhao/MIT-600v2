# 6.00 Problem Set 5
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

# TODO: NewsStory

class NewsStory:

    def __init__(self, guid, title, subject, summary, link):
        # this is the constructor
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_subject(self):
        return self.subject

    def get_summary(self):
        return self.summary

    def get_link(self):
        return self.link


#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5
from string import translate,maketrans,punctuation

class WordTrigger(Trigger):
    def __init__(self, word):
        self.word = word

    def is_word_in(self, text):

        # make translation table and split text into list of words
        T = maketrans(punctuation, ' '*len(punctuation))
        word_list = translate(text, T).split()

        # check for word in
        if self.word in word_list:
            return True
        else:
            return False

class TitleTrigger(WordTrigger):
    def __init__(self, word):
        self.word = str(word).lower()
        # WordTrigger.__init__(self, self.word)

    def evaluate(self, story):
        # lower case title
        title = str(story.get_title()).lower()
        if WordTrigger.is_word_in(self, title):
            return True
        else:
            return False


class SubjectTrigger(WordTrigger):
    def __init__(self, word):
        self.word = str(word).lower()

    def evaluate(self, story):
        subject = str(story.get_subject()).lower()
        if WordTrigger.is_word_in(self, subject):
            return True
        else:
            return False

class SummaryTrigger(WordTrigger):
    def __init__(self, word):
        self.word = str(word).lower()

    def evaluate(self, story):
        summary = str(story.get_summary()).lower()
        if WordTrigger.is_word_in(self, summary):
            return True
        else:
            return False

# Composite Triggers
# Problems 6-8

class NotTrigger(Trigger):
    def __init__(self, T):
        self.trigger = T

    def evaluate(self, x):
        if self.trigger.evaluate(x):
            return False
        else:
            return True

class AndTrigger(Trigger):
    def __init__(self, T1, T2):
        self.trigger1 = T1
        self.trigger2 = T2

    def evaluate(self, x):
        if self.trigger1.evaluate(x) and self.trigger2.evaluate(x):
            return True
        else:
            return False

class OrTrigger(Trigger):
    def __init__(self, T1, T2):
        self.trigger1 = T1
        self.trigger2 = T2

    def evaluate(self, x):
        if self.trigger1.evaluate(x) or self.trigger2.evaluate(x):
            return True
        else:
            return False


# Phrase Trigger
# Question 9

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase

    def evaluate(self, story):
        in_title = self.phrase in story.get_title()
        in_subject = self.phrase in story.get_subject()
        in_summary = self.phrase in story.get_summary()

        if in_title or in_subject or in_summary:
            return True
        else:
            return False



#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist, triggers):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    filtered = []
    for s in stories:
        for t in triggerlist:
            if triggers[t].evaluate(s):
                filtered.append(s)

    return filtered

#======================
# Part 4
# User-Specified Triggers
#======================

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    triggers = {}
    triggerList = []
    for l in lines:
        # for each line let's check what we have
        tmp = l.split(' ')
        if tmp[0] == 'ADD':
            triggerList.extend(tmp[1:])
        else:
            tmp_name = tmp[0]
            tmp_type = tmp[1]
            tmp_arg = tmp[2:]
            if tmp_type == 'TITLE':
                triggers[tmp_name] = TitleTrigger(tmp_arg[0])
            elif tmp_type == 'SUBJECT':
                triggers[tmp_name] = SubjectTrigger(tmp_arg[0])
            elif tmp_type == 'SUMMARY':
                triggers[tmp_name] = SummaryTrigger(tmp_arg[0])
            elif tmp_type == 'PHRASE':
                triggers[tmp_name] = PhraseTrigger(' '.join(tmp_arg))
            elif tmp_type == 'NOT':
                triggers[tmp_name] = NotTrigger(triggers[tmp_arg[0]])
            elif tmp_type == 'AND':
                triggers[tmp_name] = AndTrigger(triggers[tmp_arg[0]],triggers[tmp_arg[1]])
            elif tmp_type == 'OR':
                triggers[tmp_name] = OrTrigger(triggers[tmp_arg[0]],triggers[tmp_arg[1]])
    # print triggers
    # print triggerList
    return triggers, triggerList

import thread

def main_thread(p):
    # # A sample trigger list - you'll replace
    # # this with something more configurable in Problem 11
    # t1 = SubjectTrigger("Obama")
    # t2 = SummaryTrigger("MIT")
    # t3 = PhraseTrigger("Supreme Court")
    # t4 = OrTrigger(t2, t3)
    # triggerlist = [t1, t4]
    
    # TODO: Problem 11
    # After implementing readTriggerConfig, uncomment this line 
    triggers, triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []
    
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # print triggers['t3'].evaluate(stories[0])
        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist, triggers)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

