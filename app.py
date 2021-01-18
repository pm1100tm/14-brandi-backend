import decimal
import datetime

from flask.json    import JSONEncoder
from flask         import Flask
from flask_cors    import CORS

from view import create_endpoints

from model   import OrderDao, OrderDetailDao, EnquiryDao
from service import OrderService, EnquiryService

from model   import SellerInfoDao, SellerDao
from service import SellerService, SellerInfoService, ProductManageService

from model import (
    DestinationDao,
    CartItemDao,
    SenderDao,
    EventDao,
    StoreOrderDao,
    SellerShopDao
)
from service import (
    UserService,
    DestinationService,
    CartItemService,
    SenderService,
    EventService,
    ProductListService,
    StoreOrderService,
    CategoryListService,
    SellerShopService,
    BookmarkService,
    EventListService,
    ProductEnquiryService
)


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime.date):
                return obj.isoformat(sep=' ')
            if isinstance(obj, datetime.datetime):
                return obj.isoformat(sep=' ')
            if isinstance(obj, decimal.Decimal):
                return float(obj)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


class Services:
    pass

class ManageProductService:
    pass


def create_app(test_config=None):
    app = Flask(__name__)
    app.debug = True
    app.json_encoder = CustomJSONEncoder
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    
    # By default, submission of cookies across domains is disabled due to the security implications.
    CORS(app, resources={r'*': {'origins': '*'}})
    
    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)
    
    database = app.config['DB']
    
    # persistence Layer
    destination_dao  = DestinationDao()
    cart_item_dao    = CartItemDao()
    sender_dao       = SenderDao()
    event_dao        = EventDao()
    store_order_dao  = StoreOrderDao()
    order_dao        = OrderDao()
    enquiry_dao      = EnquiryDao()
    seller_shop_dao  = SellerShopDao()
    
    # admin2
    order_detail_dao = OrderDetailDao()
    seller_info_dao = SellerInfoDao()
    
    # service
    services = Services
    
    services.user_service          = UserService(app.config)
    services.destination_service   = DestinationService(destination_dao)
    services.cart_item_service     = CartItemService(cart_item_dao)
    services.store_order_service   = StoreOrderService(store_order_dao)
    services.product_list_service  = ProductListService()
    services.category_list_service = CategoryListService()

    services.event_list_service           = EventListService()
    services.sender_service               = SenderService(sender_dao)
    services.event_service                = EventService(event_dao)
    services.seller_service               = SellerService(app.config)
    services.bookmark_service             = BookmarkService()
    services.product_enquiry_list_service = ProductEnquiryService()
    services.seller_shop_service          = SellerShopService(seller_shop_dao)
    services.seller_info_service          = SellerInfoService(seller_info_dao)
    
    #admin1
    services.event_service        = EventService(event_dao)
    services.order_service        = OrderService(order_dao)
    services.order_detail_service = OrderService(order_detail_dao)
    services.enquiry_service      = EnquiryService(enquiry_dao)
    
    #admin2
    services.seller_service          = SellerService(app.config)
    services.seller_info_service     = SellerInfoService(seller_info_dao)
    services.product_manage_service  = ProductManageService()
    
    # presentation Layer
    create_endpoints(app, services, database)
    
    return app
