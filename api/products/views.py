from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from pymongo import MongoClient
import re


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

	mongo_client = MongoClient(host=settings.MONGO_HOST, port=settings.MONGO_PORT)
	mongo_db = mongo_client[settings.MONGO_NAME]
	db = mongo_db[category.lower()]

	rSearch = search
	rBrand = brand
	in_stock = in_stock.lower()
	if search != '*':
		search = '.*'+search+'.*'
		rSearch = re.compile(search, re.IGNORECASE)
	if brand is not None:
		brand = '.*'+brand+'.*'
		rBrand = re.compile(brand, re.IGNORECASE)
	else:
		rBrand = re.compile(".*")
	if in_stock == 'false' or in_stock == 'true':
		results = db.find({"$and": [
						{"$or":[{'title':rSearch},{'description':rSearch}]},
							{'brand':rBrand},
							{'inStock':in_stock}
						]},{'_id':False})[:count]
	else:
		results = db.find({"$and": [
							{"$or":[{'title':rSearch},{'description':rSearch}]},
							{'brand':rBrand}
						]},{'_id': False})[:count]
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
