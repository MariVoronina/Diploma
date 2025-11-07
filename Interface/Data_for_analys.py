from Data import *
import plotly.express as px
import plotly.graph_objects as go


vur = dox_i_ras_obuch[dox_i_ras_obuch["Наименование"] == "Выручка"].values[0][2:]
temp_vur = pd.DataFrame(columns=["Год", "Выручка", "Темпы роста, %"])
temp_vur["Год"] = dox_i_ras_obuch.columns[2:]
temp_vur["Выручка"] = vur
rev_vur = list(reversed(vur))
temp = [str(round(((rev_vur[i] - rev_vur[i-1])/rev_vur[i-1])*100, 2)) for i in range(1, len(temp_vur["Год"].values))]
temp = list(reversed(temp))
temp.append("-")
temp_vur["Темпы роста, %"] = temp

fig1_1 = px.line(temp_vur, x="Год", y="Выручка")
fig1_1.update_layout(xaxis_title="Год", yaxis_title="Тыс. руб")

temp_act = pd.DataFrame(columns=["Год", "Чистые активы", "Внеоборотные активы", "Всего активов"])
temp_act["Всего активов"] = bux_balans[bux_balans["Наименование"] == "БАЛАНС (актив)"].values[0][2:]
temp_act["Внеоборотные активы"] = vneob_activ[vneob_activ["Наименование"] == "Итого внеоборотных активов"].values[0][2:]
temp_act["Чистые активы"] = chist_act[chist_act["Наименование"] == "Чистые активы на 31 декабря отчетного года"].values[0][2:]
temp_act["Год"] = bux_balans.columns[2:]

fig1_2 = go.Figure()
fig1_2.add_trace(go.Scatter(
    name="Чистые активы",
    mode="lines+markers", x=temp_act["Год"].values, y=temp_act["Чистые активы"].values,
    xperiodalignment="end"
))
fig1_2.add_trace(go.Scatter(
    name="Внеоборотные активы",
    mode="lines+markers",x=temp_act["Год"].values, y=temp_act["Внеоборотные активы"].values,
    xperiodalignment="end"
))
fig1_2.add_trace(go.Bar(
    name="Всего активов",
    x=temp_act["Год"].values, y=temp_act["Всего активов"].values,
    xperiodalignment="middle"
))
fig1_2.update_xaxes(showgrid=True, ticklabelmode="period")
fig1_2.update_layout(xaxis_title="Год", yaxis_title="Тыс. руб")


rent = pd.DataFrame(columns=["Год", "Выручка", "Чистая прибыль", "EBIT"])
rent["Чистая прибыль"] = itog_kap[itog_kap["Наименование"] == "Чистая прибыль"].values[0][2:]
rent["Выручка"] = dox_i_ras_obuch[dox_i_ras_obuch["Наименование"] == "Выручка"].values[0][2:]
rent["Год"] = bux_balans.columns[2:]
prib = itog_kap[itog_kap["Наименование"] == "Чистая прибыль"].values[0][2:]
tax_prib = den_pot[den_pot["Наименование"] == "Налога на прибыль организаций"].values[0][2:]
proz = proch_dox_i_ras[proch_dox_i_ras["Наименование"] == "Проценты к уплате"].values[0][2:]
ebit = [proz[i] + tax_prib[i] + prib[i] for i in range(len(proz))]
rent["EBIT"] = ebit

fig1_3 = go.Figure()
fig1_3.add_trace(go.Bar(
    name="Выручка",
    x=rent["Год"].values, y=rent["Выручка"].values,
    xperiodalignment="middle"
))
fig1_3.add_trace(go.Bar(
    name="Чистая прибыль",
    x=rent["Год"].values, y=rent["Чистая прибыль"].values,
    xperiodalignment="middle"
))
fig1_3.add_trace(go.Bar(
    name="EBIT",
    x=rent["Год"].values, y=rent["EBIT"].values,
    xperiodalignment="middle"
))
fig1_3.update_xaxes(showgrid=True, ticklabelmode="period")
fig1_3.update_layout(xaxis_title="Год", yaxis_title="Тыс. руб")

col = ["Наименование"]
for year in bux_balans.columns[2:]:
    col.append(year)
oz_likv = pd.DataFrame(columns=col)
ob_ac = ob_activ[ob_activ["Наименование"] == "Итого оборотных активов"].values[0][2:]
zap = ob_activ[ob_activ["Наименование"] == "Запасы"].values[0][2:]
obuz = krat_obs[krat_obs["Наименование"] == "ИТОГО краткосрочных обязательств"].values[0][2:]
den = ob_activ[ob_activ["Наименование"] == "Денежные средства и денежные эквиваленты"].values[0][2:]
tek_lik = [round(ob_ac[i]/obuz[i], 2) for i in range(len(obuz))]
bus_lik = [round((ob_ac[i]-zap[i])/obuz[i], 2) for i in range(len(obuz))]
abs_lik =  [round(den[i]/obuz[i], 4) for i in range(len(obuz))]
row = ["Коэффициент текущей ликвидности"]
for value in tek_lik:
    row.append(value)
oz_likv.loc[0] = row
row = ["Коэффициент быстрой ликвидности"]
for value in bus_lik:
    row.append(value)
oz_likv.loc[1] = row
row = ["Коэффициент абсолютной ликвидности"]
for value in abs_lik:
    row.append(value)
oz_likv.loc[2] = row


act = list(reversed(bux_balans[bux_balans["Наименование"] == "БАЛАНС (актив)"].values[0][2:]))
mid_act = [round((act[i-1]+act[i])/2, 2) for i in range(1, len(act))]
mid_act = list(reversed(mid_act))
mid_act.append("-")
kap = kap_i_rez[kap_i_rez["Наименование"] == "ИТОГО капитал"].values[0][2:]
dolg = dolg_obs[dolg_obs["Наименование"] == "ИТОГО долгосрочных обязательств"].values[0][2:]
krat = krat_obs[krat_obs["Наименование"] == "ИТОГО краткосрочных обязательств"].values[0][2:]
all_ob = [dolg[i]+krat[i] for i in range(len(krat))]
sobs_kap = [kap[i] - all_ob[i] for i in range(len(krat))]

oz_rent = pd.DataFrame(columns=col)
roa = [str(round(prib[i]/mid_act[i]*100, 2)) for i in range(len(mid_act)-1)]
roa.append("-")
roe = [str(round(prib[i]/sobs_kap[i]*100, 2)) for i in range(len(prib))]
ros = [str(round(prib[i]/vur[i]*100, 2)) for i in range(len(prib))]
row = ["Рентабельность активов(ROA), %"]
for value in roa:
    row.append(value)
oz_rent.loc[0] = row
row = ["Рентабельность собственного капитала(ROE), %"]
for value in roe:
    row.append(value)
oz_rent.loc[1] = row
row = ["Рентабельность продаж(ROS), %"]
for value in ros:
    row.append(value)
oz_rent.loc[2] = row


op_prib = dox_i_ras_obuch[dox_i_ras_obuch["Наименование"] == "Прибыль (убыток) от продаж"].values[0][2:]

oz_ust = pd.DataFrame(columns=col)
avt = [round(sobs_kap[i]/vur[i], 2) for i in range(len(vur))]
fin_zav = [round(all_ob[i]/vur[i], 2) for i in range(len(vur))]
pokr_proz = [round(op_prib[i]/proz[i], 2) for i in range(len(op_prib))]
row = ["Коэффициент автономии"]
for value in avt:
    row.append(value)
