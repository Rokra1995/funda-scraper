from scrapy.exporters import CsvItemExporter
from funda.settings import CSV_SEP

#Custom exporter to be able to change the seperator in the settings.py file
# © Robin Kratschmayr
class CsvCustomSeperator(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        kwargs['encoding'] = 'utf-8'
        kwargs['delimiter'] = CSV_SEP
        super(CsvCustomSeperator, self).__init__(*args, **kwargs)