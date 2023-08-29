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

# attempt verify with same identity value and "expected_certificate_subject" as issuer
identity = Identity(
    identity=token.identity
    issuer=token.expected_certificate_subject
)
result = verifier.verify(materials, identity)
print(f"\nVerify with {token.identity}")
print(f"  {result})

# attempt verify with another identity and "expected_certificate_subject" as issuer
identity2 = Identity(
    identity="https://github.com/jku/token-test/.github/workflows/test-sign.yml@$refs/heads/main"
    issuer=token.expected_certificate_subject
)
result = verifier.verify(materials, identity2)
print(f"\nVerify with other identity")
print(f"  {result})
