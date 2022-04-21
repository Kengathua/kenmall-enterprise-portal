from django.test import TestCase

from kenmall_enterprise_portal.debit.models import (
    Brand, Category, Inventory, Item, ItemAttribute,
    ItemModel, ItemUnits, Product, Sales, Section, Stock, Units)

from model_bakery import baker


class TestSection(TestCase):

    def test_create_section(self):
        sec = baker.make(Section, section_name='Section A', section_type='KITCHEN')

        assert sec
        assert Section.objects.count() == 1


class TestCategory(TestCase):

    def test_create_category(self):
        sec = baker.make(Section, section_name='Section A', section_type='KITCHEN')
        cat = baker.make(Category, section=sec, category_name='Cat A')

        assert cat
        assert Category.objects.count() == 1


class TestBrand(TestCase):

    def test_create_category(self):
        brand = baker.make(Brand, brand_name='Brand A')

        assert brand
        assert Brand.objects.count() == 1


class TestItemModel(TestCase):

    def test_create_item_model(self):
        sec = baker.make(Section, section_name='Section A', section_type='KITCHEN')
        cat = baker.make(Category, section=sec, category_name='Cat A')
        brand = baker.make(Brand, brand_name='Brand A')
        model = baker.make(ItemModel, category=cat, brand=brand, model_name='JSFPOEUTE 560')

        assert model
        assert ItemModel.objects.count() == 1


class TestUnits(TestCase):

    def test_create_unit(self):
        sec = baker.make(Section, section_name='Section A', section_type='KITCHEN')
        cat = baker.make(Category, section=sec, category_name='Cat A')
        units = baker.make(Units, units_name='UNITS', units_code = 'FHF-001')
        units.category.set([cat])
        units.save()
        assert units
        assert Units.objects.count() == 1


class TestItem(TestCase):

    def test_create_item(self):
        sec = baker.make(Section, section_name='Section A', section_type='KITCHEN')
        cat = baker.make(Category, section=sec, category_name='Cat A')
        brand = baker.make(Brand, brand_name='Brand A')
        model = baker.make(ItemModel, category=cat, brand=brand, model_name='JSFPOEUTE 560')
        units = baker.make(Units, units_name='UNITS')
        units.category.set([cat])
        units.save()

        item = baker.make(Item, model=model, make_year=2020)
        assert item
        assert Item.objects.count() == 1


class TestItemUnits(TestCase):

    def test_create_item_units(self):
        sec = baker.make(Section, section_name='Section A', section_type='KITCHEN')
        cat = baker.make(Category, section=sec, category_name='Cat A')
        brand = baker.make(Brand, brand_name='Brand A')
        model = baker.make(ItemModel, category=cat, brand=brand, model_name='JSFPOEUTE 560')
        s_units = baker.make(Units, units_name='SALES UNITS')
        s_units.category.set([cat])
        s_units.save()

        p_units = baker.make(Units, units_name='PURCHASES UNITS')
        p_units.category.set([cat])
        p_units.save()

        item = baker.make(Item, model=model, make_year=2020)
        item_units = baker.make(ItemUnits, item=item, sales_units=s_units, purchases_units=p_units, items_per_purchase_unit=1)

        assert item_units
        assert ItemUnits.objects.count() == 1


class TestItemAttribute(TestCase):

    def test_create_item_attribute(self):
        sec = baker.make(Section, section_name='Section A', section_type='KITCHEN')
        cat = baker.make(Category, section=sec, category_name='Cat A')
        brand = baker.make(Brand, brand_name='Brand A')
        model = baker.make(ItemModel, category=cat, brand=brand, model_name='JSFPOEUTE 560')
        units = baker.make(Units, units_name='UNITS')
        units.category.set([cat])
        units.save()
        item = baker.make(Item, model=model, make_year=2020)
        item_attr = baker.make(ItemAttribute, item=item, attribute_type='SPECIAL OFFER', attribute_value='Special Offer')
        assert item_attr
        assert ItemAttribute.objects.count() == 1


class TestInventory(TestCase):

    def test_create_inventory_record(self):
        sec = baker.make(Section, section_name='Section A', section_type='KITCHEN')
        cat = baker.make(Category, section=sec, category_name='Cat A')
        brand = baker.make(Brand, brand_name='Brand A')
        model = baker.make(ItemModel, category=cat, brand=brand, model_name='JSFPOEUTE 560')
        units = baker.make(Units, units_name='UNITS')
        units.category.set([cat])
        units.save()
        item = baker.make(Item, model=model, make_year=2020)
        baker.make(ItemAttribute, item=item, attribute_type='SPECIAL OFFER', attribute_value='Special Offer')
        inventory_record = baker.make(Inventory, item=item, unit_price=10000, quantity_added=5)
        assert inventory_record
        assert Inventory.objects.count() == 1


class TestProduct(TestCase):

    def test_create_product(self):
        sec = baker.make(Section, section_name='Section A', section_type='KITCHEN')
        cat = baker.make(Category, section=sec, category_name='Cat A')
        brand = baker.make(Brand, brand_name='Brand A')
        model = baker.make(ItemModel, category=cat, brand=brand, model_name='JSFPOEUTE 560')
        units = baker.make(Units, units_name='UNITS')
        units.category.set([cat])
        units.save()
        item = baker.make(Item, model=model, make_year=2020)
        baker.make(ItemAttribute, item=item, attribute_type='SPECIAL OFFER', attribute_value='Special Offer')
        inventory_record = baker.make(Inventory, item=item, unit_price=10000, quantity_added=5)
        Product.objects.all().delete()
        product = baker.make(Product, inventory=inventory_record,)

        assert product
        assert Product.objects.count() == 1


class TestSales(TestCase):

    def test_create_sales_record(self):
        sec = baker.make(Section, section_name='Section A', section_type='KITCHEN')
        cat = baker.make(Category, section=sec, category_name='Cat A')
        brand = baker.make(Brand, brand_name='Brand A')
        model = baker.make(ItemModel, category=cat, brand=brand, model_name='JSFPOEUTE 560')
        units = baker.make(Units, units_name='UNITS')
        units.category.set([cat])
        units.save()
        item = baker.make(Item, model=model, make_year=2020)
        baker.make(ItemAttribute, item=item, attribute_type='SPECIAL OFFER', attribute_value='Special Offer')
        sales_record = baker.make(Sales, item=item, amount=20000, quantity=2)
        assert sales_record
        assert Sales.objects.count() == 1


class TestStock(TestCase):

    def test_create_stock_record(self):
        sec = baker.make(Section, section_name='Section A', section_type='KITCHEN')
        cat = baker.make(Category, section=sec, category_name='Cat A')
        brand = baker.make(Brand, brand_name='Brand A')
        model = baker.make(ItemModel, category=cat, brand=brand, model_name='JSFPOEUTE 560')
        units = baker.make(Units, units_name='UNITS')
        units.category.set([cat])
        units.save()
        item = baker.make(Item, model=model, make_year=2020)
        baker.make(ItemAttribute, item=item, attribute_type='SPECIAL OFFER', attribute_value='Special Offer')
        inventory_record = baker.make(Inventory, item=item, unit_price=10000, quantity_added=5)
        Stock.objects.all().delete()
        stock_record = baker.make(Stock, inventory_item=inventory_record, )
        assert stock_record
        assert Stock.objects.count() == 1
