from openpyxl import load_workbook
from .models import IndicatorDescriptor, IndicatorData
from unidecode import unidecode


class IndicatorManager(object):
	
	def fix_fieldname(self, name):
		"""
		"""
		return unidecode(name).replace(" ", "_")


	def load_meta(self, filename):
		"""
		"""
		wb = load_workbook(filename = filename)
		sheet = wb.get_sheet_by_name('info')
		name = sheet.rows[1][1].value
		code = sheet.rows[0][1].value

		return { 'code':code, 'name':name }


	def load_categories(self):
		"""
		"""


	def load_data(self, filename):
		"""
		"""
		data = []
		wb = load_workbook(filename = filename)
		sheet_data = wb.get_sheet_by_name('dati')	
		header = sheet_data.rows[0]
		fields = []
		for cell in header:
			fieldname = self.fix_fieldname(cell.value)
			fields.append(fieldname)

		for row in sheet_data.rows[1:]:
			obj = dict()
			for i, cell in enumerate(row):
				field_name = fields[i]
				value  = cell.value
				obj[field_name] = value
			data.append(obj)
		return data




	def import_file(self, filename, update=False):
		"""
		"""
		meta = self.load_meta(filename)
		data = self.load_data(filename)

		if not update:
			self.insert_indicator(meta, data)
		else:
			self.update_indicator(meta, data)


	def insert_indicator(self, meta, data):
		"""
		"""
		ind = IndicatorDescriptor(**meta)
		ind.save()

		for d in data:
			d['code'] = meta['code']
			data_item = IndicatorData(**d)
			data_item.save()
			print data_item, d


	
	def update_indicator(self, meta, data):
		"""
		"""
		ind = IndicatorDescriptor.objects.get(code=meta['code'])
		ind.update(**meta)

	
	def drop_indicator(self, code):
		"""
		"""
		ind = IndicatorDescriptor.objects(code=code)
		ind.delete()

		data_items = IndicatorData.objects(code=code)
		data_items.delete()






