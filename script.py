import json
import random
import urllib.request, urllib.parse
from prettytable import PrettyTable

userHandles = [
    "abhi_.25",
    "abhijit1505",
    "Deepanshu_Singh",
    "dibas",
    "dolamanee6122",
    "Evil_Nobita",
    "saifncoder",
]
availableTags = [
    "binary search",
    "bitmasks",
    "brute force",
    "combinatorics",
    "constructive algorithms",
    "data structures",
    "dfs and similar",
    "divide and conquer",
    "dp",
    "dsu",
    "games",
    "graphs",
    "greedy",
    "implementation",
    "number theory",
    "probabilities",
    "shortest paths",
    "sortings",
    "strings",
    "trees",
]
questionRatings = [1200, 1300, 1400, 1500, 1600, 1700, 1800]
URL_START = "https://codeforces.com/api/"


def checkSolvedByUser(que, userHandle):
    contestId = str(que["contestId"])
    index = que["index"]
    name = que["name"]
    urlForSubmission = (
        URL_START
        + "contest.status?contestId="
        + contestId
        + "&from=1&count=100&handle="
        + userHandle
    )

    with urllib.request.urlopen(urlForSubmission) as url:
        submissionList = json.loads(url.read().decode())
        if not submissionList["status"] == "OK":
            return None
        submissionList = submissionList["result"]
        for submission in submissionList:
            problem = submission["problem"]
            if problem["name"] == name and submission["verdict"] == "OK":
                return True
    return False


def checkQuestionNotSolved(que):
    for userHandle in userHandles:
        if checkSolvedByUser(que, userHandle):
            return False
    return True


def getQuestionId(queRating, queTag):
    urlForProblem = (
        URL_START
        + "problemset.problems?tags="
        + urllib.parse.quote(queTag)
        + ";"
        + str(queRating)
        + "-"
        + str(queRating)
    )

    with urllib.request.urlopen(urlForProblem) as url:
        quesList = json.loads(url.read().decode())
        if not quesList["status"] == "OK":
            return None
        quesList = quesList["result"]["problems"]
        for _ in range(100):
            que = random.choice(quesList)
            if not "rating" in que or not que["rating"] == queRating:
                continue
            if checkQuestionNotSolved(que):
                return que
    return None


outputTable = PrettyTable(["Contest ID", "Question", "Name", "Rating", "Tags"])
for questionRating in questionRatings:
    question = None
    print("Checking for problems with rating " + str(questionRating) + "...")
    for _ in range(10):
        if question:
            break
        questionTag = random.choice(availableTags)
        question = getQuestionId(questionRating, questionTag)
    if not question:
        print("Cant find valid Problem")
        exit()
    outputTable.add_row(
        [
            question["contestId"],
            question["index"],
            question["name"],
            question["rating"],
            question["tags"],
        ]
    )
print(outputTable)
