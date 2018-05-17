# LV Signup Apps

This project is intended to be used by the BdP LV Bayern e.V. to handle signups of their events.
It has django backend with a React front end loosely coupled through the django rest framework.

## Dependencies

 - sudo apt-get install xvfb libfontconfig wkhtmltopdf

## Example process
1. Create a new event
   1. Signup corridor
   2. Name, start time, end time and description of event
2. Create or choose question
   1. Choose from old questions (has the advantage of auto completed values for the user)
    2. Create new question: text, type, choices and required
3. Send a permanent link to the future participants
4. Participants signs up without logging in
5. Success page with note about obligatory Consent PDF
5. Confirmation of signup per E-Mail with Consent PDF (in first step withouth login token)
6. Staff for the event can login and download signups in Excel sheet



## API
- GET /api/question_set
- GET /api/question_set/?q=
- GET /api/question_set/<pk:pk>
- POST /api/event/new um Staff und postalische Adresse ergänzen
- GET /api/event/<pk:pk>
- GET /api/event/<pk:pk>/signup „Mit vorausgefüllten Antworten“ um E-Mail und AGB erweitern
- POST /api/event/<pk:pk>/signup „Anmelden“ um E-Mail und AGB erweitern
- POST /api/login
- POST /api/logout
- GET /api/staff
- GET /api/staff_event/
- GET /api/staff_event/<pk:pk> „Dashboard“
- POST /api/staff_event/<pk:pk>/send_postal_confirmation_mail/<person_pk:pk>
- POST /api/staff_event/<pk:pk>
- GET /api/staff_event/<pk:pk>/submissions?format=xlsx
- GET /api/staff_event/<pk:pk>/consent_pdf/<person_pk:pk>


## To be implemented
- Readthedocs + Api documentation setup: CHRISTOPH
- Dockerfile: CHRISTOPH
- E-Mailing, Consent PDF and Excel: DANIEL
- Survey creation API: DANIEL
- Staff API: CHRISTOPH
- Vue.JS setup: CHRISTOPH
- User UI: DANIEL
- Staff UI: CHRISTOPH
- Write tests: DANIEL



## Longlist
- File-Upload
- User login
- Edit survey question (add, remove, edit) after publishing
- Login bruteforce checken
- Monitoring
- Backup der Datenbank
- Automatic tests on travis/appveyor
- Sequential events
- Filling surveys in parallel
- Ende.-zu-Ende automatisch
- Add question to published survey
- Remove question from survey
- Duplicate rows shall be possible
- Script-Injection
- Staff list testen (add, remove, empty)



