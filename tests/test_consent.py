import unittest
import json

from GDPRconsent.consent import Consent
from GDPRconsent.consent_decoder import StringConsentDecoder


class TestConsent(unittest.TestCase):

    def test_consent_example_binary_string(self):

        string_consent = b'BOEFEAyOEFEAyAHABDENAI4AAAB9vABAASA'
        consent = StringConsentDecoder(string_consent)

        self.assertEqual(
            consent.str_code,
            '000001001110000100000101000100000000110010001110000100000101000100'
            '000000110010000000000111000000000001000011000100001101000000001000'
            '111000000000000000000000000001111101101111000000000001000000000000'
            '0100100000'
        )

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

    def test_consent_real_binary_string(self):

        string_consent = \
            b'BOPPwkaOPPwkaAKABBENA6-AAAAap7_______9______9uz_Gv_r_f__33e8_39' \
            b'v_h_7_-___m_-3zV4-_lvR11yPA1OrfIrwFBi'
        consent = StringConsentDecoder(string_consent)

        self.assertEqual(
            consent.str_code,
            '000001001110001111001111110000100100011010001110001111001111110000'
            '100100011010000000001010000000000001000001000100001101000000111010'
            '111110000000000000000000000000011010101001111011111111111111111111'
            '111111111111111111111111111101111111111111111111111111111111111111'
            '111101101110110011111111000110101111111111101011111111011111111111'
            '111111110111110111011110111100111111110111111101101111111111100001'
            '111111111011111111111110111111111111111111100110111111111110110111'
            '110011010101111000111110111111100101101111010001110101110101110010'
            '001111000000110101001110101011011111001000101011110000000101000001'
            '100010'
        )

    def test_consent_decoder_real_consent_string(self):
        string_consent = \
            b'BOPPwkaOPPwkaAKABBENA6-AAAAap7_______9______9uz_Gv_r_f__33e8_39' \
            b'v_h_7_-___m_-3zV4-_lvR11yPA1OrfIrwFBi'
        consent = Consent.from_bytes(string_consent)

        self.assertEqual(consent.version, 1)
        self.assertEqual(consent.cmp_id, 10)
        self.assertEqual(consent.consent_language, 'en')
        self.assertEqual(consent.max_vendor_id, 426)
        self.assertEqual(
            consent.purposes_allowed,
            '111110000000000000000000'
        )
        self.assertEqual(consent.vendors_consent[229], 1)
        self.assertEqual(consent.vendors_consent[1], 1)

    def test_consent_decoder_real2_consent_string(self):
        string_consent = 'BOP2j8_OP2j8_AHABBESA5-AAAAaZ7______b9_3__7_9uz_Cv_' \
                         'K7Xf_nnW0721PVA_rXOz_gE7YRAEIAkAAAAAAAAAAAAAAAAAA'
        consent = Consent.from_bytes(string_consent)

        self.assertEqual(consent.version, 1)
        self.assertEqual(consent.cmp_id, 7)
        self.assertEqual(consent.consent_language, 'es')
        self.assertEqual(consent.max_vendor_id, 422)
        self.assertEqual(
            consent.purposes_allowed,
            '111110000000000000000000'
        )
        self.assertEqual(consent.vendors_consent[320], 0)
        self.assertEqual(consent.vendors_consent[63], 1)

    def test_consent_decoder_fake(self):
        string_consent = 'BOP2eaEOP2eaEAAAAAAAA7-AAAAEwAMAAAgAAIAAQIA'
        consent = Consent.from_bytes(string_consent)

        self.assertEqual(consent.version, 1)
        self.assertEqual(consent.cmp_id, 0)
        self.assertEqual(consent.consent_language, 'aa')
        self.assertEqual(consent.max_vendor_id, 76)
        self.assertEqual(
            consent.purposes_allowed,
            '111110000000000000000000'
        )
        self.assertEqual(consent.vendors_consent[76], 1)
        self.assertEqual(consent.vendors_consent[1], 0)


if __name__ == '__main__':
    unittest.main()
