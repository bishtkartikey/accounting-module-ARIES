from odoo import models, fields, api


class BankAttributeOptions(models.Model):
    _name = 'bank.attribute.options'
    _description = 'Bank Attribute Options'

    name = fields.Char(string='Option Name', required=True)
    code = fields.Char(string='Option Code', required=True)
    attribute_type = fields.Selection([
        ('bank_type', 'Bank Type'),
        ('account_type', 'Account Type'),
        ('cheque_status', 'Cheque Status'),
    ], string='Attribute Type', required=True)



class BankDetails(models.Model):
    _name = 'bank.details'
    _description = 'Bank Details'
    _order = 'name, branch_name'

    # Basic Fields
    name = fields.Char(string='Bank Name', required=True)
    branch_name = fields.Char(string='Branch Name', required=True)
    branch_code = fields.Char(string='Branch Code', required=True)
    ifsc_code = fields.Char(string='IFSC Code', required=True)

    # Dynamic Bank Type Selection
    @api.model
    def _get_bank_types(self):
        options = self.env['bank.attribute.options'].search([('attribute_type', '=', 'bank_type')])
        return [(opt.code, opt.name) for opt in options] + [('other', 'Other')]

    bank_type = fields.Selection(
        selection='_get_bank_types',
        string='Bank Type'
    )

    # Contact Information
    address = fields.Text(string='Address')
    city = fields.Char(string='City')
    state = fields.Char(string='State')
    country = fields.Char(string='Country', default='India')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')

    # Relations
    bank_accounts = fields.One2many('bank.account', 'bank_id', string='Accounts')
    active = fields.Boolean(default=True)

    def name_get(self):
        result = []
        for rec in self:
            name = f"{rec.name} ({rec.branch_name})"
            result.append((rec.id, name))
        return result


class BankAccount(models.Model):
    _name = 'bank.account'
    _description = 'Bank Account'
    _order = 'account_number'
    _rec_name = 'bank_id'

    # Reference Fields
    bank_id = fields.Many2one('bank.details', string='Bank', required=True)
    object_head_id = fields.Many2one('account.form', string='Object Head', required=True)
    related_object_head_id = fields.Many2one(
        'account.object.head',
        related='object_head_id.object_head_id',
        string='Linked Object Head',
        store=True
    )

    # Account Information
    account_number = fields.Char(string='Account Number', required=True)
    micr_code = fields.Char(string='MICR Code')
    account_holder = fields.Char(string='Account Holder', required=True)

    # Dynamic Selection Fields
    @api.model
    def _get_account_numbers(self):
        accounts = self.search([])
        return [(acc.account_number, f"{acc.account_number} - {acc.account_holder}") for acc in accounts]

    account_number_selection = fields.Selection(
        selection='_get_account_numbers',
        string='Select Account',
        help="Select from existing accounts"
    )

    @api.model
    def _get_micr_codes(self):
        accounts = self.search([('micr_code', '!=', False)])
        return [(acc.micr_code, f"{acc.micr_code} ({acc.account_holder})") for acc in accounts]

    micr_code_selection = fields.Selection(
        selection='_get_micr_codes',
        string='Select MICR Code',
        help="Select from existing MICR codes"
    )

    @api.model
    def _get_account_holders(self):
        accounts = self.search([])
        return [(acc.account_holder, acc.account_holder) for acc in accounts]

    account_holder_selection = fields.Selection(
        selection='_get_account_holders',
        string='Select Account Holder',
        help="Select from existing account holders"
    )

    # Dynamic Object Head Selection
    @api.model
    def _get_object_heads(self):
        heads = self.env['account.form'].search([])
        return [(head.id, head.name) for head in heads]

    object_head_selection = fields.Selection(
        selection='_get_object_heads',
        string='Select Object Head',
        help="Select from chart of accounts"
    )

    # Account Type

    account_type = fields.Selection([
        ('sb', 'Savings Bank'),
        ('ca', 'Current Account')
    ], string='Account Type', required=True)

    cheques = fields.One2many('cheque.master', 'bank_account_id', string='Cheques')

    # Status
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('dormant', 'Dormant')
    ], string='Status', default='active')

    # Onchange Methods
    # @api.onchange('account_number_selection')
    # def _onchange_account_number_selection(self):
    #     if self.account_number_selection:
    #         account = self.search([('account_number', '=', self.account_number_selection)], limit=1)
    #         if account:
    #             self.update({
    #                 'account_number': account.account_number,
    #                 'account_holder': account.account_holder,
    #                 'micr_code': account.micr_code,
    #                 'bank_id': account.bank_id.id,
    #                 'object_head_id': account.object_head_id.id
    #             })

    # @api.onchange('object_head_selection')
    # def _onchange_object_head_selection(self):
    #     if self.object_head_selection:
    #         self.object_head_id = int(self.object_head_selection)

    # @api.onchange('micr_code_selection')
    # def _onchange_micr_code_selection(self):
    #     if self.micr_code_selection:
    #         account = self.search([('micr_code', '=', self.micr_code_selection)], limit=1)
    #         if account:
    #             self.update({
    #                 'account_number': account.account_number,
    #                 'account_holder': account.account_holder,
    #                 'micr_code': account.micr_code,
    #                 'bank_id': account.bank_id.id,
    #                 'object_head_id': account.object_head_id.id
    #             })

    # @api.onchange('account_holder_selection')
    # def _onchange_account_holder_selection(self):
    #     if self.account_holder_selection:
    #         accounts = self.search([('account_holder', '=', self.account_holder_selection)])
    #         if len(accounts) == 1:
    #             self.update({
    #                 'account_number': accounts.account_number,
    #                 'account_holder': accounts.account_holder,
    #                 'micr_code': accounts.micr_code,
    #                 'bank_id': accounts.bank_id.id,
    #                 'object_head_id': accounts.object_head_id.id
    #             })

    def name_get(self):
        result = []
        for record in self:
            # Safe check: make sure bank_id is set
            bank_name = record.bank_id.name if record.bank_id else "No Bank"
            display_name = f"{record.account_holder} - {bank_name}"
            result.append((record.id, display_name))
        return result


class ChequeMaster(models.Model):
    _name = 'cheque.master'
    _description = 'Cheque Management'
    _order = 'cheque_number'

    # Reference Fields
    bank_account_id = fields.Many2one('bank.account', string='Bank Account', required=True)

    # Cheque Information
    cheque_number = fields.Char(string='Cheque Number', required=True)
    amount = fields.Float(string='Amount', required=True)
    date_issued = fields.Date(string='Issue Date', default=fields.Date.today)
    beneficiary = fields.Char(string='Beneficiary Name')

    # Dynamic Status Selection
    @api.model
    def _get_cheque_statuses(self):
        options = self.env['bank.attribute.options'].search([('attribute_type', '=', 'cheque_status')])
        return [(opt.code, opt.name) for opt in options]

    status = fields.Selection(
        selection='_get_cheque_statuses',
        string='Status',
        default='issued'
    )
    remarks = fields.Text(string='Remarks')
    # Related Fields
    bank_id = fields.Many2one(related='bank_account_id.bank_id', string='Bank', store=True)
    account_holder = fields.Char(related='bank_account_id.account_holder', string='Account Holder', store=True)
    object_head_id = fields.Many2one(related='bank_account_id.object_head_id', string='Object Head', store=True)

    def name_get(self):
        result = []
        for rec in self:
            name = f"{rec.cheque_number} - {rec.bank_account_id.account_number}"
            result.append((rec.id, name))
        return result