# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockPicking(models.Model):
	_inherit = "stock.picking"

	analytic_account_id = fields.Many2one(comodel_name="account.analytic.account", string="Compte Analytique")

	@api.onchange("analytic_account_id")
	def change_analytic_account(self):
		for rec in self:
			rec.move_ids_without_package.analytic_account_id = rec.analytic_account_id

class StockMove(models.Model):
	_inherit = "stock.move"

	analytic_account_id = fields.Many2one(comodel_name="account.analytic.account", string="Compte Analytique")
	unit_cost = fields.Float(string="Coût Unitaire")