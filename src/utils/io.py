import csv

def flatten_dict(d: dict) -> list:
    '''
        For example d = {'a': 1, 'b': {'c': 2, 'd': 3}}
        
        then the output is [1, 2, 3]
    '''
    output = []
    
    for key in d.keys():
        if isinstance(d[key], dict):
            output.extend(flatten_dict(d[key]))
        else:
            output.append(d[key])
        
    return output

def write_csv(file_name: str, data, mode: str = 'a') -> None:
    '''
        data can be a dict or a list of dict
    '''
    
    if isinstance(data, dict):
        # Flatten dict and write to csv file
        with open(file_name, mode, newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(flatten_dict(data))
    elif isinstance(data, list):
        # Flatten dict and write to csv file
        with open(file_name, mode, newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for d in data:
                writer.writerow(flatten_dict(d))
    else:
        raise ValueError('Data must be a dict or a list of dict')

# if __name__ == '__main__':
#     data = {
#         'a': 1,
#         'b': {
#             'c': 2,
#             'd': 3
#         }
#     }
    
    
#     write_csv(r'C:\Users\Thinkbook 14 G3 ACL\Documents\GitHub\Kaxim-Stocks-Topic-2\results\exchange_rate.csv', data)
    