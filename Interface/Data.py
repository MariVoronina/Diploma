import pandas as pd
from sqlalchemy import create_engine
import codecs

from datetime import date, timedelta

start_date = date(2025, 2, 5)
end_date = date(2025, 5, 28)

date_list = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
date_list = [d.strftime("%Y-%m-%d") for d in date_list]



file = codecs.open( "C:\\WORK\\analys_substances.txt", "r", "utf-8" )
data = file.read()
dosage_substances = eval(data)
file.close()


engine = create_engine(
    "{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}".format(
        dialect="postgresql",
        driver="psycopg2",
        username="maria",
        password="maria",
        host="localhost",
        port=5432,
        database="delta"
    )
)
with engine.connect() as db_conn:
    information = pd.read_sql_table("information", con=db_conn)
    categories = list(set(information["category"].values))
    substances = sorted(list(set(information["substance"].values)))
    manufactures = list(set(information["manufacture"].values))


bux_balans = pd.read_excel("C:\\WORK\\Бухгалтерский баланс.xlsx", sheet_name="Лист1")
vneob_activ = pd.read_excel("C:\\WORK\\Бухгалтерский баланс.xlsx", sheet_name="Лист6")
ob_activ = pd.read_excel("C:\\WORK\\Бухгалтерский баланс.xlsx", sheet_name="Лист2")
kap_i_rez = pd.read_excel("C:\\WORK\\Бухгалтерский баланс.xlsx", sheet_name="Лист3")
dolg_obs = pd.read_excel("C:\\WORK\\Бухгалтерский баланс.xlsx", sheet_name="Лист4")
krat_obs = pd.read_excel("C:\\WORK\\Бухгалтерский баланс.xlsx", sheet_name="Лист5")

dox_i_ras_obuch = pd.read_excel("C:\\WORK\\Отчет о финансовых результатах.xlsx", sheet_name="Лист1")
proch_dox_i_ras = pd.read_excel("C:\\WORK\\Отчет о финансовых результатах.xlsx", sheet_name="Лист2")
sovoc_fin_rez = pd.read_excel("C:\\WORK\\Отчет о финансовых результатах.xlsx", sheet_name="Лист3")

itog_kap = pd.read_excel("C:\\WORK\\Отчет об изменение капитала.xlsx", sheet_name="Лист1")
ustav_kap = pd.read_excel("C:\\WORK\\Отчет об изменение капитала.xlsx", sheet_name="Лист2")
rez_kap = pd.read_excel("C:\\WORK\\Отчет об изменение капитала.xlsx", sheet_name="Лист3")
nerasp_prib = pd.read_excel("C:\\WORK\\Отчет об изменение капитала.xlsx", sheet_name="Лист4")
chist_act = pd.read_excel("C:\\WORK\\Отчет об изменение капитала.xlsx", sheet_name="Лист5")
sobs_ak = pd.read_excel("C:\\WORK\\Отчет об изменение капитала.xlsx", sheet_name="Лист6")
dob_kap = pd.read_excel("C:\\WORK\\Отчет об изменение капитала.xlsx", sheet_name="Лист7")

otch = pd.read_excel("C:\\WORK\\Отчет о движении денежных средств.xlsx", sheet_name="Лист1")
den_pot = pd.read_excel("C:\\WORK\\Отчет о движении денежных средств.xlsx", sheet_name="Лист2")
den_pot_inv = pd.read_excel("C:\\WORK\\Отчет о движении денежных средств.xlsx", sheet_name="Лист3")
den_pot_fin = pd.read_excel("C:\\WORK\\Отчет о движении денежных средств.xlsx", sheet_name="Лист4")

otch_zel = pd.read_excel("C:\\WORK\\Отчет о целевом использовании денежных средств.xlsx", sheet_name="Лист1")
post = pd.read_excel("C:\\WORK\\Отчет о целевом использовании денежных средств.xlsx", sheet_name="Лист2")
isp = pd.read_excel("C:\\WORK\\Отчет о целевом использовании денежных средств.xlsx", sheet_name="Лист3")


pharm_manuf = pd.read_excel("C:\\WORK\\Динамика фарм рынка.xlsx", sheet_name="Лист1")
pharms = pd.read_excel("C:\\WORK\\Динамика фарм рынка.xlsx", sheet_name="Лист2")
roz_zak = pd.read_excel("C:\\WORK\\Динамика фарм рынка.xlsx", sheet_name="Лист3")
gos_zak = pd.read_excel("C:\\WORK\\Динамика фарм рынка.xlsx", sheet_name="Лист4")