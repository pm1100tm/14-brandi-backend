import pymysql

from utils.custom_exceptions import (
    ProductNotExist,
    ProductImageNotExist,
    StockNotNotExist,
    ProductCreateDenied,
    ProductCodeUpdatedDenied,
    ProductImageCreateDenied,
    StockCreateDenied,
    ProductHistoryCreateDenied,
    ProductSalesVolumeCreateDenied,
    ProductBookMarkVolumeCreateDenied,
    ProductOriginTypesNotExist,
    ColorNotExist,
    SizeNotExist,
    MainCategoryNotExist,
    SubCategoryNotExist
)


class ProductManageDao:
    """ Persistence Layer
        
        Attributes: None
        
        Author: 심원두
        
        History:
            2020-12-31(심원두): 초기 생성
            2021-01-03(심원두): 상품 리스트 기능 구현, 상품 상세 정보 조회 기능 작성 중
    """

    def insert_product(self, connection, data):
        """ 상품 정보 등록 (상품 정보 테이블)

        Args:
            connection: 데이터베이스 연결 객체
            data      : 서비스 레이어에서 넘겨 받은 products 테이블 등록에 사용될 데이터

        Author: 심원두

        Returns:
            product_id : products 테이블에 신규 등록된 id 값

        History:
            2020-12-29(심원두): 초기 생성
            2020-12-31(심원두): Docstring 수정

        Raises:
            500, {'message': 'product create denied',
                  'errorMessage': 'unable_to_create_product'} : 상품 정보 등록 실패
        """
    
        sql = """
        INSERT INTO products (
            `is_display`
            ,`is_sale`
            ,`main_category_id`
            ,`sub_category_id`
            ,`is_product_notice`
            ,`manufacturer`
            ,`manufacturing_date`
            ,`product_origin_type_id`
            ,`name`
            ,`description`
            ,`detail_information`
            ,`origin_price`
            ,`discount_rate`
            ,`discounted_price`
            ,`discount_start_date`
            ,`discount_end_date`
            ,`minimum_quantity`
            ,`maximum_quantity`
            ,`seller_id`
            ,`account_id`
        ) VALUES (
            %(is_display)s
            ,%(is_sale)s
            ,%(main_category_id)s
            ,%(sub_category_id)s
            ,%(is_product_notice)s
            ,%(manufacturer)s
            ,%(manufacturing_date)s
            ,%(product_origin_type_id)s
            ,%(product_name)s
            ,%(description)s
            ,%(detail_information)s
            ,%(origin_price)s
            ,%(discount_rate)s
            ,%(discounted_price)s
            ,%(discount_start_date)s
            ,%(discount_end_date)s
            ,%(minimum_quantity)s
            ,%(maximum_quantity)s
            ,%(seller_id)s
            ,%(account_id)s
        );
        """
    
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                product_id = cursor.lastrowid
            
                if not product_id:
                    raise ProductCreateDenied('unable_to_create_product')
            
                return product_id
    
        except Exception as e:
            raise e

    def update_product_code(self, connection, data):
        """ 상품 정보 갱신 (product_code 갱신)

            Args:
                connection: 데이터베이스 연결 객체
                data      : 서비스 레이어에서 넘겨 받은 products 테이블 갱신에 사용될 데이터

            Author: 심원두

            Returns:
                0 : products 테이블 갱신 실패
                1 : products 테이블 갱신 성공 (product_code)

            History:
                2020-12-29(심원두): 초기 생성
                2020-12-31(심원두): Docstring 수정

            Raises:
                500, {'message': 'product code update denied',
                      'errorMessage': 'unable_to_update_product_code'} : 상품 코드 갱신 실패
        """
    
        sql = """
            UPDATE
                products
            SET
                `product_code` = %(product_code)s
            WHERE
                id = %(product_id)s
            AND
                is_deleted = 0;
        """
    
        try:
            with connection.cursor() as cursor:
                result = cursor.execute(sql, data)
            
                if not result:
                    raise ProductCodeUpdatedDenied('unable_to_update_product_code')
    
        except Exception as e:
            raise e

    def insert_product_image(self, connection, data):
        """ 상품 이미지 정보 등록

            Args:
                connection: 데이터베이스 연결 객체
                data      : 서비스 레이어에서 넘겨 받은 product_images 테이블 등록에 사용될 데이터

            Author: 심원두

            Returns:
                0 : products_images 테이블 데이터 생성 실패
                1 : products_images 테이블 데이터 생성 성공

            History:
                2020-12-29(심원두): 초기 생성
                2020-12-31(심원두): Docstring 수정

            Raises:
                500, {'message': 'product image create denied',
                      'errorMessage': 'unable_to_create_product_image'} : 상품 이미지 정보 등록 실패
        """
    
        sql = """
        INSERT INTO product_images(
            `image_url`
            , `product_id`
            , `order_index`
        ) VALUES (
            %(image_url)s
            ,%(product_id)s
            ,%(order_index)s
        );
        """
    
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                result = cursor.lastrowid
            
                if not result:
                    raise ProductImageCreateDenied('unable_to_create_product_image')
            
                return result
    
        except Exception as e:
            raise e

    def insert_stock(self, connection, data):
        """ 상품 옵션 정보 등록

            Args:
                connection: 데이터베이스 연결 객체
                data      : 서비스 레이어에서 넘겨 받은 상품 옵션 정보 이미지 등록에 사용될 데이터

            Author: 심원두

            Returns:
                0 : stocks 테이블 데이터 생성 실패
                1 : stocks 테이블 데이터 생성 성공

            History:
                2020-12-29(심원두): 초기 생성
                2020-12-31(심원두): Docstring 수정

            Raises:
                500, {'message': 'stock create denied',
                      'errorMessage': 'unable_to_create_stocks'}: 상품 이미지 정보 등록 실패
        """
    
        sql = """
            INSERT INTO stocks(
                 `product_option_code`
                , `is_stock_manage`
                , `remain`
                , `color_id`
                , `size_id`
                , `product_id`
            ) VALUES (
                %(product_option_code)s
                ,%(is_stock_manage)s
                ,%(remain)s
                ,%(color_id)s
                ,%(size_id)s
                ,%(product_id)s
            );
        """
    
        try:
            with connection.cursor() as cursor:
                result = cursor.execute(sql, data)
            
                if not result:
                    raise StockCreateDenied('unable_to_create_stocks')
            
                return result
    
        except Exception as e:
            raise e

    def insert_product_history(self, connection, data):
        """ 상품 이력 정보 등록

            Args:
                connection: 데이터베이스 연결 객체
                data      : 서비스 레이어에서 넘겨 받은 상품 옵션 정보 이미지 등록에 사용될 데이터

            Author: 심원두

            Returns:
                0 : product_histories 테이블 데이터 생성 실패
                1 : product_histories 테이블 데이터 생성 성공

            History:
                2020-12-29(심원두): 초기 생성
                2020-12-31(심원두): Docstring 수정

            Raises:
                500, {'message': 'product history create denied',
                      'errorMessage': 'unable_to_create_product_history'} : 상품 이미지 정보 등록 실패
        """
    
        sql = """
            INSERT INTO product_histories (
                `product_id`
                ,`product_name`
                ,`is_display`
                ,`is_sale`
                ,`origin_price`
                ,`discounted_price`
                ,`discount_rate`
                ,`discount_start_date`
                ,`discount_end_date`
                ,`minimum_quantity`
                ,`maximum_quantity`
                ,`updater_id`
            ) VALUES (
                %(product_id)s
                ,%(product_name)s
                ,%(is_display)s
                ,%(is_sale)s
                ,%(origin_price)s
                ,%(discounted_price)s
                ,%(discount_rate)s
                ,%(discount_start_date)s
                ,%(discount_end_date)s
                ,%(minimum_quantity)s
                ,%(maximum_quantity)s
                ,%(account_id)s
            );
        """
    
        try:
            with connection.cursor() as cursor:
                result = cursor.execute(sql, data)
            
                if not result:
                    raise ProductHistoryCreateDenied('unable_to_create_product_history')
            
                return result
    
        except Exception as e:
            raise e

    def insert_product_sales_volumes(self, connection, product_id):
        """ 상품 판매량 정보 초기 등록

            Args:
                connection : 데이터베이스 연결 객체
                product_id : 서비스 레이어에서 넘겨 받은 product_sales_volumes 테이블 데이터 생성에 사용될 값

            Author: 심원두

            Returns:
                0 : product_sales_volumes 테이블 데이터 생성 실패
                1 : product_sales_volumes 테이블 데이터 생성 성공

            History:
                2020-12-29(심원두): 초기 생성
                2020-12-31(심원두): Docstring 수정

            Raises:
                500, {'message': 'product sales volume create denied',
                      'errorMessage': 'unable_to_create_product_sales_volumes'} : 상품 판매량 정보 생성 실패
        """
    
        sql = """
            INSERT INTO product_sales_volumes (
                `product_id`
            ) VALUES (
                %s
            );
        """
    
        try:
            with connection.cursor() as cursor:
                result = cursor.execute(sql, product_id)
            
                if not result:
                    raise ProductSalesVolumeCreateDenied('unable_to_create_product_sales_volumes')
            
                return result
    
        except Exception as e:
            raise e

    def insert_bookmark_volumes(self, connection, product_id):
        sql = """
            INSERT INTO bookmark_volumes (
                `product_id`
            ) VALUES (
                %s
            );
        """
    
        try:
            with connection.cursor() as cursor:
                result = cursor.execute(sql, product_id)
            
                if not result:
                    raise ProductBookMarkVolumeCreateDenied('unable_to_create_bookmark_volumes')
            
                return result
    
        except Exception as e:
            raise e

    def get_product_origin_types(self, connection):
        """ 원산지 정보 취득

            Args:
                connection : 데이터베이스 연결 객체

            Author: 심원두

            Returns:
                result : product_origin_types 테이블의 키, 원산지명

            History:
                2020-12-29(심원두): 초기 생성
                2020-12-31(심원두): Docstring 수정

            Raises:
                500, {'message': 'fail to get product origin types',
                      'errorMessage': 'fail_to_get_product_origin_types'} : 원산지 정보 취득 실패
        """
        sql = """
            SELECT
                id
                ,name
            FROM
                product_origin_types
            WHERE
                is_deleted = 0
            ORDER BY
                id;
        """
    
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
            
                if not result:
                    raise ProductOriginTypesNotExist('fail_to_get_product_origin_types')
            
                return result
    
        except Exception as e:
            raise e

    def get_size_list(self, connection):
        """사이즈 정보 취득

            Args:
                connection: 데이터베이스 연결 객체

            Author: 심원두

            Returns:
                result : 테이블에서 취득한 사이즈 정보의 키, 사이즈명

            History:
                2020-12-30(심원두): 초기 생성
                2020-12-31(심원두): 메세지 수정

            Raises:
                500, {'message': 'fail to get size list',
                      'errorMessage': 'fail_to_get_size_list'} : 사이즈 정보 취득 실패
        """
    
        sql = """
            SELECT
                id
                ,name
            FROM
                sizes
            WHERE
                is_deleted = 0
            ORDER BY
                id;
        """
    
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
            
                if not result:
                    raise SizeNotExist('fail_to_get_size_list')
            
                return result
    
        except Exception as e:
            raise e

    def get_color_list(self, connection):
        """ 색상 정보 취득

            Args:
                connection: 데이터베이스 연결 객체

            Author: 심원두

            Returns:
                result : colors 테이블에서 취득한 색상 정보의 키, 색상명

            History:
                2020-12-30(심원두): 초기 생성
                2020-12-31(심원두): 메세지 수정

            Raises:
                500, {'message': 'fail to get color list',
                      'errorMessage': 'fail_to_get_color_list'}: 색상 정보 취득 실패
        """
    
        sql = """
            SELECT
                id
                ,name
            FROM
                colors
            WHERE
                is_deleted = 0
            ORDER BY
                id;
        """
    
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
            
                if not result:
                    raise ColorNotExist('fail_to_get_color_list')
            
                return result
    
        except Exception as e:
            raise e
    
    def get_main_category_list(self, connection):
        """ 메인 카테고리 정보 취득

            Args:
                connection: 데이터베이스 연결 객체

            Author: 심원두

            Returns:
                result : main_categories 테이블에서 취득한 키, 카테고리명

            History:
                2020-12-30(심원두): 초기 생성
                2020-12-31(심원두): 메세지 수정

            Raises:
                500, {'message': 'fail to get main category list',
                      'errorMessage': 'fail_to_get_main_category_list'}: 메인 카테고리 정보 취득 실패
        """
    
        sql = """
            SELECT
                id
                ,`name`
            FROM
                main_categories
            WHERE
                is_deleted = 0
            ORDER BY
                id;
        """
    
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                if not result:
                    raise MainCategoryNotExist('fail_to_get_main_category_list')
            
                return result
    
        except Exception as e:
            raise e

    def get_sub_category_list(self, connection, data):
        """ 메인 카테고리에 따른 서브 카테고리 정보 취득

            Args:
                connection: 데이터베이스 연결 객체
                data      : 메인 카테고리에 따른 서브 카테고리 정보를 얻기 위한 데이터

            Author: 심원두

            Returns:
                result : sub_categories 테이블에서 취득한 키, 카테고리명

            History:
                2020-12-30(심원두): 초기 생성
                2020-12-31(심원두): 메세지 수정

            Raises:
                500, {'message': 'fail to get sub category list',
                      'errorMessage': 'fail_to_get_sub_category_list'}: 색상 정보 취득 실패
        """
    
        sql = """
            SELECT
                sub_category.id AS 'sub_category_id'
                ,sub_category.`name` AS 'sub_category_name'
            FROM
                sub_categories as sub_category
                INNER JOIN main_categories as main_category
                    ON sub_category.main_category_id = main_category.id
            WHERE
                sub_category.is_deleted = 0
                AND main_category.id = %(main_category_id)s
        """
    
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchall()
            
                if not result:
                    raise SubCategoryNotExist('fail_to_get_sub_category_list')
            
                return result
    
        except Exception as e:
            raise e


    def __generate_where_sql(self, data):
        """상품 리스트 검색에 필요한 조건 쿼리문 편집
            
            Args:
                data :
                    내부 메서드 get_products_total_count(), search_products() 에서
                    넘겨 받은 딕셔너리 객체
            
            Author: 심원두
            
            Returns:
                return result (상품 총 갯수)
            
            History:
                2020-12-31(심원두): 초기 생성
                2021-01-03(심원두): 쿼리문 수정. 검색자가 셀러일 경우 조건문 추가 구현 예정
            
            Raises: -
        """
        
        where_condition = ""
        
        try:
            if data['lookup_start_date'] and data['lookup_end_date']:
                where_condition += \
                    "\nAND product.updated_at" \
                    "\nBETWEEN CONCAT(%(lookup_start_date)s, ' 00:00:00')" \
                    "\nAND CONCAT(%(lookup_end_date)s, ' 23:59:59')"
            
            if data['seller_name']:
                where_condition += "\nAND seller.`name` = %(seller_name)s"
            
            if data['product_name']:
                where_condition += "\nAND product.`name` LIKE %(product_name)s"
            
            if data['product_id']:
                where_condition += "\nAND product.id = %(product_id)s"
            
            if data['product_code']:
                where_condition += "\nAND product.product_code = %(product_code)s"
            
            if data['seller_attribute_type_ids']:
                where_condition += "\nAND seller_attribute_type.id IN %(seller_attribute_type_ids)s "
                
            if data['is_sale']:
                if int(data['is_sale']) != 1:
                    data['is_sale'] = "0"
                where_condition += "\nAND product.is_sale = %(is_sale)s"
            
            if data['is_display']:
                if int(data['is_display']) != 1:
                    data['is_display'] = "0"
                where_condition += "\nAND product.is_display = %(is_display)s"
            
            if data['is_discount']:
                if int(data['is_discount']) == 1:
                    where_condition += "\nAND product.discount_rate > 0"
                else:
                    where_condition += "\nAND product.discount_rate = 0"
            
            # TODO: Login Decorator : seller sign-in not master
            if data['seller_id']:
                where_condition += "\nAND product.seller_id = %(seller_id)s" \
        
        except Exception as e:
            raise e
        
        return where_condition
        
    def get_total_products_count(self, connection, data):
        """상품 리스트 총 갯수 취득
        
            Args:
                connection : 데이터베이스 연결 객체
                data       : 비지니스 레이어에서 넘겨 받은 딕셔너리 객체
    
            Author: 심원두
    
            Returns:
                return result (상품 총 갯수)
    
            History:
                2020-12-31(심원두): 초기 생성
                2021-01-03(심원두): 상품 리스트 총 갯수 취득 기능 작성
            
            Raises: -
        """
        
        sql = """
        SELECT
            COUNT(*) AS total_count
        FROM
            PRODUCTS AS product
            INNER JOIN PRODUCT_IMAGES AS product_image
                ON product.id = product_image.product_id AND product_image.order_index = 1
            INNER JOIN SELLERS AS seller
                ON seller.account_id = product.seller_id
            INNER JOIN SELLER_ATTRIBUTE_TYPES AS seller_attribute_type
                ON seller_attribute_type.id = seller.seller_attribute_type_id
        WHERE
            product.is_deleted = 0
            AND product_image.is_deleted = 0
            AND product_image.order_index = 1
        """
        sql += self.__generate_where_sql(data)
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            result = cursor.fetchone()
            return result
    
    def search_products(self, connection, data):
        """상품 리스트 검색
        
            Args:
                connection: 데이터베이스 연결 객체
                data      : 비지니스 레이어에서 넘겨 받은 딕셔너리 객체
            
            Author: 심원두
            
            Returns: result (상품 정보 리스트)
            
            History:
                2020-12-31(심원두): 초기 생성
                2021-01-03(심원두): 쿼리 수정
                 -seller_attribute_type 검색 조건을 완전 일치 검색에서 IN 으로 수정
            Raises:
                -
        """
        
        sql = """
        SELECT
            product.updated_at AS 'updated_at'
            ,product_image.image_url AS 'product_image_url'
            ,product.`name` AS 'product_name'
            ,product.product_code AS 'product_code'
            ,product.id AS 'product_id'
            ,seller_attribute_type.`name` AS 'seller_attribute_type'
            ,seller.`name` AS 'seller_name'
            ,product.origin_price AS 'origin_price'
            ,product.discounted_price AS 'discounted_price'
            ,product.discount_rate AS 'discount_rate'
            ,product.is_sale AS 'is_sale'
            ,product.is_display AS 'is_display'
        FROM
            PRODUCTS AS product
            INNER JOIN PRODUCT_IMAGES AS product_image
                ON product.id = product_image.product_id AND product_image.order_index = 1
            INNER JOIN SELLERS AS seller
                ON seller.account_id = product.seller_id
            INNER JOIN SELLER_ATTRIBUTE_TYPES AS seller_attribute_type
                ON seller_attribute_type.id = seller.seller_attribute_type_id
        WHERE
            product.is_deleted = 0
            AND product_image.is_deleted = 0
            AND product_image.order_index = 1
        """
        
        sql     += self.__generate_where_sql(data)
        order_by = "\nORDER BY product.id DESC"
        limit    = "\nLIMIT %(offset)s, %(limit)s;"
        
        sql += order_by + limit
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            result = cursor.fetchall()
            return result
    
    def get_product_detail(self, connection, data):
        """상품 상세 정보 취득
            
            Args:
                connection : 데이터베이스 연결 객체
                data       : 서비스 레이어에서 넘겨 받은 상품 검색에 사용될 키값
                
            Author: 심원두
            
            Returns:
                result : 상품 정보
            
            History:
                2021-01-02(심원두): 초기 생성
                2021-01-02(심원두): 쿼리문 수정
            
            Raises:
                500, {'message': 'product does not exist',
                      'errorMessage': 'product_does_not_exist'} : 상품 정보 취득 실패
        """
        
        sql = """
        SELECT
            product.`id` AS 'product_id'
            ,product.`product_code` AS 'product_code'
            ,product.seller_id AS 'seller_id'
            ,seller.`name` AS 'seller_name'
            ,product.`is_sale` AS 'is_sale'
            ,product.`is_display` AS 'is_display'
            ,product.main_category_id AS 'main_category_id'
            ,main_category.`name` AS 'main_category_name'
            ,product.sub_category_id AS 'sub_category_id'
            ,sub_category.`name` AS 'sub_category_name'
            ,product.`is_product_notice` AS 'is_product_notice'
            ,product.`manufacturer` AS 'manufacturer'
            ,product.`manufacturing_date` AS 'manufacturing_date'
            ,product.`product_origin_type_id` AS 'product_origin_type_id'
            ,product_origin_type.`name` AS 'product_origin_type_name'
            ,product.`name` AS 'product_name'
            ,product.`description` AS 'description'
            ,product.`detail_information` AS 'detail_information'
            ,product.`origin_price` AS 'origin_price'
            ,product.`discount_rate` AS 'discount_rate'
            ,product.`discounted_price` AS 'discounted_price'
            ,product.`discount_start_date` AS 'discount_start_date'
            ,product.`discount_end_date` AS 'discount_end_date'
            ,product.`minimum_quantity` AS 'minimum_quantity'
            ,product.`maximum_quantity` AS 'maximum_quantity'
            ,product.`updated_at` AS 'updated_at'
        FROM
            products AS product
        INNER JOIN sellers AS seller
            ON product.seller_id = seller.account_id
        INNER JOIN main_categories AS main_category
            ON product.main_category_id = main_category.id
        INNER JOIN sub_categories AS sub_category
            ON product.sub_category_id = sub_category.id
        LEFT JOIN product_origin_types AS product_origin_type
            ON product.product_origin_type_id = product_origin_type.id
        WHERE
            product.is_deleted = 0
            AND product.`product_code` = %(product_code)s
        """
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            result = cursor.fetchone()
            
            if not result:
                raise ProductNotExist('product_does_not_exist')
            
            return result
    
    def get_product_images(self, connection, data):
        """상품 이미지 정보 리스트 취득
        
            Args:
                connection : 데이터베이스 연결 객체
                data       : 서비스 레이어에서 넘겨 받은 상품 이미지 취득에 사용될 키값
                
            Author: 심원두
            
            Returns:
                result : 상품 이미지 정보 리스트
            
            History:
                2021-01-02(심원두): 초기 생성
                2021-01-03(심원두): 불필요한 취득 항목 삭제
                
            Raises:
                500, {'message': 'product image not exist',
                      'errorMessage': 'product_image_not_exist'}: 상품 이미지 정보 취득 실패
        """
        
        sql = """
        SELECT
            image_url AS 'product_image_url'
            ,order_index AS 'order_index'
        FROM
            product_images
        WHERE
            is_deleted = 0
            AND product_id = %(product_id)s
        ORDER BY
            order_index ASC;
        """
        
        try:
            
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchall()
                
                if not result:
                    raise ProductImageNotExist('product_image_not_exist')
                
                return result
        
        except Exception as e:
            raise e
    
    def get_product_options(self, connection, data):
        """상품 옵션 리스트 취득
            
            Args:
                connection : 데이터베이스 연결 객체
                data       : 서비스 레이어에서 넘겨 받은 상품 옵션 정보 취득에 사용될 키값
                
            Author: 심원두
            
            Returns:
                result : 상품 옵셥 리스트
                
            History:
                2021-01-02(심원두): 초기 생성
                2021-01-03(심원두): 컬럼 is_stock_manage 추가 대응
            Raises:
                500, {'message': 'stock info not exist',
                      'errorMessage': 'stock_does_not_exist'} : 옵션 정보 취득 실패
        """
        
        sql = """
        SELECT
            stock.id AS 'stock_id'
            ,stock.product_option_code AS 'product_option_code'
            ,color.`id` AS 'color_id'
            ,color.`name` AS 'color_name'
            ,size.`id` AS 'size_id'
            ,size.`name` AS 'size_name'
            ,stock.remain AS 'remain'
            ,stock.`is_stock_manage` AS 'is_stock_manage'
        FROM
            stocks AS stock
            INNER JOIN colors AS color
                ON stock.color_id = color.id
            INNER JOIN sizes AS size
                ON stock.size_id = size.id
        WHERE
            stock.is_deleted = 0
            AND stock.product_id = %(product_id)s
        ORDER BY
            stock.product_option_code ASC;
        """
        
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchall()
                
                if not result:
                    raise StockNotNotExist('stock_does_not_exist')
        
                return result
        
        except Exception as e:
            raise e