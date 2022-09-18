from math import sqrt, floor
import requests

EXP_FIELD = 0
LVL_FIELD = 0

BASE = 10000
GROWTH = 2500

HALF_GROWTH = 0.5 * GROWTH

REVERSE_PQ_PREFIX = -(BASE - 0.5 * GROWTH)/GROWTH
REVERSE_CONST = REVERSE_PQ_PREFIX * REVERSE_PQ_PREFIX
GROWTH_DIVIDES_2 = 2/GROWTH

def getLevel(exp):
    return floor(1+REVERSE_PQ_PREFIX + sqrt(REVERSE_CONST+GROWTH_DIVIDES_2*exp))

def getExactLevel(exp):
    return getLevel(exp) + getPercentageToNextLevel(exp)

def getExpFromLevelToNext(level):
    return GROWTH * (level-1) + BASE

def getTotalExpToLevel(level):
    lv = floor(level)
    x0 = getTotalExpToFullLevel(lv)
    if level == lv:
        return x0
    else:
        return (getTotalExpToFullLevel(lv+1) - x0) * (level % 1) + x0

def getTotalExpToFullLevel(level):
    return (HALF_GROWTH * (level-2) + BASE) * (level-1)

def getPercentageToNextLevel(exp):
    lv = getLevel(exp)
    x0 = getTotalExpToLevel(lv)
    return (exp-x0) / (getTotalExpToLevel(lv+1) - x0)

def getExperience(EXP_FIELD, LVL_FIELD):
    exp = int(EXP_FIELD)
    exp += getTotalExpToFullLevel(LVL_FIELD+1)
    return exp

def getRank(user, api):
        """ This function returns a player's rank, from their data. """
        data = requests.get(f"https://api.hypixel.net/player?key={api}&name={user}").json()

        if "rank" in data["player"] and data["player"]["rank"] != "NORMAL":
            rank = data["player"]["rank"]
        elif "newPackageRank" in data["player"]:
            rank = data["player"]["newPackageRank"]
        elif "packageRank" in data["player"]:
            rank = data["player"]["packageRank"]
        else:
            rank = "Non-Donor"

        rank = rank.replace('*', '')
        rank = rank.replace('`', '')
        rank = rank.replace('_', '')
        rank = rank.replace('PLUS', '+')

        return rank