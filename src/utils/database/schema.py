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
        
        