oz_ust.loc[0] = row
row = ["Коэффициент финансовой зависимости"]
for value in fin_zav:
    row.append(value)
oz_ust.loc[1] = row
row = ["Коэффициент покрытыия процентов"]
for value in pokr_proz:
    row.append(value)
oz_ust.loc[2] = row


pokr = [round(vur[i]/all_ob[i], 2) for i in range(len(vur))]
oz_plat = pd.DataFrame(columns=col)
row = ["Коэффициент покрытия обязательств"]
for value in pokr:
    row.append(value)
oz_plat.loc[0] = row
row = ["Коэффициент обслуживания долга"]
for value in pokr_proz:
    row.append(value)
oz_plat.loc[1] = row


sebest = dox_i_ras_obuch[dox_i_ras_obuch["Наименование"] == "Себестоимость продаж"].values[0][2:]
deb = list(reversed(ob_activ[ob_activ["Наименование"] == "Дебиторская задолженность"].values[0][2:]))
zap_r = list(reversed(zap))
mid_deb = [round((deb[i-1]+deb[i])/2, 2) for i in range(1, len(deb))]
mid_deb = list(reversed(mid_deb))
mid_deb.append("-")
mid_zap = [round((zap_r[i-1]+zap_r[i])/2, 2) for i in range(1, len(zap_r))]
mid_zap = list(reversed(mid_zap))
mid_zap.append("-")
obor_act = [round(vur[i]/mid_act[i], 2) for i in range(len(mid_act)-1)]
obor_act.append("-")
obor_zap = [round(sebest[i]/mid_zap[i], 2) for i in range(len(mid_zap)-1)]
obor_zap.append("-")
obor_deb = [round(vur[i]/mid_deb[i], 2) for i in range(len(mid_deb)-1)]
obor_deb.append("-")

oz_del = pd.DataFrame(columns=col)
row = ["Обрачиваемость активов"]
for value in obor_act:
    row.append(value)
oz_del.loc[0] = row
row = ["Обрачиваемость запасов"]
for value in obor_zap:
    row.append(value)
oz_del.loc[1] = row
row = ["Обрачиваемость дебиторской задолженности"]
for value in obor_deb:
    row.append(value)
oz_del.loc[2] = row


vur_per1 = vur[:5]
vur_per2 = vur[5:9]
vur_per3 = vur[-4:]
val_prib = []
val_prib.append(round((max(vur_per1) - min(vur_per1))/(sum(vur_per1)/len(vur_per1))*100, 2))
val_prib.append(round((max(vur_per2) - min(vur_per2))/(sum(vur_per2)/len(vur_per2))*100, 2))
val_prib.append(round((max(vur_per3) - min(vur_per3))/(sum(vur_per3)/len(vur_per3))*100, 2))
val = pd.DataFrame(columns=["Наименование", "2020-2024", "2016-2019", "2012-2015"])
row = ["Волатильность прибыли, %"]
for value in val_prib:
    row.append(value)
val.loc[0] = row

k_zad = [round(all_ob[i]/sobs_kap[i], 2) for i in range(len(all_ob))]
oz_risk = pd.DataFrame(columns=col)
row = ["Коэффициент задолженности"]
for value in k_zad:
    row.append(value)
oz_risk.loc[0] = row


fig2_1 = px.pie(pharm_manuf, values='Доля, руб. (%)', names='Корпорация',
                      title="Топ-20 наиболее значимых фармацевтичсеких производителей по доле от объема рыка на российском рынке")
fig2_2 = px.pie(pharms, values='Доля рынка, %', names='Название аптечной сети (штаб-квартира)',
                      title="Топ-20 наиболее значимых аптечных сетей по доле от объема рыка на российском рынке")


bezr_seg1 = information[(information["category"] == "Безрецептурные лекарства") & (information["price"] > 1000)]
bezr_seg2 = information[(information["category"] == "Безрецептурные лекарства") & (information["price"] <= 1000) & (information["price"] > 500)]
bezr_seg3 = information[(information["category"] == "Безрецептурные лекарства") & (information["price"] <= 500) & (information["price"] >= 100)]
bezr_seg4 = information[(information["category"] == "Безрецептурные лекарства") & (information["price"] < 100)]
rez_seg1 = information[(information["category"] == "Рецептурные лекарства") & (information["price"] > 1000)]
rez_seg2 = information[(information["category"] == "Рецептурные лекарства") & (information["price"] <= 1000) & (information["price"] > 500)]
rez_seg3 = information[(information["category"] == "Рецептурные лекарства") & (information["price"] <= 500) & (information["price"] >= 100)]
rez_seg4 = information[(information["category"] == "Рецептурные лекарства") & (information["price"] < 100)]

mean_bez_frame1 = bezr_seg1.groupby(['date_inf']).agg({'price': ['mean']})
mean_bez_frame2 = bezr_seg2.groupby(['date_inf']).agg({'price': ['mean']})
mean_bez_frame3 = bezr_seg3.groupby(['date_inf']).agg({'price': ['mean']})
mean_bez_frame4 = bezr_seg4.groupby(['date_inf']).agg({'price': ['mean']})
mean_rez_frame1 = rez_seg1.groupby(['date_inf']).agg({'price': ['mean']})
mean_rez_frame2 = rez_seg2.groupby(['date_inf']).agg({'price': ['mean']})
mean_rez_frame3 = rez_seg3.groupby(['date_inf']).agg({'price': ['mean']})
mean_rez_frame4 = rez_seg4.groupby(['date_inf']).agg({'price': ['mean']})

bez_man_frame1 = bezr_seg1['manufacture'].value_counts().to_frame().reset_index()
bez_man_frame2 = bezr_seg2['manufacture'].value_counts().to_frame().reset_index()
bez_man_frame3 = bezr_seg3['manufacture'].value_counts().to_frame().reset_index()
bez_man_frame4 = bezr_seg4['manufacture'].value_counts().to_frame().reset_index()
rez_man_frame1 = rez_seg1['manufacture'].value_counts().to_frame().reset_index()
rez_man_frame2 = rez_seg2['manufacture'].value_counts().to_frame().reset_index()
rez_man_frame3 = rez_seg3['manufacture'].value_counts().to_frame().reset_index()
rez_man_frame4 = rez_seg4['manufacture'].value_counts().to_frame().reset_index()

bez_max1 = sorted(bez_man_frame1["count"].values)[-7:]
bez_max2 = sorted(bez_man_frame2["count"].values)[-7:]
bez_max3 = sorted(bez_man_frame3["count"].values)[-7:]
bez_max4 = sorted(bez_man_frame4["count"].values)[-7:]
rez_max1 = sorted(rez_man_frame1["count"].values)[-7:]
rez_max2 = sorted(rez_man_frame2["count"].values)[-7:]
rez_max3 = sorted(rez_man_frame3["count"].values)[-7:]
rez_max4 = sorted(rez_man_frame4["count"].values)[-7:]

