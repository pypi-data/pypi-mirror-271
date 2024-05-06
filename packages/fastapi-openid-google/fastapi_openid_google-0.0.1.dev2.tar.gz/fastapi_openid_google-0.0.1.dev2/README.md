# fastapi-openid-google

Google OpenID integration for FastAPI.

## Usage

```python
import fastapi

from fastapi_openid_google import setup_openid

app = fastapi.FastAPI()
setup_openid(app)


@app.get("/")
def home(
    request: fastapi.Request,
):
    if request.state.user:
        return {
            "current_user": request.state.user,
            "logout": f"/logout",
        }
    else:
        return {"login": f"/login"}
```
