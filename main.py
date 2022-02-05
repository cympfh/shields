import io
import logging
import urllib.parse

import cachetools
import requests
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from rich.logging import RichHandler

logging.basicConfig(level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
logger = logging.getLogger("shields")
app = FastAPI(name="shields")


class ShieldsAPI:
    @staticmethod
    async def get(params: dict[str, str]) -> StreamingResponse:
        query = urllib.parse.urlencode(params)
        url = f"https://img.shields.io/static/v1?{query}"
        data = requests.get(url)
        return StreamingResponse(
            io.BytesIO(data.text.encode("utf-8")), status_code=200, media_type="image/svg+xml"
        )


class AtCoder:
    @cachetools.cached(cache=cachetools.TTLCache(maxsize=1024, ttl=600))
    def rating(username: str, color: str = "auto") -> tuple[int, str]:
        """Returns rating and its color"""
        url = f"https://atcoder.jp/users/{username}/history/json"
        rating = requests.get(url).json()[-1].get("NewRating", 0)
        if color == "auto":
            # https://atcoder.jp/posts/16
            if rating >= 2800:
                color = "red"
            elif rating >= 2400:
                color = "orange"
            elif rating >= 2000:
                color = "yellow"
            elif rating >= 1600:
                color = "blue"
            elif rating >= 1200:
                color = "cyan"
            elif rating >= 800:
                color = "brightgreen"
            elif rating >= 400:
                color = "brown"
            else:
                color = "lightgray"

        return rating, color


class Codeforces:
    @cachetools.cached(cache=cachetools.TTLCache(maxsize=1024, ttl=600))
    def rating(username: str, color: str = "auto") -> tuple[int, str]:
        """Returns rating and its color

        NOTE: This is slow.
        """
        url = f"https://codeforces.com/api/user.info?handles={username}"
        rating = requests.get(url).json().get("result", [{"rating": 0}])[0].get("rating", 0)
        if color == "auto":
            # https://codeforces.com/blog/entry/68288
            if rating >= 2400:
                color = "red"
            elif rating >= 2000:
                color = "orange"
            elif rating >= 1800:
                color = "purple"
            elif rating >= 1600:
                color = "blue"
            elif rating >= 1400:
                color = "cyan"
            elif rating >= 1200:
                color = "green"
            elif rating >= 1000:
                color = "brightgreen"
            else:
                color = "lightgray"
        return rating, color


class Speedrun:
    @cachetools.cached(cache=cachetools.LRUCache(maxsize=1024))
    def game(gamename: str) -> str:
        url = f"https://www.speedrun.com/api/v1/games?name={gamename}"
        return requests.get(url).json().get("data", [])[0].get("id", "")

    @cachetools.cached(cache=cachetools.TTLCache(maxsize=1024, ttl=600))
    def runs(username: str) -> list:
        url = f"https://www.speedrun.com/api/v1/users/{username}/personal-bests"
        return requests.get(url).json().get("data", [])

    @staticmethod
    async def place(username: str, gamename: str) -> int:
        records = Speedrun.runs(username)
        gameid = Speedrun.game(gamename)
        for record in records:
            if record.get("run", {}).get("game", "") == gameid:
                return record.get("place", 0)
        raise Exception(f"Not found Run for Game(name={gamename}, id={gameid})")

    @staticmethod
    async def realtime(username: str, gamename: str) -> int:
        records = Speedrun.runs(username)
        gameid = Speedrun.game(gamename)
        for record in records:
            if record.get("run", {}).get("game", "") == gameid:
                return record.get("run", {}).get("times", {}).get("realtime_t", 0)
        raise Exception(f"Not found Run for Game(name={gamename}, id={gameid})")


@app.get("/shields")
async def get(label: str, message: str, color: str):
    return await ShieldsAPI.get({"label": label, "message": message, "color": color})


@app.get("/shields/atcoder/rating")
async def get(username: str, color: str = "auto"):
    rating, color = AtCoder.rating(username, color)
    return await ShieldsAPI.get({"label": "AtCoder", "message": rating, "color": color})


@app.get("/shields/codeforces/rating")
async def get(username: str, color: str = "auto"):
    rating, color = Codeforces.rating(username, color)
    return await ShieldsAPI.get({"label": "Codeforces", "message": rating, "color": color})


@app.get("/shields/speedrun/place")
async def get(username: str, gamename: str, color: str = "green"):
    place = await Speedrun.place(username, gamename)

    def ordinal(n: int) -> str:
        if n % 10 == 1 and n != 11:
            return f"{n}st"
        elif n % 10 == 2 and n != 12:
            return f"{n}nd"
        elif n % 10 == 3 and n != 13:
            return f"{n}rd"
        else:
            return f"{n}th"

    return await ShieldsAPI.get({"label": gamename, "message": ordinal(place), "color": color})


@app.get("/shields/speedrun/realtime")
async def get(username: str, gamename: str, color: str = "green"):
    realtime = await Speedrun.realtime(username, gamename)  # sec

    def format(realtime: int) -> str:
        days = realtime // (24 * 60 * 60)
        hours = realtime // (60 * 60) % 24
        minutes = realtime // 60 % 60
        seconds = realtime % 60
        if days > 0:
            return f"{days}d {hours}h {minutes}m {seconds}s"
        elif hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    return await ShieldsAPI.get({"label": gamename, "message": format(realtime), "color": color})