bez_max_man_frame1 = bez_man_frame1[(bez_man_frame1["manufacture"] != "Не указан") & (bez_man_frame1["count"].isin(bez_max1))]
bez_max_man_frame2 = bez_man_frame2[(bez_man_frame2["manufacture"] != "Не указан") & (bez_man_frame2["count"].isin(bez_max2))]
bez_max_man_frame3 = bez_man_frame3[(bez_man_frame3["manufacture"] != "Не указан") & (bez_man_frame3["count"].isin(bez_max3))]
bez_max_man_frame4 = bez_man_frame4[(bez_man_frame4["manufacture"] != "Не указан") & (bez_man_frame4["count"].isin(bez_max4))]
rez_max_man_frame1 = rez_man_frame1[(rez_man_frame1["manufacture"] != "Не указан") & (rez_man_frame1["count"].isin(rez_max1))]
rez_max_man_frame2 = rez_man_frame2[(rez_man_frame2["manufacture"] != "Не указан") & (rez_man_frame2["count"].isin(rez_max2))]
rez_max_man_frame3 = rez_man_frame3[(rez_man_frame3["manufacture"] != "Не указан") & (rez_man_frame3["count"].isin(rez_max3))]
rez_max_man_frame4 = rez_man_frame4[(rez_man_frame4["manufacture"] != "Не указан") & (rez_man_frame4["count"].isin(rez_max4))]

bez_man1 = bez_max_man_frame1["manufacture"].values
bez_man2 = bez_max_man_frame2["manufacture"].values
bez_man3 = bez_max_man_frame3["manufacture"].values
bez_man4 = bez_max_man_frame4["manufacture"].values
rez_man1 = rez_max_man_frame1["manufacture"].values
rez_man2 = rez_max_man_frame2["manufacture"].values
rez_man3 = rez_max_man_frame3["manufacture"].values
rez_man4 = rez_max_man_frame4["manufacture"].values

mean_bez_man_frame1 = bezr_seg1[bezr_seg1["manufacture"].isin(bez_man1)].groupby(['date_inf', "manufacture"]).agg({'price': ['mean']})
mean_bez_man_frame2 = bezr_seg2[bezr_seg2["manufacture"].isin(bez_man2)].groupby(['date_inf', "manufacture"]).agg({'price': ['mean']})
mean_bez_man_frame3 = bezr_seg3[bezr_seg3["manufacture"].isin(bez_man3)].groupby(['date_inf', "manufacture"]).agg({'price': ['mean']})
mean_bez_man_frame4 = bezr_seg4[bezr_seg4["manufacture"].isin(bez_man4)].groupby(['date_inf', "manufacture"]).agg({'price': ['mean']})
mean_rez_man_frame1 = rez_seg1[rez_seg1["manufacture"].isin(rez_man1)].groupby(['date_inf', "manufacture"]).agg({'price': ['mean']})
mean_rez_man_frame2 = rez_seg2[rez_seg2["manufacture"].isin(rez_man2)].groupby(['date_inf', "manufacture"]).agg({'price': ['mean']})
mean_rez_man_frame3 = rez_seg3[rez_seg3["manufacture"].isin(rez_man3)].groupby(['date_inf', "manufacture"]).agg({'price': ['mean']})
mean_rez_man_frame4 = rez_seg4[rez_seg4["manufacture"].isin(rez_man4)].groupby(['date_inf', "manufacture"]).agg({'price': ['mean']})

bez_date1 = date_list
bez_date2 = date_list
bez_date3 = date_list
bez_date4 = date_list
rez_date1 = date_list
rez_date2 = date_list
rez_date3 = date_list
rez_date4 = date_list

bez_mean_man11 = [float(mean_bez_man_frame1["price"]["mean"][i]) for i in range(0, len(mean_bez_man_frame1["price"]["mean"]), 6)]
bez_mean_man12 = [float(mean_bez_man_frame1["price"]["mean"][i]) for i in range(1, len(mean_bez_man_frame1["price"]["mean"]), 6)]
bez_mean_man13 = [float(mean_bez_man_frame1["price"]["mean"][i]) for i in range(2, len(mean_bez_man_frame1["price"]["mean"]), 6)]
bez_mean_man14 = [float(mean_bez_man_frame1["price"]["mean"][i]) for i in range(3, len(mean_bez_man_frame1["price"]["mean"]), 6)]
bez_mean_man15 = [float(mean_bez_man_frame1["price"]["mean"][i]) for i in range(4, len(mean_bez_man_frame1["price"]["mean"]), 6)]
bez_mean_man16 = [float(mean_bez_man_frame1["price"]["mean"][i]) for i in range(5, len(mean_bez_man_frame1["price"]["mean"]), 6)]
bez_mean_man21 = [float(mean_bez_man_frame2["price"]["mean"][i]) for i in range(0, len(mean_bez_man_frame2["price"]["mean"]), 6)]
bez_mean_man22 = [float(mean_bez_man_frame2["price"]["mean"][i]) for i in range(1, len(mean_bez_man_frame2["price"]["mean"]), 6)]
bez_mean_man23 = [float(mean_bez_man_frame2["price"]["mean"][i]) for i in range(2, len(mean_bez_man_frame2["price"]["mean"]), 6)]
bez_mean_man24 = [float(mean_bez_man_frame2["price"]["mean"][i]) for i in range(3, len(mean_bez_man_frame2["price"]["mean"]), 6)]
bez_mean_man25 = [float(mean_bez_man_frame2["price"]["mean"][i]) for i in range(4, len(mean_bez_man_frame2["price"]["mean"]), 6)]
bez_mean_man26 = [float(mean_bez_man_frame2["price"]["mean"][i]) for i in range(5, len(mean_bez_man_frame2["price"]["mean"]), 6)]
bez_mean_man31 = [float(mean_bez_man_frame3["price"]["mean"][i]) for i in range(0, len(mean_bez_man_frame3["price"]["mean"]), 6)]
bez_mean_man32 = [float(mean_bez_man_frame3["price"]["mean"][i]) for i in range(1, len(mean_bez_man_frame3["price"]["mean"]), 6)]
bez_mean_man33 = [float(mean_bez_man_frame3["price"]["mean"][i]) for i in range(2, len(mean_bez_man_frame3["price"]["mean"]), 6)]
bez_mean_man34 = [float(mean_bez_man_frame3["price"]["mean"][i]) for i in range(3, len(mean_bez_man_frame3["price"]["mean"]), 6)]
bez_mean_man35 = [float(mean_bez_man_frame3["price"]["mean"][i]) for i in range(4, len(mean_bez_man_frame3["price"]["mean"]), 6)]
bez_mean_man36 = [float(mean_bez_man_frame3["price"]["mean"][i]) for i in range(5, len(mean_bez_man_frame3["price"]["mean"]), 6)]
bez_mean_man41 = [float(mean_bez_man_frame4["price"]["mean"][i]) for i in range(0, len(mean_bez_man_frame4["price"]["mean"]), 6)]
bez_mean_man42 = [float(mean_bez_man_frame4["price"]["mean"][i]) for i in range(1, len(mean_bez_man_frame4["price"]["mean"]), 6)]
bez_mean_man43 = [float(mean_bez_man_frame4["price"]["mean"][i]) for i in range(2, len(mean_bez_man_frame4["price"]["mean"]), 6)]
bez_mean_man44 = [float(mean_bez_man_frame4["price"]["mean"][i]) for i in range(3, len(mean_bez_man_frame4["price"]["mean"]), 6)]
bez_mean_man45 = [float(mean_bez_man_frame4["price"]["mean"][i]) for i in range(4, len(mean_bez_man_frame4["price"]["mean"]), 6)]
bez_mean_man46 = [float(mean_bez_man_frame4["price"]["mean"][i]) for i in range(5, len(mean_bez_man_frame4["price"]["mean"]), 6)]

