"""Tests for textforge.extraction module."""

from textforge.extraction import (
    extract_all,
    extract_dates,
    extract_emails,
    extract_hex_colors,
    extract_ip_addresses,
    extract_phone_numbers,
    extract_urls,
    extract_uuids,
)


class TestExtractEmails:
    def test_basic(self):
        results = extract_emails("Contact me at user@example.com for info.")
        assert len(results) == 1
        assert results[0].value == "user@example.com"
        assert results[0].pattern == "email"

    def test_multiple(self):
        text = "Email a@b.com or c@d.org"
        results = extract_emails(text)
        assert len(results) == 2

    def test_none_found(self):
        assert extract_emails("no emails here") == []

    def test_complex_email(self):
        results = extract_emails("test.user+tag@sub.domain.co.uk")
        assert len(results) == 1

    def test_positions(self):
        text = "Email: user@example.com end"
        results = extract_emails(text)
        assert results[0].start == 7
        assert results[0].end == 23


class TestExtractUrls:
    def test_http(self):
        results = extract_urls("Visit http://example.com today.")
        assert len(results) == 1
        assert "http://example.com" in results[0].value

    def test_https(self):
        results = extract_urls("Go to https://example.com/path?q=1")
        assert len(results) == 1

    def test_www(self):
        results = extract_urls("Check www.example.com for details.")
        assert len(results) == 1

    def test_none_found(self):
        assert extract_urls("no urls here") == []


class TestExtractPhoneNumbers:
    def test_us_format(self):
        results = extract_phone_numbers("Call 555-123-4567 today.")
        assert len(results) >= 1

    def test_international(self):
        results = extract_phone_numbers("Call +1-555-123-4567")
        assert len(results) >= 1

    def test_none_found(self):
        results = extract_phone_numbers("no phone numbers")
        assert len(results) == 0


class TestExtractIPAddresses:
    def test_ipv4(self):
        results = extract_ip_addresses("Server at 192.168.1.1 is up.")
        assert len(results) == 1
        assert results[0].value == "192.168.1.1"
        assert results[0].pattern == "ipv4"

    def test_invalid_ipv4(self):
        results = extract_ip_addresses("Invalid: 999.999.999.999")
        assert len(results) == 0

    def test_ipv6(self):
        results = extract_ip_addresses("IPv6: 2001:0db8:85a3:0000:0000:8a2e:0370:7334")
        assert len(results) >= 1

    def test_none_found(self):
        assert extract_ip_addresses("no ips here") == []


class TestExtractUUIDs:
    def test_valid(self):
        text = "ID: 550e8400-e29b-41d4-a716-446655440000"
        results = extract_uuids(text)
        assert len(results) == 1
        assert results[0].pattern == "uuid"

    def test_none_found(self):
        assert extract_uuids("no uuids") == []


class TestExtractDates:
    def test_iso_format(self):
        results = extract_dates("Date: 2024-01-15")
        assert len(results) == 1

    def test_us_format(self):
        results = extract_dates("Date: 01/15/2024")
        assert len(results) == 1

    def test_month_name(self):
        results = extract_dates("January 15, 2024")
        assert len(results) == 1

    def test_none_found(self):
        assert extract_dates("no dates") == []


class TestExtractHexColors:
    def test_six_digit(self):
        results = extract_hex_colors("Color: #FF5733")
        assert len(results) == 1
        assert results[0].pattern == "hex_color"

    def test_three_digit(self):
        results = extract_hex_colors("Color: #F00")
        assert len(results) == 1

    def test_zerox_prefix(self):
        results = extract_hex_colors("Color: 0xFF5733")
        assert len(results) == 1

    def test_none_found(self):
        assert extract_hex_colors("no colors") == []


class TestExtractAll:
    def test_mixed(self):
        text = "Email user@example.com, visit https://example.com, IP 192.168.1.1"
        results = extract_all(text)
        assert len(results) >= 3
        # Should be sorted by position
        for i in range(len(results) - 1):
            assert results[i].start <= results[i + 1].start

    def test_empty(self):
        assert extract_all("") == []
