from typing import List


COLUMNS_NAMES = {'sick_people_id': 'Идентификатор больного', 
                 'full_name': 'ФИО', 
                 'birth_date': 'Дата рождения',
                 'social_status_id': 'Идентификатор социального статуса',
                 'phone_number': 'Номер телефона', 
                 'address': 'Адрес',
                 'call_request_id': 'Идентифиатор заявки на вызов', 
                 'call_date_time': 'Дата заявки на вызов', 
                 'call_reason_id': 'Идентификатор причины вызова', 
                 'money_payment': 'Оплата', 
                 'call_reason_name': 'Причина вызова', 
                 'first_aid_station_id': 'Идентификатор скорой помощи', 
                 'first_aid_station_number': 'Номер скорой помощи', 
                 'city_district': 'Район города',
                 'employees_amount': 'Количество сотрудников',
                 'phone_number': 'Номер телефона',
                 'address': 'Адрес',
                 'procedure_id': 'Идентификатор процедуры',
                 'procedure_name': 'Наименование процедуры', 
                 'procedure_application_id': 'Идентификатор процедуры и заявки на вызов', 
                 'application_id': 'Идентификатор заявки на вызов',
                 'social_status_name': 'Социальный статус', 
                 'abanoned_station_id': 'Идентификатор заброшенной станции скорой помощи', 
                 'station_number': 'Номер станции скорой помощи',
                 'healthy_people_id': 'Идентификатор здорового',
                 'new_sick_person_id': 'Идентификатор нового больного',
                 'new_full_name': 'ФИО нового больного', 
                 'new_birth_date': 'Дата рождения нового больного',
                 'new_phone_number': 'Номер телефона нового больного', 
                 'new_address': 'Адрес нового больного'
                 }

REVERSED_COLUMNS_NAMES = {value: key for key, value in COLUMNS_NAMES.items()}

TABLES_DICT = {
    "Больные": "sick_people",
    "Заявки на вызов": "call_requests",
    "Причины вызова": "call_reason",
    "Станции скорой помощи": "first_aid_stations",
    "Процедуры": "procedure",
    "Заявки на процедуры": "procedure_application",
    "Социальные статусы": "social_status",
    "Заброшенные станции скорой помощи": "abandoned_first_aid_stations",
    "Выздоровевшие пациенты": "healthy_people",
    "Новые больные": "new_sick_people"
}

CHILDREN_TABLES = {
    "Больные": ["Социальные статусы"],
    "Заявки на вызов": ["Больные", "Причины вызова"],
    "Заявки на процедуры": ["Процедуры", "Заявки на вызов"]
}

MODIFIED_VIEW = "symmetricInnerRequestWithoutConditionTwo"
QUERIES = ['leftOuterJoinRequest', 'requestOnRequestLeftJoin', 'rightOuterJoinRequest', 
'symmetricInnerRequestWithConditionDateOne', 'symmetricInnerRequestWithConditionDateTwo', 
'symmetricInnerRequestWithConditionExternalKeyOne', 'symmetricInnerRequestWithConditionExternalKeyTwo', 
'symmetricInnerRequestWithoutConditionOne', 'symmetricInnerRequestWithoutConditionThree', 
'symmetricInnerRequestWithoutConditionTwo', 'queryOnTotalQuery', 'totalQueryWithDataCondition', 
'totalQueryWithDataGroupCondition', 'totalQueryWithGroupCondition',  'totalQueryWithSubquery', 
'totalQueryWithoutCondition', 'totalQueryWithTotalAvgFields', 'totalQueryWithDataMaskCondition',
'unionQuery', 'queryWithIn', 'queryWithNotIn', 'queryWithCase', 
'totalQueryWithDataConditionWithoutIndex', 'totalQueryWihDataConditionWithIndex']

PARAMS = ['', 'birth_date', '', 'call_date_time', 'call_date_time call_date_time', 'social_status_name', 
'full_name', '', '', '', '', 'call_reason_id', 'call_reason_id call_reason_id', '', '', '', '', 
'', '', 'birth_date birth_date', 'birth_date birth_date', '', 'station_number', 'employees_amount']
