# akn_sdk/exceptions.py

class AKNError(Exception):
    pass


class AuthenticationError(AKNError):
    pass


class ProtocolVersionError(AKNError):
    pass


class SignatureVerificationError(AKNError):
    pass


class RegistrationError(AKNError):
    pass