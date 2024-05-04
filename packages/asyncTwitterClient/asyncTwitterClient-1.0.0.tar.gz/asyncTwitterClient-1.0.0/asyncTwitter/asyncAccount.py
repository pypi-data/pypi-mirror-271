import orjson
import mimetypes
import random
import hashlib
import time
import math

from logging import Logger
from copy import deepcopy
from tqdm import tqdm
from datetime import datetime
from httpx import AsyncClient, Response
from .constants import (
    Operation,
    MAX_IMAGE_SIZE,
    MAX_GIF_SIZE,
    MAX_VIDEO_SIZE,
    UPLOAD_CHUNK_SIZE,
    MEDIA_UPLOAD_SUCCEED,
    MEDIA_UPLOAD_FAIL,
    follow_settings,
    follower_notification_settings,
)
from .util import (
    get_headers,
    log,
    urlencode,
    find_key,
    RED,
    RESET,
    Path,
    get_cursor,
    GREEN,
)
from colorama import Fore
from uuid import uuid1, getnode
from string import ascii_letters

try:
    from asyncTwitter.twoCaptcha import TwoCaptcha
except Exception:
    from ..asyncTwitter.twoCaptcha import TwoCaptcha

from .asyncLogin import asyncLogin
from httpx_socks import AsyncProxyTransport
from urllib import parse

