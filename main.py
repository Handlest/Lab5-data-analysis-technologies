import datetime

import numpy as np
import pandas as pd


def time_delta_converter(timedelta):
    years = timedelta.days // 364
    month = timedelta.days % 364 // 30
    days = timedelta.days % 364 % 30
    return f'{f"{years} г. " if years != 0 else ""}{month} мес. {days} дн.'


path = './data.xlsx'
data = pd.read_excel(path)
data['фамилия'] = data['ФИО сотрудника'].str.split().str[0]
data['имя'] = data['ФИО сотрудника'].str.split().str[1]
data['отчество'] = data['ФИО сотрудника'].str.split().str[2]

data['Пол'] = np.where(data['ФИО сотрудника'].str.split().str[2].str[-1] == 'А', 'Женский', 'Мужской')
data['Возраст на дату приема'] = ((data['Дата приема'] - data["Дата рождения"]) / np.timedelta64(1, 'D') / 365).astype('int8')
data['Пенсионного возраста'] = np.where(data['Возраст на дату приема'] >= 60, 'да', 'нет')
data["Стаж"] = (data['Дата увольнения'].replace(pd.NaT, pd.Timestamp('01.01.2017')) - data['Дата приема']).apply(time_delta_converter)

pd.set_option('display.max_columns', 20)
print(data.head())

working_on_2017 = data[data['Дата увольнения'].isna() & (data['Дата приема'] <= '2017-01-01')].shape[0]
print(f"Количество работающих на 01.01.2017: {working_on_2017}")

fired_on_2017 = data[data['Дата увольнения'].notna() & (data['Дата увольнения'] <= '2017-01-01')].shape[0]
print(f"Количество уволенных на 01.01.2017: {fired_on_2017}")

# Количество уволенных на 01.01.2009:
fired_on_2009 = data[data['Дата увольнения'].notna() & (data['Дата увольнения'] <= '2009-01-01')].shape[0]
print(f"Количество уволенных на 01.01.2009: {fired_on_2009}")

# Средний возраст уволенных:
mean_age_of_fired = data[data['Дата увольнения'].notna()]['Возраст на дату приема'].mean()
print(f"Средний возраст уволенных: {mean_age_of_fired:.2f}")

# Какого пола больше уволили:
sex_of_fired = data[data['Дата увольнения'].notna()]['Пол'].value_counts().idxmax()
print(f"Больше всего уволили сотрудников пола: {sex_of_fired}")

# Количество сотрудников с фамилией, начинающейся на букву "М":
has_lastname_stars_M = data[data['фамилия'].str.startswith('М')].shape[0]
print(f"Количество сотрудников на 'М': {has_lastname_stars_M}")

# Количество различных причин увольнения:
fire_reasons = data['Причина увольнения'].nunique()
print(f"Количество различных причин увольнения: {fire_reasons}")

# Самая частая причина увольнения:
most_recent_fire_reason = data['Причина увольнения'].mode().iloc[0]
print(f"Самая частая причина увольнения: {most_recent_fire_reason}")

