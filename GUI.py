from testscapper import *
from UndergroundScrapper import *
from appJar import gui

def press(btn):
	subredditName = app.getEntry('Name of Subreddit to Scrape: r/').lower()
	print("Scrapping started on "+subredditName)
	scrap_go(subredditName)
def press(btn):
	demoPage = app.getEntry('Scrape Democratic Underground Page').lower()
	print("Scrapping started on "+demoPage)
	democrat_go(demoPage)

app=gui("NoCap Scraping Tool")
app.setFont(20)
app.setBg("Teal")
app.setFg("White")
app.addLabel("title","NoCap Scrapping" )
app.addLabelEntry("Name of Subreddit to Scrape: r/")
app.addButton("Scrape Subreddit", press)
app.addLabelEntry("Name of Page to Scrape on Democratic Underground: ")
app.addButton("Scrape Democratic Underground Page", press)
app.enableEnter(press)
app.go()