class AsyncAccount:
    """The AsyncAccount class is used to interact with the Twitter API.
    It contains account specific methods like tweeting, liking, following, etc.

    a = AsyncAccount(debug=True, twoCaptchaApiKey="2CaptchaKey")
    await a.asyncAuthenticate(email="email", password="password", username="username", cookies="cookies.json", proxies="http://)
    await a.asyncTweet("Hello World!")
    """

    def __init__(
        self,
        save: bool = True,
        debug: bool = False,
        twid: bool = False,
        twoCaptchaApiKey: str = None,
        proxies: str = None,
        httpxSocks: bool = False,
        **kwargs,
    ):
        """Initailize the AsyncAccount class.

        Args:
            save (bool, optional): Enable or disable saving files. Defaults to True.
            debug (bool, optional): Enable or disable debug logging. Defaults to False.
            twid (bool, optional): Provide the accounts Rest_Id. Defaults to False.
            twoCaptchaApiKey (str, optional): Provide a TwoCaptcha API key. Defaults to None.

            Do not confuse save with save_cookies. Save is used to save files like images and videos.

            twoCaptchaAPIKey is used to solve captchas for unlocking the account.

            **kwargs: Additional arguments to pass to the logger.
        """
        self.save = save
        self.debug = debug
        self.twid = twid
        self.gql_api = "https://twitter.com/i/api/graphql"
        self.v1_api = "https://api.twitter.com/1.1"
        self.v2_api = "https://twitter.com/i/api/2"
        self.logger = self._init_logger(**kwargs)
        self.rate_limits = {}
        self.twoCaptcha = TwoCaptcha(main=self, apiKey=twoCaptchaApiKey)
        self.proxyString = proxies

        if httpxSocks and proxies:
            self.proxies = {
                "transport": AsyncProxyTransport.from_url(proxies),
                "proxies": None,
            }
        else:
            self.proxies = {"transport": None, "proxies": proxies}

        self.ogProxyString = proxies

        # print(f'AsyncAcc Logger: {self.logger}')

    async def unlockViaArkoseCaptcha(self) -> dict:
        """
        This method is used to unlock the account via Arkose Captcha.
        Provide the TwoCaptcha API key in the constructor/__init__ to use this method.

        This function really needs someone to find a way to find real ui_metrics values.
        Theyre just static currently, could be getting accounts banned.

        Also needs a way to use the authenticated session instead of copying it,
        not sure why it wont just werk for me.
        """

        copyOfHeaders = dict(self.session.headers.copy())
        copyOfHeaders.pop("authorization", None)
        copyOfHeaders.pop("x-csrf-token", None)
        copyOfHeaders.pop("x-twitter-auth-type", None)
        copyOfHeaders.pop("x-guest-token", None)
        copyOfHeaders.pop("x-twitter-active-user", None)
        copyOfHeaders.pop("x-twitter-client-language", None)
        copyOfHeaders.pop("connection", None)
        copyOfHeaders.pop("cookie", None)
        submitHeaders = {
            "cache-control": "max-age=0",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "upgrade-insecure-requests": "1",
            "origin": "https://twitter.com",
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "referer": "https://twitter.com/account/access",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "priority": "u=0, i",
        }

        getHeaders = {
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "referer": "https://twitter.com/i/flow/login",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "priority": "u=0, i",
            # "cookie": '_ga=GA1.2.396964430.1714338740; _gid=GA1.2.792491738.1714338740; kdt=m12M1xdg7Mw0a3TbACWbIZJlu8VBUL2P6A5dpJYj; lang=en; dnt=1; guest_id=v1%3A171436913069729690; guest_id_marketing=v1%3A171436913069729690; guest_id_ads=v1%3A171436913069729690; personalization_id="v1_m3Td5kYJdlAANN2W+uUNhw=="; gt=1784819612883832954; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCGQKXSiPAToMY3NyZl9p%250AZCIlMzRkMjJmOTBjYWU0ZWNjZTgwNDAyMzFiYzMzZDY2NjA6B2lkIiUyNmU0%250AMDdlN2YzZGQzYzFkNjBkZTZmMjllMGVmMWIxNg%253D%253D--2c40ae37af3d86c0038dd6e274d5e855ca2573d8; twid="u=1061735362350014464"; auth_token=20e72527a43d3f80ff1aff5e1db0512bfc54e182; ct0=0dee2493408e84c1bc084e1ba6ebab9cfbbe1b46edfae1b2c00bcc852e780560d78782f9354cbd7cc52f5de18d3a001d2376eb4cf93b72d22196e796eace1a782bc66d02a54e4cd46336d1e844a0ad14',
        }

        params = {"lang": "en"}

        newClient = AsyncClient(
            headers=copyOfHeaders,
            cookies=self.session.cookies,
            verify=False,
            timeout=30,
            http2=True,
            **self.proxies,
        )

        if self.debug:
            print(
                dict(newClient.headers),
                file=open("newClientHeaders.json", "w", encoding="utf-8"),
            )

        endpointUrl = "https://twitter.com/account/access"

        getRespForData = await newClient.get(
            endpointUrl,
            # params=params,
            headers=getHeaders,
        )

        if self.debug:
            print(
                getRespForData.text, file=open("unlockGet.html", "w", encoding="utf-8")
            )

        authenticityToken = getRespForData.text.split(
            '<input type="hidden" name="authenticity_token" value="'
        )[1].split('"')[0]
        assignmentToken = getRespForData.text.split(
            '<input type="hidden" name="assignment_token" value="'
        )[1].split('"')[0]
        lang = getRespForData.text.split('<input type="hidden" name="lang" value="')[
            1
        ].split('"')[0]

        if self.debug:
            self.logger.info(
                f"[UNLOCK {self.username}] Authenticity Token Found, getting solved Captcha...: {authenticityToken}"
            )

        if self.proxyString:
            parsedProxy = parse.urlparse(self.proxyString)

            kwargs = {
                "proxyType": parsedProxy.scheme,
                "proxyAddress": parsedProxy.hostname,
                "proxyPort": parsedProxy.port,
                "proxyLogin": parsedProxy.username,
                "proxyPassword": parsedProxy.password,
                "userAgent": dict(self.session.headers).get(
                    "user-agent",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.3",
                ),
            }
        else:
            kwargs = {
                "userAgent": dict(self.session.headers).get(
                    "user-agent",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.3",
                ),
            }

        submitCaptchaTask = await self.twoCaptcha.createTask(
            websiteUrl="https://twitter.com/account/access",
            websiteKey="0152B4EB-D2DC-460A-89A1-629838B529C9",
            **kwargs,
        )

        captchaTaskId = submitCaptchaTask.get("taskId")

        if self.debug:
            self.logger.debug(
                f"[UNLOCK {self.username}] Captcha Task ID: {captchaTaskId}"
            )

        captchaResults = await self.twoCaptcha.checkTaskUntilFinished(
            captchaTaskId, sleepTime=15, maxRetries=20
        )

        solutionToken = captchaResults.get("solution", {}).get("token")

        if self.debug:
            self.logger.debug(
                f"[UNLOCK {self.username}] Captcha Solution Token: {solutionToken}"
            )

        if not solutionToken:
            if self.debug:
                self.logger.debug("Failed to solve Captcha.")
                return {"success": False, "error": "Failed to solve Captcha."}

        payload = {
            "authenticity_token": authenticityToken,
            "assignment_token": assignmentToken,
            "lang": lang,
            "flow": "",
            "verification_string": solutionToken,  # Captcha solve
            "language_code": lang,
        }

        unlockResponse = await newClient.post(
            endpointUrl,
            data=payload,
            follow_redirects=True,
            params=params,
            headers=submitHeaders,
        )

        if (
            "your account is now available for use" in unlockResponse.text.lower()
            or '<div class="textgroup-text">' in unlockResponse.text.lower()
            or "https://twitter.com/?lang" in str(unlockResponse.url)
        ):
            unlocked = True
        else:
            unlocked = False

        if self.debug:
            self.logger.debug(
                f"[UNLOCK {self.username}] Captcha Unlock: {unlocked} | Unlock Response status_code: {unlockResponse.status_code}"
            )
            print(unlockResponse.text, file=open("unlock.html", "w", encoding="utf-8"))

        if unlocked:
            authenticityToken = unlockResponse.text.split(
                '<input type="hidden" name="authenticity_token" value="'
            )[1].split('"')[0]
            assignmentToken = unlockResponse.text.split(
                '<input type="hidden" name="assignment_token" value="'
            )[1].split('"')[0]
            finishPayload = {
                "authenticity_token": authenticityToken,
                "assignment_token": assignmentToken,
                "lang": lang,
                "flow": "",
                "ui_metrics": {  # What the fuck is this? Thinking of randomizing values or keys + values at same length and type
                    "rf": {
                        "a164b41fad0433b3eb8ef1474015a1c192606f211d5cab98860739135a6f57d2": -110,
                        "a846abda2338f92a076af6e5f40e8171ddfa1f5f802abc62f1fb39cfd0138301": -1,
                        "ace36e17c04cb2475c443874a57310e469013dbecf948d84137d12b6ad71e025": 0,
                        "a25211b004a8e34850978eeb17bab27bca8653a820c1c58442766f317ce2f965": -127,
                    },
                    "s": "s0TtDv7i3G_2y2Dx1m-IOiI6st_0zRgRrfYDgKHX7jpHDp0q0bm2Bj7youdKVhxivyJTOpD0t6QrhVGbeUwN3rGreAE2p06HTYtVT_iWDmwdHTmbrOoFM4ws3pNLHb7AGB6ceguzlW8J51qGwY1DrCLFxMFm3_rQ6T0Cu7gp1CsVutURjyEdzecozhS57mEaryVBaxImglAON7SbByk-cOj5FMki6pH3SxFvaOaA3A1Y7CiOU7pQ07KdFhCUcyfM1xkWY3kdH9-lw9sOPBaTrjX15d0L6RTnEcsqtINE8NNZJ5QFaXLNbrlEtSGW29ugUlZphX5Z24iM1-Zn6g6uBgAAAY8W4QwM",
                },
            }
            finishUnlockResp = await newClient.post(
                endpointUrl,
                data=finishPayload,
                follow_redirects=True,
                headers=submitHeaders,
                params=params,
            )

            if "https://twitter.com/?lang" in str(finishUnlockResp.url):
                unlocked = True
                if self.debug:
                    self.logger.debug(f"{GREEN}Account Unlocked Successfully!!!{RESET}")
            else:
                unlocked = False
                if self.debug:
                    self.logger.debug(f"{RED}Failed to unlock account.{RESET}")

        return {"success": unlocked}

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
        self.ogProxyString = proxies
        self.proxyString = proxies

        if httpxSocks and proxies:
            self.proxies = {
                "transport": AsyncProxyTransport.from_url(proxies),
                "proxies": None,
            }
        else:
            self.proxies = {"transport": None, "proxies": proxies}

        kwargs.update(**self.proxies)

        # print(f'AsyncAcc Got: {email}, {username}, {password}, {session}, {self.cookies}, {self.proxies}')

        self.session = await self._async_validate_session(
            email=self.email,
            username=self.username,
            password=self.password,
            session=session,
            cookies=self.cookies,
            **kwargs,
        )

        if not self.session:
            self.logger.error(f"Failed to authenticate account: {self.username}")
            return None

        return self.session

    async def asyncGQL(
        self,
        method: str,
        operation: tuple,
        variables: dict,
        features: dict = Operation.default_features,
    ) -> dict:
        qid, op = operation
        params = {
            "queryId": qid,
            "features": features,
            "variables": Operation.default_variables | variables,
        }
        if method == "POST":
            data = {"json": params}
        else:
            data = {"params": {k: orjson.dumps(v).decode() for k, v in params.items()}}
        gqlResponse = await self.session.request(
            method=method,
            url=f"{self.gql_api}/{qid}/{op}",
            # url="https://fuck.com",
            headers=get_headers(self.session),
            **data,
        )
        self.rate_limits[op] = {
            k: int(v) for k, v in gqlResponse.headers.items() if "rate-limit" in k
        }
        if self.debug:
            log(self.logger, gqlResponse)
        return gqlResponse.json()

    async def asyncV1(self, path: str, params: dict) -> dict:
        headers = get_headers(self.session)
        headers["content-type"] = "application/x-www-form-urlencoded"
        v1Response = await self.session.post(
            f"{self.v1_api}/{path}", headers=headers, data=urlencode(params)
        )
        if self.debug:
            log(self.logger, v1Response)
        return v1Response.json()

    async def asyncCreatePoll(
        self, text: str, choices: list[str], poll_duration: int
    ) -> dict:
        options = {
            "twitter:card": "poll4choice_text_only",
            "twitter:api:api:endpoint": "1",
            "twitter:long:duration_minutes": poll_duration,  # max: 10080
        }
        for i, c in enumerate(choices):
            options[f"twitter:string:choice{i + 1}_label"] = c

        headers = get_headers(self.session)
        headers["content-type"] = "application/x-www-form-urlencoded"
        url = "https://caps.twitter.com/v2/cards/create.json"
        createPollResponse = await self.session.post(
            url, headers=headers, params={"card_data": orjson.dumps(options).decode()}
        )
        card_uri = createPollResponse.json()["card_uri"]
        createPollResponse = await self.asyncTweet(
            text, poll_params={"card_uri": card_uri}
        )
        return createPollResponse

    async def asyncDM(self, text: str, receivers: list[int], media: str = "") -> dict:
        variables = {
            "message": {},
            "requestId": str(uuid1(getnode())),
            "target": {"participant_ids": receivers},
        }
        if media:
            media_id = await self._async_upload_media(media, is_dm=True)
            variables["message"]["media"] = {"id": media_id, "text": text}
        else:
            variables["message"]["text"] = {"text": text}
        dmResponse = await self.asyncGQL(
            "POST", Operation.useSendMessageMutation, variables
        )
        if find_key(dmResponse, "dm_validation_failure_type"):
            self.logger.debug(f"{RED}Failed to send DM(s) to {receivers}{RESET}")
        return dmResponse

    async def asyncTweet(self, text: str, *, media: any = None, **kwargs) -> dict:
        variables = {
            "tweet_text": text,
            "dark_request": False,
            "media": {
                "media_entities": [],
                "possibly_sensitive": False,
            },
            "semantic_annotation_ids": [],
        }

        if reply_params := kwargs.get("reply_params", {}):
            variables |= reply_params
        if quote_params := kwargs.get("quote_params", {}):
            variables |= quote_params
        if poll_params := kwargs.get("poll_params", {}):
            variables |= poll_params

        draft = kwargs.get("draft")
        schedule = kwargs.get("schedule")

        if draft or schedule:
            variables = {
                "post_tweet_request": {
                    "auto_populate_reply_metadata": False,
                    "status": text,
                    "exclude_reply_user_ids": [],
                    "media_ids": [],
                },
            }
            if media:
                for m in media:
                    media_id = await self._async_upload_media(m["media"])
                    variables["post_tweet_request"]["media_ids"].append(media_id)
                    if alt := m.get("alt"):
                        await self._async_add_alt_text(media_id, alt)

            if schedule:
                variables["execute_at"] = (
                    datetime.strptime(schedule, "%Y-%m-%d %H:%M").timestamp()
                    if isinstance(schedule, str)
                    else schedule
                )
                return await self.asyncGQL(
                    "POST", Operation.CreateScheduledTweet, variables
                )

            return await self.asyncGQL("POST", Operation.CreateDraftTweet, variables)

        # regular tweet
        if media:
            for m in media:
                media_id = await self._async_upload_media(m["media"])
                print(f"Media: {media_id}")
                variables["media"]["media_entities"].append(
                    {"media_id": media_id, "tagged_users": m.get("tagged_users", [])}
                )
                if alt := m.get("alt"):
                    await self._async_add_alt_text(media_id, alt)

        return await self.asyncGQL("POST", Operation.CreateTweet, variables)

    async def asyncScheduleTweet(
        self, text: str, date: int | str, *, media: list = None
    ) -> dict:
        variables = {
            "post_tweet_request": {
                "auto_populate_reply_metadata": False,
                "status": text,
                "exclude_reply_user_ids": [],
                "media_ids": [],
            },
            "execute_at": (
                datetime.strptime(date, "%Y-%m-%d %H:%M").timestamp()
                if isinstance(date, str)
                else date
            ),
        }
        if media:
            for m in media:
                media_id = await self._async_upload_media(m["media"])
                variables["post_tweet_request"]["media_ids"].append(media_id)
                if alt := m.get("alt"):
                    await self._async_add_alt_text(media_id, alt)
        return await self.asyncGQL("POST", Operation.CreateScheduledTweet, variables)

    async def asyncScheduleReply(
        self, text: str, date: int | str, tweet_id: int, *, media: list = None
    ) -> dict:
        variables = {
            "post_tweet_request": {
                "auto_populate_reply_metadata": True,
                "in_reply_to_status_id": tweet_id,
                "status": text,
                "exclude_reply_user_ids": [],
                "media_ids": [],
            },
            "execute_at": (
                datetime.strptime(date, "%Y-%m-%d %H:%M").timestamp()
                if isinstance(date, str)
                else date
            ),
        }
        if media:
            for m in media:
                media_id = await self._async_upload_media(m["media"])
                variables["post_tweet_request"]["media_ids"].append(media_id)
                if alt := m.get("alt"):
                    await self._async_add_alt_text(media_id, alt)
        return await self.asyncGQL("POST", Operation.CreateScheduledTweet, variables)

    async def asyncUnscheduleTweet(self, tweet_id: int) -> dict:
        variables = {"scheduled_tweet_id": tweet_id}
        return await self.asyncGQL("POST", Operation.DeleteScheduledTweet, variables)

    async def asyncUntweet(self, tweet_id: int) -> dict:
        variables = {"tweet_id": tweet_id, "dark_request": False}
        return await self.asyncGQL("POST", Operation.DeleteTweet, variables)

    async def asyncReply(self, text: str, tweet_id: int, media: list = None) -> dict:
        variables = {
            "tweet_text": text,
            "reply": {
                "in_reply_to_tweet_id": tweet_id,
                "exclude_reply_user_ids": [],
            },
            "batch_compose": "BatchSubsequent",
            "dark_request": False,
            "media": {
                "media_entities": [],
                "possibly_sensitive": False,
            },
            "semantic_annotation_ids": [],
        }

        if media:
            for m in media:
                media_id = await self._async_upload_media(m["media"])
                print(f"Media: {media_id}")
                variables["media"]["media_entities"].append(
                    {"media_id": media_id, "tagged_users": m.get("tagged_users", [])}
                )
                if alt := m.get("alt"):
                    await self._async_add_alt_text(media_id, alt)

        return await self.asyncGQL("POST", Operation.CreateTweet, variables)

    async def asyncQuote(self, text: str, tweet_id: int, media: list = None) -> dict:
        variables = {
            "tweet_text": text,
            # can use `i` as it resolves to screen_name
            "attachment_url": f"https://twitter.com/i/status/{tweet_id}",
            "dark_request": False,
            "media": {
                "media_entities": [],
                "possibly_sensitive": False,
            },
            "semantic_annotation_ids": [],
        }

        if media:
            for m in media:
                media_id = await self._async_upload_media(m["media"])
                print(f"Media: {media_id}")
                variables["media"]["media_entities"].append(
                    {"media_id": media_id, "tagged_users": m.get("tagged_users", [])}
                )
                if alt := m.get("alt"):
                    await self._async_add_alt_text(media_id, alt)

        return await self.asyncGQL("POST", Operation.CreateTweet, variables)

    async def asyncRetweet(self, tweet_id: int) -> dict:
        variables = {"tweet_id": tweet_id, "dark_request": False}
        return await self.asyncGQL("POST", Operation.CreateRetweet, variables)

    async def asyncUnretweet(self, tweet_id: int) -> dict:
        variables = {"source_tweet_id": tweet_id, "dark_request": False}
        return await self.asyncGQL("POST", Operation.DeleteRetweet, variables)

    async def asyncLike(self, tweet_id: int) -> dict:
        variables = {"tweet_id": tweet_id}
        return await self.asyncGQL("POST", Operation.FavoriteTweet, variables)

    async def asyncUnlike(self, tweet_id: int) -> dict:
        variables = {"tweet_id": tweet_id}
        return await self.asyncGQL("POST", Operation.UnfavoriteTweet, variables)

    async def asyncBookmark(self, tweet_id: int) -> dict:
        variables = {"tweet_id": tweet_id}
        return await self.asyncGQL("POST", Operation.CreateBookmark, variables)

    async def asyncUnbookmark(self, tweet_id: int) -> dict:
        variables = {"tweet_id": tweet_id}
        return await self.asyncGQL("POST", Operation.DeleteBookmark, variables)

    async def asyncCreateList(self, name: str, description: str, private: bool) -> dict:
        variables = {
            "isPrivate": private,
            "name": name,
            "description": description,
        }
        return await self.asyncGQL("POST", Operation.CreateList, variables)

    async def asyncUpdateList(
        self, list_id: int, name: str, description: str, private: bool
    ) -> dict:
        variables = {
            "listId": list_id,
            "isPrivate": private,
            "name": name,
            "description": description,
        }
        return await self.asyncGQL("POST", Operation.UpdateList, variables)

    async def asyncUpdatedPinnedLists(self, list_ids: list[int]) -> dict:
        """
        Update pinned lists.
        Reset all pinned lists and pin all specified lists in the order they are provided.

        @param list_ids: list of list ids to pin
        @return: response
        """
        return await self.asyncGQL(
            "POST", Operation.ListsPinMany, {"listIds": list_ids}
        )

    async def asyncPinList(self, list_id: int) -> dict:
        return await self.asyncGQL("POST", Operation.ListPinOne, {"listId": list_id})

    async def asyncUnpinList(self, list_id: int) -> dict:
        return await self.asyncGQL("POST", Operation.ListUnpinOne, {"listId": list_id})

    async def asyncAddListMember(self, list_id: int, user_id: int) -> dict:
        return await self.asyncGQL(
            "POST", Operation.ListAddMember, {"listId": list_id, "userId": user_id}
        )

    async def asyncRemoveListMember(self, list_id: int, user_id: int) -> dict:
        return await self.asyncGQL(
            "POST", Operation.ListRemoveMember, {"listId": list_id, "userId": user_id}
        )

    async def asyncDeleteList(self, list_id: int) -> dict:
        return await self.asyncGQL("POST", Operation.DeleteList, {"listId": list_id})

    async def asyncUpdateListBanner(self, list_id: int, media: str) -> dict:
        media_id = self._upload_media(media)
        variables = {"listId": list_id, "mediaId": media_id}
        return await self.asyncGQL("POST", Operation.EditListBanner, variables)

    async def asyncDeleteListBanner(self, list_id: int) -> dict:
        return await self.asyncGQL(
            "POST", Operation.DeleteListBanner, {"listId": list_id}
        )

    async def asyncFollowTopic(self, topic_id: int) -> dict:
        return await self.asyncGQL(
            "POST", Operation.TopicFollow, {"topicId": str(topic_id)}
        )

    async def asyncUnfollowTopic(self, topic_id: int) -> dict:
        return await self.asyncGQL(
            "POST", Operation.TopicUnfollow, {"topicId": str(topic_id)}
        )

    async def asyncPin(self, tweet_id: int) -> dict:
        return await self.asyncV1(
            "account/pin_tweet.json", {"tweet_mode": "extended", "id": tweet_id}
        )

    async def asyncUnpin(self, tweet_id: int) -> dict:
        return await self.asyncV1(
            "account/unpin_tweet.json", {"tweet_mode": "extended", "id": tweet_id}
        )

    async def asyncFollow(self, user_id: int) -> dict:
        settings = deepcopy(follow_settings)
        settings |= {"user_id": user_id}
        return await self.asyncV1("friendships/create.json", settings)

    async def asyncUnfollow(self, user_id: int) -> dict:
        settings = deepcopy(follow_settings)
        settings |= {"user_id": user_id}
        return await self.asyncV1("friendships/destroy.json", settings)

    async def asyncMute(self, user_id: int) -> dict:
        return await self.asyncV1("mutes/users/create.json", {"user_id": user_id})

    async def asyncUnmute(self, user_id: int) -> dict:
        return await self.asyncV1("mutes/users/destroy.json", {"user_id": user_id})

    async def asyncEnableFollowerNotifications(self, user_id: int) -> dict:
        settings = deepcopy(follower_notification_settings)
        settings |= {"id": user_id, "device": "true"}
        return await self.asyncV1("friendships/update.json", settings)

    async def disableFollowerNotifications(self, user_id: int) -> dict:
        settings = deepcopy(follower_notification_settings)
        settings |= {"id": user_id, "device": "false"}
        return await self.asyncV1("friendships/update.json", settings)

    async def asyncBlock(self, user_id: int) -> dict:
        return await self.asyncV1("blocks/create.json", {"user_id": user_id})

    async def asyncUnblock(self, user_id: int) -> dict:
        return await self.asyncV1("blocks/destroy.json", {"user_id": user_id})

    async def asyncUpdateProfileImage(self, media: str) -> Response:
        media_id = self._upload_media(media, is_profile=True)
        url = f"{self.v1_api}/account/update_profile_image.json"
        headers = get_headers(self.session)
        params = {"media_id": media_id}
        updateProfileImageResponse = await self.session.post(
            url, headers=headers, params=params
        )
        return updateProfileImageResponse

    async def asyncUpdateProfileBanner(self, media: str) -> Response:
        media_id = self._upload_media(media, is_profile=True)
        url = f"{self.v1_api}/account/update_profile_banner.json"
        headers = get_headers(self.session)
        params = {"media_id": media_id}
        updateProfileBannerResponse = await self.session.post(
            url, headers=headers, params=params
        )
        return updateProfileBannerResponse

    async def asyncUpdateProfileInfo(self, **kwargs) -> Response:
        url = f"{self.v1_api}/account/update_profile.json"
        headers = get_headers(self.session)
        updateProfileInfoResponse = await self.session.post(
            url, headers=headers, params=kwargs
        )
        return updateProfileInfoResponse

    async def asyncUpdateSearchSettings(self, settings: dict) -> Response:
        twid = int(self.session.cookies.get("twid").split("=")[-1].strip('"'))
        headers = get_headers(self.session)
        updateSearchSettingsResponse = await self.session.post(
            url=f"{self.v1_api}/strato/column/User/{twid}/search/searchSafety",
            headers=headers,
            json=settings,
        )
        return updateSearchSettingsResponse

    async def asyncUpdateSettings(self, settings: dict) -> dict:
        return await self.asyncV1("account/settings.json", settings)

    async def asyncChangePassword(self, old: str, new: str) -> dict:
        params = {
            "current_password": old,
            "password": new,
            "password_confirmation": new,
        }
        headers = get_headers(self.session)
        headers["content-type"] = "application/x-www-form-urlencoded"
        url = "https://twitter.com/i/api/i/account/change_password.json"
        changePasswordResponse = await self.session.post(
            url, headers=headers, data=urlencode(params)
        )
        return changePasswordResponse.json()

    async def asyncRemoveInterests(self, *args):
        """
        Pass 'all' to remove all interests
        """
        removeInterestsResponse = await self.session.get(
            f"{self.v1_api}/account/personalization/twitter_interests.json",
            headers=get_headers(self.session),
        )
        current_interests = removeInterestsResponse.json()["interested_in"]
        if args == "all":
            disabled_interests = [x["id"] for x in current_interests]
        else:
            disabled_interests = [
                x["id"] for x in current_interests if x["display_name"] in args
            ]
        payload = {
            "preferences": {
                "interest_preferences": {
                    "disabled_interests": disabled_interests,
                    "disabled_partner_interests": [],
                }
            }
        }
        removeInterestsResponse = await self.session.post(
            f"{self.v1_api}/account/personalization/p13n_preferences.json",
            headers=get_headers(self.session),
            json=payload,
        )
        return removeInterestsResponse

    async def asyncHomeTimeline(self, limit=math.inf) -> list[dict]:
        return await self._async_paginate(
            "POST", Operation.HomeTimeline, Operation.default_variables, limit
        )

    async def asyncHomeLatestTimeline(self, limit=math.inf) -> list[dict]:
        return await self._async_paginate(
            "POST", Operation.HomeLatestTimeline, Operation.default_variables, limit
        )

    async def asyncBookmarks(self, limit=math.inf) -> list[dict]:
        return await self._async_paginate("GET", Operation.Bookmarks, {}, limit)

    async def _async_paginate(
        self, method: str, operation: tuple, variables: dict, limit: int
    ) -> list[dict]:
        initial_data = await self.asyncGQL(method, operation, variables)
        res = [initial_data]
        ids = set(find_key(initial_data, "rest_id"))
        dups = 0
        DUP_LIMIT = 3

        cursor = get_cursor(initial_data)
        while (dups < DUP_LIMIT) and cursor:
            prev_len = len(ids)
            if prev_len >= limit:
                return res

            variables["cursor"] = cursor
            data = await self.asyncGQL(method, operation, variables)

            cursor = get_cursor(data)
            ids |= set(find_key(data, "rest_id"))

            if self.debug:
                self.logger.debug(f"cursor: {cursor}\tunique results: {len(ids)}")

            if prev_len == len(ids):
                dups += 1

            res.append(data)
        return res

    async def _async_upload_media(
        self, filename: str, is_dm: bool = False, is_profile=False
    ) -> int | None:
        """
        https://developer.twitter.com/en/docs/twitter-api/v1/media/upload-media/uploading-media/media-best-practices
        """

        def format_size(size: int) -> str:
            return f"{(size / 1e6):.2f} MB"

        def create_error_message(category: str, size: int, max_size: int) -> str:
            return f"cannot upload {format_size(size)} {category}, max size is {format_size(max_size)}"

        def check_media(category: str, size: int) -> None:
            if category == "image" and size > MAX_IMAGE_SIZE:
                raise Exception(create_error_message(category, size, MAX_IMAGE_SIZE))
            if category == "gif" and size > MAX_GIF_SIZE:
                raise Exception(create_error_message(category, size, MAX_GIF_SIZE))
            if category == "video" and size > MAX_VIDEO_SIZE:
                raise Exception(create_error_message(category, size, MAX_VIDEO_SIZE))

        # if is_profile:
        #     url = 'https://upload.twitter.com/i/media/upload.json'
        # else:
        #     url = 'https://upload.twitter.com/1.1/media/upload.json'

        url = "https://upload.twitter.com/i/media/upload.json"

        file = Path(filename)
        total_bytes = file.stat().st_size
        headers = get_headers(self.session)

        upload_type = "dm" if is_dm else "tweet"
        media_type = mimetypes.guess_type(file)[0]
        media_category = (
            f"{upload_type}_gif"
            if "gif" in media_type
            else f'{upload_type}_{media_type.split("/")[0]}'
        )

        check_media(media_category, total_bytes)

        params = {
            "command": "INIT",
            "media_type": media_type,
            "total_bytes": total_bytes,
            "media_category": media_category,
        }
        uploadMediaResponse = await self.session.post(
            url=url, headers=headers, params=params
        )

        if uploadMediaResponse.status_code >= 400:
            raise Exception(f"{uploadMediaResponse.text}")

        media_id = uploadMediaResponse.json().get("media_id_string")

        desc = f"uploading: {file.name}"
        with tqdm(
            total=total_bytes, desc=desc, unit="B", unit_scale=True, unit_divisor=1024
        ) as pbar:
            with open(file, "rb") as fp:
                i = 0
                while chunk := fp.read(UPLOAD_CHUNK_SIZE):
                    params = {
                        "command": "APPEND",
                        "media_id": media_id,
                        "segment_index": i,
                    }
                    try:
                        pad = bytes(
                            "".join(random.choices(ascii_letters, k=16)),
                            encoding="utf-8",
                        )
                        data = b"".join(
                            [
                                b"------WebKitFormBoundary",
                                pad,
                                b'\r\nContent-Disposition: form-data; name="media"; filename="blob"',
                                b"\r\nContent-Type: application/octet-stream",
                                b"\r\n\r\n",
                                chunk,
                                b"\r\n------WebKitFormBoundary",
                                pad,
                                b"--\r\n",
                            ]
                        )
                        _headers = {
                            b"content-type": b"multipart/form-data; boundary=----WebKitFormBoundary"
                            + pad
                        }
                        uploadMediaResponse = await self.session.post(
                            url=url,
                            headers=headers | _headers,
                            params=params,
                            content=data,
                        )
                    except Exception as e:
                        self.logger.error(
                            f"Failed to upload chunk, trying alternative method\n{e}"
                        )
                        try:
                            files = {"media": chunk}
                            uploadMediaResponse = await self.session.post(
                                url=url, headers=headers, params=params, files=files
                            )
                        except Exception as e:
                            self.logger.error(f"Failed to upload chunk\n{e}")
                            return

                    if (
                        uploadMediaResponse.status_code < 200
                        or uploadMediaResponse.status_code > 299
                    ):
                        self.logger.debug(
                            f"{RED}{uploadMediaResponse.status_code} {uploadMediaResponse.text}{RESET}"
                        )

                    i += 1
                    pbar.update(fp.tell() - pbar.n)

        params = {"command": "FINALIZE", "media_id": media_id, "allow_async": "true"}

        if is_dm:
            params |= {"original_md5": hashlib.md5(file.read_bytes()).hexdigest()}
        uploadMediaResponse = await self.session.post(
            url=url, headers=headers, params=params
        )

        if uploadMediaResponse.status_code == 400:
            self.logger.debug(
                f"{RED}{uploadMediaResponse.status_code} {uploadMediaResponse.text}{RESET}"
            )
            return

        # self.logger.debug(f'processing, please wait...')
        processing_info = uploadMediaResponse.json().get("processing_info")
        while processing_info:
            print("entering processing info loop")
            state = processing_info["state"]
            if error := processing_info.get("error"):
                self.logger.debug(f"{RED}{error}{RESET}")
                return
            if state == MEDIA_UPLOAD_SUCCEED:
                break
            if state == MEDIA_UPLOAD_FAIL:
                self.logger.debug(
                    f"{RED}{uploadMediaResponse.status_code} {uploadMediaResponse.text} {RESET}"
                )
                return
            check_after_secs = processing_info.get(
                "check_after_secs", random.randint(1, 5)
            )
            time.sleep(check_after_secs)
            params = {"command": "STATUS", "media_id": media_id}
            uploadMediaResponse = await self.session.get(
                url=url, headers=headers, params=params
            )
            print(f"Status Response: {uploadMediaResponse.text}")
            print(f"Status Response Status: {uploadMediaResponse.status_code}")
            processing_info = uploadMediaResponse.json().get("processing_info")
        # self.logger.debug

        return uploadMediaResponse.json().get("media_id_string")

    async def _async_validate_session(
        self,
        email: str,
        username: str,
        password: str,
        session: object,
        cookies: dict,
        **kwargs,
    ):
        # print(f'AsyncAcc Got: {email}, {username}, {password}, {session}, {kwargs}')

        if self.debug:
            self.logger.debug(f"{Fore.MAGENTA}Validating session with pString: {self.proxyString} selfProxies: {self.proxies} ogProxyString: {self.ogProxyString}{RESET}")

        # try validating cookies dict
        if isinstance(cookies, dict) and all(
            cookies.get(c) for c in {"ct0", "auth_token"}
        ):
            _session = AsyncClient(
                cookies=cookies,
                follow_redirects=True,
                http2=True,
                verify=False,
                timeout=30,
                **self.proxies,
            )
            _session.authDetails = {"username": username, "password": password, "email": email}
            _session._init_with_cookies = True
            _session.headers.update(get_headers(_session))
            # print("Logging with cookies Dict 100%")
            if self.debug:
                self.logger.debug(
                    f"{GREEN}{self.username} Logged in with cookies dict{RESET}"
                )
            return _session

        # try validating cookies from file
        if isinstance(cookies, str):
            _session = AsyncClient(
                cookies=orjson.loads(Path(cookies).read_bytes()),
                follow_redirects=True,
                http2=True,
                verify=False,
                timeout=30,
                **self.proxies,
            )
            _session.authDetails = {"username": username, "password": password, "email": email}
            _session._init_with_cookies = True
            _session.headers.update(get_headers(_session))
            if self.debug:
                self.logger.debug(
                    f"{GREEN}{self.username} Logged in with cookies file{RESET}"
                )
            return _session

        # validate credentials
        if all((email, username, password)) and not session and not cookies:
            loginResults = await asyncLogin(email, username, password, **kwargs)

            if not loginResults:
                return False

            session = loginResults

            session._init_with_cookies = False
            # print("Logging with user pass 100%")
            if self.debug:
                self.logger.debug(
                    f"{GREEN}{self.username} Logged in with user/pass{RESET}"
                )
            return session

        # invalid credentials, try validating session
        if session and all(session.cookies.get(c) for c in {"ct0", "auth_token"}):
            session._init_with_cookies = True
            return session

        return False

    async def _async_add_alt_text(self, media_id: int, text: str) -> Response:
        params = {"media_id": media_id, "alt_text": {"text": text}}
        url = f"{self.v1_api}/media/metadata/create.json"
        addAltTextResponse = await self.session.post(
            url, headers=get_headers(self.session), json=params
        )
        return addAltTextResponse

    def _init_logger(self, **kwargs) -> Logger:
        class logger:
            def warning(self, *args):
                print(f"{Fore.YELLOW}[-] WARNING: {args[0]}{RESET}")

            def info(self, *args):
                print(f"{GREEN}[+] INFO: {args[0]}{RESET}")

            def debug(self, *args):
                print(f"{Fore.CYAN}[+] DEBUG: {args[0]}{RESET}")

            def error(self, *args):
                print(f"{RED}[-] ERROR: {args[0]}{RESET}")

            def critical(self, *args):
                print(f"{RED}[!] CRITICAL: {args[0]}{RESET}")

        self.logger = logger()

        return self.logger

    def id(self) -> int:
        """Get User ID"""
        if not self.twid:
            potentialTwid = self.session.cookies.get("twid")

            if not potentialTwid:
                raise Exception("Session is missing twid cookie")

            self.twid = int(potentialTwid.split("=")[-1].strip().rstrip())

        return self.twid

    def save_cookies(self, fname: str = None, toFile=True):
        """Save cookies to file"""
        cookies = self.session.cookies
        if toFile:
            Path(f'{fname or cookies.get("username")}.cookies').write_bytes(
                orjson.dumps(dict(cookies))
            )
        return dict(cookies)
