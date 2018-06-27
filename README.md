# gdpr-consent-string
Python implementation of parser for GDPR consent string

## Installing
Install using pip:
```bash
pip install git+https://github.com/AccesoGroup/gdpr-consent-string
```

## Usage

```python

from GDPRconsent import Consent

consent = Consent.from_bytes(b'BOEFEAyOEFEAyAHABDENAI4AAAB9vABAASA')

consent.to_json()
```

```json
{
  "cmp_id": 7,
  "max_vendor_id": 2011,
  "purposes_allowed": "111000000000000000000000",
  "consent_language": "en",
  "encoding_type": 1,
  "vendor_list_version": 8,
  "version": 1,
  "consent_screen": 3,
  "created": "2017-11-07T19:15:55Z",
  "cmp_version": 1,
  "last_updated": "2017-11-07T19:15:55Z",
  "vendors_consent": {
    "0": 1,
    "1": 1,
    "2": 1,
    "3": 1,
    "4": 1,
    "5": 1,
    "6": 1,
    "7": 1,
    "8": 1,
    "9": 0,
    "10": 1,
     [...]
}
```

## State
At this moment this software has not been heavily tested for all kinds
of consent strings. Use with caution.

## Links

 GDPR-Transparency-and-Consent-Framework - string and vendor list formats v1.1:
 https://github.com/InteractiveAdvertisingBureau/GDPR-Transparency-and-Consent-Framework/blob/master/Consent%20string%20and%20vendor%20list%20formats%20v1.1%20Final.md

