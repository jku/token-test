import os
from sigstore.oidc import detect_credential
from securesystemslib.signer import (
    KEY_FOR_TYPE_AND_SCHEME,
    Key,
    SigstoreKey,
    SigstoreSigner,
)

KEY_FOR_TYPE_AND_SCHEME[("sigstore-oidc", "Fulcio")] = SigstoreKey

token = detect_credential()
print(token)

url = os.environ["GITHUB_SERVER_URL"]
repo = os.environ["GITHUB_REPOSITORY"]
ref = os.environ["GITHUB_REF"]

print(f"{url}/{repo}/.github/workflows/test-sign.yml@{ref}")
