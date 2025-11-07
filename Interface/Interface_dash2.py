from dash import Dash, dcc, html, Input, Output, callback

from Data_for_analys import *
from Main import *


def generate_table(dataframe, max_rows=25):
    return html.Table(
        [html.Tr([html.Th("№"), html.Th("Дата обращения"), html.Th("Источник"), html.Th("Категория"), html.Th("Бренд/Действующее вещество"), html.Th("Производитель"), html.Th("Название"), html.Th("Цена, руб.")])] +

        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


def fin_generate_table(dataframe, style=None):
    if style is None:
        return html.Table(
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(len(dataframe))]
        )
    else:
        return html.Table(style=style, children=
            [html.Tr([html.Th(col) for col in dataframe.columns])] +

            [html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(len(dataframe))]
        )


choice_categories = []
choice_substances = []
choice_manufactures = []
start_date = "2025-02-05"
end_date = "2025-04-30"

analys_substances = []
analys_start_date = "2025-02-05"
analys_end_date = "2025-04-30"


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(id="app-content", children=[html.Img(src='assets/Вертекс.png', style={"height": "100px", "width": "290px"}),
    dcc.Tabs(id="tabs", value='data',colors={"border": "#76B120"}, children=[
        dcc.Tab(label='Обновление данных', id="tab-renew", value='renew', style={"backgroundColor": "#00457C", 'color': "white"},
                children=[html.Div(id='renew-content', style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"},
                                   children=[html.H5("Обновить данные на текущее число", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                             html.Button('Обновить данные', id='renew-data', n_clicks=0, style={"margin-left": "740px", "margin-bottom": "22px","backgroundColor": "#00457C", 'color': "white"})
                                             ]
                                   )
                ]
                ),
        dcc.Tab(label='Просмотр данных', id="tab-data", value='data', style={"backgroundColor": "#00457C", 'color': "white"},
                children=[html.Div(children=[html.H5("Выберите, какие данные хотели бы посмотреть", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                    dcc.Tabs(id="tab-data-tabs", colors={"border": "#76B120"}, style={"margin-bottom": "15px"}, children=[
                    dcc.Tab(label="Данные с онлайн-витрин аптек", id="tab-data-base",  style={"backgroundColor": "#00457C", 'color': "white"}, children=[
                        html.Div(id='tab-data-base-content', style={"margin-top": "15px"},
                        children=[html.H5("Настройте фильтры для выбора данных", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                        html.Div(children=[
                        dcc.DatePickerRange(
                            id='date-picker-range',
                            start_date=date(2025, 2, 5),
                            end_date_placeholder_text='Выберите конечную дату'
                                            ),
                        dcc.Dropdown(categories, id='tab-dat-base-category', multi=True, placeholder="Выберите категорию лекарственных препаратов", style={"width": 350}),
                        dcc.Dropdown(substances, id='tab-dat-base-substance', multi=True, placeholder="Выберите действующее вещество/бренд", style={"width": 350}),
                        dcc.Dropdown(manufactures, id='tab-dat-base-manufacture', multi=True, placeholder="Выберите производителя", style={"width": 350})
                               ], style={"display": "flex", "justify-content": "space-between"}),
                        html.Div(children=[
                            html.Button('Посмотреть данные', id='tab-dat-base-look-data', n_clicks=0, style={"margin-left": "600px", "margin-right": "20px", "backgroundColor": "#00457C", 'color': "white"}),
                            html.Button('Скачать данные', id='tab-dat-base-download-data', n_clicks=0, style={"margin-right": "600px", "margin-left": "50px", "backgroundColor": "#00457C", 'color': "white"}),
                            dcc.Download(id="download-base-dataframe")
                        ], style={"display": "flex", "margin-top": "22px", "margin-bottom": "10px"})
                ])

                    ]),
                    dcc.Tab(label="Налоговые данные АО 'Вертекс'", id="tab-data-tax",  style={"backgroundColor": "#00457C", 'color': "white"}, children=[
                        html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-top": "5px solid #76B120", "border-bottom": "0px", "border-left": "0px", "border-right": "0px"}, children=[
                        dcc.Tabs(id="tab-data-tax-tabs", colors={"border": "#76B120"}, style={"margin-bottom": "15px"}, children=[
                            dcc.Tab(label="Бухгалтерский баланс", style={"backgroundColor": "#00457C", 'color': "white"}, children=[
                                html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                                    html.H5("Бухгалтерский баланс (в тыс. руб.)", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                    fin_generate_table(bux_balans)
                                ]),
                                html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                                    html.H5("Внеоборотные активы (в тыс. руб.)", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                    fin_generate_table(vneob_activ)
                                ]),
                                html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                                    html.H5("Оборотные активы (в тыс. руб.)", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                    fin_generate_table(ob_activ)
                                ]),
                                html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                                    html.H5("Капитал и резервы (в тыс. руб.)", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                    fin_generate_table(kap_i_rez)
                                ]),
                                html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                                    html.H5("Долгосрочные обязательства (в тыс. руб.)", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                    fin_generate_table(dolg_obs)
                                ]),
                                html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                                    html.H5("Краткосрочные обязательства (в тыс. руб.)", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                    fin_generate_table(krat_obs)
                                ])
                            ]),
                            dcc.Tab(label="Отчет о движении денежных средств", style={"backgroundColor": "#00457C", 'color': "white"}, children=[
                                html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                                    html.H5("Отчет о движении денежных средств (в тыс. руб.)", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                    fin_generate_table(otch)
                                ]),
                                html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                                    html.H5("Днежные потоки от текущих операций (в тыс. руб.)", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                    fin_generate_table(den_pot)
                                ]),
                                html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                                    html.H5("Днежные потоки от инвестиционных операций (в тыс. руб.)", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                    fin_generate_table(den_pot_inv)
                                ]),
                                html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                                    html.H5("Днежные потоки от финансовых операций (в тыс. руб.)", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                    fin_generate_table(den_pot_fin)
                                ])
                            ]),
                            dcc.Tab(label="Отчет о финансовых результатах", style={"backgroundColor": "#00457C", 'color': "white"}, children=[
                                html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                                    html.H5("Доходы и расходы по обычным видам деятельности (в тыс. руб.)", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                    fin_generate_table(dox_i_ras_obuch)
                                ]),
                                html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                                    html.H5("Прочие доходы и расходы (в тыс. руб.)", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                    fin_generate_table(proch_dox_i_ras)
                                ]),
                                html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                                    html.H5("Совокупный финансовый результат (в тыс. руб.)", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                    fin_generate_table(sovoc_fin_rez)
                                ])
                            ]),
                            dcc.Tab(label="Отчет о целевом использовании денежных средств", style={"backgroundColor": "#00457C", 'color': "white"}, children=[
                                html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                                    html.H5("Отчет о целевом использовании полученных средств (в тыс. руб.)", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                    fin_generate_table(otch_zel)
                                ]),
                                html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                                    html.H5("Поступило средств (в тыс. руб.)", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                    fin_generate_table(post)
                                ]),
                                html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                                    html.H5("Использовано средств (в тыс. руб.)", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                    fin_generate_table(isp)
                                ])
                            ]),
                            dcc.Tab(label="Отчет об изменении капитала", style={"backgroundColor": "#00457C", 'color': "white"}, children=[
                                html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                                    html.H5("Итого (в тыс. руб.)", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                    fin_generate_table(itog_kap)
                                ]),
                                html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                                    html.H5("Уставный капитал (в тыс. руб.)", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                    fin_generate_table(ustav_kap)
                                ]),
                                html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                                    html.H5("Резервный капитал (в тыс. руб.)", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                    fin_generate_table(rez_kap)
                                ]),
                                html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                                    html.H5("Нераспределенная прибыль (непокрытый убыток) (в тыс. руб.)", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                    fin_generate_table(nerasp_prib)
                                ]),
                                html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                                    html.H5("Чистые активы (в тыс. руб.)", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                    fin_generate_table(chist_act)
                                ]),
                                html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                                    html.H5("Собственные акции (в тыс. руб.)", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                    fin_generate_table(sobs_ak)
                                ]),
                                html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                                    html.H5("Добавочный капитал (в тыс. руб.)", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                    fin_generate_table(dob_kap)
                                ]),

                            ])
                        ])])
                    ])
                ])], style={"margin-top": "25px", "backgroundColor": "white", "border-top": "3px solid #76B120", "border-bottom": "0px", "border-left": "0px", "border-right": "0px"})
                ]),
        dcc.Tab(label='Анализ данных', id="tab-graphs",value='graphs', style={"backgroundColor": "#00457C", 'color': "white"}, children=[
            html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-top": "5px solid #76B120", "border-bottom": "0px", "border-left": "0px", "border-right": "0px"}, children=[
                dcc.Tabs(id="tab-graphs-tabs", colors={"border": "#76B120"}, style={"margin-bottom": "15px"}, children=[
                    dcc.Tab(label="Общий анализ рынка", style={"backgroundColor": "#00457C", 'color': "white"}, children=[
                        html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                            dcc.Graph(figure=fig2_1)
                        ]),
                        html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                            dcc.Graph(figure=fig2_2)
                        ]),
                        html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                            html.Div(style={"display": "flex", "justify-content": "space-between"}, children=[
                                html.H5("Динамика розничных продаж по ФО России", style={"margin-top": "22px", "margin-bottom": "22px", "margin-left": "105px"}),
                                html.H5("Динамика государственных закупок по ФО России", style={"margin-top": "22px", "margin-bottom": "22px", "margin-right": "105px"})
                            ]),
                            html.Div(style={"display": "flex", "justify-content": "space-between"}, children=[
                                fin_generate_table(roz_zak, style={"margin-left": "35px"}),
                                fin_generate_table(gos_zak, style={"margin-right": "35px"})
                            ])
                        ]),
                        html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                            dcc.Graph(figure=fig3_2)
                        ]),
                        html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                            dcc.Graph(figure=fig3_1)
                        ]),
                        html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                            dcc.Graph(figure=fig3_3)
                        ]),
                        html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                            dcc.Graph(figure=fig3_4)
                        ]),
                        html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                            dcc.Graph(figure=fig3_5)
                        ]),
                        html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                            dcc.Graph(figure=fig3_6)
                        ]),
                        html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                            dcc.Graph(figure=fig3_7)
                        ]),
                        html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                            dcc.Graph(figure=fig3_8)
                        ])
                    ]),
                    dcc.Tab(id="tab-analys-sub", label="Анализ по лекарственным перпаратам", style={"backgroundColor": "#00457C", 'color': "white"}, children=[
                        html.Div(style={"margin-top": "15px"},
                        children=[html.H5("Укажите период и действующее вещество в лекарственных препаратах", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                        html.Div(children=[
                        dcc.DatePickerRange(style={"margin-left": "265px"},
                            id='analys-date-picker-range',
                            start_date=date(2025, 2, 5),
                            end_date_placeholder_text='Выберите конечную дату'
                                            ),
                        dcc.Dropdown(substances, id='tab-analys-substance', multi=True, placeholder="Выберите действующее вещество/бренд", style={"margin-right": "265px", "width": "300px"}),
                               ], style={"display": "flex", "justify-content": "space-between"}),
                        html.Div(children=[
                            html.Button('Получить анализ', id='tab-analys-data', n_clicks=0, style={"margin-left": "740px", "backgroundColor": "#00457C", 'color': "white"}),
                        ], style={"margin-top": "22px", "margin-bottom": "10px"})
                    ])]),
                    dcc.Tab(label="Внешний финансовый анализ деятельности АО 'Вертекс'", style={"backgroundColor": "#00457C", 'color': "white"}, children=[
                        html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                            html.H5("Динамика выручки АО 'Вертекс'", style={"text-align": "center", "margin-top": "22px", "margin-bottom": "22px"}),
                            html.Div(style={"display": "flex", "justify-content": "space-between",}, children=[
                            dcc.Graph(figure=fig1_1, style={"margin-left": "85px"}),
                            fin_generate_table(temp_vur, style={"margin-right": "85px"})])
                        ]),
                        html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                            html.H5("Динамика активов АО 'Вертекс'", style={"text-align": "center", "margin-top": "22px", "margin-bottom": "22px"}),
                            dcc.Graph(figure=fig1_2)
                        ]),
                        html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                            html.H5("Основные показатели рентабельности АО 'Вертекс'", style={"text-align": "center", "margin-top": "22px", "margin-bottom": "22px"}),
                            dcc.Graph(figure=fig1_3)
                        ]),
                        html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                            html.H5("Оценка ликвидности АО 'Вертекс'", style={"text-align": "center", "margin-top": "22px", "margin-bottom": "22px"}),
                            fin_generate_table(oz_likv)
                        ]),
                        html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                            html.H5("Оценка рентабельности АО 'Вертекс'", style={"text-align": "center", "margin-top": "22px", "margin-bottom": "22px"}),
                            fin_generate_table(oz_rent)
                        ]),
                        html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                            html.H5("Оценка финансовой устойчивости АО 'Вертекс'", style={"text-align": "center", "margin-top": "22px", "margin-bottom": "22px"}),
                            fin_generate_table(oz_ust)
                        ]),
                        html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                            html.H5("Оценка платежеспособности АО 'Вертекс'", style={"text-align": "center", "margin-top": "22px", "margin-bottom": "22px"}),
                            fin_generate_table(oz_plat)
                        ]),
                        html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                            html.H5("Оценка деловой активности АО 'Вертекс'", style={"text-align": "center", "margin-top": "22px", "margin-bottom": "22px"}),
                            fin_generate_table(oz_del)
                        ]),
                        html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                            html.H5("Оценка рисков деятельности АО 'Вертекс'", style={"text-align": "center", "margin-top": "22px", "margin-bottom": "22px"}),
                            fin_generate_table(val),
                            fin_generate_table(oz_risk)
                        ])

                    ])
                ])])

        ])
                ]
                ),
    ])


