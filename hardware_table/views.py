import urllib.request
import json

from django.shortcuts import render
from django.http import HttpResponse

#from hardware_table.models import HardwareModule




# =============================
JSON_SPARES = 'https://job.firstvds.ru/spares.json'
JSON_ALTS = 'https://job.firstvds.ru/alternatives.json'

# =============================
def get_data_from_url(url):
	request = urllib.request.urlopen(url)
	result = json.loads(request.read().decode('utf-8'))
	
	return result
	
# =============================
def parse_and_calc_data():
	spares = get_data_from_url(JSON_SPARES)
	alts = get_data_from_url(JSON_ALTS)
	
	# список уже обработанных модулей (запчастей) из JSON_ALTS
	added = []
	
	# =================================
	table_data = [] # имя_модуля, сколько_должно_быть, текущее_кол-во, заказано, выделить_красным_в_таблице
	
	# проход по "списку" взаимозаменяемости
	for altname, item in alts['alternatives'].items():
		mustbe = []
		count = []
		arrive = []
		
		for modname in item:
			if not spares.get(modname) is None:
				mustbe.append(spares[modname]['mustbe'])
				count.append(spares[modname]['count'])
				arrive.append(spares[modname]['arrive'])
				
				added.append(modname)

		else:
			mustbe = max(mustbe)
			color = True if mustbe > sum(count + arrive) else False
			
			table_data.append((altname, mustbe, sum(count), sum(arrive), color))
	
	# =================================
	# проход по основному списку
	for sparename, item in spares.items():
		if sparename in added:
			continue
		
		mustbe = item['mustbe']
		count = item['count']
		arrive = item['arrive']
		color = True if mustbe > count+arrive else False
				
		table_data.append((sparename, mustbe, count, arrive, color))
	
	table_data = sorted(table_data)
	
	# =================================
	return table_data
	
# =============================
def hw_need_buy(request):
	table_data = parse_and_calc_data()
	
	# =================================
	need_data = {}  # словарь с модулями, которые необходимо докупить и их количеством
	# расчитываем кол-во модулей, которое необходимо докупить
	for sparename, mustbe, count, arrive, color in table_data:
		if color:
			need = mustbe - count+arrive
			need_data[sparename] = {'count' : need}
	
	# =================================	
	return HttpResponse(json.dumps(need_data), content_type="application/json")

# =============================
def index(request):
	# получаем данные
	table_data = parse_and_calc_data()
	# =================================
	template = 'hardware_table/hardware_table.html'

	context = {
		'data' : table_data,
	}
	
	return render(request, template, context)
