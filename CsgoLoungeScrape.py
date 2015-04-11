#!/usr/bin/python
from lxml import html

class CsgoLoungeScraper:

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
      "flyingv" : "The Flying V"
  }

  def fixName(self, name):
    if name.lower() in self.nameMap:
      return self.nameMap[name.lower()]
    return name
                    

  def getGames(self, start, end):
    result = []

    for i in range(start,end):
      try:
        t = html.parse('http://csgolounge.com/match?m={0}'.format(i))
      except:
        continue
      outcome = map(lambda x: x.text, t.findall(".//div[@class='box-shiny-alt']//b"))
      odds = map(lambda x: int(x.text[:-1]), t.findall(".//div[@class='box-shiny-alt']//i"))

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
        print '{0}:{1}'.format(game['winner'], game['loser'])
        result.append(game)
    return result