rez_mean_man11 = [float(mean_rez_man_frame1["price"]["mean"][i]) for i in range(0, len(mean_rez_man_frame1["price"]["mean"]), 6)]
rez_mean_man12 = [float(mean_rez_man_frame1["price"]["mean"][i]) for i in range(1, len(mean_rez_man_frame1["price"]["mean"]), 6)]
rez_mean_man13 = [float(mean_rez_man_frame1["price"]["mean"][i]) for i in range(2, len(mean_rez_man_frame1["price"]["mean"]), 6)]
rez_mean_man14 = [float(mean_rez_man_frame1["price"]["mean"][i]) for i in range(3, len(mean_rez_man_frame1["price"]["mean"]), 6)]
rez_mean_man15 = [float(mean_rez_man_frame1["price"]["mean"][i]) for i in range(4, len(mean_rez_man_frame1["price"]["mean"]), 6)]
rez_mean_man16 = [float(mean_rez_man_frame1["price"]["mean"][i]) for i in range(5, len(mean_rez_man_frame1["price"]["mean"]), 6)]
rez_mean_man21 = [float(mean_rez_man_frame2["price"]["mean"][i]) for i in range(0, len(mean_rez_man_frame2["price"]["mean"]), 6)]
rez_mean_man22 = [float(mean_rez_man_frame2["price"]["mean"][i]) for i in range(1, len(mean_rez_man_frame2["price"]["mean"]), 6)]
rez_mean_man23 = [float(mean_rez_man_frame2["price"]["mean"][i]) for i in range(2, len(mean_rez_man_frame2["price"]["mean"]), 6)]
rez_mean_man24 = [float(mean_rez_man_frame2["price"]["mean"][i]) for i in range(3, len(mean_rez_man_frame2["price"]["mean"]), 6)]
rez_mean_man25 = [float(mean_rez_man_frame2["price"]["mean"][i]) for i in range(4, len(mean_rez_man_frame2["price"]["mean"]), 6)]
rez_mean_man26 = [float(mean_rez_man_frame2["price"]["mean"][i]) for i in range(5, len(mean_rez_man_frame2["price"]["mean"]), 6)]
rez_mean_man31 = [float(mean_rez_man_frame3["price"]["mean"][i]) for i in range(0, len(mean_rez_man_frame3["price"]["mean"]), 6)]
rez_mean_man32 = [float(mean_rez_man_frame3["price"]["mean"][i]) for i in range(1, len(mean_rez_man_frame3["price"]["mean"]), 6)]
rez_mean_man33 = [float(mean_rez_man_frame3["price"]["mean"][i]) for i in range(2, len(mean_rez_man_frame3["price"]["mean"]), 6)]
rez_mean_man34 = [float(mean_rez_man_frame3["price"]["mean"][i]) for i in range(3, len(mean_rez_man_frame3["price"]["mean"]), 6)]
rez_mean_man35 = [float(mean_rez_man_frame3["price"]["mean"][i]) for i in range(4, len(mean_rez_man_frame3["price"]["mean"]), 6)]
rez_mean_man36 = [float(mean_rez_man_frame3["price"]["mean"][i]) for i in range(5, len(mean_rez_man_frame3["price"]["mean"]), 6)]
rez_mean_man41 = [float(mean_rez_man_frame4["price"]["mean"][i]) for i in range(0, len(mean_rez_man_frame4["price"]["mean"]), 6)]
rez_mean_man42 = [float(mean_rez_man_frame4["price"]["mean"][i]) for i in range(1, len(mean_rez_man_frame4["price"]["mean"]), 6)]
rez_mean_man43 = [float(mean_rez_man_frame4["price"]["mean"][i]) for i in range(2, len(mean_rez_man_frame4["price"]["mean"]), 6)]
rez_mean_man44 = [float(mean_rez_man_frame4["price"]["mean"][i]) for i in range(3, len(mean_rez_man_frame4["price"]["mean"]), 6)]
rez_mean_man45 = [float(mean_rez_man_frame4["price"]["mean"][i]) for i in range(4, len(mean_rez_man_frame4["price"]["mean"]), 6)]
rez_mean_man46 = [float(mean_rez_man_frame4["price"]["mean"][i]) for i in range(5, len(mean_rez_man_frame4["price"]["mean"]), 6)]

bez_mean1 = list(mean_bez_frame1["price"]["mean"].values)
bez_mean2 = list(mean_bez_frame2["price"]["mean"].values)
bez_mean3 = list(mean_bez_frame3["price"]["mean"].values)
bez_mean4 = list(mean_bez_frame4["price"]["mean"].values)
rez_mean1 = list(mean_rez_frame1["price"]["mean"].values)
rez_mean2 = list(mean_rez_frame2["price"]["mean"].values)
rez_mean3 = list(mean_rez_frame3["price"]["mean"].values)
rez_mean4 = list(mean_rez_frame4["price"]["mean"].values)

if len(bez_mean1) < len(bez_date1):
    length = len(bez_mean1)
    for i in range(len(bez_date1) - length):
        bez_mean1.append(sum(bez_mean1) / len(bez_mean1))
if len(bez_mean2) < len(bez_date2):
    length = len(bez_mean2)
    for i in range(len(bez_date2) - length):
        bez_mean2.append(sum(bez_mean2) / len(bez_mean2))
if len(bez_mean3) < len(bez_date1):
    length = len(bez_mean3)
    for i in range(len(bez_date1) - length):
        bez_mean3.append(sum(bez_mean3) / len(bez_mean3))
if len(bez_mean4) < len(bez_date1):
    length = len(bez_mean4)
    for i in range(len(bez_date1) - length):
        bez_mean4.append(sum(bez_mean4) / len(bez_mean4))
if len(rez_mean1) < len(rez_date1):
    length = len(rez_mean1)
    for i in range(len(rez_date1) - length):
        rez_mean1.append(sum(rez_mean1) / len(rez_mean1))
if len(rez_mean2) < len(rez_date2):
    length = len(rez_mean2)
    for i in range(len(rez_date2) - length):
        rez_mean2.append(sum(rez_mean2) / len(rez_mean2))
if len(rez_mean3) < len(rez_date1):
    length = len(rez_mean3)
    for i in range(len(rez_date1) - length):
        rez_mean3.append(sum(rez_mean3) / len(rez_mean3))
if len(rez_mean4) < len(rez_date1):
    length = len(rez_mean4)
    for i in range(len(rez_date1) - length):
        rez_mean4.append(sum(rez_mean4) / len(rez_mean4))


if len(bez_mean_man11) < len(bez_date1):
    length = len(bez_mean_man11)
    for i in range(len(bez_date1) - length):
        bez_mean_man11.append(sum(bez_mean_man11) / len(bez_mean_man11))
if len(bez_mean_man12) < len(bez_date1):
    length = len(bez_mean_man12)
    for i in range(len(bez_date1) - length):
        bez_mean_man12.append(sum(bez_mean_man12) / len(bez_mean_man12))
if len(bez_mean_man13) < len(bez_date1):
    length = len(bez_mean_man13)
    for i in range(len(bez_date1) - length):
        bez_mean_man13.append(sum(bez_mean_man13) / len(bez_mean_man13))
if len(bez_mean_man14) < len(bez_date1):
    length = len(bez_mean_man14)
    for i in range(len(bez_date1) - length):
        bez_mean_man14.append(sum(bez_mean_man14) / len(bez_mean_man14))
elif len(bez_mean_man14) > len(bez_date1):
    raz = len(bez_mean_man14) - len(bez_date1)
    bez_mean_man14 = bez_mean_man14[:len(bez_mean_man14) - raz]
if len(bez_mean_man15) < len(bez_date1):
    length = len(bez_mean_man15)
    for i in range(len(bez_date1) - length):
        bez_mean_man15.append(sum(bez_mean_man15) / len(bez_mean_man15))
