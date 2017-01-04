from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from pymongo import MongoClient
import re



def getBrands():
	mongo_client = MongoClient(host=settings.MONGO_HOST, port=settings.MONGO_PORT)
	mongo_db = mongo_client[settings.MONGO_NAME]
	db = mongo_db.mobile

	brands = []
	for each in db.find():
		if each['brand'].lower() not in brands:
			brands.append(each['brand'].lower())
	return brands

brands = getBrands()

def normalizeQuery(query):
	if len(query) <= 5:
		return query
	ls = []
	for i in brands:
		if i in query.lower():
			index = query.lower().find(i)
			ls = [query[index:index+len(i)], query[:index]+query[index+len(i):]]
			return ls
	if ls == []:
		for n in query.lower():
			if n.isdigit():
				ind = query.lower().find(n)
				if query[ind-1] != ' ':
					res = query[:ind] + " " + query[ind:]
				else:
					res = query[:ind] + query[ind:]
				return res
	return query

def searchDB(category, rSearch, rBrand, in_stock, count):

	mongo_client = MongoClient(host=settings.MONGO_HOST, port=settings.MONGO_PORT)
	mongo_db = mongo_client[settings.MONGO_NAME]
	db = mongo_db[category.lower()]

	if in_stock == 'false' or in_stock == 'true':
		return db.find({"$and": [
						{"$or":[{'title':rSearch},{'description':rSearch}]},
							{'brand':rBrand},
							{'inStock':in_stock}
						]},{'_id':False})[:count]
	else:
		return db.find({"$and": [
							{"$or":[{'title':rSearch},{'description':rSearch}]},
							{'brand':rBrand}
						]},{'_id': False})[:count]


@csrf_exempt
def getList(request, category):
	response = {}
	if not request.method == "GET":
		response = {'status': 400, 'info': 'Bad Request'}
		return JsonResponse(response)

	if category.lower() not in settings.ALLOWED_CATEGORIES:
		response = {'status': 0, 'info': 'Check the Request Url'}
		return JsonResponse(response)

	search = request.GET.get('search', '')
	brand = request.GET.get('brand', '')
	in_stock = request.GET.get('instock', '')
	count = request.GET.get('count', '')

	search = str(search) if search != '' else '*'
	brand = str(brand) if brand != '' else None
	in_stock = str(in_stock) if in_stock != '' else 'all'
	count = int(count) if count != '' else None

	q = ''
	if search != '*' and len(search) > 5:
		try:
			brand, q = normalizeQuery(search)
		except:
			q = normalizeQuery(search)

	rSearch = search if q == '' else q
	rBrand = brand
	in_stock = in_stock.lower()
	print rSearch
	if search != '*':
		rSearch = '.*'+rSearch+'.*'
		rSearch = re.compile(rSearch, re.IGNORECASE)
	if brand is not None:
		brand = '.*'+brand+'.*'
		rBrand = re.compile(brand, re.IGNORECASE)
	else:
		rBrand = re.compile(".*")
	results = searchDB(category=category, rSearch=rSearch, rBrand=rBrand, in_stock=in_stock, count=count)

	if results.count() == 0:
		q = normalizeQuery(search)
		search = '.*'+q+'.*'
		rSearch = re.compile(search, re.IGNORECASE)
		print q
		results = searchDB(category=category, rSearch=rSearch, rBrand=rBrand, in_stock=in_stock, count=count)
		if results.count() == 0:
			try:
				q = q.split()
				prod, mod = q[0], q[1]
				search = prod[0:-1]+" "+prod[-1]+mod
				search = '.*'+search+'.*'
				rSearch = re.compile(search, re.IGNORECASE)
				print q
				results = searchDB(category=category, rSearch=rSearch, rBrand=rBrand, in_stock=in_stock, count=count)
			except Exception as e:
				print str(e)
	response = {}
	response['status'] = 1
	ls = []
	for each in results:
		ls.append(each)
	response['info'] = ls

	return JsonResponse(response)

@csrf_exempt
def getProduct(request, category):
	response = {}
	if not request.method == "GET":
		response = {'status': 400, 'info': 'Bad Request'}
		return JsonResponse(response)

	if category.lower() not in settings.ALLOWED_CATEGORIES:
		response = {'status': 0, 'info': 'Check the Request Url'}
		return JsonResponse(response)

	mongo_client = MongoClient(host=settings.MONGO_HOST, port=settings.MONGO_PORT)
	mongo_db = mongo_client[settings.MONGO_NAME]
	db = mongo_db[category.lower()]

	productId = request.GET.get("productid", "")
	if productId == "":
		response = {'status': 406, 'info': 'insufficient parameters'}
		return JsonResponse(response)
	result = db.find({"productId": productId}, {'_id': False})
	ls = []
	for i in result:
		ls.append(i)
	response = {'status': 1, 'info': ls}
	return JsonResponse(response)
