from datetime import datetime

class OrderedList:
    def __init__(self,list_of_values) -> None:
        self._data = self._basic_method(list_of_values=list_of_values)
    
    def __repr__(self) -> str:
        return self.tail()
    
    def _basic_method(self,list_of_values):
        mod_func = lambda date_string: datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)
        nd = {'datetime':[],'open':[],'high':[],'low':[],'close':[],'volume':[],'oi':[]}
        for row in list_of_values:
            nd['datetime'].append(mod_func(row[0]))
            nd['open'].append(row[1])
            nd['high'].append(row[2])
            nd['low'].append(row[3])
            nd['close'].append(row[4])
            nd['volume'].append(row[5])
            nd['oi'].append(row[6])
        return nd
    
    def print_dict_as_table(self,data):
        max_lengths = [max(len(str(value)) for value in col) for col in data.values()]
        header_row = "|".join(header.center(length) for header, length in zip(data.keys(), max_lengths))
        print(header_row)
        separator = "+".join("-" * length for length in max_lengths)
        print(separator)
        for i in range(len(next(iter(data.values())))):
            row_values = [str(data[key][i]).center(length) for key, length in zip(data.keys(), max_lengths)]
            row = "|".join(row_values)
            print(row)

    def head(self, val=5):
        data_head = {key: value[:val] for key, value in self._data.items()}
        self.print_dict_as_table(data_head)
    
    def iloc(self,start, end):
        data_head = {key: value[start:end] for key, value in self._data.items()}
        self.print_dict_as_table(data_head)
    
    def tail(self, val=5):
        data_head = {key: value[-val:] for key, value in self._data.items()}
        self.print_dict_as_table(data_head)