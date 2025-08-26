from odoo import models, fields, api

class AccountCategory(models.Model):
    _name = 'account.category'
    _description = 'Category'
    name = fields.Char(string="Category Name", required=True)
    code = fields.Char(string="Category Code", required=True)


class AccountObjectClass(models.Model):
    _name = 'account.object.class'
    _description = 'Object Class'
    name = fields.Char(string="Object Class Name", required=True)
    class_id = fields.Char(string="Class ID", required=True)  # Unique ID for the class (e.g., 00, 01, etc.)
    category_id = fields.Many2one('account.category', string="Category", required=True)


class ObjectHead(models.Model):
    _name = 'account.object.head'
    _description = 'Object Head Data'
    name = fields.Char(string='Object Head', required=True)
    object_class_id = fields.Many2one('account.object.class', string="Object Class", required=True)
    description = fields.Text(string="Description")



class AccountFormModel(models.Model):
    _name = 'account.form'
    _description = 'Chart Form'
    _rec_name = 'name'
    category_id = fields.Many2one('account.category', string="Category", required=True)
    object_class_id = fields.Many2one(
        'account.object.class',
        string="Object Class",
        domain="[('category_id', '=', category_id)]",
        required=True
    )
    object_head_id = fields.Many2one(
        'account.object.head',
        string="Object Head",
        domain="[('object_class_id', '=', object_class_id)]",
        required=True
    )
    description = fields.Text(string="Description")
    name = fields.Char(string="Name", compute="_compute_name", store=True)
    object_head_code = fields.Char(string="Object Head Code", readonly=True)


    @api.onchange('object_head_id')
    def onchange_object_head(self):

        if self.object_head_id:
            self.description = self.object_head_id.description
        else:
            self.description = False

    @api.depends('object_head_id')
    def _compute_name(self):
        """Compute the name based on the Object head."""
        for record in self:
            record.name = record.object_head_id.name

    @api.onchange('category_id')
    def onchange_category_id(self):
        """Reset object_class_id when category changes."""
        self.object_class_id = False

    @api.model
    def create(self, vals):
        """Generate a unique object head code during record creation."""
        if vals.get('category_id') and vals.get('object_class_id'):
            category = self.env['account.category'].browse(vals['category_id'])
            object_class = self.env['account.object.class'].browse(vals['object_class_id'])

            sequence_count = self.search_count([
                ('category_id', '=', vals['category_id']),
                ('object_class_id', '=', vals['object_class_id'])
            ]) + 1
            # Format the sequence number with leading zeros (e.g., 001, 002, etc.)
            sequence_str = f"{sequence_count:03d}"
            vals['object_head_code'] = f"{category.code}{object_class.class_id}{sequence_str}"

        return super(AccountFormModel, self).create(vals)
