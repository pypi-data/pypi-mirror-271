import asyncio
import logging.config
import math
import random
import re
import sys
import time
import aiofiles
import orjson
import websockets

from logging import Logger
from httpx import URL, AsyncClient, Limits, ReadTimeout, Response
from httpx_socks import AsyncProxyTransport
from tqdm.asyncio import tqdm_asyncio
from .asyncLogin import asyncLogin
from .constants import (
    Operation,
    SpaceState,
    trending_params,
)
from .util import (
    BLUE,
    CYAN,
    GREEN,
    MAGENTA,
    RED,
    RESET,
    YELLOW,
    Path,
    batch_ids,
    build_params,
    find_key,
    flatten,
    get_cursor,
    get_headers,
    get_json,
    init_session,
    log,
    save_json,
    set_qs,
    urlsplit,
)


class AsyncScraper:
    """Twitter scraper class for async operations.

    It performs actions like getting user data, tweets, followers, etc asynchronously.
    """

    def __init__(
        self,
        save: bool = True,
        debug: bool = False,
        pbar: bool = True,
        out: str = "data",
        proxies: str = None,
        makeFiles: bool = False,
        httpxSocks: bool = False,
        **kwargs,
    ):
        """Initialize the scraper.

        Args:
            save (bool, optional): Save data to disk. Defaults to True.
            debug (bool, optional): Debug mode. Defaults to False.
            pbar (bool, optional): Show progress bar. Defaults to True.
            out (str, optional): Output directory. Defaults to "data".
            makeFiles (bool, optional): Make files. Defaults to False.

        Keyword Args:
            max_connections (int, optional): Maximum connections. Defaults to 100.
        """
        self.makeFiles = makeFiles
        self.save = save
        self.debug = debug
        self.pbar = pbar
        self.out = Path(out)
        self.guest = False
        self.logger = self._init_logger(**kwargs)
        self.max_connections = kwargs.get("max_connections", 100)

        if httpxSocks:
            self.transport = AsyncProxyTransport.from_url(proxies)
            self.proxies = None
            self.proxyString = proxies
        else:
            self.proxies = proxies
            self.transport = None
            self.proxyString = proxies


        # print(f'Logger: {self.logger}')

    async def asyncAuthenticate(
        self,
        email: str = None,
        username: str = None,
        password: str = None,
        session: AsyncClient = None,
        proxies: str = None,
        httpxSocks: bool = False,
        cookies: dict = None,
        **kwargs,
    ) -> AsyncClient:
        """
        This is used to authenticate the account.

        If email:username:pass is provided will attempt to login
        If cookies ct0&auth_token are provided will attempt to validate the session using cookies.

        Args:
            email (str): Email of the account.
            username (str): Username of the account.
            password (str): Password of the account.
            session (AsyncClient): Session to use.
            proxies (str): Proxies to use.
            cookies (dict): Cookies to use.
            **kwargs: Additional arguments to pass to the logger.

        Returns:
            AsyncClient: The session authenticated session
        """

        self.email = email
        self.username = username
        self.password = password
        self.twitterId = False
        self.twitterRestId = False
        self.cookies = cookies

        if httpxSocks:
            self.transport = AsyncProxyTransport.from_url(proxies)
            self.proxies = None
            self.proxyString = proxies
        else:
            self.proxies = proxies
            self.transport = None
            self.proxyString = proxies

        # print(f'AsyncAcc Got: {email}, {username}, {password}, {session}, {self.cookies}, {self.proxies}')

        self.session = await self._async_validate_session(
            email=self.email, 
            username=self.username, 
            password=self.password, 
            session=session, 
            cookies=self.cookies,
            **kwargs
        )


        return self.session

    async def asyncUsers(self, screen_names: list[str], **kwargs) -> list[dict]:
        """
        Get user data by screen names.

        @param screen_names: list of screen names (usernames)
        @param kwargs: optional keyword arguments
        @return: list of user data as dicts
        """
        return await self._asyncrun(Operation.UserByScreenName, screen_names, **kwargs)

    async def asyncTweetsById(self, tweet_ids: list[int], **kwargs) -> list[dict]:
        """
        Get tweet metadata by tweet ids.

        @param tweet_ids: list of tweet ids
        @param kwargs: optional keyword arguments
        @return: list of tweet data as dicts
        """
        return await self._asyncrun(Operation.TweetResultByRestId, tweet_ids, **kwargs)

    async def asyncTweetsDetails(self, tweet_ids: list[int], **kwargs) -> list[dict]:
        """
        Get tweet data by tweet ids.

        Includes tweet metadata as well as comments, replies, etc.

        @param tweet_ids: list of tweet ids
        @param kwargs: optional keyword arguments
        @return: list of tweet data as dicts
        """
        return await self._asyncrun(Operation.TweetDetail, tweet_ids, **kwargs)

    async def asyncTweets(self, user_ids: list[int], **kwargs) -> list[dict]:
        """
        Get tweets by user ids.

        Metadata for users tweets.

        @param user_ids: list of user ids
        @param kwargs: optional keyword arguments
        @return: list of tweet data as dicts
        """
        return await self._asyncrun(Operation.UserTweets, user_ids, **kwargs)

    async def asyncTweetsAndReplies(self, user_ids: list[int], **kwargs) -> list[dict]:
        """
        Get tweets and replies by user ids.

        Tweet metadata, including replies.

        @param user_ids: list of user ids
        @param kwargs: optional keyword arguments
        @return: list of tweet data as dicts
        """
        return await self._asyncrun(Operation.UserTweetsAndReplies, user_ids, **kwargs)

    async def asyncMedia(self, user_ids: list[int], **kwargs) -> list[dict]:
        """
        Get media by user ids.

        Tweet metadata, filtered for tweets containing media.

        @param user_ids: list of user ids
        @param kwargs: optional keyword arguments
        @return: list of tweet data as dicts
        """
        return await self._asyncrun(Operation.UserMedia, user_ids, **kwargs)

    async def asyncLikes(self, user_ids: list[int], **kwargs) -> list[dict]:
        """
        Get likes by user ids.

        Tweet metadata for tweets liked by users.

        @param user_ids: list of user ids
        @param kwargs: optional keyword arguments
        @return: list of tweet data as dicts
        """
        return await self._asyncrun(Operation.Likes, user_ids, **kwargs)

    async def asyncFollowers(self, user_ids: list[int], **kwargs) -> list[dict]:
        """
        Get followers by user ids.

        User data for users followers list.

        @param user_ids: list of user ids
        @param kwargs: optional keyword arguments
        @return: list of user data as dicts
        """
        return await self._asyncrun(Operation.Followers, user_ids, **kwargs)

    async def asyncFollowing(self, user_ids: list[int], **kwargs) -> list[dict]:
        """
        Get following by user ids.

        User metadata for users following list.

        @param user_ids: list of user ids
        @param kwargs: optional keyword arguments
        @return: list of user data as dicts
        """
        return await self._asyncrun(Operation.Following, user_ids, **kwargs)

    async def asyncFavoriters(self, tweet_ids: list[int], **kwargs) -> list[dict]:
        """
        Get favoriters by tweet ids.

        User data for users who liked these tweets.

        @param tweet_ids: list of tweet ids
        @param kwargs: optional keyword arguments
        @return: list of user data as dicts
        """
        return await self._asyncrun(Operation.Favoriters, tweet_ids, **kwargs)

    async def asyncRetweeters(self, tweet_ids: list[int], **kwargs) -> list[dict]:
        """
        Get retweeters by tweet ids.

        User data for users who retweeted these tweets.

        @param tweet_ids: list of tweet ids
        @param kwargs: optional keyword arguments
        @return: list of user data as dicts
        """
        return await self._asyncrun(Operation.Retweeters, tweet_ids, **kwargs)

    async def asyncTweetStats(self, user_ids: list[int], **kwargs) -> list[dict]:
        """
        Get tweet statistics by user ids.

        @param user_ids: list of user ids
        @param kwargs: optional keyword arguments
        @return: list of tweet statistics as dicts
        """
        return await self._asyncrun(Operation.TweetStats, user_ids, **kwargs)

    async def asyncUsersByIds(self, user_ids: list[int], **kwargs) -> list[dict]:
        """
        Get user data by user ids.

        Special batch query for user data. Most efficient way to get user data.

        @param user_ids: list of user ids
        @param kwargs: optional keyword arguments
        @return: list of user data as dicts
        """
        return await self._asyncrun(
            Operation.UsersByRestIds, batch_ids(user_ids), **kwargs
        )

    async def asyncRecommendedUsers(
        self, user_ids: list[int] = None, **kwargs
    ) -> list[dict]:
        """
        Get recommended users by user ids, or general recommendations if no user ids are provided.

        @param user_ids: list of user ids
        @param kwargs: optional keyword arguments
        @return: list of recommended users data as dicts
        """
        if user_ids:
            contexts = [
                {"context": orjson.dumps({"contextualUserId": x}).decode()}
                for x in user_ids
            ]
        else:
            contexts = [{"context": None}]
        return await self._asyncrun(Operation.ConnectTabTimeline, contexts, **kwargs)

    async def asyncProfileSpotlights(
        self, screen_names: list[str], **kwargs
    ) -> list[dict]:
        """
        Get user data by screen names.

        This endpoint is included for completeness only.
        Use the batched query `users_by_ids` instead if you wish to pull user profile data.

        @param screen_names: list of user screen names (usernames)
        @param kwargs: optional keyword arguments
        @return: list of user data as dicts
        """
        return await self._asyncrun(
            Operation.ProfileSpotlightsQuery, screen_names, **kwargs
        )

    async def asyncUsersById(self, user_ids: list[int], **kwargs) -> list[dict]:
        """
        Get user data by user ids.

        This endpoint is included for completeness only.
        Use the batched query `users_by_ids` instead if you wish to pull user profile data.


        @param user_ids: list of user ids
        @param kwargs: optional keyword arguments
        @return: list of user data as dicts
        """
        return await self._asyncrun(Operation.UserByRestId, user_ids, **kwargs)

    async def asyncDownloadMedia(
        self,
        ids: list[int],
        photos: bool = True,
        videos: bool = True,
        chunk_size: int = 8192,
    ) -> None:
        """
        Download media from tweets by tweet ids.

        @param ids: list of tweet ids containing media
        @param photos: flag to include photos
        @param videos: flag to include videos
        @param chunk_size: chunk size for download
        @return: None
        """
        out = Path("media")
        out.mkdir(parents=True, exist_ok=True)
        tweets = self.asyncTweetsById(ids)
        urls = []
        for tweet in tweets:
            tweet_id = find_key(tweet, "id_str")[0]
            url = f"https://twitter.com/i/status/{tweet_id}"
            media = [y for x in find_key(tweet, "media") for y in x]
            if photos:
                photo_urls = list(
                    {
                        u
                        for m in media
                        if "ext_tw_video_thumb" not in (u := m["media_url_https"])
                    }
                )
                [urls.append([url, photo]) for photo in photo_urls]
            if videos:
                video_urls = [
                    x["variants"] for m in media if (x := m.get("video_info"))
                ]
                hq_videos = {
                    sorted(v, key=lambda d: d.get("bitrate", 0))[-1]["url"]
                    for v in video_urls
                }
                [urls.append([url, video]) for video in hq_videos]

        async def process():
            async with AsyncClient(
                headers=self.session.headers,
                cookies=self.session.cookies,
                proxies=self.proxies,
            ) as client:
                tasks = (download(client, x, y) for x, y in urls)
                if self.pbar:
                    return await tqdm_asyncio.gather(*tasks, desc="Downloading media")
                return await asyncio.gather(*tasks)

        async def download(client: AsyncClient, post_url: str, cdn_url: str) -> None:
            name = urlsplit(post_url).path.replace("/", "_")[1:]
            ext = urlsplit(cdn_url).path.split("/")[-1]
            try:
                r = await client.get(cdn_url)
                if self.makeFiles:
                    # print('Making files!!')
                    async with aiofiles.open(out / f"{name}_{ext}", "wb") as fp:
                        for chunk in r.iter_bytes(chunk_size=chunk_size):
                            await fp.write(chunk)
            except Exception as e:
                self.logger.error(
                    f"[{RED}error{RESET}] Failed to download media: {post_url} {e}"
                )

        # asyncio.run(process())
        await process()

    async def asyncTrends(self, utc: list[str] = None) -> dict:
        """
        Get trends for all UTC offsets

        @param utc: optional list of specific UTC offsets
        @return: dict of trends
        """

        async def get_trends(client: AsyncClient, offset: str, url: str):
            try:
                client.headers["x-twitter-utcoffset"] = offset
                r = await client.get(url)
                trends = find_key(r.json(), "item")
                return {t["content"]["trend"]["name"]: t for t in trends}
            except Exception as e:
                self.logger.error(f"[{RED}error{RESET}] Failed to get trends\n{e}")

        async def process():
            url = set_qs("https://twitter.com/i/api/2/guide.json", trending_params)
            offsets = utc or [
                "-1200",
                "-1100",
                "-1000",
                "-0900",
                "-0800",
                "-0700",
                "-0600",
                "-0500",
                "-0400",
                "-0300",
                "-0200",
                "-0100",
                "+0000",
                "+0100",
                "+0200",
                "+0300",
                "+0400",
                "+0500",
                "+0600",
                "+0700",
                "+0800",
                "+0900",
                "+1000",
                "+1100",
                "+1200",
                "+1300",
                "+1400",
            ]
            async with AsyncClient(headers=get_headers(self.session)) as client:
                tasks = (get_trends(client, o, url) for o in offsets)
                if self.pbar:
                    return await tqdm_asyncio.gather(*tasks, desc="Getting trends")
                return await asyncio.gather(*tasks)

        # trends = asyncio.run(process())
        trends = await process()
        out = self.out / "raw" / "trends"
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{time.time_ns()}.json").write_text(
            orjson.dumps(
                {
                    key: value
                    for trendDict in trends
                    for key, value in trendDict.items()
                },
                option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS,
            ).decode(),
            encoding="utf-8",
        )
        return trends

    async def asyncSpaces(
        self,
        *,
        rooms: list[str] = None,
        search: list[dict] = None,
        audio: bool = False,
        chat: bool = False,
        **kwargs,
    ) -> list[dict]:
        """
        Get Twitter spaces data

        - Get data for specific rooms or search for rooms.
        - Get audio and/or chat data for rooms.

        @param rooms: list of room ids
        @param search: list of dicts containing search parameters
        @param audio: flag to include audio data
        @param chat: flag to include chat data
        @param kwargs: optional keyword arguments
        @return: list of spaces data
        """
        if rooms:
            spaces = await self._asyncrun(Operation.AudioSpaceById, rooms, **kwargs)
        else:
            res = await self._asyncrun(Operation.AudioSpaceSearch, search, **kwargs)
            search_results = set(find_key(res, "rest_id"))
            spaces = await self._asyncrun(
                Operation.AudioSpaceById, search_results, **kwargs
            )
        if audio or chat:
            return self._get_space_data(spaces, audio, chat)
        return spaces

    def _get_space_data(self, spaces: list[dict], audio=True, chat=True):
        streams = self._async_check_streams(spaces)
        chat_data = None
        if chat:
            temp = []  # get necessary keys instead of passing large dicts
            for stream in filter(lambda x: x["stream"], streams):
                meta = stream["space"]["data"]["audioSpace"]["metadata"]
                if meta["state"] not in {SpaceState.Running, SpaceState.NotStarted}:
                    temp.append(
                        {
                            "rest_id": meta["rest_id"],
                            "chat_token": stream["stream"]["chatToken"],
                            "media_key": meta["media_key"],
                            "state": meta["state"],
                        }
                    )
            chat_data = self._async_get_chat_data(temp)
        if audio:
            temp = []
            for stream in streams:
                if stream.get("stream"):
                    chunks = self._async_get_chunks(
                        stream["stream"]["source"]["location"]
                    )
                    temp.append(
                        {
                            "rest_id": stream["space"]["data"]["audioSpace"][
                                "metadata"
                            ]["rest_id"],
                            "chunks": chunks,
                        }
                    )
            self._async_download_audio(temp)
        return chat_data

    async def _get_stream(self, client: AsyncClient, media_key: str) -> dict | None:
        params = {
            "client": "web",
            "use_syndication_guest_id": "false",
            "cookie_set_host": "twitter.com",
        }
        url = f"https://twitter.com/i/api/1.1/live_video_stream/status/{media_key}"
        try:
            r = await client.get(url, params=params)
            return r.json()
        except Exception as e:
            self.logger.error(f"stream not available for playback\n{e}")

    async def _init_chat(self, client: AsyncClient, chat_token: str) -> dict:
        payload = {"chat_token": chat_token}  # stream['chatToken']
        url = "https://proxsee.pscp.tv/api/v2/accessChatPublic"
        r = await client.post(url, json=payload)
        return r.json()

    async def _get_chat(
        self, client: AsyncClient, endpoint: str, access_token: str, cursor: str = ""
    ) -> list[dict]:
        payload = {
            "access_token": access_token,
            "cursor": cursor,
            "limit": 1000,  # or 0
            "since": None,
            "quick_get": True,
        }
        url = f"{endpoint}/chatapi/v1/history"
        r = await client.post(url, json=payload)
        data = r.json()
        res = [data]
        while cursor := data.get("cursor"):
            try:
                r = await client.post(url, json=payload | {"cursor": cursor})
                if r.status_code == 503:
                    # not our fault, service error, something went wrong with the stream
                    break
                data = r.json()
                res.append(data)
            except ReadTimeout as e:
                self.logger.debug(f"End of chat data\n{e}")
                break

        parsed = []
        for r in res:
            messages = r.get("messages", [])
            for msg in messages:
                try:
                    msg["payload"] = orjson.loads(msg.get("payload", "{}"))
                    msg["payload"]["body"] = orjson.loads(msg["payload"].get("body"))
                except Exception as e:
                    self.logger.error(f"Failed to parse chat message\n{e}")
            parsed.extend(messages)
        return parsed

    async def _async_get_chunks(self, location: str) -> list[str]:
        try:
            url = URL(location)
            stream_type = url.params.get("type")
            r = await self.session.get(
                url=location,
                params={"type": stream_type},
                headers={"authority": url.host},
            )
            # don't need an m3u8 parser
            chunks = re.findall("\n(chunk_.*)\n", r.text, flags=re.I)
            url = "/".join(location.split("/")[:-1])
            return [f"{url}/{chunk}" for chunk in chunks]
        except Exception as e:
            self.logger.error(f"Failed to get chunks\n{e}")

    async def _async_get_chat_data(self, keys: list[dict]) -> list[dict]:
        async def get(c: AsyncClient, key: dict) -> dict:
            info = await self._init_chat(c, key["chat_token"])
            chat = await self._get_chat(c, info["endpoint"], info["access_token"])
            if self.save:
                (self.out / "raw" / f"chat_{key['rest_id']}.json").write_bytes(
                    orjson.dumps(chat)
                )
            return {
                "space": key["rest_id"],
                "chat": chat,
                "info": info,
            }

        async def process():
            (self.out / "raw").mkdir(parents=True, exist_ok=True)
            limits = Limits(
                max_connections=self.max_connections, max_keepalive_connections=10
            )
            headers = self.session.headers if self.guest else get_headers(self.session)
            cookies = self.session.cookies
            async with AsyncClient(
                limits=limits, headers=headers, cookies=cookies, timeout=20
            ) as c:
                tasks = (get(c, key) for key in keys)
                if self.pbar:
                    return await tqdm_asyncio.gather(
                        *tasks, desc="Downloading chat data"
                    )
                return await asyncio.gather(*tasks)

        return await process()
        # return asyncio.run(process())

    async def _async_download_audio(self, data: list[dict]) -> None:
        async def get(s: AsyncClient, chunk: str, rest_id: str) -> tuple:
            r = await s.get(chunk)
            return rest_id, r

        async def process(data: list[dict]) -> list:
            limits = Limits(
                max_connections=self.max_connections, max_keepalive_connections=10
            )
            headers = self.session.headers if self.guest else get_headers(self.session)
            cookies = self.session.cookies
            async with AsyncClient(
                limits=limits, headers=headers, cookies=cookies, timeout=20
            ) as c:
                tasks = []
                for d in data:
                    tasks.extend([get(c, chunk, d["rest_id"]) for chunk in d["chunks"]])
                if self.pbar:
                    return await tqdm_asyncio.gather(*tasks, desc="Downloading audio")
                return await asyncio.gather(*tasks)

        # chunks = asyncio.run(process(data))
        chunks = await process(data)
        streams = {}
        [streams.setdefault(_id, []).append(chunk) for _id, chunk in chunks]
        # ensure chunks are in correct order
        for k, v in streams.items():
            streams[k] = sorted(
                v, key=lambda x: int(re.findall("_(\d+)_\w\.aac$", x.url.path)[0])
            )
        out = self.out / "audio"
        out.mkdir(parents=True, exist_ok=True)
        for space_id, chunks in streams.items():
            # 1hr ~= 50mb
            with open(out / f"{space_id}.aac", "wb") as fp:
                [fp.write(c.content) for c in chunks]

    async def _async_check_streams(self, keys: list[dict]) -> list[dict]:
        async def get(c: AsyncClient, space: dict) -> dict:
            media_key = space["data"]["audioSpace"]["metadata"]["media_key"]
            stream = await self._get_stream(c, media_key)
            return {"space": space, "stream": stream}

        async def process():
            limits = Limits(
                max_connections=self.max_connections, max_keepalive_connections=10
            )
            headers = self.session.headers if self.guest else get_headers(self.session)
            cookies = self.session.cookies
            async with AsyncClient(
                limits=limits, headers=headers, cookies=cookies, timeout=20
            ) as c:
                return await asyncio.gather(*(get(c, key) for key in keys))

        # return asyncio.run(process())
        return await process()

    async def _asyncrun(
        self,
        operation: tuple[dict, str, str],
        queries: set | list[int | str | dict],
        **kwargs,
    ):
        keys, qid, name = operation
        # stay within rate-limits
        if (queriesLength := len(queries)) > 500:
            self.logger.warning(
                f"Got {queriesLength} queries, truncating to first 500."
            )
            queries = list(queries)[:500]

        if all(isinstance(q, dict) for q in queries):
            # data = asyncio.run(self._process(operation, list(queries), **kwargs))
            data = await self._process(operation, list(queries), **kwargs)
            return get_json(data, **kwargs)

        # queries are of type set | list[int|str], need to convert to list[dict]
        _queries = [
            {dictKey: query} for query in queries for dictKey, dictValue in keys.items()
        ]

        # res = asyncio.run(self._process(operation, _queries, **kwargs))
        res = await self._process(operation, _queries, **kwargs)

        data = get_json(res, **kwargs)
        return data.pop() if kwargs.get("cursor") else flatten(data)

    async def _query(self, client: AsyncClient, operation: tuple, **kwargs) -> Response:
        keys, qid, name = operation
        params = {
            "variables": Operation.default_variables | keys | kwargs,
            "features": Operation.default_features,
        }
        r = await client.get(
            f"https://twitter.com/i/api/graphql/{qid}/{name}",
            params=build_params(params),
        )
        if self.debug:
            log(self.logger, self.debug, r)
        if self.save:
            save_json(r, self.out, name, **kwargs)
        return r

    async def _process(self, operation: tuple, queries: list[dict], **kwargs):
        limits = Limits(
            max_connections=self.max_connections, max_keepalive_connections=10
        )
        headers = self.session.headers if self.guest else get_headers(self.session)
        cookies = self.session.cookies
        async with AsyncClient(
            limits=limits,
            headers=headers,
            cookies=cookies,
            timeout=20,
            proxies=self.proxies,
        ) as c:
            # Limit queries to 1
            queryLimit = kwargs.pop("queryLimit", False)

            if queryLimit:
                queries = queries[:queryLimit]

            tasks = (self._paginate(c, operation, **q, **kwargs) for q in queries)

            if self.pbar:
                return await tqdm_asyncio.gather(*tasks, desc=operation[-1])
            return await asyncio.gather(*tasks)

    async def _paginate(self, client: AsyncClient, operation: tuple, **kwargs):
        limit = kwargs.pop("limit", math.inf)
        cursor = kwargs.pop("cursor", None)
        is_resuming = False
        dups = 0
        DUP_LIMIT = 3
        if cursor:
            is_resuming = True
            res = []
            ids = set()
        else:
            try:
                r = await self._query(client, operation, **kwargs)
                initial_data = r.json()

                res = [r]
                # ids = get_ids(initial_data, operation) # todo
                ids = set(find_key(initial_data, "rest_id"))
                cursor = get_cursor(initial_data)
            except Exception as e:
                self.logger.error("Failed to get initial pagination data", e)
                return
        while (dups < DUP_LIMIT) and cursor:
            prev_len = len(ids)
            if prev_len >= limit:
                break
            try:
                r = await self._query(client, operation, cursor=cursor, **kwargs)
                data = r.json()
            except Exception as e:
                self.logger.error(f"Failed to get pagination data\n{e}")
                return
            cursor = get_cursor(data)
            # ids |= get_ids(data, operation) # todo
            ids |= set(find_key(data, "rest_id"))
            if self.debug:
                self.logger.debug(f"Unique results: {len(ids)}\tcursor: {cursor}")
            if prev_len == len(ids):
                dups += 1
            res.append(r)
        if is_resuming:
            return res, cursor
        return res

    async def _space_listener(self, chat: dict, frequency: int):
        def rand_color():
            return random.choice([RED, GREEN, RESET, BLUE, CYAN, MAGENTA, YELLOW])

        uri = f"wss://{URL(chat['endpoint']).host}/chatapi/v1/chatnow"
        with open("chatlog.jsonl", "ab") as fp:
            async with websockets.connect(uri) as ws:
                await ws.send(
                    orjson.dumps(
                        {
                            "payload": orjson.dumps(
                                {"access_token": chat["access_token"]}
                            ).decode(),
                            "kind": 3,
                        }
                    ).decode()
                )
                await ws.send(
                    orjson.dumps(
                        {
                            "payload": orjson.dumps(
                                {
                                    "body": orjson.dumps(
                                        {"room": chat["room_id"]}
                                    ).decode(),
                                    "kind": 1,
                                }
                            ).decode(),
                            "kind": 2,
                        }
                    ).decode()
                )

                prev_message = ""
                prev_user = ""
                while True:
                    msg = await ws.recv()
                    temp = orjson.loads(msg)
                    kind = temp.get("kind")
                    if kind == 1:
                        signature = temp.get("signature")
                        payload = orjson.loads(temp.get("payload"))
                        payload["body"] = orjson.loads(payload.get("body"))
                        res = {
                            "kind": kind,
                            "payload": payload,
                            "signature": signature,
                        }
                        fp.write(orjson.dumps(res) + b"\n")
                        body = payload["body"]
                        message = body.get("body")
                        user = body.get("username")
                        # user_id = body.get('user_id')
                        final = body.get("final")

                        if frequency == 1:
                            if final:
                                if user != prev_user:
                                    print()
                                    print(f"({rand_color()}{user}{RESET})")
                                    prev_user = user
                                # print(message, end=' ')
                                print(message)

                        # dirty
                        if frequency == 2:
                            if user and (not final):
                                if user != prev_user:
                                    print()
                                    print(f"({rand_color()}{user}{RESET})")
                                    prev_user = user
                                new_message = re.sub(
                                    f"^({prev_message})", "", message, flags=re.I
                                ).strip()
                                if len(new_message) < 100:
                                    print(new_message, end=" ")
                                    prev_message = message

    async def _get_live_chats(self, client: AsyncClient, spaces: list[dict]):
        async def get(c: AsyncClient, space: dict) -> list[dict]:
            media_key = space["data"]["audioSpace"]["metadata"]["media_key"]
            r = await c.get(
                url=f"https://twitter.com/i/api/1.1/live_video_stream/status/{media_key}",
                params={
                    "client": "web",
                    "use_syndication_guest_id": "false",
                    "cookie_set_host": "twitter.com",
                },
            )
            r = await c.post(
                url="https://proxsee.pscp.tv/api/v2/accessChatPublic",
                json={"chat_token": r.json()["chatToken"]},
            )
            return r.json()

        limits = Limits(max_connections=self.max_connections)
        async with AsyncClient(headers=client.headers, limits=limits, timeout=30) as c:
            tasks = (get(c, _id) for _id in spaces)
            if self.pbar:
                return await tqdm_asyncio.gather(
                    *tasks, desc="Getting live transcripts"
                )
            return await asyncio.gather(*tasks)

    async def asyncSpaceLiveTranscript(self, room: str, frequency: int = 1):
        """
        Log live transcript of a space

        @param room: room id
        @param frequency: granularity of transcript. 1 for real-time, 2 for post-processed or "finalized" transcript
        @return: None
        """

        async def get(spaces: list[dict]):
            client = init_session(proxies=self.proxies)
            chats = await self._get_live_chats(client, spaces)
            await asyncio.gather(*(self._space_listener(c, frequency) for c in chats))

        spaces = self.asyncSpaces(rooms=[room])
        # asyncio.run(get(spaces))
        await get(spaces)

    async def asyncSpacesLive(self, rooms: list[str]):
        """
        Capture live audio stream from spaces

        Limited to 500 rooms per IP, as defined by twitter's rate limits.

        @param rooms: list of room ids
        @return: None
        """

        def chunk_idx(chunk: str) -> int:
            return int(re.findall("_(\d+)_\w\.aac", chunk)[0])

        def sort_chunks(chunks: list[str]) -> list[str]:
            return sorted(chunks, key=lambda x: chunk_idx(x))

        def parse_chunks(txt: str) -> list[str]:
            return re.findall("\n(chunk_.*)\n", txt, flags=re.I)

        async def get_m3u8(client: AsyncClient, space: dict) -> dict:
            try:
                media_key = space["data"]["audioSpace"]["metadata"]["media_key"]
                r = await client.get(
                    url=f"https://twitter.com/i/api/1.1/live_video_stream/status/{media_key}",
                    params={
                        "client": "web",
                        "use_syndication_guest_id": "false",
                        "cookie_set_host": "twitter.com",
                    },
                )
                data = r.json()
                room = data["shareUrl"].split("/")[-1]
                return {"url": data["source"]["location"], "room": room}
            except Exception as e:
                room = space["data"]["audioSpace"]["metadata"]["rest_id"]
                self.logger.error(
                    f"Failed to get stream info for https://twitter.com/i/spaces/{room}\n{e}"
                )

        async def get_chunks(client: AsyncClient, url: str) -> list[str]:
            try:
                url = URL(url)
                r = await client.get(
                    url=url,
                    params={"type": url.params.get("type")},
                    headers={"authority": url.host},
                )
                base = "/".join(str(url).split("/")[:-1])
                return [f"{base}/{c}" for c in parse_chunks(r.text)]
            except Exception as e:
                self.logger.error(f"Failed to get chunks\n{e}")

        async def poll_space(client: AsyncClient, space: dict) -> dict | None:
            curr = 0
            lim = 10
            all_chunks = set()
            playlist = await get_m3u8(client, space)
            if not playlist:
                return
            chunks = await get_chunks(client, playlist["url"])
            if not chunks:
                return
            out = self.out / "live"
            out.mkdir(parents=True, exist_ok=True)
            async with aiofiles.open(out / f'{playlist["room"]}.aac', "wb") as fp:
                while curr < lim:
                    chunks = await get_chunks(client, playlist["url"])
                    if not chunks:
                        return {"space": space, "chunks": sort_chunks(all_chunks)}
                    new_chunks = set(chunks) - all_chunks
                    all_chunks |= new_chunks
                    for c in sort_chunks(new_chunks):
                        try:
                            self.logger.debug(f"write: chunk [{chunk_idx(c)}]\t{c}")
                            r = await client.get(c)
                            await fp.write(r.content)
                        except Exception as e:
                            self.logger.error(f"Failed to write chunk {c}\n{e}")
                    curr = 0 if new_chunks else curr + 1
                    # wait for new chunks. dynamic playlist is updated every 2-3 seconds
                    await asyncio.sleep(random.random() + 1.5)
            return {"space": space, "chunks": sort_chunks(all_chunks)}

        async def process(spaces: list[dict]):
            limits = Limits(max_connections=self.max_connections)
            headers, cookies = self.session.headers, self.session.cookies
            async with AsyncClient(
                limits=limits, headers=headers, cookies=cookies, timeout=20
            ) as c:
                return await asyncio.gather(*(poll_space(c, space) for space in spaces))

        spaces = self.asyncSpaces(rooms=rooms)
        # return asyncio.run(process(spaces))
        return await process(spaces)

    def _init_logger(self, **kwargs) -> Logger:
        if self.debug:
            self.logger = logging.getLogger("asyncTwitter")
            self.logger.setLevel(logging.DEBUG)  # Set the logging level for this logger

            # Create a StreamHandler that sends log messages to stdout
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.DEBUG)  # Set the logging level for this handler

            # Create a formatter and add it to the handler
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)

            # Add the handler to the logger
            self.logger.addHandler(handler)
            return self.logger

    async def _async_validate_session(self, *args, **kwargs):
        email, username, password, session = args

        # invalid credentials and session
        cookies = kwargs.get("cookies")
        proxies = kwargs.get("proxies")

        # try validating cookies dict
        if isinstance(cookies, dict) and all(
            cookies.get(c) for c in {"ct0", "auth_token"}
        ):
            _session = AsyncClient(
                cookies=cookies, follow_redirects=True, proxies=proxies
            )
            _session.headers.update(get_headers(_session))
            # print("Logging in from Cookies Dict 100%!!!")
            return _session

        # try validating cookies from file
        if isinstance(cookies, str):
            _session = AsyncClient(
                cookies=orjson.loads(Path(cookies).read_bytes()),
                follow_redirects=True,
                proxies=proxies,
            )
            _session.headers.update(get_headers(_session))
            # print("Logging in from Cookies File 100%!!!")
            return _session

        # validate credentials
        if all((email, username, password)):
            # print("Logging in from Credentials 100%!!!")
            return await asyncLogin(email, username, password, **kwargs)

        # invalid credentials, try validating session
        if session and all(session.cookies.get(c) for c in {"ct0", "auth_token"}):
            return session

        # no session, credentials, or cookies provided. use guest session.
        if self.debug:
            self.logger.warning(
                f"{RED}This is a guest session, some endpoints cannot be accessed.{RESET}\n"
            )
        self.guest = True
        return session

    @property
    def id(self) -> int:
        """Get User ID"""
        return int(re.findall('"u=(\d+)"', self.session.cookies.get("twid"))[0])

    def save_cookies(self, fname: str = None, toFile=True):
        """Save cookies to file"""
        cookies = self.session.cookies
        if toFile:
            Path(f'{fname or cookies.get("username")}.cookies').write_bytes(
                orjson.dumps(dict(cookies))
            )
        return dict(cookies)
