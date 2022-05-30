# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError

class AccountJournal(models.Model):
    _inherit = "account.journal"

    lock_date= fields.Date(string="Lock Date")

class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        if self.type == "out_invoice" and not self.env.user.has_group('button.group_student'):
            raise UserError("NO Rights to Access")
        return self.new_action_post()

    def new_action_post(self):
        res = super(AccountMove, self).action_post()
        for x in self.filtered(lambda x: x.state == 'posted'):
            y = x.journal_id.lock_date
            if x.date <= y:
                raise UserError("Out of Date")
        return res
