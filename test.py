import io
from sigstore.oidc import detect_credential, IdentityToken, Issuer
from sigstore.sign import SigningContext
from sigstore.verify import VerificationMaterials, Verifier
from sigstore.verify.policy import Identity

token = IdentityToken(detect_credential())

print("IdentityToken")
print(f"  identity: {token.identity}")
print(f"  issuer: {token.issuer} (expected subject: {token.expected_certificate_subject})")

# sign
context = SigningContext.production()
with context.signer(token) as signer:
    sign_result = signer.sign(io.BytesIO(b""))
    bundle = sign_result._to_bundle()

materials = VerificationMaterials.from_bundle(
    input_=io.BytesIO(b""),
    bundle=bundle,
    offline=True
)
verifier = Verifier.production()

# attempt verify with same identity value and "expected_certificate_subject" as issuer: this fails as the identity does not match certificates SAN
identity = Identity(
    identity=token.identity,
    issuer=token.expected_certificate_subject
)
result = verifier.verify(materials, identity)
assert not result
print(f"\nVerify with {token.identity}")
print(f"  {result}")

# attempt verify with another identity and "expected_certificate_subject" as issuer: this succeeds
identity2 = Identity(
    identity="https://github.com/jku/token-test/.github/workflows/test-sign.yml@refs/heads/main",
    issuer=token.expected_certificate_subject
)
result = verifier.verify(materials, identity2)
assert result
print(f"\nVerify with https://github.com/jku/token-test/.github/workflows/test-sign.yml@refs/heads/main")
print(f"  {result}")
