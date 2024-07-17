import datetime
from datetime import timedelta

class MicroApp():
    '''App logic & behaviour'''
    def __init__(self, db_charmer, api_charmer) -> None:
        self.db = db_charmer
        self.api = api_charmer   
            
    # метод по умолчанию возвращает понедельник
    def next_weekday(self, date:datetime = datetime.date.today(), weekday:int = 0): # 0 = Понедельник, 1 = Вторник, 2 = Среда...
        days_ahead = weekday - date.weekday()
        if days_ahead <= weekday:
            days_ahead += 7
        result = date + timedelta(days = days_ahead)
        return result
            
            
    def daemon_check(self):
        today = datetime.date.today()
        try:
            sql_0 = self.db.spells['check_tb_schedule']
            sql_1 = self.db.spells["slots_check_available"] # next week
            
            schedule_data = self.db.db_charm(sql_0)
            # FIELDS:       id  active_status   OMC_number  doctor_identifier   last_check  timing_gap  next_check  reminder_day_before   slots_check_available
            # DATA TYPE:    int     bool        varchar     varchar             date        integer     date        date                  date
            # INDEX:        0       1           2           3                   4           5           6           7                     8
            
            for line in schedule_data:
                person_id = line[2]
                doctor_id = line[3]
                
                # нужно ли напомнить о предстоящем посещении врача за день до даты записи?
                if line[7] == today:
                    self.api.Connect_Gosuslugi('send_note_0', person_id) # Да
                
                # нужна ли повторная запись?
                elif line[1] is True:
                    last_check = line[4] + timedelta(days=line[5])
        
                    # пришло ли время повторной записи?
                    if today > last_check:
                        
                        # был ли запрос слотов ранее? если нет:
                        if line[8] is None:
                            result = self.api.Connect_MED('request_slots', doctor_id)  # запрашиваем слоты (1)
                            if result:
                                self.api.Connect_Gosuslugi('send_note_1', person_id)   # есть слоты 
                            else:
                                next_monday = self.next_weekday()                      # нет слотов, подождём до понедельника
                                sql_1.replace('placeholder_1', next_monday).replace('placeholder_2', line[0])
                                schedule_data = self.db.db_charm(sql_1) 
                                
                        # уже был запрос слотов, проверяем заново
                        elif line[8] == today:
                            result = self.api.Connect_MED('request_slots', doctor_id)  # запрашиваем слоты (2)
                            if result:
                                self.api.Connect_Gosuslugi('send_note_1', person_id)   # есть слоты
                            else:
                                self.api.Connect_Gosuslugi('send_note_2', person_id)   # нет слотов, записываемся к терапевту
        except Exception as e:
            print("ERROR: ", e)