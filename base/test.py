# -*- coding: utf-8 -*
if __name__ == '__main__':
	# readPath = sys.argv[1]
	# whitePath = sys.argv[2]
	data='uni_order_id,data_from,partner,plat_code,order_id,uni_shop_id,uni_id,guide_id,shop_id,plat_account,total_fee,item_discount_fee,trade_discount_fee,adjust_fee,post_fee,discount_rate,payment_no_postfee,payment,pay_time,product_num,order_status,is_refund,refund_fee,insert_time,created,endtime,modified,trade_type,receiver_name,receiver_country,receiver_state,receiver_city,receiver_district,receiver_town,receiver_address,receiver_mobile,trade_source,delivery_type,consign_time,orders_num,is_presale,presale_status,first_fee_paytime,last_fee_paytime,first_paid_fee,tenant,tidb_modified,step_paid_fee,seller_flag'
	datalist = data.split(',')
	for unit in datalist:
		print("'"+unit+"',"+unit+",")