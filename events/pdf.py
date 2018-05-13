import pdfkit
from django.template.loader import render_to_string


def generate_pdf_application_document(signup):
    context = {'signup': signup,
               'question_sets': signup.event.question_sets.all(),
               'questions': [qs.questions.all() for qs in signup.event.question_sets.all()],
               'answers': [[signup.answer_set.get(question=q).get_child_class() for q in qs.questions.all()]
                           for qs in signup.event.question_sets.all()]
               }

    html = render_to_string('mails/standard_application.html', context)

    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None
    }

    # https://github.com/JazzCore/python-pdfkit
    # Use False instead of output path to save pdf to a variable
    pdf = pdfkit.from_string(html, False, options=options)

    return pdf
