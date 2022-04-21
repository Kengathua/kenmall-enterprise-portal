"""Debit side models file."""
import math
from pyexpat import model
import uuid

from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models import CASCADE, PROTECT
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError

from kenmall_enterprise_portal.common.models import AbstractBase, ToEDIAbstractBase
from kenmall_enterprise_portal.whitelists.models import Whitelist

ITEM_ATTRIBUTE_TYPES = (
    ('SPECIAL OFFER', 'SPECIAL OFFER'),
    ('SPECIAL FEATURE', 'SPECIAL FEATURE'),
    ('SPECIFICATION', 'SPECIFICATION'),
    ('DESCRIPTION', 'DESCRIPTION')
)

UNITS_TYPE = (
    ('SALE', 'SALE'),
    ('PURCHASE', 'PURCHASE')
)


PRODUCT_STATUS_CHOICES = (
    ('AVAILABLE', 'AVAILABLE'),
    ('SOLD', 'SOLD'),
    ('DAMAGED', 'DAMAGED')
)


LIVING_ROOM = 'LIVING ROOM'
AVAILABLE = 'AVAILABLE'

ON_SALE_STATUSES = ['AVAILABLE', 'ON DEPOSIT']


def captalize_field(field_names):
    for field_name in field_names:
        val = getattr(field_name, False)
        if val:
            setattr(field_name, val.upper())

class Section(AbstractBase):
    """Sections for items."""
    section_name = models.CharField(
        null=False, blank=False, max_length=250)
    section_code = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        """Meta class for section model"""

        ordering = ['-section_name']


class Category(AbstractBase):
    """Item categories model eg. Electronics, Jewellery."""
    section = models.ForeignKey(
        Section, null=False, blank=False, on_delete=PROTECT)
    category_name = models.CharField(max_length=300)
    category_code = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        """Meta class for category."""

        ordering = ['-section', '-category_name']

class ItemType(AbstractBase):
    """Item types model eg TV, Fridge."""
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    type_name = models.CharField(max_length=300)
    type_code = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        """Meta class for item type model."""

        ordering = ['-category', '-type_name']

class Brand(AbstractBase):
    """Item brand model for items eg. Samsung, LG."""
    item_type = models.ForeignKey(ItemType, on_delete=models.PROTECT)
    brand_name = models.CharField(max_length=250)
    brand_code = models.CharField(max_length=250, null=True, blank=True)

    @property
    def categories(self):
        """Get categories related to this brand."""
        models = ItemModel.objects.filter(brand=self)
        categories = []
        for model in models:
            categories.append(model.category.category_name)
        
        return categories

    class Meta:
        """Meta class for item brands."""

        ordering = ['-brand_name']


class ItemModel(AbstractBase):
    """Item models model"""
    category = models.ForeignKey(
        Category, null=False, blank=False, on_delete=PROTECT)
    brand = models.ForeignKey(
        Brand, null=False, blank=False, on_delete=PROTECT)
    model_name = models.CharField(max_length=250)
    model_code = models.CharField(max_length=250, null=True, blank=True)

    def clean(self) -> None:
        return super().clean()

    class Meta:
        """Meta class for item models."""

        ordering = ['-model_name']


class Units(ToEDIAbstractBase):
    category = models.ManyToManyField(Category)  # TV, Fridge
    units_name = models.CharField(
        null=False, blank=False, max_length=300)
    units_code = models.CharField(
        null=True, blank=True, max_length=250)

    def clean(self) -> None:
        return super().clean()


    class Meta:
        """Meta class dor item measure units."""

        ordering = ['-units_name']


@receiver(post_save, sender=Units)
def units_post_save(sender, instance, **kwargs):
    unpushed_units = sender.objects.filter(pushed_to_edi = False)
    for entry in unpushed_units.values('category'):
        if entry['category']:
            pass
            # push_units_to_edi()

    # if kwargs['created']:
    #     pass


class Item(AbstractBase):
    model = models.OneToOneField(
        ItemModel, null=False, blank=False, on_delete=PROTECT)
    barcode = models.CharField(
        null=False, blank=False, max_length=250)
    item_code = models.CharField(
        max_length=250, null=True, blank=True)
    item_name = models.CharField(
        max_length=250, null=True, blank=True)
    make_year = models.IntegerField(null=True, blank=True)

    def get_item_name(self):
        category = self.model.category.category_name
        brand = self.model.brand.brand_name
        model = self.model.model_name

        item_name = brand + ' ' + model + ' ' + category
        self.item_name = item_name

    def clean(self) -> None:
        self.get_item_name()
        return super().clean()

    class Meta:
        """Meta class for items."""

        ordering = ['-item_name']


