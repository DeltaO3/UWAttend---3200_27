---
title: "Project Acceptance Tests"
author: "Group 27"
date: "2024-08-05"
geometry: "margin=1in"  # Adjust the margin as needed
---

## Acceptance Criteria and Tests

### 1. User Authentication

**Acceptance Criteria:**

- Users must be able to securely log in and log out.
- Passwords must be encrypted.

**Tests:**

- Verify that users can create accounts with a secure password.
- Verify that users can log in with their credentials.
- Test login functionality with valid and invalid credentials.
- Ensure passwords are stored encrypted in the database.

### 2. Student Sign In/Out

**Acceptance Criteria:**

- Teachers must be able to sign students in and out.
- The system must record the time of sign-in and sign-out.

**Tests:**

- Verify that a teacher can sign a student in.
- Verify that a teacher can sign a student out.
- Check that the sign-in and sign-out times are recorded accurately in the database.

### 3. Barcode Scanning

**Acceptance Criteria:**

- The app must support barcode scanning for student IDs.
- Barcodes must be linked to the correct student records.

**Tests:**

- Test barcode scanning functionality with valid student ID barcodes.
- Verify that scanned barcodes link to the correct student records.
- Test the system with invalid barcodes to ensure proper error handling.

### 4. Data Management

**Acceptance Criteria:**

- The app must integrate with internal Calista databases for enrollment data.
- The app must allow export of data in CSV format.

**Tests:**

- Verify that the app can pull data from the Calista database.
- Test data synchronisation between the app and the database.
- Verify that the app can export data in CSV format and download to local machine.

### 5. Performance

**Acceptance Criteria:**

- The app must load within 3 seconds on a standard internet connection.
- The app must handle at least 10 simultaneous users without performance degradation.

**Tests:**

- Measure the app's load time on a local connection as well as through the internet.
- Perform load testing to ensure the app can handle 10 simultaneous users.

### 6. Security

**Acceptance Criteria:**

- Data exchanged between the app and the database must be encrypted using AES.
- The app must include CRC checks for data integrity.

**Tests:**

- Verify that data is encrypted during transmission using AES.
- Test CRC checks to ensure data integrity.

### 7. User Interface

**Acceptance Criteria:**

- The app must be intuitive and easy to use.
- The app must be accessible on various devices and screen sizes.

**Tests:**

- Conduct user testing to ensure the app is easy to navigate.
- Verify that the app displays correctly on different devices (e.g., desktops, tablets, smartphones).

### 8. Additional Features

**Acceptance Criteria:**

- The app must support grading and consent for photographs.
- The app must allow for offline data storage and synchronisation when the internet is available.

**Tests:**

- Verify the functionality for grading and obtaining consent for photographs.
- Test the app's ability to store data offline and synchronise it once the internet connection is restored.
