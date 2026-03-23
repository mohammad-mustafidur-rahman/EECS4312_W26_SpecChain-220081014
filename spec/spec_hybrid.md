# Requirement ID: FR_hybrid_1
- Description: The system shall provide a dropdown menu in the settings allowing the user to select from 5 supported interface languages.
- Source Persona: Global User Alex
- Traceability: H1
- Acceptance Criteria: Given the user selects Spanish from settings, then the navigation labels must update to Spanish text without requiring an application restart.
- Notes: The AI wrote a useless requirement about "guessing navigation." I changed it to a specific language localization feature based on actual user feedback.

# Requirement ID: FR_hybrid_2
- Description: The system shall allow users to export a 14-day symptom summary report as a PDF document.
- Source Persona: Clinical Patient Mia
- Traceability: H2
- Acceptance Criteria: Given the user has 14 days of data, when they tap Export, the system generates a valid PDF containing their mood graph.
- Notes: We can't test if a user "reduces symptoms" since that's a medical outcome. I changed this to a tangible software feature: exporting a PDF for their doctor.

# Requirement ID: FR_hybrid_3
- Description: The system shall include a settings toggle to disable sharing device IDs with third-party analytics services.
- Source Persona: Privacy-Conscious Jake
- Traceability: H3
- Acceptance Criteria: When the analytics toggle is disabled, the application blocks all network requests to third-party tracking domains.
- Notes: "Ensure privacy" is too vague to test. I rewrote it to require a specific opt-out toggle in the settings menu.

# Requirement ID: FR_hybrid_4
- Description: The system shall display a 14-day mood trend chart without requiring a premium subscription.
- Source Persona: Privacy-Conscious Jake
- Traceability: H3
- Acceptance Criteria: When a free-tier user logs 14 days of data, a line chart of their entries is visible and not hidden by a paywall.
- Notes: Wrote this requirement to directly fix the complaint about the 14-day basic results being hidden behind a paywall.

# Requirement ID: FR_hybrid_5
- Description: The system shall trigger a modal with regional crisis hotline numbers if a user selects the Severe Depression tag.
- Source Persona: Crisis Tracker Sarah
- Traceability: H5
- Acceptance Criteria: Given the user selects Severe Depression, when they click save, a non-dismissible popup with emergency contacts is displayed.
- Notes: The AI suggested an "increase in self-awareness" which isn't testable. I replaced it with the critical safety feature (crisis hotline) needed for severe inputs.

# Requirement ID: FR_hybrid_6
- Description: The system shall provide a text field allowing users to attach alphanumeric notes up to 500 characters to a daily log.
- Source Persona: Clinical Patient Mia
- Traceability: H2
- Acceptance Criteria: During mood logging, the text field accepts user input and saves it to the database alongside the mood score.
- Notes: Scrapped the AI's hallucinated "community" feature and replaced it with a custom notes field for doctor visits, matching the actual reviews.

# Requirement ID: FR_hybrid_7
- Description: The system shall visually differentiate premium features using a 16x16px padlock icon on the free dashboard.
- Source Persona: Budget-Restricted Emily
- Traceability: H4
- Acceptance Criteria: All modules requiring a paid subscription must render the padlock icon in the upper right corner of their UI card.
- Notes: You can't write a software test for "value for money." I changed the requirement to adding visual padlocks on premium features instead.

# Requirement ID: FR_hybrid_8
- Description: The system shall limit full-screen promotional pop-ups for the therapy feature to a maximum of one occurrence per 7 days.
- Source Persona: Budget-Restricted Emily
- Traceability: H4
- Acceptance Criteria: If the user dismisses the therapy promotion, the app will block that specific promotional modal for the next 168 hours.
- Notes: Changed this from the AI's generic "basic insights" to a specific cooldown timer for the aggressive therapy popups.

# Requirement ID: FR_hybrid_9
- Description: The system shall provide clickable tooltips defining clinical terms used within the assessment questionnaires.
- Source Persona: Global User Alex
- Traceability: H1
- Acceptance Criteria: Clicking any underlined clinical term must open a modal displaying a plain-language definition.
- Notes: The AI made up a "personalized coaching" feature. I changed it to an interactive tooltip for clinical terms, which actually aids the users.

# Requirement ID: FR_hybrid_10
- Description: The system shall permit the user to complete a standard mood logging action requiring exactly 3 screen taps.
- Source Persona: Budget-Restricted Emily
- Traceability: H4
- Acceptance Criteria: From the home screen, clicking Log, clicking a mood, and clicking Save records the entry into the database.
- Notes: Swapped out the vague "fluid interface" fluff for a hard metric: logging a mood must take 3 taps or less.