class ItemUnits(AbstractBase):
    item = models.ForeignKey(
        Item, null=False, blank=False, on_delete=CASCADE)
    sales_units = models.ForeignKey(
        Units, null=False, blank=False,
        related_name='selling_units', on_delete=PROTECT)  # eg Dozen
    purchases_units = models.ForeignKey(
        Units, null=False, blank=False,
        related_name='purchasing_units', on_delete=PROTECT)  # eg Pieces
    items_per_purchase_unit = models.FloatField()           # eg 12


class ItemAttribute(AbstractBase):
    item = models.ForeignKey(
        Item, null=False, blank=False, on_delete=CASCADE)
    attribute_type = models.CharField(
        max_length=300, choices=ITEM_ATTRIBUTE_TYPES)
    attribute_value = models.TextField()

    @property
    def special_features(self):
        attributes = self.__class__.objects.filter(
            item=self.item, attribute_type='SPECIAL FEATURE')
        special_features = []

        for attribute in attributes:
            special_features.append(attribute.attribute_value)
        
        return special_features

    @property
    def special_offers(self):
        attributes = self.__class__.objects.filter(
            item=self.item, attribute_type='SPECIAL OFFER')
        special_offers = []

        for attribute in attributes:
            special_offers.append(attribute.attribute_value)
        
        return special_offers
    
    @property
    def specifications(self):
        attributes = self.__class__.objects.filter(
            item=self.item, attribute_type='SPECIFICATION')
        specifications = []

        for attribute in attributes:
            specifications.append(attribute.attribute_value)

        return specifications
    
    @property
    def description(self):
        attributes = self.__class__.objects.filter(
            item=self.item, attribute_type='DESCRIPTION')
        description = []

        for attribute in attributes:
            description.append(attribute.attribute_value)

        return description

    class Meta:
        """Meta class for Item attributes."""

        ordering = ['-attribute_type', '-attribute_value']


class ItemImage(AbstractBase):
    item = models.ForeignKey(
        Item, null=False, blank=False, on_delete=CASCADE)
    image = models.ImageField()
    hero_product_image = models.BooleanField(default=False)

    # clean to check if no item image has been selected
    # set the first image to be the hero image

    def update_hero_product_image(self):
        """The newly selected image as the
        hero image will be the default hero image."""
        if self.hero_product_image: # check if its calid during test
            item_images = self.__class__.objects.filter(item=self.item)

            for item_image in item_images:
                if item_image.hero_product_image:
                    item_image.hero_product_image = False
                    item_image.save()

    def clean(self) -> None:
        return super().clean()


class Inventory(AbstractBase):
    item = models.ForeignKey(
        Item, null=False, blank=False, on_delete=PROTECT)
    on_sale = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    unit_price = models.FloatField()
    quantity_added = models.FloatField(null=True, blank=True)
    quantity_removed = models.FloatField(null=True, blank=True)
    added_total = models.FloatField(null=True, blank=True)
    opening_stock = models.FloatField(default=0)
    in_stock = models.FloatField(null=True, blank=True)
    opening_total = models.FloatField(default=0)
    in_stock_total = models.FloatField(null=True, blank=True)

    def calculate_added_total(self):
        self.added_total = self.quantity_added * self.unit_price

    def calculate_in_stock(self):
        if self.quantity_added:
            self.in_stock = self.opening_stock + float(self.quantity_added)

    def calculate_in_stock_total(self):
        self.in_stock_total = self.opening_total + self.added_total


    def clean(self) -> None:
        self.calculate_added_total()
        self.calculate_in_stock()
        self.calculate_in_stock_total()
        return super().clean()
    # retain previous closing total as opening or 0 if if none

    class Meta:
        """Meta class for inventory."""

        ordering = ['item']


def add_inventory_item_as_new_products(enterprise, created_on, created_by, updated_on, updated_by, instance):
    if instance.on_sale:
        fraction_quantity, whole_quantities = math.modf(instance.quantity_added)

        if whole_quantities:
            for whole_quantity in range(int(whole_quantities)):
                slug = slugify(instance.item.item_name + '_' + str(uuid.uuid4()))
                Product.objects.get_or_create(
                    enterprise=enterprise, created_on=created_on,
                    created_by=created_by, updated_on=updated_on,
                    updated_by=updated_by, inventory=instance,
                    quantity=1, slug=slug)

        if fraction_quantity:
            slug = slugify(instance.item.item_name + '_' + str(uuid.uuid4()))
            Product.objects.get_or_create(
                enterprise=enterprise, created_on=created_on,
                created_by=created_by, updated_on=updated_on,
                updated_by=updated_by, inventory=instance,
                quantity=fraction_quantity, slug=slug)


