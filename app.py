import streamlit as st
import requests
import xml.etree.ElementTree as ET

def poluchit_valutu():
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    response = requests.get(url)
    root = ET.fromstring(response.text)
    rates = {"RUB": 1.0}
    for valute in root.findall("Valute"):
        char_code = valute.find("CharCode").text
        value = float(valute.find("VunitRate").text.replace(",", "."))
        rates[char_code] = value
    return rates

rates = poluchit_valutu()
currencies = list(rates.keys())
st.title('Конвертер валют')
st.write('Курсы валют с сайта ЦБ РФ')
amount = st.number_input("Введине сумму:", min_value = 0.0, step = 1.0)
from_currencies = st.selectbox("Из валюты:", currencies)
to_currencies = st.selectbox('В валюту:', currencies)

if st.button("Конвертировать"):
    if from_currencies in rates and to_currencies in rates:
        converted_amount = amount*rates[from_currencies]/rates[to_currencies]
        st.success(f"{amount} {from_currencies} = {converted_amount:.3f} {to_currencies}")
    else:
        st.error("Ошибка: выбранная валюта не найдена в курсах ЦБ")

if st.button("Обновить курсы"):
    st.cache_data.clear()
    rates = poluchit_valutu()
    st.success("Курсы обновлены")
