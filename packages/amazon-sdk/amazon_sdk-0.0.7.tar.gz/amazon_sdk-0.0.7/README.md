# Amazon SDK

## Setup

1. Install the package:

```bash
pip install --upgrade Amazon_SDK
```

2. Add file `.env` with the Amazon credentials:

```plaintext
LWA_APP_ID=<your_app_id>
LWA_CLIENT_SECRET=<your_client_secret>
SP_API_REFRESH_TOKEN=<your_refresh_token>
```

## Usage

For example see `usage_example.py`

Differences with `bol_SDK`:
- Use methods in class `AmazonSDK`, with detailed documentation
- No need to pass `access_token` as a parameter, which is automatically handled by the SDK

## Build

```bash
poetry build
```

## Publish

```bash
poetry publish
```