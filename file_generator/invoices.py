import datetime

from docxtpl import DocxTemplate
import os

template_path = 'file_generator/templates/single-load-invoice.docx'
doc_name = 'Invoice#{}.docx'
save_path = 'files/loads/invoices/{}'


def convert(origin):
    command2 = 'lowriter --convert-to pdf {}'.format(origin)
    os.chdir('files/loads/invoices')
    os.system(command2)
    return

def generate_invoice(to_be_invoiced, carrier):
    doc = DocxTemplate(template_path)
    from app.models.load import Load
    from django.db.models import QuerySet
    if isinstance(to_be_invoiced, Load):
        to_be_invoiced = [to_be_invoiced]
        invoice_number = to_be_invoiced.id
    elif isinstance(to_be_invoiced, QuerySet):
        invoice_number = str(hash((load.id for load in to_be_invoiced)))
    else:
        raise TypeError('Given argument \'to_be_invoiced\' must be Load or QuerySet instance')
    context = {
        'carrier_name': carrier.name,
        'carrier_address': carrier.address,
        'broker_name': to_be_invoiced.first().broker_company.name,
        'broker_address': to_be_invoiced.first().broker_company.address,
        'invoice_number': invoice_number,
        'date': datetime.datetime.now(),
        'details': []
    }
    for load in to_be_invoiced:
        context['details'].append({'description': load.order_number,
                                   'rate': load.rate,
                                   'accss': load.get_accessorial_total(),
                                   'total': load.total})
    print(context)
    doc.render(context)
    doc.save(save_path.format(doc_name.format(context['invoice_number'])))
    convert(doc_name.format(context['invoice_number']))
