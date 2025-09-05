# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SandbergscraperPipeline:
    def process_item(self, item, spider):
        #just  an exemple XD
        adapter = ItemAdapter(item)

        field_names = adapter.field_names()

        value = adapter.get("price")
        adapter["price"] = value.strip()
        ##herei can processs each item ..
        #later on work .
        return item
