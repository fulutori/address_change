import sys
import re

addr_list = open("japan.csv", "rt", encoding="utf-8")  #都道府県の緯度経度情報と住所が結び付けられたもの
town_dic = {} #都道府県、市区町村別に一意の住所を格納

for addr in addr_list:
	addr = addr.replace('\n', '')
	addr = addr.split(",")
	target = addr[0]+addr[1]+addr[2]
	if addr[0] in town_dic: #都道府県すでに存在するとき
		if addr[1] in town_dic[addr[0]]: #市区町村がすでに存在するとき
			if addr[2] in town_dic[addr[0]][addr[1]]: #町域がすでに登録されているとき
				pass
			else:
				town_dic[addr[0]][addr[1]].append(addr[2]) #町域を登録
		else:
			town_dic[addr[0]][addr[1]] = [] #市区町村の中にリストを作成
			town_dic[addr[0]][addr[1]].append(addr[2]) #都道府県の辞書の中に市区町村を登録
	else:
		town_dic[addr[0]] = {} #辞書を都道府県名で作成
		town_dic[addr[0]][addr[1]] = [] #都道府県名の辞書の中にリストを市区町村名で作成
		town_dic[addr[0]][addr[1]].append(addr[2]) #町域を登録
addr_list.close()
#print(town_dic)

f = open("town_list_sj_new.csv","a", encoding="shift_jis")
#f = open("town_list_new.csv","a", encoding="utf-8")
for pref in town_dic: #CSVファイルに書き出し
	for city in town_dic[pref]:
		for town in town_dic[pref][city]:
			f.write(pref+","+city+","+town+",0"+"\n")
f.close()