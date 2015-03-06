#!/usr/bin/python
from lxml import html
from datetime import datetime, timedelta

class Scraper:

  def __init__(self):
    self.cache = []

  # Scrape 'num' games from Hltv.org starting at 'start'
  def fetch(self, start, num):
    games = []
    page = 0
    while(len(games) < num):
      t = html.parse('http://www.hltv.org/?pageid=188&gameid=2&offset={0}'.format(page*50 + start))
      page += 1

      scores = t.xpath(".//*[starts-with(@href, '/?pageid=179')]")
      dates = t.xpath(".//*[starts-with(@href, '/?pageid=188&matchid=')]")
      maps = t.xpath(".//div[@style='font-weight:normal;width:10%;float:left;text-align:center;font-weight:normal;color:black;']")

      #get scores and maps from html
      scores = [r.text_content().replace(')','').split('(') for r in scores]
      dates = [datetime.strptime(d.text_content(), '%d/%m %y') for d in dates]
      maps = [m.text_content() for m in maps]

      #group scores and sort so that winner is always the first entry
      scores = [sorted(scores[i*2:(i+1)*2], key=lambda r: int(r[1]), reverse=True) for i in range((len(scores)/2))]
      
      # combine map and score data
      results = zip(scores, maps, dates)

      games += results
    return games

  def mapGames(self,matches):
    mappedGames = {}
    for r in matches:
      game = (r[0][0][0].encode("ascii",errors="ignore").strip(),r[0][1][0].encode("ascii", errors="ignore").strip())
      mappedGames.setdefault(r[1], []).append(game)
      mappedGames.setdefault('all',[]).append(game)
    return mappedGames

  def decidedMatches(self):
    # filter draws
    matches = filter(lambda x: x[0][0][1] != x[0][1][1], self.cache)
    return matches

  def getGamesForDays(self, days, start = 0):
    tStart = datetime.utcnow() - timedelta(start)

    matches = self.decidedMatches() 
    pos = next((i for i,v in enumerate(matches) if (tStart - v[2] > timedelta(days))), None)
    if pos == None:
      self.getGames(0, len(self.cache) + 200)
      return self.getGamesForDays(days, start)

    pStart = next((i for i,v in enumerate(matches) if (v[2] < tStart)), None) 

    return self.mapGames(matches[pStart:pos])

  # returns a dictionary with map name as key, and played games on that map ordered from 
  # newest to oldest. Special key 'all' contains games from all maps
  def getGames(self, start, num):
    matches = self.decidedMatches()
    # check if the required matches are already in our cache
    cacheLen = len(self.cache)
    if start + num > len(matches):
      m = self.fetch(len(self.cache), (start + num) - len(matches))
      self.cache = self.cache + m
      return self.getGames(start, num)

    mappedGames = self.mapGames(matches)

    for k in mappedGames:
      mappedGames[k] = mappedGames[k][start : start + num]

    #results = [((r[0][0][0].encode("utf8").strip(),r[0][1][0].encode("utf8").strip()),r[1]) for r in matches[start : num + start]]
    #Create a dictionary of maps -> match results
    #mappedGames = {}
    #for r in results:
    #  mappedGames.setdefault(r[1], []).append(r[0])
    #  mappedGames.setdefault('all', []).append(r[0])

    return mappedGames
