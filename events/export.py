from io import BytesIO
import xlsxwriter

from .models import Event, QuestionSet


def event_to_xlsx_buffer(event):
    # create a workbook in memory
    output = BytesIO()

    workbook = xlsxwriter.Workbook(output)

    worksheet2 = workbook.add_worksheet()
    fill_worksheet_with_signups(event, workbook, worksheet2)

    workbook.close()

    return output


def fill_worksheet_with_overview(event, workbook, worksheet):
    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', 'Veranstaltung', bold)


def fill_worksheet_with_signups(event, workbook, worksheet):
    x = 0
    y = 0
    for question_set in QuestionSet.objects.filter(event=event):
        for question in question_set.questions.all():
            worksheet.write(x, y, question.text)

            for signup in event.signup_set.all():
                AnswerClass = question.get_answer_field(question.type)

                answer = AnswerClass.objects.filter(question=question, signup=signup).first()
                x += 1
                worksheet.write(x, y, answer.get_serialized_value())

            x = 0
            y += 1





