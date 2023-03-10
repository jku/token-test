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

identity = f"{url}/{repo}/.github/workflows/test-sign.yml@{ref}"
issuer="https://token.actions.githubusercontent.com"

# TODO this should happen in SigstoreSigner.import_()
public_key = Key.from_dict(
  "abcdef",
  {
    "keytype": "sigstore-oidc",
    "scheme": "Fulcio",
    "keyval": {
      "issuer": issuer,
      "identity": identity,
    },
  },
)
signer = SigstoreSigner(token, public_key)
sig = signer.sign(b"data")

print("KEY", public_key.to_dict())
print("SIG", sig.to_dict())
