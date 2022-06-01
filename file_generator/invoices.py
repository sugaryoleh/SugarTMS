import datetime

from docxtpl import DocxTemplate
import os

template_path = 'file_generator/templates/load-invoice.docx'
doc_name = 'Invoice#{}'
save_path = 'files/loads/invoices'
docx = '.docx'
pdf = '.pdf'


def convert_docx_to_pdf(origin):
    command = 'lowriter --convert-to pdf {}'.format(origin)
    os.chdir(save_path)
    os.system(command)

    return


def delete_file(path):
    os.system('rm {}'.format(path))


def get_description(load):
    from app.models.load.load import Load

    first_pu_address = Load.LoadManager.get_first_pu_stage(load).facility.address
    first_pu_address = '{}, {}'.format(first_pu_address.city, first_pu_address.state.code)
    last_del_address = Load.LoadManager.get_last_del_stage(load).facility.address
    last_del_address = '{}, {}'.format(last_del_address.city, last_del_address.state.code)
    return '{} - {}'.format(first_pu_address, last_del_address)


def get_details(to_be_invoiced):
    details = []
    from app.models.load.load import Load
    if isinstance(to_be_invoiced, Load):
        to_be_invoiced = [to_be_invoiced]
    for load in to_be_invoiced:
        details.append({'description': get_description(load),
                        'rate': load.rate,
                        'accss': load.get_accessorial_total(),
                        'total': load.total})
    return details


def generate_invoice(load, carrier):
    from app.models.load.load import Load

    if not isinstance(load, Load):
        raise TypeError('Given argument \'load\' must be Load instance')
    doc = DocxTemplate(template_path)

    context = {
        'carrier_name': carrier.name,
        'carrier_address': carrier.address,
        'broker_name': load.broker_company.name,
        'broker_address': load.broker_company.address,
        'invoice_number': load.id,
        'date': datetime.datetime.now(),
        'details': get_details(load)
    }
    doc.render(context)
    temp_path = save_path + '/{}'.format(doc_name.format(context['invoice_number']))+docx
    doc.save(temp_path)
    file_name = doc_name.format(context['invoice_number'])
    convert_docx_to_pdf(file_name+docx)
    delete_file(file_name+docx)
    return file_name+pdf


# def generate_invoice(to_be_invoiced, carrier, broker):
#     doc = DocxTemplate(template_path)
#     from location.models.load import Load
#     from django.db.models import QuerySet
#     if isinstance(to_be_invoiced, Load):
#         invoice_number = to_be_invoiced.id
#         to_be_invoiced = [to_be_invoiced]
#     elif isinstance(to_be_invoiced, QuerySet):
#         invoice_number = str(hash((load.id for load in to_be_invoiced)))
#     else:
#         raise TypeError('Given argument \'to_be_invoiced\' must be Load or QuerySet instance')
#     context = {
#         'carrier_name': carrier.name,
#         'carrier_address': carrier.address,
#         'broker_name': to_be_invoiced.first().broker_company.name,
#         'broker_address': to_be_invoiced.first().broker_company.address,
#         'invoice_number': invoice_number,
#         'date': datetime.datetime.now(),
#         'details': []
#     }
#     for load in to_be_invoiced:
#         first_pu_address = Load.LoadManager.get_first_pu_stage(load).facility.address
#         first_pu_address = '{}, {}'.format(first_pu_address.city, first_pu_address.state.code)
#         last_del_address = Load.LoadManager.get_last_del_stage(load).facility.address
#         last_del_address = '{}, {}'.format(last_del_address.city, last_del_address.state.code)
#         context['details'].append({'description': '{} - {}'.format(first_pu_address, last_del_address),
#                                    'rate': load.rate,
#                                    'accss': load.get_accessorial_total(),
#                                    'total': load.total})
#     doc.render(context)
#     temp_path = save_path + '/{}'.format(doc_name.format(context['invoice_number']))
#     doc.save(temp_path)
#     convert_docx_to_pdf(doc_name.format(context['invoice_number']))
#     delete_file(temp_path)
