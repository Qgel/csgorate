#!/usr/bin/python
from lxml import html

class CsgoLoungeScraper:

  # Mapping of names on csgolounge to names 
  # used by the ranking (i.e. from Hltv.org)
  nameMap = {
      "cw" : "CPH Wolves",
      "vp" : "Virtus.pro",
      "dignitas" : "dignitas",
      "fsid3" : "FlipSid3",
      "inshock" : "INSHOCK",
      "cplay" : "CPLAY",
      "g2" : "Gamers2",
      "trident" : "TRIDENT",
      "sline" : "Streamline",
      "chiefs" : "The Chiefs",
      "avantg" : "AVANT GARDE",
      "vox" : "Vox Eminor",
      "imm" : "Immunity",
      "fnatic" : "fnatic",
      "na'vi" : "Natus Vincere",
      "penta" : "PENTA",
      "fxfire" : "Fenix Fire",
      "flyingv" : "The Flying V",
      "g4u" : "Games4u",
      "hr" : "HellRaisers",
      "dc" : "Damage Control",
      "x6tence" : "x6tence",
      "mouz" : "mousesports",
      "piter" : "PiTER"
  }

  def fixName(self, name):
    if name.lower() in self.nameMap:
      return self.nameMap[name.lower()]
    return name

  def __init__(self):
    self.cache = []
    self.cacheIndex = None
                    

  def getGames(self, targetDays):
    if len(self.cache) == 0 or targetDays >= self.cache[-1]['days']:
      if self.cacheIndex is None:
        t = html.parse('http://csgolounge.com')
        self.cacheIndex = int(t.find(".//div[@class='matchleft']/a").attrib['href'][-4:])
      self._fetchGames(targetDays)
    return self._getCachedGames(targetDays)

  def _getCachedGames(self, targetDays):
    pos = next((i for i,v in enumerate(self.cache) if v['days'] > targetDays), len(self.cache))
    return self.cache[:pos]

  def _fetchGames(self, targetDays):
    days = 0
    while(days <= targetDays):
      try:
        t = html.parse('http://csgolounge.com/match?m={0}'.format(self.cacheIndex))
      except:
        continue
      self.cacheIndex -= 1

      outcome = map(lambda x: x.text, t.findall(".//div[@class='box-shiny-alt']//b"))
      odds = map(lambda x: int(x.text[:-1]), t.findall(".//div[@class='box-shiny-alt']//i"))
      timeData = []
      try:
        timeData = t.find(".//div[@class='box-shiny-alt']/div/div").text.split(" ")
      except:
        continue

      if len(timeData) >= 2:
        if "day" in timeData[1]:
          days = int(timeData[0])
        elif "month" in timeData[1]:
          days = int(timeData[0]) * 30

      game = {}
      if(len(outcome) < 2):
        continue

      if 'win' in outcome[0]:
        game = {'winner' : [outcome[0][0:(outcome[0].index('(') - 1)], odds[0]], 'loser' : [outcome[1], odds[1]]}
      elif 'win' in outcome[1]:
        winner = 1
        game = {'winner' : [outcome[1][0:(outcome[1].index('(') - 1)], odds[1]], 'loser' : [outcome[0], odds[0]]}

      if(len(game) > 0):
        game['winner'][0] = self.fixName(game['winner'][0])
        game['loser'][0] = self.fixName(game['loser'][0])
        game['days'] = days
        print '{0}:{1}'.format(game['winner'], game['loser'])
        self.cache.append(game)
