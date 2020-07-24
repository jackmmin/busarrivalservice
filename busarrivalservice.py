# 정류소 조회 서비스에서 정류소 번호로 stationId 가져오기
# 가져온 stationId로 버스번호 출력(staOrder 값으로 버스 도착 정보 조회에서 같은 버스 매칭)
# 버스 도착 정보 조회 서비스에서 staOrder로 같은 버스 구분하여 버스의 남은 시간, 남은 좌석 출력

import requests
from bs4 import BeautifulSoup
import sys

class Busarrivalservice:
    def __init__(self):
        self.busstationnum = input("정류장 번호를 입력해주세요. : ")

    # 정류소 조회 서비스 api
    def busstation(self):
        self.busstation_url = 'http://openapi.gbis.go.kr/ws/rest/busstationservice'
        serviceKey = '공공데이터사이트에서 발급받은 키를 입력하세요.'
        # 사용자가 원하는 정류장 번호 입력받기
        busstation_queryParams = '?' + 'serviceKey=' + serviceKey + '&keyword=' + self.busstationnum
        # busstation 결과값 파싱해오기
        url = self.busstation_url + busstation_queryParams
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.content, "html.parser")
        bs_obj_resultcode = bs_obj.select('resultcode')[0].get_text()

        # 만약 제대로된 값을 가져오지 않으면 종료
        if bs_obj_resultcode != '0':
            print("경기 지역의 버스정류장 번호가 아닙니다.")
            sys.exit(1)

        # stationid 저장
        self.bs_obj_stationid = str(bs_obj.stationid)[11:-12]


    # 가져온 stationid로 버스리스트 가져오기
    def buslist(self):
        buslist_queryParams = '/route?' + 'serviceKey=' + 'B%2BDl7oIiROOrq%2BtI3vhlxzj4q684rQu0tU1Ctpj8SnPcfmtFkygehhb5JLKUVNZAIVr%2Bqiq3aFB4mgrVKFyfsA%3D%3D' \
                                 + '&stationId=' + self.bs_obj_stationid
        url = self.busstation_url + buslist_queryParams
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.content, "html.parser")
        self.bs_obj_str = str(bs_obj.msgbody)

    # busroutelist값이 여러 개일 때 각각 변수에 busroutelist 저장
    def busroutelist(self):
        start = 1
        end = 1
        temp1 = []
        while (end - 1 != -1):
            busroutelist_sta = self.bs_obj_str.find('<busroutelist>', start)
            busroutelist_end = self.bs_obj_str.find('</busroutelist>', end)
            start = busroutelist_sta + 1
            end = busroutelist_end + 1
            if end - 1 != -1:
                temp1.append(self.bs_obj_str[busroutelist_sta:busroutelist_end + 15])

        # busroutelist에서 필요한 routename과 staorder 저장
        self.temp11 = []
        for i in temp1:
            busstation_dict = {}
            routename_sta = i.find('<routename>')
            routename_end = i.find('</routename>')
            if routename_sta != -1:
                busstation_dict['routename'] = i[routename_sta + 11:routename_end]

            busstation_staorder_sta = i.find('<staorder>')
            busstation_staorder_end = i.find('</staorder>')
            if busstation_staorder_sta != -1:
                busstation_dict['staorder'] = i[busstation_staorder_sta + 10:busstation_staorder_end]

            self.temp11.append(busstation_dict)

    # 버스 도착 서비스 api
    def busarrival(self):
        self.busarrival_url = 'http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station'

        # busarrival_url를 사용하여 남은 시간 데이터 가져오기
        busarrival_queryParams = '?' + 'serviceKey=' + 'B%2BDl7oIiROOrq%2BtI3vhlxzj4q684rQu0tU1Ctpj8SnPcfmtFkygehhb5JLKUVNZAIVr%2Bqiq3aFB4mgrVKFyfsA%3D%3D' \
                                 + '&stationId=' + self.bs_obj_stationid
        url = self.busarrival_url + busarrival_queryParams
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.content, "html.parser")
        self.bs_obj_str2 = str(bs_obj.msgbody)

    def busarrivallist(self):
        # busarrival값이 여러 개일 때 각각 변수에 busarrivallist 저장
        start = 1
        end = 1
        temp2 = []
        while (end - 1 != -1):
            busarrivallist_sta = self.bs_obj_str2.find('<busarrivallist>', start)
            busarrivallist_end = self.bs_obj_str2.find('</busarrivallist>', end)
            start = busarrivallist_sta + 1
            end = busarrivallist_end + 1
            if end - 1 != -1:
                temp2.append(self.bs_obj_str2[busarrivallist_sta:busarrivallist_end + 17])

        # busarrivallist에서 필요한 predicttime, remainSeatCnt, staorder마다 나누기
        self.temp22 = []
        for k in temp2:
            busarrival_dict = {}

            busarrival_predicttime_sta = k.find('<predicttime1>')
            busarrival_predicttime_end = k.find('</predicttime1>')
            if busarrival_predicttime_sta != -1:
                busarrival_dict['predicttime1'] = k[busarrival_predicttime_sta + 14:busarrival_predicttime_end]

            busarrival_remainSeatCnt_sta = k.find('<remainseatcnt1>')
            busarrival_remainSeatCnt_end = k.find('</remainseatcnt1>')
            if busarrival_remainSeatCnt_sta != -1:
                busarrival_dict['remainseatcnt1'] = k[busarrival_remainSeatCnt_sta + 16:busarrival_remainSeatCnt_end]

            busarrival_staorder_sta = k.find('<staorder>')
            busarrival_staorder_end = k.find('</staorder>')
            if busarrival_staorder_sta != -1:
                busarrival_dict['staorder'] = k[busarrival_staorder_sta + 10:busarrival_staorder_end]

            self.temp22.append(busarrival_dict)

    def start(self):
        # staorder에 해당하는 버스의 남은시간 출력
        print("***" + self.busstationnum + "정류장의 버스 도착 시간 안내" + "***")
        print("(버스이름 : 남은 시간(남은 자리)) ---- 남은 자리(-1:정보없음, 0~:빈자리수).")
        print('-----------------------------------------------------------------')

        for n in self.temp11:
            for m in self.temp22:
                if n['staorder'] == m['staorder']:
                    print(n['routename'] + "번 버스 : " + m['predicttime1'] + "분" + "(" + m['remainseatcnt1'] + "석" + ")")

        print('-----------------------------------------------------------------')

