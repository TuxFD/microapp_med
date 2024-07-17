import config

class API_Charmer():
    '''Third-party software API support'''
    def __init__(self) -> None:
        self.spells = {
            'MED_API' : '',
            
            'Gosuslugi_API' : '',
            
            'GosNotes_1' : '', # есть слоты
            
            'GosNotes_2' : '', # нет слотов, терапевт
            
            'GosNotes_3' : '', # напоминание о записи завтра
        }
        
    def Connect_MED(self, request = '', address = config.MED_adress, id:int = 0):
        if id == 0: exit(1)
        ...
        
    def Connect_Gosuslugi(self, request = '', address = config.Gosuslugi_adress, id:int = 0):
        if id == 0: exit(1)
        ...
        
    def Connect_SMS(self, request = '', address = config.SMS_adress, id:int = 0):
        if id == 0: exit(1)
        ...