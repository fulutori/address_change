import sys
import re

addr_list = open("japan.csv", "r", encoding="utf-8") #都道府県の緯度経度情報と住所が結び付けられたもの
fp = open("x-ken-all.csv", "r", encoding="shift_jis") #住所とその郵便番号が結び付けられたもの
sin_kyu_list = open("sin-kyu.csv", "r", encoding="utf-8") #新字と旧字の対応表
zipno_dic = {} #郵便番号用辞書
kanji_dic = {} #新旧字用辞書

#新旧字の対応表から辞書を作成する
for kanji in sin_kyu_list:
	kanji = kanji.replace("\n","")
	kanji = kanji.split(",")
	kanji_dic[kanji[1]] = kanji[0]
sin_kyu_list.close()

#住所と郵便番号のCSVファイルから辞書を作成
for line in fp:
	line = line.replace(' ', '')
	line = line.replace('"', '')
	line = line.replace('\n', '')
	cells = line.split(",")
	zipno = cells[0] # 郵便番号
	ken = cells[1] # 都道府県
	shi = cells[2] # 市区
	cho = cells[3] # 市区以下
	title = ken + shi + cho
	zipno_dic[title] = zipno
fp.close()

cnt = 0
moji_cnt = 0
e_flag = 0
for addr in addr_list:
	addr = addr.replace('\n', '')
	addr = addr.split(",")
	ken = addr[0]
	shi = addr[1]
	cho = addr[2]
	target = ken+shi+cho
	if target in zipno_dic: #住所をzipno_dicで検索
		moji_cnt += 1
		continue
	else:
		old_target = target
		target = re.sub(r'[一二三四五六七八九十]丁目',"",target) #住所から「〇丁目」を削除する
		target = re.sub(r'[一二三四五六七八九十]丁',"",target)
		if target in zipno_dic: #「〇丁目」を削除した住所をzipno_dicで検索
			moji_cnt += 1
			continue
		else:
			for t in range(len(target)):
				if target[t] in kanji_dic: #住所に旧字が含まれているか調べる
					target = target.replace(target[t],kanji_dic[target[t]]) #旧字を新字に変換
					if target in zipno_dic: #旧字を新字に変換した住所をzipno_dicで検索
						moji_cnt += 1
						e_flag = 1
						break
			if e_flag == 1: #新旧字変換して郵便番号がヒットしたら次の住所へ
				e_flag = 0
				continue

			for i in range(len(addr[2])+1): #町域を先頭から一文字ずつ削って検索
				text = cho[i:]
				target = ken+shi+text
				if target in zipno_dic:
					moji_cnt += 1
					e_flag = 1
					break
			if e_flag == 1:
				e_flag = 0
				continue

			for i in range(len(addr[2])+1): #町域を末尾から一文字ずつ削って検索
				text = cho[-i:]
				target = ken+shi+text
				if target in zipno_dic:
					moji_cnt += 1
					e_flag = 1
					break
			if e_flag == 1:
				e_flag = 0
				continue
			else: #あらゆる手段を用いても郵便番号がヒットしなかったとき
				target = ken + shi #市で検索
				if target in zipno_dic:
					moji_cnt += 1
				else:
					cnt+=1
addr_list.close()
print(cnt)
print(moji_cnt)