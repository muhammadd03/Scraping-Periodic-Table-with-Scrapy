###########################################################################################################
# CAN NOT EXTARCT DATA FROM THE WEBSITE BECAUSE OF SCRAPY-PLAYWRIGHT INCOMPATIBILITY WITH WINDOWS
# AS THE WEBSITE IS A JAVASCRIPT RENDERED WEBSITE
# USE AN ALTERNATIVE .I.E, SPPLASH OR ANY OTHER
# WHEN YOU EXECUTE THE SCRIPT FOR THE FIRST TIME SAVE THE DATA TO AN JSON FILE .I.E, elements.json
###########################################################################################################
import scrapy
from elems.items import PeriodicElementItem
from scrapy.loader import ItemLoader
from scrapy_playwright.page import PageMethod

class PeriodicElementsSpider(scrapy.Spider):
    name = "periodic_elements"
    allowed_domains = ["nih.gov"]

    def start_requests(self):
        yield scrapy.Request('https://pubchem.ncbi.nlm.nih.gov/periodic-table/',
                             meta=dict(
                                 playwright=True,
                                 playwrigth_page_method=[
                                     PageMethod('wait_for_selector', 'div.ptable')
                                 ]
                             ))

    async def parse(self, response):
        for element in response.css('div.ptable div.element'):
            i = ItemLoader(item=PeriodicElementItem(), selector=element)

            i.add_css('symbol', '[data-tooltip="Symbol"]')
            i.add_css('name', '[data-tooltip="Name"]')
            i.add_css('atomic_number', '[data-tooltip="Atmoic Number"]')
            i.add_css('atomic_mass', '[data-tooltip*="Atomic Mass"]')
            i.add_css('chemical_group', '[data-tooltip="Chemical Group Block"]')

            yield i.load_item()




