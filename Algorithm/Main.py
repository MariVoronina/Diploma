from bs4 import BeautifulSoup
from transliterate import translit
import re
from datetime import date
import pandas as pd
import codecs
from sqlalchemy import create_engine
from sqlalchemy.sql import text


from Utils import *
from Site import *


file = codecs.open( "C:\\WORK\\dictionary_search.txt", "r", "utf-8" )
data = file.read()
drugs_search = eval(data)
file.close()

file = codecs.open( "C:\\WORK\\drugs_search.txt", "r", "utf-8" )
data = file.read()
drug_choices = eval(data)
file.close()

file = codecs.open( "C:\\WORK\\pharmacies.txt", "r", "utf-8" )
data = file.read()
pharmacies_choices = eval(data)
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
    pharmacies = pd.read_sql_table("pharmacies", con=db_conn)


def scraping_cards(search_url, search_item, forbidden_words, search_next_page, search_next, search_page):

    html = get_html(search_url)
    html_search = BeautifulSoup(html, "html.parser")

    if isinstance(search_item, str):
        search_drugs = [search_item, translit(search_item, language_code='ru', reversed=True)]
        if "-" in search_item:
            dr = search_item.split("-")[0]
            for item in search_item.split("-")[1:]:
                dr = dr + f"_{item}"
            search_drugs += [dr, translit(dr, language_code='ru', reversed=True)]
        if " " in search_item:
            dr1 = search_item.split(" ")[0]
            dr2 = search_item.split(" ")[0]
            for item in search_item.split(" ")[1:]:
                dr1 = dr1 + f"_{item}"
                dr2 = dr2 + f"-{item}"
            search_drugs += [dr1, translit(dr1, language_code='ru', reversed=True), dr2,
                             translit(dr2, language_code='ru', reversed=True)]
    else:
        search_drugs = []
        for var in search_item:
            search_drugs += [var, translit(var, language_code='ru', reversed=True)]
            if "-" in var:
                dr = var.split("-")[0]
                for item in var.split("-")[1:]:
                    dr = dr + f"_{item}"
                search_drugs += [dr, translit(dr, language_code='ru', reversed=True)]
            if " " in var:
                dr1 = var.split(" ")[0]
                dr2 = var.split(" ")[0]
                for item in var.split(" ")[1:]:
                    dr1 = dr1 + f"_{item}"
                    dr2 = dr2 + f"-{item}"
                search_drugs += [dr1, translit(dr1, language_code='ru', reversed=True), dr2,
                                 translit(dr2, language_code='ru', reversed=True)]

    haveNext = True
    drugs = []
    n = 0
    while haveNext:
        items_pages = html_search.find_all('a')
        drugs_pages = search_by_words(items_pages, search_drugs)
        if "Редерм" in search_item:
            drugs_pages = [page for page in drugs_pages if not contains_words(page, ["Redermik", "Redermic"])]
        hrefs = [drug.get("href") for drug in drugs_pages if
                     not contains_words(drug, forbidden_words) and find_no_filter(drug)]
        d = [h for h in set(hrefs) if h not in set(drugs)]
        drugs = drugs + d

        pagins = search_by_words(items_pages, search_next_page)
        nexts = search_by_words(set(pagins), search_next)
        if len(nexts) == 0:
            nexts = [page for page in pagins if find_parent_next(page)]

        if len(nexts) == 0:
            if n == 0:
                divs = html_search.find_all('div')
                navig = search_by_words(set(divs), ["navigation", "navigat"])
                if len(navig) == 0:
                    haveNext = False
                else:
                    navig = navig[0]
                    children = list(navig.children)
                    current = [child for child in children if child != "\n" and contains_from(str(child), ['current'])][0]
                    next = [child for child in children if
                            child != "\n" and child.text != "..." and int(child.text) > int(current.text)]
                    if len(next) == 0:
                        haveNext = False
                    else:
                        next = next[0]
                        split_adresss = next.get("href").split("&")
                        next_page = [s for s in split_adresss if contains_from(s, search_page)][0]
                        page_url = search_url + f'&{next_page}'
                        web_search = get_html(page_url)
                        html_search = BeautifulSoup(web_search, "html.parser")
            else:
                haveNext = False

        elif len(nexts) == 1:
            if "wer" in search_url and "_2" in str(nexts[0]):
                haveNext = False
            next = nexts[0]
            if next.get("href") == "":
                haveNext = False
            elif contains_words(next, ["disabled"]) or "disabled" in list(next.attrs.keys()):
                haveNext = False
            else:
                n += 1
                split_adresss = next.get("href").split("&")
                next_page = [s for s in split_adresss if contains_from(s, search_page)][0]
                page_url = search_url + f'&{next_page}'
                web_search = get_html(page_url)
                html_search = BeautifulSoup(web_search, "html.parser")
        else:
            nexts_maybe = [el for el in nexts if el.get("href") != "" and not (
                        contains_words(el, ["disabled"]) or "disabled" in list(el.attrs.keys()))]
            if "wer" in search_url:
                nexts_maybe = [el for el in nexts_maybe if not "_2" in str(el)]
            if len(nexts_maybe) == 0:
                haveNext = False
            else:
                n += 1
                next = nexts_maybe[0]
                split_adresss = next.get("href").split("&")
                next_page = [s for s in split_adresss if contains_from(s, search_page)][0]
                page_url = search_url + f'&{next_page}'
                web_search = get_html(page_url)
                html_search = BeautifulSoup(web_search, "html.parser")

    return drugs


