"""
Security Test Payloads Utility

Provides common security test payloads for SQL injection, XSS,
and other vulnerability testing scenarios.
"""


class SecurityPayloads:
    """Collection of security test payloads"""

    # SQL Injection Payloads
    SQL_INJECTION_PAYLOADS = [
        "' OR '1'='1",
        "' OR '1'='1' --",
        "' OR '1'='1' /*",
        "admin' --",
        "admin' #",
        "admin'/*",
        "' or 1=1--",
        "' or 1=1#",
        "' or 1=1/*",
        "') or '1'='1--",
        "') or ('1'='1--",
        "' OR 'x'='x",
        "' UNION SELECT NULL--",
        "' UNION SELECT NULL, NULL--",
        "' UNION SELECT NULL, NULL, NULL--",
        "'; DROP TABLE users--",
        "1' AND '1'='1",
        "1' AND '1'='2",
        "1' ORDER BY 1--",
        "1' ORDER BY 10--",
        "1' ORDER BY 100--",
    ]

    # Blind SQL Injection Payloads
    BLIND_SQL_INJECTION_PAYLOADS = [
        "1' AND 1=1--",
        "1' AND 1=2--",
        "1' AND SLEEP(5)--",
        "1' AND BENCHMARK(5000000,MD5('X'))--",
    ]

    # XSS Payloads
    XSS_PAYLOADS = [
        "<script>alert('XSS')</script>",
        "<script>alert(document.cookie)</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg onload=alert('XSS')>",
        "<iframe src=javascript:alert('XSS')>",
        "<body onload=alert('XSS')>",
        "<input autofocus onfocus=alert('XSS')>",
        "<select onfocus=alert('XSS') autofocus>",
        "<textarea autofocus onfocus=alert('XSS')>",
        "<keygen autofocus onfocus=alert('XSS')>",
        "<video><source onerror=alert('XSS')>",
        "<audio src=x onerror=alert('XSS')>",
        "<details open ontoggle=alert('XSS')>",
        "<math><mtext><table><mglyph><style>img{width:expression(alert('XSS'))}</style>",
        "javascript:alert('XSS')",
        "<script>eval(atob('YWxlcnQoJ1hTUycp'))</script>",
    ]

    # Stored XSS Payloads
    STORED_XSS_PAYLOADS = [
        "<script>alert('Stored XSS')</script>",
        "<img src=x onerror=alert('Stored XSS')>",
        "<svg onload=alert('Stored XSS')>",
    ]

    # Reflected XSS Payloads
    REFLECTED_XSS_PAYLOADS = [
        " <script>alert('XSS')</script>",
        "\"><script>alert('XSS')</script>",
        "'-alert('XSS')-'",
        "><script>alert('XSS')</script>",
    ]

    # Command Injection Payloads
    COMMAND_INJECTION_PAYLOADS = [
        "; ls -la",
        "| ls -la",
        "& ls -la",
        "&& ls -la",
        "| whoami",
        "; whoami",
        "`whoami`",
        "$(whoami)",
    ]

    # Path Traversal Payloads
    PATH_TRAVERSAL_PAYLOADS = [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
        "....//....//....//etc/passwd",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "..%252f..%252f..%252fetc%252fpasswd",
    ]

    # Weak Passwords for Testing
    WEAK_PASSWORDS = [
        "password",
        "123456",
        "12345678",
        "qwerty",
        "123456789",
        "12345",
        "1234",
        "111111",
        "1234567",
        "abc123",
        "admin",
        "letmein",
        "welcome",
        "monkey",
        "123321",
    ]

    # Invalid Email Formats
    INVALID_EMAILS = [
        "plainaddress",
        "@missinglocal.com",
        "missingdomain@",
        "double@@domain.com",
        "space in@email.com",
        "tabCharacter\t@domain.com",
        "newlinendomain@n\\newline.com",
    ]

    # Special Characters for Input Validation
    SPECIAL_CHARACTERS = [
        "<",
        ">",
        '"',
        "'",
        "&",
        "|",
        ";",
        "`",
        "$",
        "(",
        ")",
        "{",
        "}",
        "[",
        "]",
        "*",
        "?",
        "\\",
        "/",
    ]

    # HTML Entities for Encoding Tests
    HTML_ENCODED_PAYLOADS = [
        "&lt;script&gt;alert('XSS')&lt;/script&gt;",
        "&#60;script&#62;alert('XSS')&#60;/script&#62;",
        "&lt;img src=x onerror=alert('XSS')&gt;",
    ]

    # JSON Injection Payloads
    JSON_INJECTION_PAYLOADS = [
        '{"username": "admin", "password": "admin"}',
        '{"username": "admin" OR 1=1--", "password": ""}',
    ]

    # XML Injection Payloads
    XML_INJECTION_PAYLOADS = [
        '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>',
    ]

    @classmethod
    def get_sql_payload(cls, index: int = None):
        """Get SQL injection payload by index or random"""
        import random
        if index is None:
            index = random.randint(0, len(cls.SQL_INJECTION_PAYLOADS) - 1)
        return cls.SQL_INJECTION_PAYLOADS[index]

    @classmethod
    def get_xss_payload(cls, index: int = None):
        """Get XSS payload by index or random"""
        import random
        if index is None:
            index = random.randint(0, len(cls.XSS_PAYLOADS) - 1)
        return cls.XSS_PAYLOADS[index]

    @classmethod
    def get_weak_password(cls, index: int = None):
        """Get weak password by index or random"""
        import random
        if index is None:
            index = random.randint(0, len(cls.WEAK_PASSWORDS) - 1)
        return cls.WEAK_PASSWORDS[index]

    @classmethod
    def get_invalid_email(cls, index: int = None):
        """Get invalid email by index or random"""
        import random
        if index is None:
            index = random.randint(0, len(cls.INVALID_EMAILS) - 1)
        return cls.INVALID_EMAILS[index]


class SecurityTestHelpers:
    """Helper methods for security testing"""

    @staticmethod
    def should_not_expose_sql_errors(response_text: str) -> bool:
        """Check if response exposes SQL error messages"""
        sql_error_keywords = [
            "mysql_fetch",
            "mysql_num_rows",
            "mysql_query",
            "mysqli",
            "sql syntax",
            "sql error",
            "ORA-",
            "postgresql",
            "sqlite3",
            "unterminated",
            "sqlstate",
        ]
        text_lower = response_text.lower()
        return not any(keyword in text_lower for keyword in sql_error_keywords)

    @staticmethod
    def should_not_expose_xss(response_text: str) -> bool:
        """Check if response reflects XSS payload without encoding"""
        for payload in SecurityPayloads.XSS_PAYLOADS[:5]:
            if payload in response_text:
                return False
        return True

    @staticmethod
    def check_for_sensitive_data_leak(response_text: str) -> dict:
        """Check response for sensitive data leaks"""
        import re

        findings = {
            "email_found": bool(re.search(r'[\w.-]+@[\w.-]+\.\w+', response_text)),
            "phone_found": bool(re.search(r'\d{3}[-.]?\d{3}[-.]?\d{4}', response_text)),
            "password_found": "password" in response_text.lower(),
            "ssn_found": bool(re.search(r'\d{3}-\d{2}-\d{4}', response_text)),
        }
        return findings