if len(bez_mean_man16) < len(bez_date1):
    length = len(bez_mean_man16)
    for i in range(len(bez_date1) - length):
        bez_mean_man16.append(sum(bez_mean_man16) / len(bez_mean_man16))
if len(bez_mean_man21) < len(bez_date2):
    length = len(bez_mean_man21)
    for i in range(len(bez_date2) - length):
        bez_mean_man21.append(sum(bez_mean_man21) / len(bez_mean_man21))
if len(bez_mean_man22) < len(bez_date2):
    length = len(bez_mean_man22)
    for i in range(len(bez_date2) - length):
        bez_mean_man22.append(sum(bez_mean_man22) / len(bez_mean_man22))
if len(bez_mean_man23) < len(bez_date2):
    length = len(bez_mean_man23)
    for i in range(len(bez_date2) - length):
        bez_mean_man23.append(sum(bez_mean_man23) / len(bez_mean_man23))
if len(bez_mean_man24) < len(bez_date2):
    length = len(bez_mean_man24)
    for i in range(len(bez_date2) - length):
        bez_mean_man24.append(sum(bez_mean_man24) / len(bez_mean_man24))
if len(bez_mean_man25) < len(bez_date2):
    length = len(bez_mean_man25)
    for i in range(len(bez_date2) - length):
        bez_mean_man25.append(sum(bez_mean_man25) / len(bez_mean_man25))
if len(bez_mean_man26) < len(bez_date2):
    length = len(bez_mean_man26)
    for i in range(len(bez_date2) - length):
        bez_mean_man26.append(sum(bez_mean_man26) / len(bez_mean_man26))
if len(bez_mean_man31) < len(bez_date3):
    length = len(bez_mean_man31)
    for i in range(len(bez_date3) - length):
        bez_mean_man31.append(sum(bez_mean_man31) / len(bez_mean_man31))
if len(bez_mean_man32) < len(bez_date3):
    length = len(bez_mean_man32)
    for i in range(len(bez_date3) - length):
        bez_mean_man32.append(sum(bez_mean_man32) / len(bez_mean_man32))
if len(bez_mean_man33) < len(bez_date3):
    length = len(bez_mean_man33)
    for i in range(len(bez_date3) - length):
        bez_mean_man33.append(sum(bez_mean_man33) / len(bez_mean_man33))
if len(bez_mean_man34) < len(bez_date3):
    length = len(bez_mean_man34)
    for i in range(len(bez_date3) - length):
        bez_mean_man34.append(sum(bez_mean_man34) / len(bez_mean_man34))
if len(bez_mean_man35) < len(bez_date3):
    length = len(bez_mean_man35)
    for i in range(len(bez_date3) - length):
        bez_mean_man35.append(sum(bez_mean_man35) / len(bez_mean_man35))
if len(bez_mean_man36) < len(bez_date3):
    length = len(bez_mean_man36)
    for i in range(len(bez_date3) - length):
        bez_mean_man36.append(sum(bez_mean_man36) / len(bez_mean_man36))
if len(bez_mean_man41) < len(bez_date4):
    length = len(bez_mean_man41)
    for i in range(len(bez_date4) - length):
        bez_mean_man41.append(sum(bez_mean_man41) / len(bez_mean_man41))
if len(bez_mean_man42) < len(bez_date4):
    length = len(bez_mean_man42)
    for i in range(len(bez_date4) - length):
        bez_mean_man42.append(sum(bez_mean_man42) / len(bez_mean_man42))
if len(bez_mean_man43) < len(bez_date4):
    length = len(bez_mean_man43)
    for i in range(len(bez_date4) - length):
        bez_mean_man43.append(sum(bez_mean_man43) / len(bez_mean_man43))
if len(bez_mean_man44) < len(bez_date4):
    length = len(bez_mean_man44)
    for i in range(len(bez_date4) - length):
        bez_mean_man44.append(sum(bez_mean_man44) / len(bez_mean_man44))
if len(bez_mean_man45) < len(bez_date4):
    length = len(bez_mean_man45)
    for i in range(len(bez_date4) - length):
        bez_mean_man45.append(sum(bez_mean_man45) / len(bez_mean_man45))
if len(bez_mean_man46) < len(bez_date4):
    length = len(bez_mean_man46)
    for i in range(len(bez_date4) - length):
        bez_mean_man46.append(sum(bez_mean_man46) / len(bez_mean_man46))

if len(rez_mean_man11) < len(rez_date1):
    length = len(rez_mean_man11)
    for i in range(len(rez_date1) - length):
        rez_mean_man11.append(sum(rez_mean_man11) / len(rez_mean_man11))
if len(rez_mean_man12) < len(rez_date1):
    length = len(rez_mean_man12)
    for i in range(len(rez_date1) - length):
        rez_mean_man12.append(sum(rez_mean_man12) / len(rez_mean_man12))
if len(rez_mean_man13) < len(rez_date1):
    length = len(rez_mean_man13)
    for i in range(len(rez_date1) - length):
        rez_mean_man13.append(sum(rez_mean_man13) / len(rez_mean_man13))
if len(rez_mean_man14) < len(rez_date1):
    length = len(rez_mean_man14)
    for i in range(len(rez_date1) - length):
        rez_mean_man14.append(sum(rez_mean_man14) / len(rez_mean_man14))
if len(rez_mean_man15) < len(rez_date1):
    length = len(rez_mean_man15)
    for i in range(len(rez_date1) - length):
        rez_mean_man15.append(sum(rez_mean_man15) / len(rez_mean_man15))
if len(rez_mean_man16) < len(rez_date1):
    length = len(rez_mean_man16)
    for i in range(len(rez_date1) - length):
        rez_mean_man16.append(sum(rez_mean_man16) / len(rez_mean_man16))
if len(rez_mean_man21) < len(rez_date2):
    length = len(rez_mean_man21)
    for i in range(len(rez_date2) - length):
        rez_mean_man21.append(sum(rez_mean_man21) / len(rez_mean_man21))
if len(rez_mean_man22) < len(rez_date2):
    length = len(rez_mean_man22)
    for i in range(len(rez_date2) - length):
        rez_mean_man22.append(sum(rez_mean_man22) / len(rez_mean_man22))
if len(rez_mean_man23) < len(rez_date2):
    length = len(rez_mean_man23)
    for i in range(len(rez_date2) - length):
        rez_mean_man23.append(sum(rez_mean_man23) / len(rez_mean_man23))
if len(rez_mean_man24) < len(rez_date2):
    length = len(rez_mean_man24)
    for i in range(len(rez_date2) - length):
        rez_mean_man24.append(sum(rez_mean_man24) / len(rez_mean_man24))
if len(rez_mean_man25) < len(rez_date2):
    length = len(rez_mean_man25)
    for i in range(len(rez_date2) - length):
        rez_mean_man25.append(sum(rez_mean_man25) / len(rez_mean_man25))
if len(rez_mean_man26) < len(rez_date2):
    length = len(rez_mean_man26)
    for i in range(len(rez_date2) - length):
        rez_mean_man26.append(sum(rez_mean_man26) / len(rez_mean_man26))
if len(rez_mean_man31) < len(rez_date3):
    length = len(rez_mean_man31)
    for i in range(len(rez_date3) - length):
        rez_mean_man31.append(sum(rez_mean_man31) / len(rez_mean_man31))
if len(rez_mean_man32) < len(rez_date3):
    length = len(rez_mean_man32)
    for i in range(len(rez_date3) - length):
        rez_mean_man32.append(sum(rez_mean_man32) / len(rez_mean_man32))
