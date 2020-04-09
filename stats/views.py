from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
import requests
import pandas as pd
from .models import Entry

def index(request):
	all_entries= Entry.objects.all()
	template = loader.get_template('stats/stats.html')
	grand_total=0
	grand_deaths=0
	grand_recovered=0
	for entry in all_entries:
		grand_total+=entry.total_cases
		grand_recovered+=entry.recovered
		grand_deaths+=entry.deaths

	grand_active = grand_total - grand_recovered - grand_deaths
	context = { 'all_entries': all_entries, 'grand_total': grand_total,'grand_active' : grand_active, 'grand_deaths' : grand_deaths, 'grand_recovered' : grand_recovered, }
	return HttpResponse(template.render(context, request))

def loadData(request):
	url = 'https://www.mohfw.gov.in/'
	html = requests.get(url).content
	df_list = pd.read_html(html)
	df = df_list[-1]
	df = df[:-2]
	df.columns = ['serial', 'place' , 'total_cases', 'recovered', 'deaths']
	print(df.to_dict('records'))
	Entry.objects.all().delete()
	Entry.objects.bulk_create(
		Entry(**vals) for vals in df.to_dict('records')
		)
	return redirect(index)