def update_stock(enterprise, created_on, created_by, updated_on, updated_by, instance):
    if instance.on_sale:
        stock = Stock.objects.update_or_create(
            enterprise=enterprise, created_on=created_on,
            created_by=created_by, updated_on=updated_on,
            updated_by=updated_by, inventory_item=instance
        )
        assert stock


@receiver(post_save, sender=Inventory)
def auto_update_stock(sender, instance, **kwargs):
    """Signal to process stock upon addition or deduction of items from inventory."""
    enterprise = instance.enterprise
    created_on = instance.created_on
    created_by = instance.created_by
    updated_on = instance.updated_on
    updated_by = instance.updated_by

    if kwargs['created']:
        pass
        # add_inventory_item_as_new_products(enterprise, created_on, created_by, updated_on, updated_by, instance)
        # update_stock(enterprise, created_on, created_by,
        #             updated_on, updated_by, instance)


class Product(AbstractBase):
    """Inventory product model to identify each item."""
    inventory = models.ForeignKey(
        Inventory, null=False, blank=False, on_delete=PROTECT)
    product_code = models.CharField(
        null=True, blank=True, max_length=250, unique=True)
    quantity = models.FloatField(default=1)
    slug = models.SlugField(max_length=1500)
    status = models.CharField(
        null=True, blank=True, max_length=250, choices=PRODUCT_STATUS_CHOICES,
        default=AVAILABLE)
    is_on_sale = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    @property
    def specifications(self):
        """Produce a list of specifications"""
        specifications = []

        item_specifications = ItemAttribute.objects.filter(
            item=self.inventory.item, attribute_type='SPECIFICATION')

        for item_specification in item_specifications:
            specifications.append(item_specification.attribute_value)

        return specifications

    def check_fail_unique_product_code(self, product_code):
        """Validate that product_code is unique."""
        check_fail = False
        if self.__class__.objects.filter(product_code=product_code).exists():
            check_fail = True

        return check_fail

    def generate_product_code_id(self, item, ignore_code_ids):
        """Generate an item code."""
        id = 1
        product_exists = self.__class__.objects.filter(
            inventory=self.inventory).exists()

        if product_exists:
            count = self.__class__.objects.filter(
                inventory=self.inventory).count()
            last = self.__class__.objects.filter(
                inventory=self.inventory).order_by('created_on')[count-1]
            last_product_code = last.product_code
            last_product_code_id = int(last_product_code.split('/')[2])
            id += last_product_code_id

        for code_id in ignore_code_ids:
            if id == int(code_id):
                id = id + 1

        code = ''
        if id < 10:
            code = '0{}'.format(id)
        else:
            code = str(id)

        return code

    def get_abbreviations(self, item):
        category_values = item.model.category.category_name.split()
        category_name_abbrv = ''

        if category_values != []:
            for value in category_values:
                category_name_abbrv += value[0].upper()

        item_values = item.item_name.split()
        item_name_abbrv = ''
        if item_values != []:
            for value in item_values:
                item_name_abbrv += value[0].upper()

        return category_name_abbrv, item_name_abbrv

    def generate_product_code(self, category, item, ignore_code_ids):
        """Auto generate item code."""
        category_abbrv, item_abbrv = self.get_abbreviations(item)
        rejected_product_codes = []
        product_code_id = self.generate_product_code_id(item, ignore_code_ids)
        product_code = 'EAG-P/{}-{}/00{}'.format(item_abbrv,
                                                 category_abbrv, product_code_id)

        if self.check_fail_unique_product_code(product_code):
            ignore_code_ids.append(product_code_id)
            rejected_product_codes.append(product_code)
            product_code = self.generate_product_code(category, item, ignore_code_ids)  # noqa

        return product_code

    def auto_create_product_code(self):
        """Check and create an product code for new item."""
        if not self.product_code:
            item = self.inventory.item
            category = self.inventory.item.model.category
            ignore_code_ids = ['0']
            product_code = self.generate_product_code(
                category, item, ignore_code_ids)

            self.product_code = product_code

    def add_product_to_whitelist(self):
        """Add product as a whitelist item."""
        if self.is_on_sale:
            if not Whitelist.objects.filter(product_code=self.product_code).exists():
                enterprise = self.enterprise
                created_on = self.created_on
                created_by = self.created_by
                updated_on = self.updated_on
                updated_by = self.updated_by

                whitelist = Whitelist.objects.get_or_create(
                    enterprise=enterprise, created_on=created_on,
                    created_by=created_by, updated_on=updated_on,
                    updated_by=updated_by, product_code=self.product_code,
                    is_available=True)

                assert whitelist

    def slugify_slug_field(self):
        """Slugify the slug field."""
        if not self.slug or self.slug == '':
            self.slug = slugify(
                self.inventory.item.item_name + '_' + str(uuid.uuid4()))

    def validate_item_on_sale_is_available(self):
        if self.is_on_sale and not self.status in ON_SALE_STATUSES:
            msg = 'Please confirm that {} is available'.format(
                self.inventory.item.item_name)
            raise ValidationError(
                {'on sale': msg}
            )

    def clean(self) -> None:
        """Clean product entries."""
        self.slugify_slug_field()
        self.auto_create_product_code()
        self.add_product_to_whitelist()
        self.validate_item_on_sale_is_available()
        # Validate that the quatity is less than one or else raise validation error
        return super().clean()


