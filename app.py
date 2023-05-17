import streamlit as st
import pandas as pd
import time
import random
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb

st.title('Redacted')
st.markdown("_If you don't know what this is, you never will_")
st.image('https://raw.githubusercontent.com/BenDavis71/redacted/d3aba331ea1a99afa6b889edd74df31345cb54ac/img.jpg')

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

urls = st.file_uploader('Upload Excel Doc')
if urls:
    file_name = urls.name
    urls = pd.read_excel(urls, sheet_name=1)
    urls
    urls = (urls.iloc[:, 0].fillna('').to_list())
    urls = [url.replace(' ','-') for url in urls if url.startswith('http')]

    d = {}
    for url in urls:
        msg = url.rsplit('/')[-1].replace('-', ' ') + url.rsplit('/')[-2].replace('-', ' ').replace(' i ', ' ')
        st.markdown(f"Scraping [{msg}]({url})")
        try:
            random.randint(1, 5)
            df = pd.read_html(url)[0]
            value = df[df[0]=='Total Compensation'][1].iloc[0]
            d[url] = value
            st.write(value)
        except:
            st.write(f'Not able to read from {url} - URL may be invalid')
            d[url] = 'URL Not Valid'

    st.title('Done!')

    df = pd.DataFrame(d.items())
    df.columns = ['URL', 'Total Compensation']
    df = to_excel(df)
    st.download_button('Download', df, file_name=file_name)
