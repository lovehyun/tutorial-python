# Web Application Security Vulnerabilities

## 1. SQL Injection
- **Description**: This vulnerability occurs when user input is included directly in SQL queries, allowing an attacker to manipulate the query to read or modify the database in unauthorized ways.
- **Example**: In a login form, providing a `username` like `' OR '1'='1` bypasses authentication by tricking the query.
- **Mitigation**: Use prepared statements and ORM frameworks to prevent direct user input from being part of SQL queries.

---

## 2. XSS (Cross-Site Scripting)
- **Description**: XSS vulnerabilities occur when user inputs are rendered in HTML without proper encoding, allowing malicious scripts to execute.
- **Example**: In a comment section, inserting `<script>alert('XSS')</script>` would execute the script when another user views the page.
- **Mitigation**: Sanitize and escape user input before rendering it in HTML to prevent script execution.

---

## 3. CSRF (Cross-Site Request Forgery)
- **Description**: CSRF attacks force authenticated users to submit unwanted requests to a server from a malicious site, potentially causing harmful actions without their consent.
- **Example**: If a logged-in user visits a malicious site, it may send a password change request to the original site without the user's intention.
- **Mitigation**: Use CSRF tokens to validate that requests come directly from authenticated users.

---

## 4. Insecure Direct Object References (IDOR)
- **Description**: IDOR occurs when users can access data directly through parameters or URLs, potentially accessing other users' data without proper authorization.
- **Example**: Accessing `/user_profile?user_id=1` may allow unauthorized access to other profiles if the `user_id` parameter is changed.
- **Mitigation**: Enforce authorization checks on all sensitive data access.

---

## 5. File Upload Vulnerabilities
- **Description**: This vulnerability arises when files are uploaded without validation, allowing executable or malicious files to be saved and run on the server.
- **Example**: Allowing `.php` or `.exe` files to be uploaded may allow attackers to execute scripts directly on the server.
- **Mitigation**: Restrict allowed file types, and store uploaded files in non-executable directories.

---

## 6. Weak Password Policy
- **Description**: Weak password policies allow users to choose easily guessed passwords, making accounts susceptible to brute-force or dictionary attacks.
- **Example**: Allowing `1234` as a password increases the risk of unauthorized access.
- **Mitigation**: Enforce strong password policies, including minimum length, uppercase, lowercase, numeric, and special characters.

---

## 7. Unvalidated Redirects and Forwards
- **Description**: This vulnerability allows unvalidated URL redirections based on user inputs, potentially redirecting users to phishing sites.
- **Example**: Redirecting users based on a `next` parameter in URLs can lead to phishing if it includes a malicious site.
- **Mitigation**: Restrict redirections to trusted URLs only and validate user-provided URLs.

---

## 8. Sensitive Data Exposure
- **Description**: Sensitive data exposure occurs when unencrypted sensitive information is stored or transmitted, making it vulnerable to interception.
- **Example**: Storing plain text passwords or using HTTP to transmit sensitive data leaves it vulnerable to interception.
- **Mitigation**: Use HTTPS for encrypted data transfer and hash sensitive data like passwords before storage.

---

## 9. Security Misconfiguration
- **Description**: Security misconfiguration includes leaving default or insecure server settings enabled, which can expose internal functionalities.
- **Example**: Running an application in debug mode or exposing unnecessary endpoints increases security risks.
- **Mitigation**: Regularly review server configurations to disable unnecessary features and ensure secure settings.

---

## 10. Broken Authentication and Session Management
- **Description**: This vulnerability occurs when session tokens are not securely stored or managed, allowing attackers to hijack sessions.
- **Example**: If session tokens are stored in an insecure manner or have no expiration, attackers can reuse stolen tokens for unauthorized access.
- **Mitigation**: Set expiration times for sessions and securely store session tokens using encryption.

---

These vulnerabilities are common in web applications and can lead to severe security issues. Regular security audits and secure coding practices help mitigate these risks.
