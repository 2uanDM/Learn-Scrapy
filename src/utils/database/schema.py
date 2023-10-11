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
    
    def chi_so_hang_hoa(self) -> dict:
        pass