@callback(Input('tab-dat-base-category', 'value'), prevent_initial_call=True)
def change_category(value):
    global choice_categories
    choice_categories = value


@callback(Input('tab-dat-base-substance', 'value'), prevent_initial_call=True)
def change_substance(value):
    global choice_substances
    choice_substances = value


@callback(Input('tab-dat-base-manufacture', 'value'), prevent_initial_call=True)
def change_manufacture(value):
    global choice_manufactures
    choice_manufactures = value


@callback(Input('date-picker-range', 'start_date'), prevent_initial_call=True)
def change_start_date(dat):
    global start_date
    start_date = dat


@callback(Input('date-picker-range', 'end_date'), prevent_initial_call=True)
def change_end_date(dat):
    global end_date
    end_date = dat


@callback(Input('tab-analys-substance', 'value'), prevent_initial_call=True)
def change_analys_substance(value):
    global analys_substances
    analys_substances = value


@callback(Input('analys-date-picker-range', 'start_date'), prevent_initial_call=True)
def change_analys_start_date(dat):
    global analys_start_date
    analys_start_date = dat


@callback(Input('analys-date-picker-range', 'end_date'), prevent_initial_call=True)
def change_analys_end_date(dat):
    global analys_end_date
    analys_end_date = dat


@callback(Output("tab-data-base", 'children'),
              Input('tab-dat-base-look-data', 'n_clicks'), prevent_initial_call=True)
