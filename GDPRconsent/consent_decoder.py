from datetime import datetime
import base64
import codecs


VENDOR_CONSENT_STRING_FORMAT = {
    'version' : {
        'init_bit': 0,
        'len_bit': 6,
        'type': 'int'
    },
    'created': {
        'init_bit': 6,
        'len_bit': 36,
        'type': 'date'
    },
    'last_updated': {
        'init_bit': 42,
        'len_bit': 36,
        'type': 'date'
    },
    'cmp_id': {
        'init_bit': 78,
        'len_bit': 12,
        'type': 'int'
    },
    'cmp_version': {
        'init_bit': 90,
        'len_bit': 12,
        'type': 'int'
    },
    'consent_screen': {
        'init_bit': 102,
        'len_bit': 6,
        'type': 'int'
    },
    'consent_language': {
        'init_bit': 108,
        'len_bit': 12,
        'type': 'chars'
    },
    'vendor_list_version': {
        'init_bit': 120,
        'len_bit': 12,
        'type': 'int'
    },
    'purposes_allowed': {
        'init_bit': 132,
        'len_bit': 24,
        'type': 'bin'
    },
    'max_vendor_id': {
        'init_bit': 156,
        'len_bit': 16,
        'type': 'int'
    },
    'encoding_type': {
        'init_bit': 172,
        'len_bit': 1,
        'type': 'int'
    }
}

BIT_FIELD_SECTION = {
    'bit_field': {
        'init_bit': 173,
        'type': 'int'
    }
}

RANGE_SECTION = {
    'default_consent': {
        'init_bit': 173,
        'len_bit': 1,
        'type': 'int'
    },
    'num_entries': {
        'init_bit': 174,
        'len_bit': 12,
        'type': 'int'
    }
}

SINGLE_OR_RANGE_ENTRY = {
    'single_or_range': {
        'len_bit': 1,
        'type': 'int'
    }
}

SINGLE_ENTRY = {
    'single_vendor_id': {
        'len_bit': 16,
        'type': 'int'
    }
}

RANGE_ENTRY = {
    'start_vendor_id': {
        'len_bit': 16,
        'type': 'int'
    },
    'end_vendor_id': {
        'len_bit': 16,
        'type': 'int'
    }
}


