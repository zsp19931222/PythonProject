# -*- coding: utf-8 -*-
import connect as con

province = []


def get_code():
    code = ''
    soup = con.connection("http://www.ccb.com/cn/OtherResource/bankroll/html/code_help.html")
    add_list = soup.findAll('div', attrs={'class': 'addlist'})

    for list in add_list:
        table_list = list.findAll('table')
        data = []
        for table in table_list:
            tr_list = table.findAll('td')
            for index, td in enumerate(tr_list):

                if index % 2 == 0:
                    code = td.getText()
                else:
                    area = td.getText()
                    data.append({'code': str(code).strip(), 'area': area.strip()})

        province.append({
            'province': list.find('h3').getText(),
            'data': data
        })


get_code()
for i in range(len(province)):
    for d in province[i]['data']:
        print province[i]['province'] + '----------->' + d['code'] + '<--------->' + d['area']