bas = Busarrivalservice()
bas.busstation()
bas.buslist()
bas.busroutelist()
bas.busarrival()
bas.busarrivallist()
bas.start()




# busstation_queryParams = '?' + 'serviceKey='+ 'B%2BDl7oIiROOrq%2BtI3vhlxzj4q684rQu0tU1Ctpj8SnPcfmtFkygehhb5JLKUVNZAIVr%2Bqiq3aFB4mgrVKFyfsA%3D%3D'\
#              + '&stationId=' + '200000078'
#
# busarrival_queryParams = '?' + 'serviceKey='+ 'B%2BDl7oIiROOrq%2BtI3vhlxzj4q684rQu0tU1Ctpj8SnPcfmtFkygehhb5JLKUVNZAIVr%2Bqiq3aFB4mgrVKFyfsA%3D%3D'\
#              + '&stationId=' + '200000078'
#
# url = busarrival_url + busarrival_queryParams
#
# result = requests.get(url)
# bs_obj = BeautifulSoup(result.content, "html.parser")
# print(bs_obj)
# print("곧 도착하는 버스 :", str(bs_obj.plateno1)[10:-11])
# print("운행여부 :", str(bs_obj.flag)[6:-7])
# print("남은 시간 :", str(bs_obj.predicttime1)[14:-15], "분")
# print("남은 자리 :", str(bs_obj.remainseatcnt1)[16:-17])