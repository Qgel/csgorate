#!/usr/bin/python

import jinja2
from datetime import datetime 

class SiteGen:
  def __init__(self, globalVars):
    templateLoader = jinja2.FileSystemLoader( searchpath="./template")
    self.env = jinja2.Environment(loader = templateLoader, trim_blocks = True)  
    self.env.globals.update(globalVars);

  def winTable(self, ranking, count):
    lb = [r[0] for r in ranking.ranking()][:count]
    table = [["WIN%"] + lb]
    for t1 in lb:
      row = [t1]
      for t2 in lb:
        if t1 == t2:
          row.append('-')
        else:
          row.append(ranking.winChance(t1, t2) * 100)
      table.append(row)
    return table


  def genWinTablePage(self, ranking):
    template = self.env.get_template("winTable.html")
    
    wt = self.winTable(ranking, 25)
    example = {
        "winner" : wt[4][0],
        "loser"  : wt[0][5],
        "chance" : wt[4][5]
        }

    templateVars = {
        "curMap" : ranking.name,
        "numGames" : ranking.gameCount,
        "genTime" : datetime.utcnow(),
        "winTable" : wt,
        "example" : example,
        "curPage" : "win"
        }

    return template.render(templateVars)

  def genRankingTablePage(self, ranking):
    template = self.env.get_template("ranking.html")
    
    rk = ranking.ranking()
    templateVars = {
        "curMap" : ranking.name,
        "numGames" : ranking.gameCount,
        "genTime" : datetime.utcnow(),
        "rankingTable" : rk,
        "curPage" : "rank"
        }
    return template.render(templateVars)
        

  def test(self, ranking):
    f = open("html/test.html", 'w')
    f.write(self.genWinTablePage(ranking))
    f.close();




  