def look_content(n_clicks):
    global information, choice_categories, choice_substances, choice_manufactures, start_date, end_date
    ch_c = choice_categories
    ch_s = choice_substances
    ch_m = choice_manufactures
    choice_categories = []
    choice_substances = []
    choice_manufactures = []
    result_frame = information
    if ch_c != []:
        result_frame = result_frame[result_frame['category'].isin(ch_c)]
    if ch_s != []:
        result_frame = result_frame[result_frame['substance'].isin(ch_s)]
    if ch_m != []:
        result_frame = result_frame[result_frame['manufacture'].isin(ch_m)]

    result_frame["date_inf"] = pd.to_datetime(result_frame["date_inf"].values, format="mixed", dayfirst=True)
    result_frame = result_frame[(result_frame['date_inf'] >= pd.Timestamp(start_date)) & (result_frame['date_inf'] <= pd.Timestamp(end_date))]

    return [html.Div(id='tab-data-base-content', style={"margin-top": "15px"},
                        children=[html.H5("Настройте фильтры для выбора данных", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                        html.Div(children=[
                        dcc.DatePickerRange(
                            id='date-picker-range',
                            start_date=date(2025, 2, 5),
                            end_date_placeholder_text='Выберите конечную дату'
                                            ),
                        dcc.Dropdown(categories, id='tab-dat-base-category', multi=True, placeholder="Выберите категорию лекарственных препаратов", style={"width": 350}),
                        dcc.Dropdown(substances, id='tab-dat-base-substance', multi=True, placeholder="Выберите действующее вещество/бренд", style={"width": 350}),
                        dcc.Dropdown(manufactures, id='tab-dat-base-manufacture', multi=True, placeholder="Выберите производителя", style={"width": 350})
                               ], style={"display": "flex", "justify-content": "space-between"}),
                        html.Div(children=[
                            html.Button('Посмотреть данные', id='tab-dat-base-look-data', n_clicks=0, style={"margin-left": "600px", "margin-right": "20px", "backgroundColor": "#00457C", 'color': "white"}),
                            html.Button('Скачать данные', id='tab-dat-base-download-data', n_clicks=0, style={"margin-right": "600px", "margin-left": "50px", "backgroundColor": "#00457C", 'color': "white"}),
                            dcc.Download(id="download-base-dataframe")
                        ], style={"display": "flex", "margin-top": "22px", "margin-bottom": "10px"}),
                        html.H5("Результаты выбора данных", style={"text-align": "center", "margin-top": "22px", "margin-bottom": "22px"}),
                        html.Div(id='information-content', style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"},
                                           children=[generate_table(result_frame)])
                ])

                    ]


@callback(Output("download-base-dataframe", 'data'),
              Input('tab-dat-base-download-data', 'n_clicks'), prevent_initial_call=True)
def download_content(n_clicks):
    global information, choice_categories, choice_substances, choice_manufactures, start_date, end_date
    ch_c = choice_categories
    ch_s = choice_substances
    ch_m = choice_manufactures
    choice_categories = []
    choice_substances = []
    choice_manufactures = []
    result_frame = information
    if ch_c != []:
        result_frame = result_frame[result_frame['category'].isin(ch_c)]
    if ch_s != []:
        result_frame = result_frame[result_frame['substance'].isin(ch_s)]
    if ch_m != []:
        result_frame = result_frame[result_frame['manufacture'].isin(ch_m)]
    result_frame["date_inf"] = pd.to_datetime(result_frame["date_inf"].values, format="mixed", dayfirst=True)
    result_frame = result_frame[
        (result_frame['date_inf'] >= pd.Timestamp(start_date)) & (result_frame['date_inf'] <= pd.Timestamp(end_date))]
    return dcc.send_data_frame(result_frame.to_excel, "result_excel.xlsx")


@callback(Output("tab-renew", 'children'),
              Input('renew-data', 'n_clicks'), prevent_initial_call=True)
def renew(n_clicks):
    if date.today().strftime("%d.%m.%Y") in pd.to_datetime(information["date_inf"].values, format="mixed"):
        return [html.Div(id='renew-content',
                         style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120",
                                "border-style": "solid", "padding": "5px"},
                         children=[html.H5("Обновить данные на текущее число",
                                           style={"text-align": "center", "margin-top": "22px",
                                                  "margin-bottom": "22px"}),
                                   html.Button('Обновить данные', id='renew-data', n_clicks=0,
                                               style={"margin-left": "740px", "margin-bottom": "22px",
                                                      "backgroundColor": "#76B120", 'color': "white"})
                                   ]
                         ),
                html.H2("Данные на сегоднешнюю дату уже собраны", style={"text-align": "center", "margin-top": "22px"})
                ]
    else:
        del drugs_search["Ривароксабан"]
        scraping(list(pharmacies_choices.keys()), list(drugs_search.keys()))
        return [html.Div(id='renew-content', style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"},
                                       children=[html.H5("Обновить данные на текущее число", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                                                 html.Button('Обновить данные', id='renew-data', n_clicks=0, style={"margin-left": "740px", "margin-bottom": "22px","backgroundColor": "#76B120", 'color': "white"})
                                                 ]
                                       ),
                html.H2("Данные были обновлены", style={"text-align": "center",  "margin-top": "22px"})
                    ]


@callback(Output("tab-analys-sub", 'children'),
              Input('tab-analys-data', 'n_clicks'), prevent_initial_call=True)
def analys_content(n_clicks):
    global information, analys_substances, analys_start_date, analys_end_date
    ch_s = analys_substances
    analys_substances = []
    result_frame = information
    result_frame["date_inf"] = pd.to_datetime(result_frame["date_inf"].values, format="mixed", dayfirst=True)
    result_frame = result_frame[(result_frame['date_inf'] >= pd.Timestamp(analys_start_date)) & (result_frame['date_inf'] <= pd.Timestamp(analys_end_date))]

    children = [html.Div(style={"margin-top": "15px"},
                        children=[html.H5("Укажите период и действующее вещество в лекарственных препаратах", style={"text-align": "center",  "margin-top": "22px", "margin-bottom": "22px"}),
                        html.Div(children=[
                        dcc.DatePickerRange(style={"margin-left": "265px"},
                            id='analys-date-picker-range',
                            start_date=date(2025, 2, 5),
                            end_date_placeholder_text='Выберите конечную дату'
                                            ),
                        dcc.Dropdown(substances, id='tab-analys-substance', multi=True, placeholder="Выберите действующее вещество/бренд", style={"margin-right": "265px", "width": "300px"}),
                               ], style={"display": "flex", "justify-content": "space-between"}),
                        html.Div(children=[
                            html.Button('Получить анализ', id='tab-analys-data', n_clicks=0, style={"margin-left": "740px", "backgroundColor": "#00457C", 'color': "white"}),
                        ], style={"margin-top": "22px", "margin-bottom": "10px"})
                    ])]

    for sub in ch_s:

        result_frame_sub = result_frame[result_frame['substance'] == sub]

        for dos in dosage_substances[sub]:
            result_frame_sub_dos = result_frame_sub[result_frame_sub["name_inf"].str.contains(dos)]
            if len(result_frame_sub_dos) == 0:
                continue
            else:
                group_frame = result_frame_sub_dos.groupby(['date_inf']).agg({'price': ['mean']})
                reset_frame = group_frame.reset_index()

                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=reset_frame["date_inf"].values, y=reset_frame["price"]["mean"].values,
                    xperiodalignment="middle"
                ))
                fig.update_xaxes(showgrid=True, ticklabelmode="period")
                fig.update_layout(title=f"Средняя цена на лекарственный препарат с действующим веществом {sub} и дозировкой {dos}",xaxis_title="Дата", yaxis_title="Средняя цена, руб")
                child = html.Div(style={"margin-top": "25px", "backgroundColor": "white", "border-color": "#76B120", "border-style": "solid", "padding": "5px"}, children=[
                            dcc.Graph(figure=fig)
                        ])
                children.append(child)

    return children

app.run(debug=True)