class Sales(AbstractBase):
    """Sales model."""
    item = models.ForeignKey(
        Item, null=False, blank=False, on_delete=PROTECT)
    amount = models.FloatField()
    quantity = models.FloatField()
    total = models.FloatField(null=True, blank=True)
    sell_date = models.DateField(default=timezone.now)

    def calculate_total(self):
        """Get sales total."""
        self.total = self.amount * self.quantity

    def clean(self) -> None:
        """Clean sales records."""
        self.calculate_total()
        return super().clean()

    class Meta:
        """Meta class for sales"""

        ordering = ['-sell_date']


class Stock(AbstractBase):
    """Stock model."""
    inventory_item = models.OneToOneField(
        Inventory, null=False, blank=False, unique=True,
        on_delete=PROTECT)
    quantity_of_available = models.FloatField(default=0)
    quantity_on_deposit = models.FloatField(default=0)
    quantity_total = models.FloatField(default=0)
    total_of_available = models.FloatField(
        null=True, blank=True)
    total_on_deposit = models.FloatField(
        null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    difference = models.FloatField(null=True, blank=True)


    def get_stock_quantities(self):
        """Get quantity of stock from products on sale."""
        if Inventory.objects.filter(item=self.inventory_item.item).exists():
            all_products = Product.objects.filter(
                inventory=self.inventory_item, status__in=ON_SALE_STATUSES)
            available_products = Product.objects.filter(
                inventory=self.inventory_item, status='AVAILABLE')
            on_deposit_products = Product.objects.filter(
                inventory=self.inventory_item, status='ON DEPOSIT')

            no_available_products = 0
            for available_product in available_products:
                no_available_products += available_product.quantity
            
            no_on_deposit_products = 0
            for on_deposit_product in on_deposit_products:
                no_on_deposit_products += on_deposit_product.quantity


            self.quantity_of_available = no_available_products
            self.quantity_on_deposit = no_on_deposit_products
            self.quantity_total = no_available_products - no_on_deposit_products


    def get_stock_totals(self):
        if Inventory.objects.filter(item=self.inventory_item.item).exists():

            available_products = Product.objects.filter(
                inventory=self.inventory_item, status='AVAILABLE')
            on_deposit_products = Product.objects.filter(
                inventory=self.inventory_item, status='ON DEPOSIT')

            available_products_prices = []
            for product in available_products:
                price = product.inventory.unit_price * product.quantity
                available_products_prices.append(price)

            on_deposit_products_prices = []
            for product in on_deposit_products:
                price = product.inventory.unit_price * product.quantity
                on_deposit_products_prices.append(price)

            total_of_available = sum(available_products_prices)
            total_on_deposit = sum(on_deposit_products_prices)
            total = total_of_available + total_on_deposit
            in_stock_total = self.inventory_item.in_stock_total

            self.total_of_available = total_of_available
            self.total_on_deposit = total_on_deposit
            self.total = total
            self.difference = self.total - in_stock_total

    def clean(self) -> None:
        self.get_stock_quantities()
        self.get_stock_totals()
        return super().clean()
