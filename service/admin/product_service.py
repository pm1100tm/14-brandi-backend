import io
import uuid

from PIL                     import Image

from utils.const             import ACCOUNT_ADMIN, ACCOUNT_SELLER
from config                  import S3_BUCKET_URL
from utils.amazon_s3         import S3FileManager, GenerateFilePath
from model                   import ProductManageDao, SellerDao
from utils.custom_exceptions import (
    RequiredFieldException,
    NotValidFileException,
    FileSizeException,
    FileExtensionException,
    CompareQuantityCheck,
    ComparePriceCheck,
    DateCompareException,
    FileScaleException,
    FileUploadFailException,
    LookUpDateFieldRequiredCheck,
    SellerAttributeTypeException
)


class ProductManageService:
    """ Business Layer

        Attributes:
            product_manage_dao : ProductManageDao 클래스

        Author: 심원두

        History:
            2020-12-31(심원두): 초기 생성
    """
    
    def __init__(self):
        self.product_manage_dao = ProductManageDao()
        self.seller_dao         = SellerDao()
    
    def get_product_origin_types_service(self, connection):
        """ 원산지 리스트 취득

            Args:
                connection : 데이터 베이스 연결 객체

            Author: 심원두

            Returns:
                [
                    {
                        "product_origin_type_id": 1,
                        "product_origin_type_name": "기타 "
                    },
                    {
                        "product_origin_type_id": 2,
                        "product_origin_type_name": "중국"
                    },
                ]

            Raises:
                500, {'message': 'fail to get product origin types',
                      'errorMessage': 'fail_to_get_product_origin_types'} : 원산지 정보 취득 실패

            History:
                2020-01-01(심원두): 초기 생성
                2020-01-03(심원두): 결과 편집 처리 수정
        """
        
        try:
            product_origin_types = \
                self.product_manage_dao.get_product_origin_types(
                    connection
                )
            
            result = [
                {
                    'product_origin_type_id'   : product_origin_type['id'],
                    'product_origin_type_name' : product_origin_type['name']
                } for product_origin_type in product_origin_types
            ]
        
            return result
    
        except KeyError as e:
            raise e
    
        except Exception as e:
            raise e
    
    def get_color_list_service(self, connection):
        """ 색상 리스트 취득

            Args:
                connection : 데이터 베이스 연결 객체

            Author: 심원두

            Returns:
                "result": [
                    {
                        "color_id": 1,
                        "color_name": "Black"
                    },
                    {
                        "color_id": 2,
                        "color_name": "White"
                    },
                ]

            Raises:
                500, {'message': 'fail to get color list',
                      'errorMessage': 'fail_to_get_color_list'}: 색상 정보 취득 실패

            History:
                2020-01-01(심원두): 초기 생성
                2020-01-03(심원두): 결과 편집 처리 수정
        """
        
        try:
            color_list = self.product_manage_dao.get_color_list(connection)
            
            result = [
                {
                    'color_id'   : color['id'],
                    'color_name' : color['name']
                } for color in color_list
            ]
            
            return result
        
        except KeyError as e:
            raise e
        
        except Exception as e:
            raise e

    def get_size_list_service(self, connection):
        """ 사이즈 리스트 취득

            Args:
                connection : 데이터 베이스 연결 객체

            Author: 심원두

            Returns:
                [
                    {
                        "color_id": 1,
                        "color_name": "Black"
                    },
                    {
                        "color_id": 2,
                        "color_name": "White"
                    },
                ]

            Raises:
                500, {'message': 'fail to get color list',
                      'errorMessage': 'fail_to_get_color_list'}: 색상 정보 취득 실패

            History:
                2020-01-01(심원두): 초기 생성
                2020-01-03(심원두): 결과 편집 처리 수정
        """
    
        try:
            size_list = self.product_manage_dao.get_size_list(connection)
            
            result = [
                {
                    'size_id'  : size['id'],
                    'size_name': size['name']
                } for size in size_list
            ]
        
            return result
    
        except KeyError as e:
            raise e
    
        except Exception as e:
            raise e

    def get_seller_list_by_name_service(self, connection, data, permission_type_id):
        """ 셀러 리스트 취득

            Args:
                connection         : 데이터 베이스 연결 객체
                data               : View 에서 넘겨 받은 셀러명
                permission_type_id : View 에서 넘겨 받은 권한 타입 아이디
            Author: 심원두
            
            Returns:
                [
                    {
                        "profile_image_url": "https://brandi-intern-8.s3.amazonaws.co...,
                        "seller_id": 10,
                        "seller_name": "나는셀러10"
                    },
                    {
                        "profile_image_url": "https://brandi-intern-8.s3.amazonaws.co...
                        "seller_id": 100,
                        "seller_name": "나는셀러100"
                    },
            
            Raises:
                400, {'message': 'key error',
                      'errorMessage': 'key_error' + format(e)}: 잘못 입력된 키값
                
                400, {'message': 'internal_server_error',
                      'errorMessage': 'PERMISSION_ERROR' + format(e)}: 잘못된 권한
            
            History:
                2020-01-01(심원두): 초기 생성
                2020-01-03(심원두): 결과 편집 처리 수정
                2020-01-15(심원두):
                    메서드명 변경 : search_seller_list_service > get_seller_list_by_name_service
        """
        
        try:
            if permission_type_id is not ACCOUNT_ADMIN:
                raise PermissionError('PERMISSION_ERROR')
            
            data['seller_name'] = '%' + data['seller_name'] + '%'
            
            seller_info = \
                self.seller_dao.get_seller_list_by_name(
                    connection,
                    data
                )
            
            result = [
                {
                    'seller_id'         : seller['seller_id'],
                    'seller_name'       : seller['seller_name'],
                    'profile_image_url' : S3_BUCKET_URL + seller['profile_image_url']
                                          if not seller['profile_image_url'] else None
                } for seller in seller_info
            ]
            
            return result
        
        except KeyError as e:
            raise e
        
        except Exception as e:
            raise e
    
    def get_main_category_list_service(self, connection):
        """ 메인 카테고리 정보 취득

            Args:
                connection : 데이터 베이스 연결 객체

            Author: 심원두

            Returns:
                "result": [
                    {
                        "main_category_id": 1,
                        "main_category_name": "아우터"
                    },
                    {
                        "main_category_id": 2,
                        "main_category_name": "상의"
                    },
                ]

            Raises:
                500, {'message': 'fail to get main category list',
                      'errorMessage': 'fail_to_get_main_category_list'}: 메인 카테고리 정보 취득 실패

            History:
                2020-01-01(심원두): 초기 생성
                2020-01-03(심원두): 결과 편집 처리 수정
                2020-01-15(심원두):
                    메서드명 변경 : main_category_list_service > get_main_category_list_service
        """
        
        try:
            main_category_list = \
                self.product_manage_dao.get_main_category_list(
                    connection
                )
            
            result = [
                {
                    'main_category_id'   : main_category_info['id'],
                    'main_category_name' : main_category_info['name']
                } for main_category_info in main_category_list
            ]
        
            return result
    
        except KeyError as e:
            raise e
    
        except Exception as e:
            raise e

    def get_sub_category_list_service(self, connection, data):
        """ 셀러 리스트 취득

            Args:
                connection : 데이터 베이스 연결 객체
                data       : View 에서 넘겨 받은 메인 카테고리 아이디

            Author: 심원두

            Returns:
                [
                    {
                        "sub_category_id": 13,
                        "sub_category_name": "청바지"
                    },
                    {
                        "sub_category_id": 14,
                        "sub_category_name": "슬랙스"
                    },
                ]

            Raises:
                500, {'message': 'fail to get sub category list',
                      'errorMessage': 'fail_to_get_sub_category_list'}: 색상 정보 취득 실패

            History:
                2020-01-01(심원두): 초기 생성
                2020-01-03(심원두): 결과 편집 처리 수정
        """
        
        try:
            sub_category_list = \
                self.product_manage_dao.get_sub_category_list(
                    connection,
                    data
                )
        
            result = [
                {
                    'sub_category_id'   : sub_category['sub_category_id'],
                    'sub_category_name' : sub_category['sub_category_name'],
                } for sub_category in sub_category_list
            ]
            
            return result
    
        except KeyError as e:
            raise e
    
        except Exception as e:
            raise e
    
    def create_product_service(self, connection, data):
        """ product 생성

            Parameters:
                connection : 데이터베이스 연결 객체
                data       : View 에서 넘겨받은 dict 객체

            Author: 심원두

            Returns:
                product_id : 생성한 products 테이블의 키 값

            Raises:
                400, {'message': 'key error',
                      'errorMessage': 'key_error' + format(e)}: 잘못 입력된 키값

                400, {'message': 'required field is blank',
                      'errorMessage': 'required_manufacture_information'}: 제조 정보 필드 없음

                400, {'message': 'required field is blank',
                      'errorMessage': 'required_discount_start_or_end_date'}: 필수 입력 항목 없음

                400, {'message': 'compare quantity field check error',
                      'errorMessage': 'minimum_quantity_cannot_greater_than_maximum_quantity'}: 최소 구매 수량이 최대 보다 큼

                400, {'message': 'compare price field check error',
                      'errorMessage': 'discounted_price_cannot_greater_than_origin_price'}: 할인가가 판매가 보다 큼

                400, {'message': 'compare price field check error',
                      'errorMessage': 'wrong_discounted_price'}: 판매가와 할인가 일치하지 않음

                400, {'message': 'compare price field check error',
                      'errorMessage': 'required_discount_start_or_end_date'}: 할인 시작, 종료 일자 필드 없음

                400, {'message': 'start date is greater than end date',
                      'errorMessage': 'start_date_cannot_greater_than_end_date'}: 할인 시작일이 종료일 보다 큼

                400, {'message': 'compare price field check error',
                      'errorMessage': 'discounted_price_have_to_same_with_origin_price'}: 할인가, 판매가 불일치(할인율 0)

                500, {'message': 'product create denied',
                      'errorMessage': 'unable_to_create_product'}: 상품 정보 등록 실패

            History:
                2020-12-29(심원두): 초기 생성
                2020-12-30(심원두): 예외처리 구현
                2020-01-03(심원두): 예외처리 추가/수정
        """
    
        try:
            if int(data['minimum_quantity']) != 0 and int(data['maximum_quantity']) != 0:
                if int(data['minimum_quantity']) > int(data['maximum_quantity']):
                    raise CompareQuantityCheck('minimum_quantity_cannot_greater_than_maximum_quantity')
        
            if int(data['minimum_quantity']) == 0:
                data['minimum_quantity'] = 1
        
            if int(data['maximum_quantity']) == 0:
                data['minimum_quantity'] = 20
        
            if int(data['is_product_notice']) == 0:
                data['manufacturer'] = None
                data['manufacturing_date'] = None
                data['product_origin_type_id'] = None
        
            else:
            
                if not data['manufacturer'] or not data['manufacturing_date'] or not data['product_origin_type_id']:
                    raise RequiredFieldException('required_manufacture_information')
        
            if int(data['discount_rate']) == 0:
                data['discounted_price'] = data['origin_price']
                data['discount_start_date'] = None
                data['discount_end_date'] = None
        
            else:
            
                if float(data['discounted_price']) > float(data['origin_price']):
                    raise ComparePriceCheck('discounted_price_cannot_greater_than_origin_price')
            
                if (float(data['origin_price']) * (1 - float(data['discount_rate']) / 100)) != \
                    float(data['discounted_price']):
                    raise ComparePriceCheck('wrong_discounted_price')
            
                if data['discount_start_date'] and not data['discount_end_date']:
                    raise RequiredFieldException('required_discount_start_or_end_date')
            
                if not data['discount_start_date'] and data['discount_end_date']:
                    raise RequiredFieldException('required_discount_start_or_end_date')
            
                if data['discount_start_date'] and data['discount_end_date']:
                
                    if data['discount_start_date'] > data['discount_end_date']:
                        raise DateCompareException('start_date_cannot_greater_than_end_date')
            
                else:
                    data['discount_start_date'] = None
                    data['discount_end_date'] = None
        
            data['discount_rate'] = float(data['discount_rate']) / 100
        
            print(type(data['detail_information']), data['detail_information'])
        
            return self.product_manage_dao.insert_product(connection, data)
    
        except KeyError as e:
            raise e
    
        except Exception as e:
            raise e

    def update_product_code_service(self, connection, product_id):
        """ 상품 코드(product_code) 생성 후 상품 코드 업데이트

            Args:
                connection : 데이터베이스 연결 객체
                product_id : View 에서 상품정보 등록 성공 후 넘겨 받은 해당 상품 정보 테이블의 id

            Author: 심원두

            Returns:
                0: 상품 코드 갱신 실패
                1: 상품 코드 갱신 성공

            Raises:
                400, {'message': 'key error',
                      'errorMessage': 'key_error' + format(e)}: 잘못 입력된 키값

                500, {'message': 'product code update denied',
                      'errorMessage': 'unable_to_update_product_code'}: 상품 코드 갱신 실패

            History:
                2020-12-29(심원두): 초기 생성
        """
    
        try:
            data = {
                'product_code': 'P' + str(product_id).zfill(18),
                'product_id'  : product_id
            }
        
            self.product_manage_dao.update_product_code(connection, data)
        
            return data['product_code']
    
        except KeyError as e:
            raise e
    
        except Exception as e:
            raise e

    def create_product_images_service(self, connection, seller_id, product_id, product_code, product_images):
        """ 상품 이미지 등록

            Args:
                'connection'     : 데이터베이스 연결 객체
                'seller_id'      : View 에서 넘겨 받은 셀러 아이디
                'product_id'     : View 에서 넘겨 받은 상품 아이디
                'product_images' : View 에서 넘겨 받은 이미지 파일

            Author: 심원두

            Returns:
                0: 상품 이미지 테이블 등록 실패
                1: 상품 이미지 테이블 등록 성공

            Raises:
                413, {'message': 'invalid file',
                      'errorMessage': 'invalid_file'}: 파일 이름이 공백, 혹은 파일을 정상적으로 받지 못함

                413, {'message': 'file size too large',
                      'errorMessage': 'file_size_too_large'}: 파일 사이즈 정책 위반 (4메가 이상인 경우)

                413, {'message': 'file scale too small, 640 * 720 at least',
                      'errorMessage': 'file_scale_at_least_640*720'}: 파일 스케일 정책 위반 (680*720 미만인 경우)

                413, {'message': 'only allowed jpg type',
                      'errorMessage': 'only_allowed_jpg_type'}: 파일 확장자 정책 위반 (JPG, JPEG 아닌 경우)

                500, {'message': 'image_file_upload_to_amazon_fail',
                      'errorMessage': 'image_file_upload_fail'}: 이미지 업로드 실패

                500, {'message': 'product image create denied',
                      'errorMessage': 'unable_to_create_product_image'}: 상품 이미지 등록 실패

            History:
                2020-12-29(심원두): 초기 생성
                2021-01-03(심원두): 이미지 업로드 예외 처리 수정, 파일 손상 이슈 수정
                2021-01-05(심원두): S3 에 이미지 업로드 처리를, 예외처리 처리 후에 하도록 수정.
                2021-01-06(심원두): 인덱스가 0부터 들어가는 오류 수정
        """
    
        try:
            image_buffer = []
        
            for product_image in product_images:
                if not product_image or not product_image.filename:
                    raise NotValidFileException('invalid_file')
            
                image = Image.open(product_image, 'r')
                buffer = io.BytesIO()
            
                image.save(buffer, image.format)
            
                product_image.seek(0, 2)
                if product_image.tell() > (1024 * 1024 * 4):
                    FileSizeException('file_size_too_large')
            
                buffer.seek(0)
            
                width, height, = image.size
                if width < 640 or height < 720:
                    raise FileScaleException('file_scale_at_least_640*720')
            
                if image.format != "JPEG":
                    raise FileExtensionException('only_allowed_jpg_type')
            
                image_buffer.append(buffer)
        
            for index, buffer in enumerate(image_buffer):
                file_path = GenerateFilePath().generate_file_path(
                    3,
                    seller_id=seller_id,
                    product_id=product_id
                )
            
                file_name = file_path + product_code + "-" + str(uuid.uuid4())
            
                url = S3FileManager().file_upload(
                    buffer,
                    file_name
                )
            
                if not url:
                    S3FileManager().file_delete(file_name)
                    raise FileUploadFailException('image file upload to amazon fail')
            
                data = {
                    'image_url'  : url,
                    'product_id' : product_id,
                    'order_index': index + 1
                }
            
                self.product_manage_dao.insert_product_image(connection, data)
    
        except Exception as e:
            raise e

    def create_stock_service(self, connection, product_id, stocks):
        """ 상품 옵션 정보 등록

            Args:
                connection : 데이터베이스 연결 객체
                product_id : View 에서 상품정보 등록 성공 후 넘겨 받은 상품 정보 테이블의 id
                stocks     : View 에서 넘겨 받은 상품 옵션 정보

            Author: 심원두

            Returns:
                0: 옵션 테이블 등록 실패
                1: 옵션 테이블 등록 성공

            Raises:
                400, {'message': 'key error',
                      'errorMessage': 'key_error' + format(e)}: 잘못 입력된 키값

                500, {'message': 'stock create denied',
                      'errorMessage': 'unable_to_create_stocks'}: 상품 옵션 정보 등록 실패

            History:
                2020-12-29(심원두): 초기 생성
                2020-01-03(심원두): 프론트엔드 상의 후 재고 관리 컬럼 추가에 대한 대응
        """
    
        try:
            data = {}
        
            for stock in stocks:
                product_option_code = \
                    str(product_id) + \
                    str(stock['color']).zfill(3) + \
                    str(stock['size']).zfill(3)
                
                data['product_option_code'] = product_option_code
                data['product_id'] = product_id
                data['color_id'] = stock['color']
                data['size_id'] = stock['size']
                data['remain'] = stock['remain']
            
                if not stock['isStockManage']:
                    stock['isStockManage'] = 0
            
                data['is_stock_manage'] = stock['isStockManage']
            
                if not stock['remain']:
                    data['remain'] = 0
            
                self.product_manage_dao.insert_stock(connection, data)
    
        except KeyError as e:
            raise e
    
        except Exception as e:
            raise e

    def create_product_history_service(self, connection, product_id, data):
        """ 상품 이력 정보 등록

            Args:
                connection : 데이터베이스 연결 객체
                product_id : View 에서 상품정보 등록 성공 후 넘겨 받은 상품 정보 테이블의 id
                data       : View 에서 넘겨 받은 상품 정보

            Author: 심원두

            Returns:
                0: 상품 이력 정보 등록 실패
                1: 상품 이력 정보 등록 성공

            Raises:
                400, {'message': 'key error',
                      'errorMessage': 'key_error' + format(e)}: 잘못 입력된 키값

                500, {'message': 'product history create denied',
                      'errorMessage': 'unable_to_create_product_history'}: 상품 이력 등록 실패

            History:
                2020-12-29(심원두): 초기 생성
        """
    
        try:
            data['product_id'] = product_id
            data['discount_rate'] = float(data['discount_rate']) / 100
        
            if not data['discount_start_date']:
                data['discount_start_date'] = None
        
            if not data['discount_end_date']:
                data['discount_end_date'] = None
        
            if not data['discounted_price']:
                data['discounted_price'] = None
        
            self.product_manage_dao.insert_product_history(connection, data)
    
        except KeyError as e:
            raise e
    
        except Exception as e:
            raise e

    def create_product_sales_volumes_service(self, connection, product_id):
        """ 상품 판매량 정보 초기 등록

            Args:
                connection : 데이터 베이스 연결 객체
                product_id : View 에서 상품정보 등록 성공 후 넘겨 받은 상품 정보 테이블의 id

            Author: 심원두

            Returns:
                0: 상품 판매량 정보 초기 등록 실패
                1: 상품 판매량 정보 초기 등록 성공

            Raises:
                500, {'message': 'product history create denied',
                      'errorMessage': 'unable_to_create_product_history'}: 상품 이력 등록 실패

            History:
                2020-12-29(심원두): 초기 생성
        """
    
        try:
        
            self.product_manage_dao.insert_product_sales_volumes(connection, product_id)
    
        except Exception as e:
            raise e

    def create_bookmark_volumes_service(self, connection, product_id):
        """ 북 마크 정보 초기 등록

            Args:
                connection : 데이터 베이스 연결 객체
                product_id : 상품 번호

            Author: 심원두

            Returns:
                0: 북마크 정보 초기 등록 실패
                1: 북마크 정보 초기 등록 성공

            Raises:
                500, {'message': 'bookmark volumes create denied',
                      'errorMessage': 'unable_to_create_bookmark_volumes'}: 북마크 초기 등록 실패

            History:
                2021-01-05(심원두): 초기 생성
        """
    
        try:
            
            self.product_manage_dao.insert_bookmark_volumes(connection, product_id)
            
        except Exception as e:
            raise e
    
    def search_product_service(self, connection, data):
        """ 특정 조건에 따른 product 검색
        
            Parameters:
                connection : 데이터베이스 연결 객체
                data       : View 에서 넘겨받은 딕셔너리 객체
            
            Author: 심원두

            Returns:
                "result": {
                    "product_list": [
                        {
                            "discount_rate": 0.0,
                            "discounted_price": 10000.0,
                            "is_display": 1,
                            "is_sale": 1,
                            "origin_price": 10000.0,
                            "product_code": "P000000000000001131",
                            "product_id": 1131,
                            "product_image_url": "https://brandi-intern-8.s3.amazonaws.com/sellers/3/products/1131/images/flask.jpg",
                            "product_name": "상품이름",
                            "seller_attribute_type": "쇼핑몰",
                            "seller_name": "나는셀러3",
                            "updated_at": "2021-01-02 04:11:04"
                        }, ...
                    ],
                    "total_count": 951
            
            Raises:
                400, {'message': 'key error',
                      'errorMessage': 'key_error' + format(e)}: 잘못 입력된 키 값
                      
                400, {'message': 'both date field required',
                      'errorMessage': 'both_date_field_required'}: 필수 값 유효성 체크 에러
                      
                400, {'message': 'start date is greater than end date',
                      'errorMessage': 'start_date_is_greater_than_end_date'}: 날짜 비교 유효성 체크 에러
                
                400, {'message': 'invalid seller attribute type',
                      'errorMessage': 'invalid_seller_attribute_type'}: 셀러 타입 유효성 체크 에러
        """
        
        try:
            if data['lookup_start_date'] and not data['lookup_end_date']:
                raise LookUpDateFieldRequiredCheck('both_date_field_required')

            if not data['lookup_start_date'] and data['lookup_end_date']:
                raise LookUpDateFieldRequiredCheck('both_date_field_required')
            
            if data['lookup_start_date'] and data['lookup_end_date']:
                if data['lookup_start_date'] > data['lookup_end_date']:
                    raise DateCompareException('start_date_is_greater_than_end_date')
            
            if data['seller_attribute_type_ids']:
                for type_id in data['seller_attribute_type_ids']:
                    if type_id < 0 or type_id > 7:
                        raise SellerAttributeTypeException("invalid_seller_attribute_type")
            
            if data['product_name']:
                data['product_name'] = '%' + data['product_name'] + '%'
            
            data['page_number'] = int(data['page_number'])
            data['limit']       = int(data['limit'])
            data['offset']      = (data['page_number'] * data['limit']) - data['limit']
            
            total_count  = self.product_manage_dao.get_total_products_count(
                                connection,
                                data
                            )['total_count']
            
            product_list = self.product_manage_dao.search_products(
                                connection,
                                data
                            )
            
            result = {
                'total_count'  : total_count,
                'product_list' : [
                    {
                        'updated_at'            : product['updated_at'],
                        'product_image_url'     : S3_BUCKET_URL + product['product_image_url'],
                        'product_name'          : product['product_name'],
                        'product_code'          : product['product_code'],
                        'product_id'            : product['product_id'],
                        'seller_attribute_type' : product['seller_attribute_type'],
                        'seller_name'           : product['seller_name'],
                        'origin_price'          : '{:,}'.format(int(product['origin_price'])),
                        'discounted_price'      : '{:,}'.format(int(product['discounted_price'])),
                        'discount_rate'         : int(product['discount_rate']),
                        'is_sale'               : product['is_sale'],
                        'is_display'            : product['is_display'],
                    } for product in product_list
                ]
            }
            
            return result
        
        except KeyError as e:
            raise e
        
        except Exception as e:
            raise e
    
    def detail_product_service(self, connection, data):
        """ 해당 상품 코드의 상세 정보 취득
            
            Parameters:
                connection : 데이터베이스 연결 객체
                data       : View 에서 넘겨받은 딕셔너리 객체 (상품 코드)
            
            Author: 심원두
            
            Returns:
                "result": {
                    "product_detail": {
                    "description": "상품 설명===999",
                    "detail_information": "html==============",
                    "discount_end_date": "2021-12-25 23:59:00",
                    "discount_rate": 0.1,
                    "discount_start_date": "2020-11-01 09:00:00",
                    "discounted_price": 9000.0,
                    "is_display": 1,
                    "is_product_notice": 0,
                    "is_sale": 1,
                    "main_category_id": 1,
                    "main_category_name": "아우터",
                    "manufacturer": "패션의 완성 위코드(제조)",
                    "manufacturing_date": "Wed, 01 Jan 2020 00:00:00 GMT",
                    "maximum_quantity": 20,
                    "minimum_quantity": 1,
                    "origin_price": 10000.0,
                    "product_code": "P0000000000000000999",
                    "product_id": 999,
                    "product_name": "성보의하루999",
                    "product_origin_type_id": 3,
                    "product_origin_type_name": "한국",
                    "sub_category_id": 6,
                    "sub_category_name": "무스탕/퍼",
                    "updated_at": "2020-12-31 13:25:08"
                },
                "product_images": [
                    {
                        "order_index": 1,
                        "product_image_url": "https://brandi-intern-8.s3.amazonaws.com/free-psd/simple-black
                    }
                ],
                "product_options": [
                    {
                        "color_id": 1,
                        "color_name": "Black",
                        "is_stock_manage": 0,
                        "product_option_code": "1194001008",
                        "remain": 100,
                        "size_id": 1,
                        "size_name": "Free",
                        "stock_id": 999
                    }
                ]
            }
            
            Raises:
                400, {'message': 'key error',
                      'errorMessage': 'key_error' + format(e)} : 잘못 입력된 키값
                
                500, {'message': 'product does not exist',
                      'errorMessage': 'product_does_not_exist'} : 상품 정보 취득 실패
                      
                500, {'message': 'product image not exist',
                      'errorMessage': 'product_image_not_exist'}: 상품 이미지 정보 취득 실패
                
                500, {'message': 'stock info not exist',
                      'errorMessage': 'stock_does_not_exist'}: 옵션 정보 취득 실패
        """
        
        try:
            product_detail     = self.product_manage_dao.get_product_detail(connection, data)
            
            data['product_id'] = product_detail['product_id']
            
            product_images     = self.product_manage_dao.get_product_images(connection, data)
            product_options    = self.product_manage_dao.get_product_options(connection, data)
            
            result = {
                'product_detail' : {
                    'seller_id'                : product_detail['seller_id'],
                    'seller_name'              : product_detail['seller_name'],
                    'product_code'             : product_detail['product_code'],
                    'is_sale'                  : product_detail['is_sale'],
                    'is_display'               : product_detail['is_display'],
                    'main_category_id'         : product_detail['main_category_id'],
                    'main_category_name'       : product_detail['main_category_name'],
                    'sub_category_id'          : product_detail['sub_category_id'],
                    'sub_category_name'        : product_detail['sub_category_name'],
                    'is_product_notice'        : product_detail['is_product_notice'],
                    'manufacturer'             : product_detail['manufacturer'],
                    'manufacturing_date'       : product_detail['manufacturing_date'],
                    'product_origin_type_id'   : product_detail['product_origin_type_id'],
                    'product_origin_type_name' : product_detail['product_origin_type_name'],
                    'product_name'             : product_detail['product_name'],
                    'description'              : product_detail['description'],
                    'detail_information'       : product_detail['detail_information'],
                    'origin_price'             : product_detail['origin_price'],
                    'discount_rate'            : product_detail['discount_rate'],
                    'discounted_price'         : product_detail['discounted_price'],
                    'discount_start_date'      : product_detail['discount_start_date'],
                    'discount_end_date'        : product_detail['discount_end_date'],
                    'minimum_quantity'         : product_detail['minimum_quantity'],
                    'maximum_quantity'         : product_detail['maximum_quantity'],
                    'updated_at'               : product_detail['updated_at'],
                    'product_id'               : product_detail['product_id'],
                },
                'product_images' : [
                    {
                        'product_image_url' : S3_BUCKET_URL + image['product_image_url'],
                        'order_index'       : image['order_index']
                    } for image in product_images
                ],
                'product_options': [
                    {
                        'stock_id'            : option['stock_id'],
                        'product_option_code' : option['product_option_code'],
                        'color_id'            : option['color_id'],
                        'color_name'          : option['color_name'],
                        'size_id'             : option['size_id'],
                        'size_name'           : option['size_name'],
                        'remain'              : option['remain'],
                        'is_stock_manage'     : option['is_stock_manage'],
                    } for option in product_options
                ]
            }
            
            return result
        
        except KeyError as e:
            raise e
        
        except Exception as e:
            raise e