class StringConsentDecoder:
    def __init__(self, str_code):
        self.str_code = self.transform_to_padded_binary_consent_string(str_code)

    def transform_to_padded_binary_consent_string(self, consent_string):
        padding = int(((len(consent_string) / 8)) + 1) * 8 - len(consent_string)
        code = consent_string + (b'=' * padding)
        code = base64.urlsafe_b64decode(code)
        code = bin(int(codecs.encode(code, 'hex'), 16))[2:]
        leading_zeros = '0' * (int((len(code) / 8) + 1) * 8 - len(code))
        return leading_zeros + code

    def get_binary_string(self, field):
        return self.str_code[
               field['init_bit']:field['init_bit'] + field['len_bit']]

    def get_int(self, field):
        return int(self.str_code[
                   field['init_bit']:field['init_bit'] + field['len_bit']], 2)

    def get_date(self, field):
        return datetime.utcfromtimestamp(
            int(
                self.str_code[
                    field['init_bit']:field['init_bit'] + field['len_bit']
                ], 2) / 10
        )

    def get_language_chars(self, field):
        bin_str = self.get_binary_string(field)
        char1 = chr(int(bin_str[:int(len(bin_str) / 2)], 2) + 97)
        char2 = chr(int(bin_str[int(len(bin_str) / 2):], 2) + 97)
        return ''.join([char1, char2])

    def get_field_value(self, field):
        if field['type'] == 'int':
            return self.get_int(field)
        elif field['type'] == 'date':
            return self.get_date(field)
        elif field['type'] == 'bin':
            return self.get_binary_string(field)
        elif field['type'] == 'chars':
            return self.get_language_chars(field)

    def get_version(self):
        return self.get_field_value(VENDOR_CONSENT_STRING_FORMAT['version'])

    def get_create_time(self):
        return self.get_field_value(VENDOR_CONSENT_STRING_FORMAT['created'])

    def get_update_time(self):
        return self.get_field_value(
            VENDOR_CONSENT_STRING_FORMAT['last_updated']
        )

    def get_cmp_id(self):
        return self.get_field_value(VENDOR_CONSENT_STRING_FORMAT['cmp_id'])

    def get_cmp_version(self):
        return self.get_field_value(VENDOR_CONSENT_STRING_FORMAT['cmp_version'])

    def get_consent_screen(self):
        return self.get_field_value(
            VENDOR_CONSENT_STRING_FORMAT['consent_screen'])

    def get_consent_language(self):
        return self.get_field_value(
            VENDOR_CONSENT_STRING_FORMAT['consent_language'])

    def get_vendor_list_version(self):
        return self.get_field_value(
            VENDOR_CONSENT_STRING_FORMAT['vendor_list_version'])

    def get_purposes_allowed(self):
        return self.get_field_value(
            VENDOR_CONSENT_STRING_FORMAT['purposes_allowed'])

    def get_max_vendor_id(self):
        return self.get_field_value(
            VENDOR_CONSENT_STRING_FORMAT['max_vendor_id'])

    def get_encoding_type(self):
        return self.get_field_value(
            VENDOR_CONSENT_STRING_FORMAT['encoding_type'])

    def get_default_consent(self):
        return self.get_field_value(RANGE_SECTION['default_consent'])

    def get_num_entries(self):
        return self.get_field_value(RANGE_SECTION['num_entries'])

    def get_single_vendor_id(self, start_bit):
        SINGLE_ENTRY['single_vendor_id']['init_bit'] = start_bit
        return self.get_field_value(SINGLE_ENTRY['single_vendor_id'])

    def get_range_vendor_id(self, start_bit):
        RANGE_ENTRY['start_vendor_id']['init_bit'] = start_bit
        RANGE_ENTRY['end_vendor_id']['init_bit'] = start_bit + 16
        return (
            self.get_field_value(RANGE_ENTRY['start_vendor_id']),
            self.get_field_value(RANGE_ENTRY['end_vendor_id']),
        )

    def parse_vendors_using_bit_field(self, consent, max_vendor):
        for vendor_id, consent_value in enumerate(self.str_code[173:]):
            if vendor_id + 1 > max_vendor: break
            consent.add_vendor(vendor_id + 1, consent_value)

    def parse_vendors_using_range_section(self, consent, max_vendor):
        default_consent = bool(self.get_default_consent())
        num_entries = self.get_num_entries()
        opp_vendors = self.parse_vendors_range_entries(num_entries)
        for vendor_id in range(max_vendor):
            consent.add_vendor(
                vendor_id,
                int(
                    default_consent if vendor_id not in opp_vendors
                    else not default_consent)
            )

    def parse_vendors_range_entries(self, num_entries):
        vendors = []
        bit_offset = 186
        for entry in range(num_entries):
            if int(self.str_code[bit_offset]) == 0:
                vendors.append(
                    self.get_single_vendor_id(bit_offset + 1)
                )
                bit_offset += 17
            else:
                # This way is not tested because of not test data
                start, end = self.get_range_vendor_id(bit_offset + 1)
                for vend in range(start, end):
                    vendors.append(vend)
        return vendors

    def parse_consent(self):
        from GDPRconsent.consent import Consent

        max_vendors = self.get_max_vendor_id()
        enconding_type = self.get_encoding_type()

        consent = Consent(
            self.get_version(),
            self.get_create_time(),
            self.get_update_time(),
            self.get_cmp_id(),
            self.get_cmp_version(),
            self.get_consent_screen(),
            self.get_consent_language(),
            self.get_vendor_list_version(),
            self.get_purposes_allowed(),
            max_vendors,
            enconding_type
        )

        if enconding_type == 0:  # BitField
            self.parse_vendors_using_bit_field(consent, max_vendors)
        else:  # RangeSection
            self.parse_vendors_using_range_section(consent, max_vendors)
        return consent
