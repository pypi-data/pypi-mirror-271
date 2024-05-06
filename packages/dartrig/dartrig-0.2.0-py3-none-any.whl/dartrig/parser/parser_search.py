from datetime import datetime
import re
from bs4 import BeautifulSoup


class SearchNode:
    def __init__(self, reporter="", dt="", code="", pop_id="", pop_link="", cls="", rcp_no="", param2="",
                 link="", id="", title="", is_mod_content="", is_mod_attach=""):
        self.reporter = reporter
        self.dt = dt
        self.code = code
        self.pop_id = pop_id
        self.pop_link = pop_link
        self.cls = cls
        self.rcp_no = rcp_no
        self.param2 = param2
        self.link = link
        self.id = id
        self.title = title
        self.is_mod_content = is_mod_content
        self.is_mod_attach = is_mod_attach
        self.collect_dt = datetime.now()

    def __str__(self):
        return f"reporter : {self.reporter}, dt : {self.dt}, code : {self.code}, pop_id : {self.pop_id}, pop_link : {self.pop_link}, cls : {self.cls}, rcp_no : {self.rcp_no}, param2 : {self.param2}, link : {self.link}, id : {self.id}, title : {self.title}, is_mod_content : {self.is_mod_content}, is_mod_attach : {self.is_mod_attach}, collect_dt : {self.collect_dt.strftime('%Y-%m-%d %H:%M:%S')}"

class SearchResult:
    def __init__(self, total_page, current_page, total_count, items):
        self.total_page = total_page
        self.current_page = current_page
        self.total_count = total_count
        self.items = items

    def __str__(self):
        items_str = "\n".join([str(item) for item in self.items])
        return (f"total_page : {self.total_page}, current_page : {self.current_page}, total_count : {self.total_count}, \n"
                f"items : [{items_str}]")

    @staticmethod
    def parse(html):
        soup = BeautifulSoup(html, "html.parser")
        wrap = SearchResult._parse_wrap(soup)
        items = SearchResult._parse_items(soup)
        return SearchResult(**wrap, items=items)

    @staticmethod
    def _parse_wrap(soup):
        regex = r"\[(?P<current_page>\d*)\/(?P<total_page>\d*)\]\s\[.\s(?P<total_count>[,\d]*).\]"

        wrap = soup.find("div", id="psWrap")
        m = re.match(regex, wrap.find("div", "pageInfo").text)
        page_info = m.groupdict()
        for k, v in page_info.items():
            page_info[k] = int(v.replace(",", ""))
        return page_info

    @staticmethod
    def _parse_items(soup):
        tbody = soup.find("tbody", id="tbody")

        trs = tbody.select("tr")
        return [SearchResult._parse_tr2info(tr) for tr in trs]

    @staticmethod
    def __parse_td1(td):
        wrap = td.find("span", "innerWrap")
        wrapTag = td.find("span", "innerWrapTag")
        regex = ".*openCorpInfoNew\('(?P<code>\d*)', '(?P<pop_id>[a-zA-Z]*)', '(?P<pop_link>[\/a-zA-Z0-9.]*)'\);.*"

        w = wrap if wrap else wrapTag

        if w:
            spans = w.select("span")
            ahref = w.find("a")["href"]
            m = re.match(regex, ahref)
            link_info = m.groupdict() if m else {}
            link_info["cls"] = spans[0]["title"]
            return link_info

    @staticmethod
    def __parse_td2(td):
        a = td.find("a")
        ahref = a["href"]
        aid = a["id"]
        aonclick = a["onclick"]

        regex = ".*openReportViewer\('(?P<rcp_no>\d*)','(?P<param2>.*)'\);.*"
        m = re.match(regex, aonclick)
        params = m.groupdict() if m else {}

        params["link"] = ahref
        params["id"] = aid
        params["title"] = a.text.strip().replace("\n", "").replace("\t", "")
        return params

    @staticmethod
    def _parse_tr2info(tr):
        tds = tr.select("td")
        info = {
            # 'seq': tds[0].text.strip(),
            'reporter': tds[3].text.strip(),
            'dt': tds[4].text.strip()
        }
        td1 = SearchResult.__parse_td1(tds[1])
        td2 = SearchResult.__parse_td2(tds[2])
        info.update(td1)
        info.update(td2)
        info["is_mod_content"] = "기재정정" in info.get("title")
        info["is_mod_attach"] = "첨부정정" in info.get("title")
        return SearchNode(**info)