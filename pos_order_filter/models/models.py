# -*- coding: utf-8 -*-
from odoo import models, fields,tools, api, _
import logging
_logger = logging.getLogger(__name__)

class PosOrderLine(models.Model):
	_inherit = 'pos.order.line'


	order_count = fields.Integer('Master Counter',compute='_compute_count_order',store=True)

	@api.multi
	@api.depends('order_id', 'product_id','price_subtotal','name')
	def _compute_count_order(self):		
		count=0
		check = False
		new_order_id = None
		for line in self:
			order_id = line.order_id		
			_logger.warning('Line----------- %s',  line)
			if order_id != new_order_id: 
				_logger.warning('OrderID----------- %s',  order_id)
				line.order_count = 1 
				new_order_id = line.order_id		                                        					
				count = count+1
				_logger.warning('count----------- %s',  count)
		return True
	
	
class PosOrderReport(models.Model):
    _inherit = "report.pos.order"

    no_of_orders = fields.Integer(string='No Of Orders')
#    avg_order_price = fields.Float(string='Avg Order Price', readonly=True, group_operator="avg")
    
    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_pos_order')
        self._cr.execute("""
            CREATE OR REPLACE VIEW report_pos_order AS (
                SELECT
                    MIN(l.id) AS id,
                    COUNT(*) AS nbr_lines,
                    SUM(l.order_count) AS no_of_orders,
                    s.date_order AS date,
                    SUM(l.qty * u.factor) AS product_qty,
                    SUM(l.qty * l.price_unit) AS price_sub_total,
                    SUM((l.qty * l.price_unit) * (100 - l.discount) / 100) AS price_total,
                    SUM((l.qty * l.price_unit) * (l.discount / 100)) AS total_discount,
                    (SUM(l.qty*l.price_unit)/SUM(l.qty * u.factor))::decimal AS average_price,
                    SUM(cast(to_char(date_trunc('day',s.date_order) - date_trunc('day',s.create_date),'DD') AS INT)) AS delay_validation,
                    s.id as order_id,
                    s.partner_id AS partner_id,
                    s.state AS state,
                    s.user_id AS user_id,
                    s.location_id AS location_id,
                    s.company_id AS company_id,
                    s.sale_journal AS journal_id,
                    l.product_id AS product_id,
                    pt.categ_id AS product_categ_id,
                    p.product_tmpl_id,
                    ps.config_id,
                    pt.pos_categ_id,
                    pc.stock_location_id,
                    s.pricelist_id,
                    s.session_id,
                    s.invoice_id IS NOT NULL AS invoiced
                FROM pos_order_line AS l
                    LEFT JOIN pos_order s ON (s.id=l.order_id)
                    LEFT JOIN product_product p ON (l.product_id=p.id)
                    LEFT JOIN product_template pt ON (p.product_tmpl_id=pt.id)
                    LEFT JOIN product_uom u ON (u.id=pt.uom_id)
                    LEFT JOIN pos_session ps ON (s.session_id=ps.id)
                    LEFT JOIN pos_config pc ON (ps.config_id=pc.id)
                GROUP BY
                    s.id, s.date_order, s.partner_id,s.date_order,s.state, pt.categ_id,
                    s.user_id, s.location_id, s.company_id, s.sale_journal,
                    s.pricelist_id, s.invoice_id, s.create_date, s.session_id,
                    l.product_id,
                    pt.categ_id, pt.pos_categ_id,
                    p.product_tmpl_id,
                    ps.config_id,
                    pc.stock_location_id
                HAVING
                    SUM(l.qty * u.factor) != 0
            )
        """)       
        
