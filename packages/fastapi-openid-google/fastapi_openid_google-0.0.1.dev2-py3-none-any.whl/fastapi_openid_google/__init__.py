import datetime
import json
import logging
import os
import re
import typing

import fastapi
import pydantic
import requests
from oauthlib.oauth2 import WebApplicationClient


class User(pydantic.BaseModel):
    unique_id: str
    name: str
    email: str
    profile_pic: str


class UserAuth(pydantic.BaseModel):
    id_token: str
    access_token: str
    user: User
    logged_in_at: datetime.datetime
    expires_at: datetime.datetime


class OpenIDGoogleAuthService:
    def __init__(self, google_client_id: str, google_client_secret: str):
        self.google_client_id = google_client_id
        self.google_client_secret = google_client_secret
        self.client = WebApplicationClient(google_client_id)
        self._google_provider_cfg = None
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @property
    def google_provider_cfg(self) -> dict:
        if not self._google_provider_cfg:
            self._google_provider_cfg = requests.get(
                "https://accounts.google.com/.well-known/openid-configuration"
            ).json()
        return self._google_provider_cfg

    def get_authenticated_user(self, request: fastapi.Request) -> typing.Optional[User]:
        try:
            expires_at = request.cookies.get("user.expires_at")
            self.logger.info(f"expires_at: {expires_at}")
            if expires_at:
                expires_at = datetime.datetime.fromisoformat(expires_at)
                if expires_at > datetime.datetime.utcnow().astimezone():
                    user_json = request.cookies.get("user.json")
                    self.logger.info(f"user_json: {user_json}")
                    if user_json:
                        return User(**json.loads(user_json))
        except Exception as error:
            self.logger.exception(error)
        return None

    def remove_authenticated_user(
        self, request: fastapi.Request, response: fastapi.Response
    ):
        try:
            for k in request.cookies.keys():
                if k.startswith("user."):
                    response.delete_cookie(key=k)
        except Exception as error:
            logging.exception(error)

    def login(self, redirect_uri: str):
        # Find out what URL to hit for Google login
        authorization_endpoint = self.google_provider_cfg["authorization_endpoint"]

        # Use library to construct the request for login and provide
        # scopes that let you retrieve user's profile from Google
        self.logger.info(f"redirect_uri: {redirect_uri}")
        request_uri = self.client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=redirect_uri,
            scope=[
                "openid",
                "email",
                "profile",
                # "https://www.googleapis.com/auth/devstorage.read_only",
            ],
        )
        self.logger.info(f"request_uri: {request_uri}")
        return request_uri

    def callback(self, callback_url: str, code: str, redirect_url: str) -> UserAuth:
        # Find out what URL to hit to get tokens that allow you to ask for
        # things on behalf of a user
        token_endpoint = self.google_provider_cfg["token_endpoint"]
        self.logger.info(f"token_endpoint: {token_endpoint}")

        # Prepare and send request to get tokens! Yay tokens!
        self.logger.info(f"callback_url: {callback_url}")
        self.logger.info(f"redirect_url: {redirect_url}")
        token_url, headers, body = self.client.prepare_token_request(
            token_endpoint,
            authorization_response=callback_url,
            redirect_url=redirect_url,
            code=code,
        )
        self.logger.info(f"token_url: {token_url}")
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(self.google_client_id, self.google_client_secret),
        )
        self.logger.info(
            f"{token_response.request.method} {token_response.request.url} >> {token_response.status_code} {token_response.text}"
        )

        # Parse the tokens!
        parsed_token_response = self.client.parse_request_body_response(
            token_response.text
        )
        self.logger.info(f"parsed_token_response: {parsed_token_response}")

        access_token = parsed_token_response.get("access_token")
        id_token = parsed_token_response.get("id_token")
        self.logger.info(f"access_token: {access_token}")
        self.logger.info(f"id_token: {id_token}")

        expires_in = parsed_token_response.get("expires_in")
        logged_in_at = datetime.datetime.now().astimezone()
        expires_at = logged_in_at + datetime.timedelta(seconds=expires_in)
        self.logger.info(f"logged_in_at: {logged_in_at}")
        self.logger.info(f"expires_in: {expires_in}")
        self.logger.info(f"expires_at: {expires_at}")

        # Now that we have tokens (yay) let's find and hit URL
        # from Google that gives you user's profile information,
        # including their Google Profile Image and Email
        userinfo_endpoint = self.google_provider_cfg["userinfo_endpoint"]
        self.logger.info(f"userinfo_endpoint: {userinfo_endpoint}")

        uri, headers, body = self.client.add_token(userinfo_endpoint)
        self.logger.info(f"uri: {uri}")
        self.logger.info(f"headers: {headers}")
        self.logger.info(f"body: {body}")
        userinfo_response = requests.get(uri, headers=headers, data=body)
        self.logger.info(
            f"{userinfo_response.request.method} {userinfo_response.request.url} >> {userinfo_response.status_code} {userinfo_response.text}"
        )

        # We want to make sure their email is verified.
        # The user authenticated with Google, authorized our
        # app, and now we've verified their email through Google!
        if userinfo_response.json().get("email_verified"):
            unique_id = userinfo_response.json()["sub"]
            users_email = userinfo_response.json()["email"]
            picture = userinfo_response.json()["picture"]
            users_name = userinfo_response.json()["given_name"]
        else:
            raise ValueError("User email not available or not verified by Google.")

        # Create a user in our db with the information provided
        # by Google
        user = User(
            unique_id=unique_id, name=users_name, email=users_email, profile_pic=picture
        )
        self.logger.info(f"user: {user}")

        # Send user back to homepage
        return UserAuth(
            user=user,
            logged_in_at=logged_in_at,
            expires_at=expires_at,
            id_token=id_token,
            access_token=access_token,
        )


