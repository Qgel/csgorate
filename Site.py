#!/usr/bin/python

from HltvScrape import Scraper
from Ranking import Ranking
from SiteGen import SiteGen

matchCounts = [300, 500, 800]
minMatches = 20
outDir = "./html/"

def writePage(page, name):
  with open(outDir + "{0}.html".format(name), 'w') as f:
    f.write(page)

def gen():
  availMaps = []
  scraper = Scraper()
  scraper.getGames(0, max(matchCounts))
  for cnt in matchCounts:
    matches = scraper.getGames(0, cnt)

    # find maps with at least minMatches games played
    suffMaps = filter(lambda k: len(matches[k]) > minMatches, matches)

    # sort Maps alphabetically
    suffMaps = sorted(suffMaps)

    availMaps.append(suffMaps)

    baseVars = {
        "maps" : suffMaps,
        "matchCounts" : matchCounts,
        "curCount" : cnt,
        "availMaps" : availMaps,
        "curID" : matchCounts.index(cnt)
        }
    sg = SiteGen(globalVars = baseVars)

    for mapName in suffMaps:
      r = Ranking(mapName, matches[mapName])
      wtPage = sg.genWinTablePage(r)
      rkPage = sg.genRankingTablePage(r)
      writePage(wtPage, "{0}_{1}_win".format(mapName, cnt))
      writePage(rkPage, "{0}_{1}_rank".format(mapName, cnt))
      if matchCounts[0] == cnt and mapName == "all":
        writePage(wtPage, "index")


if __name__ == "__main__":
  gen()
