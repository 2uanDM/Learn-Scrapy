from datetime import datetime

class SchemaTopic2():
    
    def ty_gia(self, date, dollar_index_dxy, usd_vcb, usd_nhnn, eur_vcb, eur_nhnn, cny_vcb, cny_nhnn) -> dict:
        '''
            Return a schema for "ty_gia" collection
        '''
        # Check valid params
        if not isinstance(date, datetime):
            raise ValueError('date must be a datetime object')
        if not isinstance(dollar_index_dxy, float):
            raise ValueError('dollar_index_dxy must be a float')
        if not isinstance(usd_vcb, float):
            raise ValueError('usd_vcb must be a float')
        if not isinstance(usd_nhnn, float):
            raise ValueError('usd_nhnn must be a float')
        if not isinstance(eur_vcb, float):
            raise ValueError('eur_vcb must be a float')
        if not isinstance(eur_nhnn, float):
            raise ValueError('eur_nhnn must be a float')
        if not isinstance(cny_vcb, float):
            raise ValueError('cny_vcb must be a float')
        if not isinstance(cny_nhnn, float):
            raise ValueError('cny_nhnn must be a float')
        
        return {
            'date': date,
            'data': {
                'dollar_index_dxy': dollar_index_dxy,
                'usd_vnd': {
                    'vcb_sell': usd_vcb,
                    'nhnn_sell':  usd_nhnn,
                },
                'eur_vnd': {
                    'vcb_sell': eur_vcb,
                    'nhnn_sell':  eur_nhnn,
                },
                'cny_vnd': {
                    'vcb_sell': cny_vcb,
                    'nhnn_sell':  cny_nhnn,
                }
            }
        }
    
    def chi_so_hang_hoa(self, date,
                        worldwide_gold_price_usd,
                        vn_gold_price_vnd,
                        ron95_price_vnd,
                        do_price_vnd,
                        brent_oil_price_usd,
                        raw_oil_price_usd,
                        vn_electric_price_vnd,
                        worldwide_steel_price_usd,
                        worldwide_copper_price_usd,
                        worldwide_aluminium_price_usd,
                        china_steel_price_cny,
                        china_copper_price_cny,
                        china_aluminium_price_cny,
                        vn_steel_price_vnd,
                        wall_tiles_price_vnd,
                        dji,
                        ssec,
                        nikkei,
                        kospi,
                        dax,
                        cac40,
                        ftse100) -> dict:
        
        # Ensure that the params are valid (all float)
        if not isinstance(date, datetime):
            raise ValueError('date must be a datetime object')
        if not isinstance(worldwide_gold_price_usd, float):
            raise ValueError('worldwide_gold_price_usd must be a float')
        if not isinstance(vn_gold_price_vnd, float):
            raise ValueError('vn_gold_price_vnd must be a float')
        if not isinstance(ron95_price_vnd, float):
            raise ValueError('ron95_price_vnd must be a float')
        if not isinstance(do_price_vnd, float):
            raise ValueError('do_price_vnd must be a float')
        if not isinstance(brent_oil_price_usd, float):
            raise ValueError('brent_oil_price_usd must be a float')
        if not isinstance(raw_oil_price_usd, float):
            raise ValueError('raw_oil_price_usd must be a float')
        if not isinstance(vn_electric_price_vnd, float):
            raise ValueError('vn_electric_price_vnd must be a float')
        if not isinstance(worldwide_steel_price_usd, float):
            raise ValueError('worldwide_steel_price_usd must be a float')
        if not isinstance(worldwide_copper_price_usd, float):
            raise ValueError('worldwide_copper_price_usd must be a float')  
        if not isinstance(worldwide_aluminium_price_usd, float):
            raise ValueError('worldwide_aluminium_price_usd must be a float')
        if not isinstance(china_steel_price_cny, float):
            raise ValueError('china_steel_price_cny must be a float')
        if not isinstance(china_copper_price_cny, float):
            raise ValueError('china_copper_price_cny must be a float')
        if not isinstance(china_aluminium_price_cny, float):
            raise ValueError('china_aluminium_price_cny must be a float')
        if not isinstance(vn_steel_price_vnd, float):
            raise ValueError('vn_steel_price_vnd must be a float')
        if not isinstance(wall_tiles_price_vnd, float):
            raise ValueError('wall_tiles_price_vnd must be a float')
        if not isinstance(dji, float):
            raise ValueError('dji must be a float')
        if not isinstance(ssec, float):
            raise ValueError('ssec must be a float')
        if not isinstance(nikkei, float):
            raise ValueError('nikkei must be a float')
        if not isinstance(kospi, float):
            raise ValueError('kospi must be a float')
        if not isinstance(dax, float):
            raise ValueError('dax must be a float')
        if not isinstance(cac40, float):
            raise ValueError('cac40 must be a float')
        if not isinstance(ftse100, float):
            raise ValueError('ftse100 must be a float')
        
        data = {
            'date': date,
            'data': {
                'worldwide_gold_price_usd': worldwide_gold_price_usd,
                'vn_gold_price_vnd': vn_gold_price_vnd,
                'ron95_price_vnd': ron95_price_vnd,
                'do_price_vnd': do_price_vnd,
                'brent_oil_price_usd': brent_oil_price_usd,
                'raw_oil_price_usd': raw_oil_price_usd,
                'vn_electric_price_vnd': vn_electric_price_vnd,
                'worldwide_steel_price_usd': worldwide_steel_price_usd,
                'worldwide_copper_price_usd': worldwide_copper_price_usd,
                'worldwide_aluminium_price_usd': worldwide_aluminium_price_usd,
                'china_steel_price_cny': china_steel_price_cny,
                'china_copper_price_cny': china_copper_price_cny,
                'china_aluminium_price_cny': china_aluminium_price_cny,
                'vn_steel_price_vnd': vn_steel_price_vnd,
                'vn_ciment_price_vnd': '',
                'wall_tiles_price_vnd': wall_tiles_price_vnd,
                'dji': dji,
                'ssec': ssec,
                'nikkei': nikkei,
                'kospi': kospi,
                'dax': dax,
                'cac40': cac40,
                'ftse100': ftse100
            }
        }
        
        return data
        
    def lai_suat_lnh(self, date, ls_quadem, ls_1tuan, ls_2tuan, ls_1thang, ls_3thang, ls_6thang, ls_9thang, ls_12thang,
                     ds_quadem, ds_1tuan, ds_2tuan, ds_1thang, ds_3thang, ds_6thang, ds_9thang, ds_12thang) -> dict: 
        
        # Ensure that the params are valid (all float)
        if not isinstance(date, datetime):
            raise ValueError('date must be a datetime object')
        if not isinstance(ls_quadem, float):
            raise ValueError('ls_quadem must be a float')
        if not isinstance(ls_1tuan, float):
            raise ValueError('ls_1tuan must be a float')
        if not isinstance(ls_2tuan, float):
            raise ValueError('ls_2tuan must be a float')
        if not isinstance(ls_1thang, float):
            raise ValueError('ls_1thang must be a float')
        if not isinstance(ls_3thang, float):
            raise ValueError('ls_3thang must be a float')
        if not isinstance(ls_6thang, float):
            raise ValueError('ls_6thang must be a float')
        if not isinstance(ls_9thang, float):
            raise ValueError('ls_9thang must be a float')
        if (not isinstance(ls_12thang, float)) and (ls_12thang is not None):
            raise ValueError('ls_12thang must be a float')
        
        # ----------------------------------------------------------------------    

        if not isinstance(ds_quadem, float):
            raise ValueError('ds_quadem must be a float')
        if not isinstance(ds_1tuan, float):
            raise ValueError('ds_1tuan must be a float')
        if not isinstance(ds_2tuan, float):
            raise ValueError('ds_2tuan must be a float')
        if not isinstance(ds_1thang, float):
            raise ValueError('ds_1thang must be a float')
        if not isinstance(ds_3thang, float):
            raise ValueError('ds_3thang must be a float')
        if not isinstance(ds_6thang, float):
            raise ValueError('ds_6thang must be a float')
        if not isinstance(ds_9thang, float):
            raise ValueError('ds_9thang must be a float')
        if (not isinstance(ds_12thang, float)) and (ds_12thang is not None):
            raise ValueError('ds_12thang must be a float')
        
        # Create the schema
        
        data = {
            'date': date,
            'data' : {
                'lai_suat': {
                    'quadem': ls_quadem,
                    '1tuan': ls_1tuan,
                    '2tuan': ls_2tuan,
                    '1thang': ls_1thang,
                    '3thang': ls_3thang,
                    '6thang': ls_6thang,
                    '9thang': ls_9thang,
                    '12thang': ls_12thang
                },
                'doanh_so': {
                    'quadem': ds_quadem,
                    '1tuan': ds_1tuan,
                    '2tuan': ds_2tuan,
                    '1thang': ds_1thang,
                    '3thang': ds_3thang,
                    '6thang': ds_6thang,
                    '9thang': ds_9thang,
                    '12thang': ds_12thang
                }
            }
        }
        
        return data

    def lai_suat_cafef(self, date, 
                       abbank, acb, bacabank, bidv, bvbank, viettinbank, eximbank, hdbank, kienlongbank, lienvietpostbank,
                       mbbank, msb, namabank, ncb, ocb, pgbank, saigonbank, shb, seabank, sacombank, techcombank, tpbank, vietabank,
                       vietbank, vietcombank, vib, vpbank, agribank) -> dict:

        # Ensure that the params are valid (all float)
        
        if not isinstance(date, datetime):
            raise ValueError('date must be a datetime object')
        if not isinstance(abbank, float):
            raise ValueError('abbank must be a float')
        if not isinstance(acb, float):
            raise ValueError('acb must be a float')
        if not isinstance(bacabank, float):
            raise ValueError('bacabank must be a float')
        if not isinstance(bidv, float):
            raise ValueError('bidv must be a float')
        if not isinstance(bvbank, float):
            raise ValueError('bvbank must be a float')
        if not isinstance(viettinbank, float):
            raise ValueError('viettinbank must be a float')
        if not isinstance(eximbank, float):
            raise ValueError('eximbank must be a float')
        if not isinstance(hdbank, float):
            raise ValueError('hdbank must be a float')
        if not isinstance(kienlongbank, float):
            raise ValueError('kienlongbank must be a float')
        if not isinstance(lienvietpostbank, float):
            raise ValueError('lienvietpostbank must be a float')
        if not isinstance(mbbank, float):
            raise ValueError('mbbank must be a float')
        if not isinstance(msb, float):
            raise ValueError('msb must be a float')
        if (not isinstance(namabank, float)) and namabank is not None:
            raise ValueError('namabank must be a float')
        if not isinstance(ncb, float):
            raise ValueError('ncb must be a float')
        if not isinstance(ocb, float):
            raise ValueError('ocb must be a float')
        if not isinstance(pgbank, float):
            raise ValueError('pgbank must be a float')
        if not isinstance(saigonbank, float):
            raise ValueError('saigonbank must be a float')
        if not isinstance(shb, float):
            raise ValueError('shb must be a float')
        if not isinstance(seabank, float):
            raise ValueError('seabank must be a float')
        if not isinstance(techcombank, float):
            raise ValueError('techcombank must be a float')
        if (not isinstance(tpbank, float)) and tpbank is not None:
            raise ValueError('tpbank must be a float')
        if not isinstance(vietabank, float):
            raise ValueError('vietabank must be a float')
        if not isinstance(vietbank, float):
            raise ValueError('vietbank must be a float')
        if not isinstance(vietcombank, float):
            raise ValueError('vietcombank must be a float')
        if not isinstance(vib, float):
            raise ValueError('vib must be a float')
        if not isinstance(vpbank, float):
            raise ValueError('vpbank must be a float')
        if not isinstance(agribank, float):
            raise ValueError('agribank must be a float')
        if not isinstance(sacombank, float):
            raise ValueError('sacombank must be a float')
        
        data = {
            'date' : date,
            'data' : {
                'abbank': abbank,
                'acb': acb,
                'bacabank': bacabank,
                'bidv': bidv,
                'bvbank': bvbank,
                'viettinbank': viettinbank,
                'eximbank': eximbank,
                'hdbank': hdbank,
                'kienlongbank': kienlongbank,
                'lienvietpostbank': lienvietpostbank,
                'mbbank': mbbank,
                'msb': msb,
                'namabank': namabank,
                'ncb': ncb,
                'ocb': ocb,
                'pgbank': pgbank,
                'saigonbank': saigonbank,
                'shb': shb,
                'seabank': seabank,
                'sacombank': sacombank,
                'techcombank': techcombank,
                'tpbank': tpbank,
                'vietabank': vietabank,
                'vietbank': vietbank,
                'vietcombank': vietcombank,
                'vib': vib,
                'vpbank': vpbank,
                'agribank': agribank
            }
        }
        
        return data 
    
    def tin_dung(self, date_created, month, year, tin_dung, cung_tien_m2, tang_truong_tin_dung, tang_truong_cung_tien_m2) -> dict:
        # Ensure that the params are valid (all float)
        if not isinstance(date_created, datetime):
            raise ValueError('date_created must be a datetime object')
        if ((not isinstance(month, int)) or (month < 1) or (month > 12)) and (month is not None):
            raise ValueError('month must be an integer from 1 to 12')
        if (not isinstance(year, int)) and (year is not None):
            raise ValueError('year must be an integer')
        if (not isinstance(tin_dung, float)) and (tin_dung is not None):
            raise ValueError('tin_dung must be a float')
        if (not isinstance(cung_tien_m2, float)) and (cung_tien_m2 is not None):
            raise ValueError('cung_tien_m2 must be a float')
        if (not isinstance(tang_truong_tin_dung, float)) and (tang_truong_tin_dung is not None):
            raise ValueError('tang_truong_tin_dung must be a float')
        if (not isinstance(tang_truong_cung_tien_m2, float)) and (tang_truong_cung_tien_m2 is not None):
            raise ValueError('tang_truong_cung_tien_m2 must be a float')

        data = {
            'date_created': date_created,
            'month': month,
            'year': year,
            'data': {
                'tin_dung' : tin_dung,
                'cung_tien_m2': cung_tien_m2,
                'tang_truong_tin_dung': tang_truong_tin_dung,
                'tang_truong_cung_tien_m2': tang_truong_cung_tien_m2
            }
        }
        
        return data
        
        