def scraping(pharmacies_search, items_search):
    global drug_choices
    global drugs_search
    global pharmacies_choices

    result_frame = pd.DataFrame(columns=["Дата обращения", "Источник", "Категория", "Бренд/Действующее вещество", "Производитель", "Название", "Цена, руб."])

    search_words = ['search', 'поиск', 'искать', 'найти', "лекарств"]
    forbidden_words = ["price", "review", "отзыв", "same", "similar", "button"]
    search_next_page = ["page", "pager", "pagination"]
    search_next = ["next", "след"]
    search_page = ["page", "pagen"]

    current_date = date.today()
    len_pharm = pharmacies.values[-1][0] + 2

    for pharmacy in pharmacies_search:

        if pharmacy == "Мегаптека" or pharmacy == "ВАптеке":
            url = pharmacies_choices[pharmacy][0]
            search_url_pharm = pharmacies_choices[pharmacy][1]
        else:
            url = pharmacies_choices[pharmacy]
            html = get_html(url)
            soup = BeautifulSoup(html, "html.parser")

            bform = True
            inputs = soup.select('form[method="get"] input')
            search = find_search(inputs, search_words)
            if search is None:
                inputs = soup.select('form input')
                search = find_search(inputs, search_words)
                if search is None:
                    inputs = soup.find_all('input')
                    search = find_search(inputs, search_words)
                    bform = False

            action = '/search/'
            name = ''

            if search is not None:
                attrs = search.attrs
                if 'name' in attrs.keys():
                    name = '?' + search.get('name') + '='

                if bform:
                    p = search.parent
                    while p.name != 'form':
                        p = p.parent
                    action = p.get('action')
                    if action is None:
                        action = '/search/'
                    elif action == ".":
                        action = '/search/'

            search_url_pharm = url + action + name

        for item_search in items_search:


            for key in drug_choices.keys():
                if item_search in drug_choices[key]:
                    category = key
                    break


            if "gorapteka" in search_url_pharm or "wer" in search_url_pharm or "megapteka" in search_url_pharm:
                drugs = []
                for value in drugs_search[item_search]:
                    search_item = value
                    if len(search_item.split(" ")) > 1:
                        search_item_drug = search_item.split(" ")[0]
                        for item in search_item.split(" ")[1:]:
                            search_item_drug = search_item_drug + f"+{item}"
                        search_url = search_url_pharm + search_item_drug
                    else:
                        search_url = search_url_pharm + search_item

                    drugs += scraping_cards(search_url, search_item, forbidden_words, search_next_page, search_next,
                                   search_page)

            else:
                search_item = item_search
                if len(search_item.split(" ")) > 1:
                    search_item_drug = search_item.split(" ")[0]
                    for item in search_item.split(" ")[1:]:
                        search_item_drug = search_item_drug + f"+{item}"
                    search_url = search_url_pharm + search_item_drug
                else:
                    search_url = search_url_pharm + search_item
                drugs = scraping_cards(search_url, drugs_search[item_search], forbidden_words, search_next_page,
                                                search_next,
                                                search_page)

            ######################################################################################################

            for drug in set(drugs):

                card_url = url + drug
                web = get_html(card_url)
                html = BeautifulSoup(web, "html.parser")

                if "vapteke" in card_url:
                    name = html.find_all("h1")[1].text
                else:
                    if "megapteka" in card_url:
                        name = html.find_all("h1")[0].text
                        if contains_from(name, ["Купить", "в аптеках"]):
                            continue
                    else:
                        if len(html.find_all("h1")) == 0:
                            name = "Нет наименования"
                        else:
                            name = html.find_all("h1")[0].text


                spans = html.find_all("span")
                prices = [span for span in spans if contains_all_words(span, ["price", "current"])]
                if len(prices) == 0:
                    prices = [span for span in spans if contains_all_words(span, ["price", "without"])]
                    if len(prices) == 0:
                        prices = [span for span in spans if contains_all_words(span, ["price", "real"])]
                        if len(prices) == 0:
                            divs = html.find_all("div")
                            prices = [div for div in divs if contains_all_words(div, ["price", "current"])]
                            if len(prices) == 0:
                                prices = [div for div in divs if contains_all_words(div, ["price", "without"])]
                                if len(prices) == 0:
                                    prices = [span for span in spans if contains_all_words(span, ["price"])]

                prices = [price for price in prices if not contains_from(str(price), ["bonus", "action"])]

                if len(prices) == 0:
                    price = "Нет предложений"
                else:
                    pr = re.search("\d{1,3}[\u202f\xa0]\d{3}[.,]\d{2}", prices[0].text)
                    if pr is None:
                        pr = re.search("\d{1,3}[\u202f\xa0]\d{1,3}", prices[0].text)
                        if pr is None:
                            pr = re.search("\d{1,3} \d{3}[.,]\d{2}", prices[0].text)
                            if pr is None:
                                pr = re.search("\d{1,3} \d{1,3}", prices[0].text)
                                if pr is None:
                                    pr = re.search("\d{1,10}[.,]\d{2}", prices[0].text)
                                    if pr is None:
                                        pr = re.search("\d{1,10}", prices[0].text)
                                        if pr is None:
                                            price = "Нет предложений"
                                        else:
                                            price = pr.group(0)
                                    else:
                                        price = pr.group(0)
                                else:
                                    price = pr.group(0).replace(" ", "")
                            else:
                                price = pr.group(0).replace(" ", "")
                        else:
                            price = pr.group(0).replace("\u202f", "").replace("\xa0", "")
                    else:
                        price = pr.group(0).replace("\u202f", "").replace("\xa0", "")

                if price != "Нет предложений":
                    price = float(price.replace(",", "."))

                if "vn1" in url or "megapteka" in url:
                    h2s = html.find_all("h2")
                    sib1 = search_by_words(h2s, ["Производитель"])
                    if len(sib1) == 0:
                        if category == "Косметика и БАДы":
                            manufacture = "АО Вертекс"
                        else:
                            manufacture = "Не указан"
                    else:
                        sib1 = sib1[0]
                        sib2 = sib1.next_sibling
                        if sib2 == "\n":
                            sib2 = sib2.next_sibling
                        manufacture = sib2.text
                elif "gorapteka" in url:
                    mn = re.search("/\w{3,25}/", name)
                    if mn is None:
                        mn = re.search("/\w{3,25} \w{3,25}/", name)
                        if mn is None:
                            if category == "Косметика и БАДы":
                                manufacture = "АО Вертекс"
                            else:
                                manufacture = "Не указан"
                        else:
                            manufacture = mn.group(0).replace("/", "", 2)
                    else:
                        manufacture = mn.group(0).replace("/", "", 2)
                elif "vapteke" in url:
                    manufacture = "Пока не понятно как"
                else:
                    divs = html.find_all("div")
                    sibs = search_by_words(divs, ["Производитель"])
                    if len(sibs) == 0:
                        if category == "Косметика и БАДы":
                            manufacture = "АО Вертекс"
                        else:
                            manufacture = "Не указан"
                    else:
                        sibs = [sib for sib in sibs if contains_words(sib, ["name", "title"])]
                        sib1 = sibs[0]
                        sib2 = sib1.next_sibling
                        if sib2 == "\n":
                            sib2 = sib2.next_sibling
                        manufacture = sib2.text

                manufacture = manufacture.replace("\n", "", 50).replace(" ", "", 500).replace("\r", "", 50)
                pharm_var = pharmacies.values
                pharm_var = [var for var in pharm_var if var[3].lower() in manufacture.lower() or translit(var[3].lower(), language_code='ru', reversed=True) in manufacture.lower()]
                if len(pharm_var) == 0:
                    if manufacture != "Неуказан":
                        if "'" in manufacture:
                            manufacture = manufacture.replace("'", "")
                        with engine.connect() as db_conn:
                            db_conn.execute(text(f"insert into pharmacies values ({len_pharm}, '{manufacture}', 'адрес', 'слово')"))
                            db_conn.commit()
                            len_pharm += 1
                            print("ДОБАВЛЕН НОВЫЙ ПРОИЗВОДИТЕЛЬ !!!  ", manufacture)


                    manufacture = "Не указан"
                elif len(pharm_var) == 1:
                    manufacture = pharm_var[0][1]
                else:
                    number = random.choice(range(len(pharm_var)))
                    manufacture = pharm_var[number][1]
                row = [current_date, url, category, item_search, manufacture, name, price]
                result_frame.loc[len(result_frame) + 1] = row

    with engine.connect() as db_conn:
        for idx, row in result_frame.iterrows():
            db_conn.execute(text(
                    f"insert into information values ({row[0]}, '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}', '{row[6]}', '{row[7]}')"))


