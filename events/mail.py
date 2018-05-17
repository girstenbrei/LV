from django.core.mail import EmailMessage

from events.pdf import generate_pdf_application_document


def send_signup_mail(signup):

    subject = "Anmelden für {}".format(signup.event.name)
    text = """
Liebe(r) {},

im Anhang findest du die von dir ausgefüllt digitale Anmeldung.
Bitte drucke sie aus, unterschreibe sie oder wenn du minderjährig bist, dann lass sie dir vom Vormund unterschreiben, 
und schicke sie per Post an die angegebene Adresse.

Du wirst eine Bestätigungsemail erhalten, sobald dein Brief bei der Adresse eingegangen ist.

Gut Pfad
Christoph Girstenbrei und Daniel Pollithy
    """.format(signup.email)

    document = generate_pdf_application_document(signup)

    mail = EmailMessage(subject=subject,
                        body=text,
                        from_email='anmeldungen@action-online.de',
                        to=[signup.email])
    mail.attach(content=document, mimetype='application/pdf')
    mail.send()
