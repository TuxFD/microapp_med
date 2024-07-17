import config
import psycopg2

class DB_Charmer():
    '''DB driver'''
    def __init__(self) -> None:
        self.spells = {
            0 : f'''dbname={config.db_name} user={config.db_user} password={config.db_pass}''',
            
            'check_tb_schedule' : '''SELECT ts.id, ts.active_status, tp.OMC_number, td.doctor_identifier, ts.last_check, ts.timing_gap, ts.next_check, ts.reminder_day_before, ts.slots_check_available FROM tb_schedule as ts, tb_person as tp, tp_doctor as td WHERE ts.person_id = tp.id AND ts.doctor_id = td.id''',
            
            'check_slots_next_date' : f''' UPDATE tb_schedule as ts SET slots_check_available = 'placeholder_1' WHERE ts.id = placeholder_2 ''',
        }
        
    def db_charm(self, sql_data:str = None, read:bool = True):
        if sql_data == None:
            print('ERROR')
        else:
            try:
                result = False
                conn = psycopg2.connect(self.spells[0])
                with conn.cursor() as cur:
                    if read: 
                        result = cur.execute(sql_data).fetchall()
                    else:
                        cur.execute(sql_data)
                        conn.commit()
                cur.close
                conn.close
                if result:
                    return result
            except Exception as e:
                print('ERROR: ', e)