if len(rez_mean_man33) < len(rez_date3):
    length = len(rez_mean_man33)
    for i in range(len(rez_date3) - length):
        rez_mean_man33.append(sum(rez_mean_man33) / len(rez_mean_man33))
if len(rez_mean_man34) < len(rez_date3):
    length = len(rez_mean_man34)
    for i in range(len(rez_date3) - length):
        rez_mean_man34.append(sum(rez_mean_man34) / len(rez_mean_man34))
if len(rez_mean_man35) < len(rez_date3):
    length = len(rez_mean_man35)
    for i in range(len(rez_date3) - length):
        rez_mean_man35.append(sum(rez_mean_man35) / len(rez_mean_man35))
if len(rez_mean_man36) < len(rez_date3):
    length = len(rez_mean_man36)
    for i in range(len(rez_date3) - length):
        rez_mean_man36.append(sum(rez_mean_man36) / len(rez_mean_man36))
if len(rez_mean_man41) < len(rez_date4):
    length = len(rez_mean_man41)
    for i in range(len(rez_date4) - length):
        rez_mean_man41.append(sum(rez_mean_man41) / len(rez_mean_man41))
if len(rez_mean_man42) < len(rez_date4):
    length = len(rez_mean_man42)
    for i in range(len(rez_date4) - length):
        rez_mean_man42.append(sum(rez_mean_man42) / len(rez_mean_man42))
if len(rez_mean_man43) < len(rez_date4):
    length = len(rez_mean_man43)
    for i in range(len(rez_date4) - length):
        rez_mean_man43.append(sum(rez_mean_man43) / len(rez_mean_man43))
if len(rez_mean_man44) < len(rez_date4):
    length = len(rez_mean_man44)
    for i in range(len(rez_date4) - length):
        rez_mean_man44.append(sum(rez_mean_man44) / len(rez_mean_man44))
if len(rez_mean_man45) < len(rez_date4):
    length = len(rez_mean_man45)
    for i in range(len(rez_date4) - length):
        rez_mean_man45.append(sum(rez_mean_man45) / len(rez_mean_man45))
if len(rez_mean_man46) < len(rez_date4):
    length = len(rez_mean_man46)
    for i in range(len(rez_date4) - length):
        rez_mean_man46.append(sum(rez_mean_man46) / len(rez_mean_man46))

col = ["Дата"]
for v in bez_man1:
    col.append(v)
bez_man_res1 = pd.DataFrame(columns=col)
bez_man_res1["Дата"] = bez_date1
col = ["Дата"]
for v in bez_man2:
    col.append(v)
bez_man_res2 = pd.DataFrame(columns=col)
bez_man_res2["Дата"] = bez_date2
col = ["Дата"]
for v in bez_man3:
    col.append(v)
bez_man_res3 = pd.DataFrame(columns=col)
bez_man_res3["Дата"] = bez_date3
col = ["Дата"]
for v in bez_man4:
    col.append(v)
bez_man_res4 = pd.DataFrame(columns=col)
bez_man_res4["Дата"] = bez_date4

col = ["Дата"]
for v in rez_man1:
    col.append(v)
rez_man_res1 = pd.DataFrame(columns=col)
rez_man_res1["Дата"] = rez_date1
col = ["Дата"]
for v in rez_man2:
    col.append(v)
rez_man_res2 = pd.DataFrame(columns=col)
rez_man_res2["Дата"] = rez_date2
col = ["Дата"]
for v in rez_man3:
    col.append(v)
rez_man_res3 = pd.DataFrame(columns=col)
rez_man_res3["Дата"] = rez_date3
col = ["Дата"]
for v in rez_man4:
    col.append(v)
rez_man_res4 = pd.DataFrame(columns=col)
rez_man_res4["Дата"] = rez_date4

bez_man_res1[bez_man1[0]] = bez_mean_man11
bez_man_res1[bez_man1[1]] = bez_mean_man12
bez_man_res1[bez_man1[2]] = bez_mean_man13
bez_man_res1[bez_man1[3]] = bez_mean_man14
bez_man_res1[bez_man1[4]] = bez_mean_man15
bez_man_res1[bez_man1[5]] = bez_mean_man16

bez_man_res2[bez_man2[0]] = bez_mean_man21
bez_man_res2[bez_man2[1]] = bez_mean_man22
bez_man_res2[bez_man2[2]] = bez_mean_man23
bez_man_res2[bez_man2[3]] = bez_mean_man24
bez_man_res2[bez_man2[4]] = bez_mean_man25
bez_man_res2[bez_man2[5]] = bez_mean_man26

bez_man_res3[bez_man3[0]] = bez_mean_man31
bez_man_res3[bez_man3[1]] = bez_mean_man32
bez_man_res3[bez_man3[2]] = bez_mean_man33
bez_man_res3[bez_man3[3]] = bez_mean_man34
bez_man_res3[bez_man3[4]] = bez_mean_man35
bez_man_res3[bez_man3[5]] = bez_mean_man36

bez_man_res4[bez_man4[0]] = bez_mean_man41
bez_man_res4[bez_man4[1]] = bez_mean_man42
bez_man_res4[bez_man4[2]] = bez_mean_man43
bez_man_res4[bez_man4[3]] = bez_mean_man44
bez_man_res4[bez_man4[4]] = bez_mean_man45
bez_man_res4[bez_man4[5]] = bez_mean_man46

rez_man_res1[rez_man1[0]] = rez_mean_man11
rez_man_res1[rez_man1[1]] = rez_mean_man12
rez_man_res1[rez_man1[2]] = rez_mean_man13
rez_man_res1[rez_man1[3]] = rez_mean_man14
rez_man_res1[rez_man1[4]] = rez_mean_man15
rez_man_res1[rez_man1[5]] = rez_mean_man16

rez_man_res2[rez_man2[0]] = rez_mean_man21
rez_man_res2[rez_man2[1]] = rez_mean_man22
rez_man_res2[rez_man2[2]] = rez_mean_man23
rez_man_res2[rez_man2[3]] = rez_mean_man24
rez_man_res2[rez_man2[4]] = rez_mean_man25
rez_man_res2[rez_man2[5]] = rez_mean_man26

rez_man_res3[rez_man3[0]] = rez_mean_man31
rez_man_res3[rez_man3[1]] = rez_mean_man32
rez_man_res3[rez_man3[2]] = rez_mean_man33
rez_man_res3[rez_man3[3]] = rez_mean_man34
rez_man_res3[rez_man3[4]] = rez_mean_man35
rez_man_res3[rez_man3[5]] = rez_mean_man36

rez_man_res4[rez_man4[0]] = rez_mean_man41
rez_man_res4[rez_man4[1]] = rez_mean_man42
rez_man_res4[rez_man4[2]] = rez_mean_man43
rez_man_res4[rez_man4[3]] = rez_mean_man44
rez_man_res4[rez_man4[4]] = rez_mean_man45
rez_man_res4[rez_man4[5]] = rez_mean_man46