_auth_service_default_instance = None


def get_auth_service_default_instance():
    global _auth_service_default_instance
    if not _auth_service_default_instance:
        google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        if not google_client_id:
            raise RuntimeError("missing GOOGLE_CLIENT_ID")
        google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        if not google_client_secret:
            raise RuntimeError("missing GOOGLE_CLIENT_ID")
        _auth_service_default_instance = OpenIDGoogleAuthService(
            google_client_id=google_client_id, google_client_secret=google_client_secret
        )
    return _auth_service_default_instance


def build_openid_router(auth_service: OpenIDGoogleAuthService = None):
    if not auth_service:
        auth_service = get_auth_service_default_instance()

    oauthlib_insecure_transport = bool(os.getenv("OAUTHLIB_INSECURE_TRANSPORT"))

    router = fastapi.APIRouter()
    no_auth_path = "/no-auth"

    @router.get("/login")
    def login(
        request: fastapi.Request,
    ):
        _base_url = str(request.base_url)
        if not oauthlib_insecure_transport:
            _base_url = re.sub(r"^https?://", "https://", _base_url)
        request_uri = auth_service.login(redirect_uri=f"{_base_url}login/callback")
        return fastapi.responses.RedirectResponse(f"{request_uri}")

    @router.get("/login/callback")
    def callback(
        request: fastapi.Request,
    ):
        # Get authorization code Google sent back to you
        code = request.query_params.get("code")

        _url = str(request.url)
        _base_url = str(request.base_url)
        if not oauthlib_insecure_transport:
            _url = re.sub(r"^https?://", "https://", _url)
            _base_url = re.sub(r"^https?://", "https://", _base_url)

        user_auth = auth_service.callback(
            code=code,
            callback_url=_url,
            redirect_url=f"{_base_url}login/callback",
        )

        response = fastapi.responses.RedirectResponse(url=_base_url)
        response.set_cookie(key="user.json", value=user_auth.user.model_dump_json())
        response.set_cookie(
            key="user.expires_at", value=user_auth.expires_at.isoformat()
        )
        return response

    @router.get("/logout")
    def logout(
        request: fastapi.Request,
    ):
        _base_url = str(request.base_url)
        if not oauthlib_insecure_transport:
            _base_url = re.sub(r"^https?://", "https://", _base_url)
        response = fastapi.responses.RedirectResponse(url=_base_url)
        auth_service.remove_authenticated_user(request, response)
        return response

    @router.get(no_auth_path)
    def no_auth(
        request: fastapi.Request,
        response: fastapi.Response,
    ):
        authenticated_user = auth_service.get_authenticated_user(request)
        if authenticated_user:
            return fastapi.responses.RedirectResponse(url=f"/")
        else:
            auth_service.remove_authenticated_user(request, response)
            return {"message": "no auth"}

    return router


def setup_openid(app: fastapi.FastAPI, auth_service: OpenIDGoogleAuthService = None):
    if not auth_service:
        auth_service = get_auth_service_default_instance()

    @app.middleware("http")
    async def add_user(request: fastapi.Request, call_next):
        request.state.user = auth_service.get_authenticated_user(request)
        return await call_next(request)

    router = build_openid_router(auth_service)
    app.include_router(router)
