### Requirement ID: FR_01
- Description: The system shall allow users to select from at least 5 different app languages in the settings menu.
- Source Persona: Global User Gia
- Traceability: Derived from review group G1
- Acceptance Criteria: Given the user is in settings, When they select 'Language', Then the app UI text updates to the chosen language.

### Requirement ID: FR_02
- Description: The system shall provide a 'Doctor Export' feature that generates a PDF summary of the last 14 days.
- Source Persona: Clinical Client Chris
- Traceability: Derived from review group G2
- Acceptance Criteria: Given a user has 14 days of data, When they click 'Export for Doctor', Then a valid PDF file is generated.

### Requirement ID: FR_03
- Description: The system shall provide a clear 'Free Features' indicator on the dashboard to show available modules.
- Source Persona: Budget Tracker Brian
- Traceability: Derived from review group G3
- Acceptance Criteria: When a free user opens the app, Then all premium-only features must be visually marked with a lock icon.

### Requirement ID: FR_04
- Description: The system shall display a monthly line graph of mood scores on the main insights tab.
- Source Persona: Pattern Seeker Pam
- Traceability: Derived from review group G4
- Acceptance Criteria: When the user navigates to Insights, Then a chart showing 30 days of mood data is rendered correctly.

### Requirement ID: FR_05
- Description: The system shall allow users to complete a mood check-in using a maximum of three screen taps.
- Source Persona: Minimalist Mike
- Traceability: Derived from review group G5
- Acceptance Criteria: From the home screen, a user can log their current mood and save it within 3 interactions.

### Requirement ID: FR_06
- Description: The system shall allow users to add custom text notes to any daily mood log.
- Source Persona: Clinical Client Chris
- Traceability: Derived from review group G2
- Acceptance Criteria: During a mood check-in, a text field is available and saves the user input to the database.

### Requirement ID: FR_07
- Description: The system shall store data locally and sync with the cloud when an internet connection is established.
- Source Persona: Minimalist Mike
- Traceability: Derived from review group G5
- Acceptance Criteria: When offline, logs are saved to device storage; when online, the 'Sync' status turns green.

### Requirement ID: FR_08
- Description: The system shall offer a one-time purchase option as an alternative to monthly subscriptions.
- Source Persona: Budget Tracker Brian
- Traceability: Derived from review group G3
- Acceptance Criteria: The payment screen includes a 'Lifetime Access' option alongside monthly/yearly plans.

### Requirement ID: FR_09
- Description: The system shall display tooltips explaining complex clinical terms used in the assessment courses.
- Source Persona: Global User Gia
- Traceability: Derived from review group G1
- Acceptance Criteria: Tapping an underlined term in a course displays a plain-language definition in a popup.

### Requirement ID: FR_10
- Description: The system shall allow users to filter their mood history by specific tags like 'Work' or 'Sleep'.
- Source Persona: Pattern Seeker Pam
- Traceability: Derived from review group G4
- Acceptance Criteria: Selecting the 'Work' filter only displays logs where the 'Work' tag was applied.