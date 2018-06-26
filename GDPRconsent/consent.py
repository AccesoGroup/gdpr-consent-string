import json

class Consent:
    def __init__(
            self,
            version,
            created,
            last_updated,
            cmp_id,
            cmp_version,
            consent_screen,
            consent_language,
            vendor_list_version,
            purposes_allowed,
            max_vendor_id,
            encoding_type
    ):
        self.version = version
        self.created = created
        self.last_updated = last_updated
        self.cmp_id = cmp_id
        self.cmp_version = cmp_version
        self.consent_screen = consent_screen
        self.consent_language = consent_language
        self.vendor_list_version = vendor_list_version
        self.purposes_allowed = purposes_allowed
        self.max_vendor_id = max_vendor_id
        self.encoding_type = encoding_type
        self.vendors_consent = {}

    def add_vendor(self, vendor_id, consent):
        self.vendors_consent[vendor_id] = consent

    def to_json(self):
        return json.dumps({
            'version': self.version,
            'created': self.created.strftime("%Y-%m-%dT%H:%M:%SZ"),
            'last_updated': self.last_updated.strftime("%Y-%m-%dT%H:%M:%SZ"),
            'cmp_id': self.cmp_id,
            'cmp_version': self.cmp_version,
            'consent_screen': self.consent_screen,
            'consent_language': self.consent_language,
            'vendor_list_version': self.vendor_list_version,
            'purposes_allowed': self.purposes_allowed,
            'max_vendor_id': self.max_vendor_id,
            'encoding_type': self.encoding_type,
            'vendors_consent': self.vendors_consent
        })

    def to_dict(self):
        return {
            'version': self.version,
            'created': self.created,
            'last_updated': self.last_updated,
            'cmp_id': self.cmp_id,
            'cmp_version': self.cmp_version,
            'consent_screen': self.consent_screen,
            'consent_language': self.consent_language,
            'vendor_list_version': self.vendor_list_version,
            'purposes_allowed': self.purposes_allowed,
            'max_vendor_id': self.max_vendor_id,
            'encoding_type': self.encoding_type,
            'vendors_consent': self.vendors_consent
        }

    @staticmethod
    def from_bytes(consent_string):
        from GDPRconsent.consent_decoder import StringConsentDecoder
        if type(consent_string) != bytes:
            raise TypeError('Consent should be bytes type')
        return StringConsentDecoder(consent_string).parse_consent()
