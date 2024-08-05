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

	analytic_account_id = fields.Many2one(related='picking_id.analytic_account_id', string="Compte Analytique", store=True, readonly=False)
	unit_cost = fields.Float(string="Coût Unitaire", compute="_compute_unit_cost", store=True)


	@api.depends('product_id')
	def _compute_unit_cost(self):
		for rec in self:
			rec.unit_cost = rec.product_id.standard_price
	
	def _action_cancel(self):
		res  = super(StockMove, self)._action_cancel()
		analytics = self.env["account.analytic.line"].sudo().search([('stock_move_id', 'in', self.ids)])
		if analytics:
			analytics.unlink()
		return res


class StockMoveLine(models.Model):
	_inherit = "stock.move.line"

	analytic_account_id = fields.Many2one(related='move_id.analytic_account_id', string="Compte Analytique",store=True)
	unit_cost = fields.Float(related='move_id.unit_cost', string="Coût Unitaire", store=True)

	def _prepare_analytic_vals(self, picking_id=False):
		if not picking_id:
			picking_id = self.picking_id
		records = [rec for rec in [self.product_id.product_tmpl_id.name, picking_id.name] if rec]
		name = "-".join(records)
		return {
			'name': name,
			'ref':picking_id.name,
			'product_id': self.product_id.id,
			'partner_id':picking_id.partner_id.id,
			'account_id': self.analytic_account_id.id,
			'amount': -self.unit_cost,
			'date': fields.Date.today(),
			'unit_amount': self.qty_done,
			'stock_move_id': self.move_id.id
		}
	
	def _create_update_analytic_records(self):
		analytics = self.env["account.analytic.line"].sudo()
		
		for line in self:
			if line.analytic_account_id.id:
				val = line._prepare_analytic_vals(picking_id=self.picking_id)
				existing_ = line._check_if_exit_analytic()
				if existing_:
					existing_.write(val)
				else:
					analytics.create(val)
		return True

	def write(self, vals):
		res = super(StockMoveLine, self).write(vals)
		if 'qty_done' in vals or vals.get('state', False) == 'done':
			self._create_update_analytic_records()
		return res
	def _check_if_exit_analytic(self):
		analytics = self.env["account.analytic.line"].sudo()
		account_id = analytics.search([('stock_move_id', '=', self.move_id.id)])
		return account_id

class AccountAnalyticLine(models.Model):
	_inherit = "account.analytic.line"

	stock_move_id = fields.Many2one("stock.move", string="Mouvement de stock")
