# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third part extension
#    Copyright (C) 2004-2014 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Report Forms',
    'version': '0.1',
    'author': 'Vertel AB',
    'category': 'base',
    'website': 'http://www.vertel.se',
    'summary': 'Use PDF-forms for advances layouted reports',
    'description': """
PDF-forms
==============


        
        <record model="ir.attachment" id="my_pdf">
            <field name="name">My PDF with form</field>
            <field name="datas_fname">my_pdf.pdf</field>
            <field name="res_model">ir.ui.view</field>
            <field name="type">url</field>
            <field name="url">/website/static/my_pdf.pdf</field>
        </record>
        <record id="applicant_attach3" model="ir.attachment">
            <field name="datas">UHJvZmlsZQ0KDQpOYW1lICAgICAgICAgIDpKb3NlDQpBZGRyZXNzICAgICAgIDo5MywgUHJlc3MgQXZlbnVlDQogICAgICAgICAgICAgICAgICAgOkxlIEJvdXJnZXQgZHUgTGFjLCA3MzM3NywNCiAgICAgICAgICAgICAgICAgICA6IEZyYW5jZSANClF1YWxpZmljYXRpb24gOk1DQQ0KRW1haWwgICAgICAgICAgIDpKb3NlQGdtYWlsLmNvbQ0KTW9iaWxlICAgICAgICAgIDo5OTY4NTEzNTg3</field>
            <field name="datas_fname">Jose_CV.txt</field>
            <field name="name">Jose_CV.txt</field>
            <field name="res_id" ref="hr_recruitment.hr_case_fresher0"/>
            <field name="res_model">hr.applicant</field>
        </record>
        
        <report 
            id="share_register.report_share_purchase_agreement"
            model="share.block"
            string="Share Purchase Agreement"
            report_type="pdf-form"
            name="share_register.share_purchase_agreement"
            file="share_register.share_purchase_agreement"
            attachment_use="True"
        />


pip install fdfgen
apt-get install pdftk


    """,
    'depends': ['report', ],
    'data': [
        ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
