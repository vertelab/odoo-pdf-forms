# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party extension
#    Copyright (C) 2004-2015 Vertel AB (<http://vertel.se>).
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

from fdfgen import forge_fdf


from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

import logging
_logger = logging.getLogger(__name__)
    
class report_forms(models.Model):
    _inherit = "report"

    @api.multi
    def render_html(self, data=None):
        _logger.info("Reporting Block")
        report = self.env['report']._get_report_from_name('share_register.blocks_report_standard')
        for company in self.env['res.company'].browse(self._ids):
            blocks = self.env['share.block'].search([('company_id','=',company.id)])

        return self.env['report'].render('share_register.blocks_report_standard', {
                    'report': report,
                    'doc_ids': self._ids,
                    'doc_model': report.model,
                    'docs': self.env['res.company'].browse(self._ids),
                })

    def create_form(self,fields):
        #fields = [('name','John Smith'),('telephone','555-1234')]
        return forge_fdf("",fields,[],[],[])

    def form_render(self,pdf_file,fields):
        
        
    @api.one
    def get_pdf(self,report_name, html=None, data=None, context=None):
        """This method generates and returns pdf version of a report.
        """
       
        # Get the ir.actions.report.xml record we are working on.
        report = self._get_report_from_name(cr, uid, report_name)
        # Check if we have to save the report or if we have to get one from the db.
        save_in_attachment = self._check_attachment_use(cr, uid, ids, report)
        # Get the paperformat associated to the report, otherwise fallback on the company one.

        # Preparing the minimal html pages
        css = ''  # Will contain local css
        headerhtml = []
        contenthtml = []
        footerhtml = []
        irconfig_obj = self.pool['ir.config_parameter']
        base_url = irconfig_obj.get_param(cr, SUPERUSER_ID, 'report.url') or irconfig_obj.get_param(cr, SUPERUSER_ID, 'web.base.url')

        # Minimal page renderer
        view_obj = self.pool['ir.ui.view']
        render_minimal = partial(view_obj.render, cr, uid, 'report.minimal_layout', context=context)

        # The received html report must be simplified. We convert it in a xml tree
        # in order to extract headers, bodies and footers.
        try:
            root = lxml.html.fromstring(html)
            match_klass = "//div[contains(concat(' ', normalize-space(@class), ' '), ' {} ')]"

            for node in root.xpath("//html/head/style"):
                css += node.text

            for node in root.xpath(match_klass.format('header')):
                body = lxml.html.tostring(node)
                header = render_minimal(dict(css=css, subst=True, body=body, base_url=base_url))
                headerhtml.append(header)

            for node in root.xpath(match_klass.format('footer')):
                body = lxml.html.tostring(node)
                footer = render_minimal(dict(css=css, subst=True, body=body, base_url=base_url))
                footerhtml.append(footer)

            for node in root.xpath(match_klass.format('page')):
                # Previously, we marked some reports to be saved in attachment via their ids, so we
                # must set a relation between report ids and report's content. We use the QWeb
                # branding in order to do so: searching after a node having a data-oe-model
                # attribute with the value of the current report model and read its oe-id attribute
                if ids and len(ids) == 1:
                    reportid = ids[0]
                else:
                    oemodelnode = node.find(".//*[@data-oe-model='%s']" % report.model)
                    if oemodelnode is not None:
                        reportid = oemodelnode.get('data-oe-id')
                        if reportid:
                            reportid = int(reportid)
                    else:
                        reportid = False

                # Extract the body
                body = lxml.html.tostring(node)
                reportcontent = render_minimal(dict(css=css, subst=False, body=body, base_url=base_url))

                contenthtml.append(tuple([reportid, reportcontent]))

        except lxml.etree.XMLSyntaxError:
            contenthtml = []
            contenthtml.append(html)
            save_in_attachment = {}  # Don't save this potentially malformed document

        # Get paperformat arguments set in the root html tag. They are prioritized over
        # paperformat-record arguments.
        specific_paperformat_args = {}
        for attribute in root.items():
            if attribute[0].startswith('data-report-'):
                specific_paperformat_args[attribute[0]] = attribute[1]

        # Run wkhtmltopdf process
        return self._run_wkhtmltopdf(
            cr, uid, headerhtml, footerhtml, contenthtml, context.get('landscape'),
            paperformat, specific_paperformat_args, save_in_attachment
        )
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