fig3_1 = go.Figure()
fig3_1.add_trace(go.Scatter(
    name=bez_man1[0],
    mode="lines+markers", x=bez_man_res1["Дата"].values, y=bez_man_res1[bez_man1[0]].values,
    xperiodalignment="end"
))
fig3_1.add_trace(go.Scatter(
    name=bez_man1[1],
    mode="lines+markers", x=bez_man_res1["Дата"].values, y=bez_man_res1[bez_man1[1]].values,
    xperiodalignment="end"
))
fig3_1.add_trace(go.Scatter(
    name=bez_man1[2],
    mode="lines+markers", x=bez_man_res1["Дата"].values, y=bez_man_res1[bez_man1[2]].values,
    xperiodalignment="end"
))
fig3_1.add_trace(go.Scatter(
    name=bez_man1[3],
    mode="lines+markers", x=bez_man_res1["Дата"].values, y=bez_man_res1[bez_man1[3]].values,
    xperiodalignment="end"
))
fig3_1.add_trace(go.Scatter(
    name=bez_man1[4],
    mode="lines+markers", x=bez_man_res1["Дата"].values, y=bez_man_res1[bez_man1[4]].values,
    xperiodalignment="end"
))
fig3_1.add_trace(go.Scatter(
    name=bez_man1[5],
    mode="lines+markers", x=bez_man_res1["Дата"].values, y=bez_man_res1[bez_man1[5]].values,
    xperiodalignment="end"
))
fig3_1.add_trace(go.Bar(
    name="Среднее значение цены на безрецептурные препараты 1 сегмента",
    x=bez_man_res1["Дата"].values, y=bez_mean1,
    xperiodalignment="middle"
))
fig3_1.update_xaxes(showgrid=True, ticklabelmode="period")
fig3_1.update_layout(title="Сравнение средних цен на безрецептурные препараты в 1 сегменте (стоимость > 1000 руб)", xaxis_title="Дата", yaxis_title="Средняя цена, руб")


fig3_2 = go.Figure()
fig3_2.add_trace(go.Scatter(
    name=bez_man2[0],
    mode="lines+markers", x=bez_man_res2["Дата"].values, y=bez_man_res2[bez_man2[0]].values,
    xperiodalignment="end"
))
fig3_2.add_trace(go.Scatter(
    name=bez_man2[1],
    mode="lines+markers", x=bez_man_res2["Дата"].values, y=bez_man_res2[bez_man2[1]].values,
    xperiodalignment="end"
))
fig3_2.add_trace(go.Scatter(
    name=bez_man2[2],
    mode="lines+markers", x=bez_man_res2["Дата"].values, y=bez_man_res2[bez_man2[2]].values,
    xperiodalignment="end"
))
fig3_2.add_trace(go.Scatter(
    name=bez_man2[3],
    mode="lines+markers", x=bez_man_res2["Дата"].values, y=bez_man_res2[bez_man2[3]].values,
    xperiodalignment="end"
))
fig3_2.add_trace(go.Scatter(
    name=bez_man2[4],
    mode="lines+markers", x=bez_man_res2["Дата"].values, y=bez_man_res2[bez_man2[4]].values,
    xperiodalignment="end"
))
fig3_2.add_trace(go.Scatter(
    name=bez_man2[5],
    mode="lines+markers", x=bez_man_res2["Дата"].values, y=bez_man_res2[bez_man2[5]].values,
    xperiodalignment="end"
))
fig3_2.add_trace(go.Bar(
    name="Среднее значение цены на безрецептурные препараты 2 сегмента",
    x=bez_man_res2["Дата"].values, y=bez_mean2,
    xperiodalignment="middle"
))
fig3_2.update_xaxes(showgrid=True, ticklabelmode="period")
fig3_2.update_layout(title="Сравнение средних цен на безрецептурные препараты в 2 сегменте (стоимость от 500 до 1000 руб)", xaxis_title="Дата", yaxis_title="Средняя цена, руб")


fig3_3 = go.Figure()
fig3_3.add_trace(go.Scatter(
    name=bez_man3[0],
    mode="lines+markers", x=bez_man_res3["Дата"].values, y=bez_man_res3[bez_man3[0]].values,
    xperiodalignment="end"
))
fig3_3.add_trace(go.Scatter(
    name=bez_man3[1],
    mode="lines+markers", x=bez_man_res3["Дата"].values, y=bez_man_res3[bez_man3[1]].values,
    xperiodalignment="end"
))
fig3_3.add_trace(go.Scatter(
    name=bez_man3[2],
    mode="lines+markers", x=bez_man_res3["Дата"].values, y=bez_man_res3[bez_man3[2]].values,
    xperiodalignment="end"
))
fig3_3.add_trace(go.Scatter(
    name=bez_man3[3],
    mode="lines+markers", x=bez_man_res3["Дата"].values, y=bez_man_res3[bez_man3[3]].values,
    xperiodalignment="end"
))
fig3_3.add_trace(go.Scatter(
    name=bez_man3[4],
    mode="lines+markers", x=bez_man_res3["Дата"].values, y=bez_man_res3[bez_man3[4]].values,
    xperiodalignment="end"
))
fig3_3.add_trace(go.Scatter(
    name=bez_man3[5],
    mode="lines+markers", x=bez_man_res3["Дата"].values, y=bez_man_res3[bez_man3[5]].values,
    xperiodalignment="end"
))
fig3_3.add_trace(go.Bar(
    name="Среднее значение цены на безрецептурные препараты 3 сегмента",
    x=bez_man_res3["Дата"].values, y=bez_mean3,
    xperiodalignment="middle"
))
fig3_3.update_xaxes(showgrid=True, ticklabelmode="period")
fig3_3.update_layout(title="Сравнение средних цен на безрецептурные препараты в 3 сегменте (стоимость от 100 до 500 руб)", xaxis_title="Дата", yaxis_title="Средняя цена, руб")


fig3_4 = go.Figure()
fig3_4.add_trace(go.Scatter(
    name=bez_man4[0],
    mode="lines+markers", x=bez_man_res4["Дата"].values, y=bez_man_res4[bez_man4[0]].values,
    xperiodalignment="end"
))
fig3_4.add_trace(go.Scatter(
    name=bez_man4[1],
    mode="lines+markers", x=bez_man_res4["Дата"].values, y=bez_man_res4[bez_man4[1]].values,
    xperiodalignment="end"
))
fig3_4.add_trace(go.Scatter(
    name=bez_man4[2],
    mode="lines+markers", x=bez_man_res4["Дата"].values, y=bez_man_res4[bez_man4[2]].values,
    xperiodalignment="end"
))
fig3_4.add_trace(go.Scatter(
    name=bez_man4[3],
    mode="lines+markers", x=bez_man_res4["Дата"].values, y=bez_man_res4[bez_man4[3]].values,
    xperiodalignment="end"
))
fig3_4.add_trace(go.Scatter(
    name=bez_man4[4],
    mode="lines+markers", x=bez_man_res4["Дата"].values, y=bez_man_res4[bez_man4[4]].values,
    xperiodalignment="end"
))
fig3_4.add_trace(go.Scatter(
    name=bez_man4[5],
    mode="lines+markers", x=bez_man_res4["Дата"].values, y=bez_man_res4[bez_man4[5]].values,
    xperiodalignment="end"
))
fig3_4.add_trace(go.Bar(
    name="Среднее значение цены на безрецептурные препараты 4 сегмента",
    x=bez_man_res4["Дата"].values, y=bez_mean4,
    xperiodalignment="middle"
))
fig3_4.update_xaxes(showgrid=True, ticklabelmode="period")
fig3_4.update_layout(title="Сравнение средних цен на безрецептурные препараты в 4 сегменте (стоимость < 100 руб)", xaxis_title="Дата", yaxis_title="Средняя цена, руб")

