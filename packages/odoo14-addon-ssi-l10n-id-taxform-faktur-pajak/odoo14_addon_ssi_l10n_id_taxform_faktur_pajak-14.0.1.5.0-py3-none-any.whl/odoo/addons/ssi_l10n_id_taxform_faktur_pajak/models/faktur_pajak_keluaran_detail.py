# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FakturPajakKeluaranDetail(models.Model):
    _name = "faktur_pajak_keluaran_detail"
    _description = "Detail Faktur Pajak Keluaran"
    _inherit = ["mixin.product_line_account"]

    faktur_pajak_keluaran_id = fields.Many2one(
        comodel_name="faktur_pajak_keluaran",
        string="# Faktur Pajak Keluaran",
        required=True,
        ondelete="cascade",
    )
