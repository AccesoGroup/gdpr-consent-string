import unittest
import json

from app.consent import Consent


class TestConsent(unittest.TestCase):

    def test_consent_decoder_example(self):

        # from: https://github.com/InteractiveAdvertisingBureau/GDPR-Transparency-and-Consent-Framework/blob/master/Consent%20string%20and%20vendor%20list%20formats%20v1.1%20Final.md#vendor-consent-string-format
        string_consent = b'BOEFEAyOEFEAyAHABDENAI4AAAB9vABAASA'
        consent = Consent.from_bytes(string_consent)

        self.assertEqual(consent.version, 1)
        self.assertEqual(consent.cmp_id, 7)
        self.assertEqual(consent.consent_language, 'en')
        self.assertEqual(
            consent.purposes_allowed,
            '111000000000000000000000'
        )
        self.assertEqual(consent.vendors_consent[9], 0)
        self.assertEqual(consent.vendors_consent[10], 1)

    def test_consent_to_dict(self):
        string_consent = b'BOEFEAyOEFEAyAHABDENAI4AAAB9vABAASA'
        consent = Consent.from_bytes(string_consent)

        consent_dict = consent.to_dict()

        self.assertEqual(consent_dict['version'], 1)
        self.assertEqual(consent_dict['cmp_id'], 7)
        self.assertEqual(consent_dict['consent_language'], 'en')
        self.assertEqual(
            consent_dict['purposes_allowed'],
            '111000000000000000000000'
        )
        self.assertEqual(consent_dict['vendors_consent'][9], 0)
        self.assertEqual(consent_dict['vendors_consent'][10], 1)

    def test_consent_to_json(self):
        string_consent = b'BOEFEAyOEFEAyAHABDENAI4AAAB9vABAASA'
        consent = Consent.from_bytes(string_consent)

        consent_dict = json.loads(consent.to_json())

        self.assertEqual(consent_dict['version'], 1)
        self.assertEqual(consent_dict['cmp_id'], 7)
        self.assertEqual(consent_dict['consent_language'], 'en')
        self.assertEqual(
            consent_dict['purposes_allowed'],
            '111000000000000000000000'
        )
        self.assertEqual(consent_dict['vendors_consent']['9'], 0)
        self.assertEqual(consent_dict['vendors_consent']['10'], 1)

    def test_consent_raise_error_when_type_is_not_bytes(self):
        string_consent = 'BOEFEAyOEFEAyAHABDENAI4AAAB9vABAASA'
        with self.assertRaises(TypeError):
            consent = Consent.from_bytes(string_consent)


if __name__ == '__main__':
    unittest.main()