fig3_5 = go.Figure()
fig3_5.add_trace(go.Scatter(
    name=rez_man1[0],
    mode="lines+markers", x=rez_man_res1["Дата"].values, y=rez_man_res1[rez_man1[0]].values,
    xperiodalignment="end"
))
fig3_5.add_trace(go.Scatter(
    name=rez_man1[1],
    mode="lines+markers", x=rez_man_res1["Дата"].values, y=rez_man_res1[rez_man1[1]].values,
    xperiodalignment="end"
))
fig3_5.add_trace(go.Scatter(
    name=rez_man1[2],
    mode="lines+markers", x=rez_man_res1["Дата"].values, y=rez_man_res1[rez_man1[2]].values,
    xperiodalignment="end"
))
fig3_5.add_trace(go.Scatter(
    name=rez_man1[3],
    mode="lines+markers", x=rez_man_res1["Дата"].values, y=rez_man_res1[rez_man1[3]].values,
    xperiodalignment="end"
))
fig3_5.add_trace(go.Scatter(
    name=rez_man1[4],
    mode="lines+markers", x=rez_man_res1["Дата"].values, y=rez_man_res1[rez_man1[4]].values,
    xperiodalignment="end"
))
fig3_5.add_trace(go.Scatter(
    name=rez_man1[5],
    mode="lines+markers", x=rez_man_res1["Дата"].values, y=rez_man_res1[rez_man1[5]].values,
    xperiodalignment="end"
))
fig3_5.add_trace(go.Bar(
    name="Среднее значение цены на рецептурные препараты 1 сегмента",
    x=rez_man_res1["Дата"].values, y=rez_mean1,
    xperiodalignment="middle"
))
fig3_5.update_xaxes(showgrid=True, ticklabelmode="period")
fig3_5.update_layout(title="Сравнение средних цен на рецептурные препараты в 1 сегменте (стоимость > 1000 руб)", xaxis_title="Дата", yaxis_title="Средняя цена, руб")


fig3_6 = go.Figure()
fig3_6.add_trace(go.Scatter(
    name=rez_man2[0],
    mode="lines+markers", x=rez_man_res2["Дата"].values, y=rez_man_res2[rez_man2[0]].values,
    xperiodalignment="end"
))
fig3_6.add_trace(go.Scatter(
    name=rez_man2[1],
    mode="lines+markers", x=rez_man_res2["Дата"].values, y=rez_man_res2[rez_man2[1]].values,
    xperiodalignment="end"
))
fig3_6.add_trace(go.Scatter(
    name=rez_man2[2],
    mode="lines+markers", x=rez_man_res2["Дата"].values, y=rez_man_res2[rez_man2[2]].values,
    xperiodalignment="end"
))
fig3_6.add_trace(go.Scatter(
    name=rez_man2[3],
    mode="lines+markers", x=rez_man_res2["Дата"].values, y=rez_man_res2[rez_man2[3]].values,
    xperiodalignment="end"
))
fig3_6.add_trace(go.Scatter(
    name=rez_man2[4],
    mode="lines+markers", x=rez_man_res2["Дата"].values, y=rez_man_res2[rez_man2[4]].values,
    xperiodalignment="end"
))
fig3_6.add_trace(go.Scatter(
    name=rez_man2[5],
    mode="lines+markers", x=rez_man_res2["Дата"].values, y=rez_man_res2[rez_man2[5]].values,
    xperiodalignment="end"
))
fig3_6.add_trace(go.Bar(
    name="Среднее значение цены на рецептурные препараты 2 сегмента",
    x=rez_man_res2["Дата"].values, y=rez_mean2,
    xperiodalignment="middle"
))
fig3_6.update_xaxes(showgrid=True, ticklabelmode="period")
fig3_6.update_layout(title="Сравнение средних цен на рецептурные препараты в 2 сегменте (стоимость от 500 до 1000 руб)", xaxis_title="Дата", yaxis_title="Средняя цена, руб")


fig3_7 = go.Figure()
fig3_7.add_trace(go.Scatter(
    name=rez_man3[0],
    mode="lines+markers", x=rez_man_res3["Дата"].values, y=rez_man_res3[rez_man3[0]].values,
    xperiodalignment="end"
))
fig3_7.add_trace(go.Scatter(
    name=rez_man3[1],
    mode="lines+markers", x=rez_man_res3["Дата"].values, y=rez_man_res3[rez_man3[1]].values,
    xperiodalignment="end"
))
fig3_7.add_trace(go.Scatter(
    name=rez_man3[2],
    mode="lines+markers", x=rez_man_res3["Дата"].values, y=rez_man_res3[rez_man3[2]].values,
    xperiodalignment="end"
))
fig3_7.add_trace(go.Scatter(
    name=rez_man3[3],
    mode="lines+markers", x=rez_man_res3["Дата"].values, y=rez_man_res3[rez_man3[3]].values,
    xperiodalignment="end"
))
fig3_7.add_trace(go.Scatter(
    name=rez_man3[4],
    mode="lines+markers", x=rez_man_res3["Дата"].values, y=rez_man_res3[rez_man3[4]].values,
    xperiodalignment="end"
))
fig3_7.add_trace(go.Scatter(
    name=rez_man3[5],
    mode="lines+markers", x=rez_man_res3["Дата"].values, y=rez_man_res3[rez_man3[5]].values,
    xperiodalignment="end"
))
fig3_7.add_trace(go.Bar(
    name="Среднее значение цены на рецептурные препараты 3 сегмента",
    x=rez_man_res3["Дата"].values, y=rez_mean3,
    xperiodalignment="middle"
))
fig3_7.update_xaxes(showgrid=True, ticklabelmode="period")
fig3_7.update_layout(title="Сравнение средних цен на рецептурные препараты в 3 сегменте (стоимость от 100 до 500 руб)", xaxis_title="Дата", yaxis_title="Средняя цена, руб")


fig3_8 = go.Figure()
fig3_8.add_trace(go.Scatter(
    name=rez_man4[0],
    mode="lines+markers", x=rez_man_res4["Дата"].values, y=rez_man_res4[rez_man4[0]].values,
    xperiodalignment="end"
))
fig3_8.add_trace(go.Scatter(
    name=rez_man4[1],
    mode="lines+markers", x=rez_man_res4["Дата"].values, y=rez_man_res4[rez_man4[1]].values,
    xperiodalignment="end"
))
fig3_8.add_trace(go.Scatter(
    name=rez_man4[2],
    mode="lines+markers", x=rez_man_res4["Дата"].values, y=rez_man_res4[rez_man4[2]].values,
    xperiodalignment="end"
))
fig3_8.add_trace(go.Scatter(
    name=rez_man4[3],
    mode="lines+markers", x=rez_man_res4["Дата"].values, y=rez_man_res4[rez_man4[3]].values,
    xperiodalignment="end"
))
fig3_8.add_trace(go.Scatter(
    name=rez_man4[4],
    mode="lines+markers", x=rez_man_res4["Дата"].values, y=rez_man_res4[rez_man4[4]].values,
    xperiodalignment="end"
))
fig3_8.add_trace(go.Scatter(
    name=rez_man4[5],
    mode="lines+markers", x=rez_man_res4["Дата"].values, y=rez_man_res4[rez_man4[5]].values,
    xperiodalignment="end"
))
fig3_8.add_trace(go.Bar(
    name="Среднее значение цены на рецептурные препараты 4 сегмента",
    x=rez_man_res4["Дата"].values, y=rez_mean4,
    xperiodalignment="middle"
))
fig3_8.update_xaxes(showgrid=True, ticklabelmode="period")
fig3_8.update_layout(title="Сравнение средних цен на рецептурные препараты в 4 сегменте (стоимость < 100 руб)", xaxis_title="Дата", yaxis_title="Средняя цена, руб")
