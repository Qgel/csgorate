#!/usr/bin/python
from HltvScrape import Scraper
from Ranking import Ranking
from SiteGen import SiteGen

matchDays = [30, 60, 180]
indexDays = 60
minMatches = 20
outDir = "./html/"

def writePage(page, name):
  with open(outDir + "{0}.html".format(name), 'w') as f:
    f.write(page)

def gen():
  availMaps = []
  scraper = Scraper()
  scraper.getGamesForDays(max(matchDays))
  for (idx,cnt) in enumerate(matchDays):
    matches = scraper.getGamesForDays(cnt)

    # find maps with at least minMatches games played
    suffMaps = filter(lambda k: len(matches[k]) > minMatches, matches)

    # sort Maps alphabetically
    suffMaps = sorted(suffMaps)

    availMaps.append(suffMaps)

    baseVars = {
        "maps" : suffMaps,
        "matchDays" : matchDays,
        "curCount" : cnt,
        "availMaps" : availMaps,
        "curID" : idx
        }
    sg = SiteGen(globalVars = baseVars)

    for mapName in suffMaps:
      r = Ranking(mapName, matches[mapName])
      wtPage = sg.genWinTablePage(r)
      rkPage = sg.genRankingTablePage(r)
      writePage(wtPage, "{0}_{1}_win".format(mapName, cnt))
      writePage(rkPage, "{0}_{1}_rank".format(mapName, cnt))
      if cnt == indexDays and mapName == "all":
        writePage(wtPage, "index")
        writePage(wtPage, "rating") # for compatibility with the old url


if __name__ == "__main__":
  gen()
