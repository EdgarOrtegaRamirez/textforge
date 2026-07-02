"""Tests for textforge.validation module."""

from textforge.validation import (
    is_valid_date,
    is_valid_email,
    is_valid_hex_color,
    is_valid_ip_address,
    is_valid_isbn,
    is_valid_json,
    is_valid_semver,
    is_valid_url,
    is_valid_uuid,
)


class TestIsValidEmail:
    def test_valid(self):
        assert is_valid_email("user@example.com") is True
        assert is_valid_email("test.user+tag@sub.domain.co.uk") is True
        assert is_valid_email("name@domain.io") is True

    def test_invalid(self):
        assert is_valid_email("") is False
        assert is_valid_email("notanemail") is False
        assert is_valid_email("@domain.com") is False
        assert is_valid_email("user@") is False
        assert is_valid_email("user@domain") is False
        assert is_valid_email("user domain.com") is False


class TestIsValidUrl:
    def test_valid(self):
        assert is_valid_url("https://example.com") is True
        assert is_valid_url("http://example.com/path?q=1") is True
        assert is_valid_url("https://sub.domain.co.uk/path") is True

    def test_invalid(self):
        assert is_valid_url("") is False
        assert is_valid_url("not a url") is False
        assert is_valid_url("ftp://example.com") is False
        assert is_valid_url("example.com") is False


class TestIsValidIpAddress:
    def test_valid_ipv4(self):
        assert is_valid_ip_address("192.168.1.1") is True
        assert is_valid_ip_address("0.0.0.0") is True
        assert is_valid_ip_address("255.255.255.255") is True
        assert is_valid_ip_address("10.0.0.1") is True

    def test_invalid_ipv4(self):
        assert is_valid_ip_address("256.1.1.1") is False
        assert is_valid_ip_address("1.2.3") is False
        assert is_valid_ip_address("abc.def.ghi.jkl") is False

    def test_valid_ipv6(self):
        assert is_valid_ip_address("2001:0db8:85a3:0000:0000:8a2e:0370:7334") is True

    def test_invalid(self):
        assert is_valid_ip_address("") is False
        assert is_valid_ip_address("not an ip") is False


class TestIsValidUuid:
    def test_valid(self):
        assert is_valid_uuid("550e8400-e29b-41d4-a716-446655440000") is True
        assert is_valid_uuid("00000000-0000-0000-0000-000000000000") is True

    def test_invalid(self):
        assert is_valid_uuid("") is False
        assert is_valid_uuid("not-a-uuid") is False
        assert is_valid_uuid("550e8400-e29b-41d4-a716") is False
        assert is_valid_uuid("550e8400e29b41d4a716446655440000") is False  # No dashes


class TestIsValidHexColor:
    def test_valid_six(self):
        assert is_valid_hex_color("#FF5733") is True
        assert is_valid_hex_color("#000000") is True

    def test_valid_three(self):
        assert is_valid_hex_color("#F00") is True
        assert is_valid_hex_color("#abc") is True

    def test_invalid(self):
        assert is_valid_hex_color("") is False
        assert is_valid_hex_color("FF5733") is False  # No #
        assert is_valid_hex_color("#GGHHII") is False
        assert is_valid_hex_color("#12") is False
        assert is_valid_hex_color("#1234567") is False


class TestIsValidDate:
    def test_iso(self):
        assert is_valid_date("2024-01-15") is True
        assert is_valid_date("2024/01/15") is True

    def test_us_format(self):
        assert is_valid_date("01/15/2024") is True

    def test_compact(self):
        assert is_valid_date("20240115") is True

    def test_invalid(self):
        assert is_valid_date("") is False
        assert is_valid_date("not a date") is False
        assert is_valid_date("2024-13-45") is False


class TestIsValidIsbn:
    def test_isbn13_valid(self):
        assert is_valid_isbn("978-3-16-148410-0") is True

    def test_isbn10_valid(self):
        assert is_valid_isbn("0-306-40615-2") is True

    def test_invalid(self):
        assert is_valid_isbn("") is False
        assert is_valid_isbn("12345") is False


class TestIsValidSemver:
    def test_valid(self):
        assert is_valid_semver("1.0.0") is True
        assert is_valid_semver("0.1.0") is True
        assert is_valid_semver("1.0.0-beta.1") is True
        assert is_valid_semver("1.0.0+build.123") is True
        assert is_valid_semver("1.0.0-alpha+001") is True

    def test_invalid(self):
        assert is_valid_semver("") is False
        assert is_valid_semver("1.0") is False
        assert is_valid_semver("v1.0.0") is False
        assert is_valid_semver("1.0.0.0") is False


class TestIsValidJson:
    def test_valid(self):
        assert is_valid_json('{"key": "value"}') is True
        assert is_valid_json("[1, 2, 3]") is True
        assert is_valid_json('"hello"') is True
        assert is_valid_json("42") is True

    def test_invalid(self):
        assert is_valid_json("") is False
        assert is_valid_json("{key: value}") is False
        assert is_valid_json("not json") is False
