import pymysql
from utils.custom_exceptions import EventDoesNotExist, CategoryMenuDoesNotMatch, CategoryDoesNotExist


class EventDao:
    """ Persistence Layer

        Attributes: None

        Author: 강두연

        History:
            2020-12-28(강두연): 초기 생성 및 조회 기능 작성
            2020-12-29(강두연): 이벤트 검색조건별 조회 작성
    """

    def get_events_list(self, connection, data):
        """기획전 정보 조회

            Args:
                connection: 데이터베이스 연결 객체
                data   : 비지니스 레이어에서 넘겨 받은 검색 조건 키벨류

            Author: 강두연

            Returns:
                return [
                    {
                        "created_at": "Mon, 28 Dec 2020 16:40:41 GMT",
                        "end_date": "Mon, 01 Mar 2021 00:00:00 GMT",
                        "event_kind": "버튼",
                        "event_name": "성보의 하루 시리즈2(버튼형)",
                        "event_number": 2,
                        "event_status": "진행중",
                        "event_type": "상품(이미지)",
                        "is_display": "노출",
                        "product_count": 59,
                        "start_date": "Mon, 19 Oct 2020 00:00:00 GMT"
                    },
                    {
                        "created_at": "Mon, 28 Dec 2020 16:40:41 GMT",
                        "end_date": "Mon, 01 Mar 2021 00:00:00 GMT",
                        "event_kind": "상품",
                        "event_name": "성보의 하루 시리즈",
                        "event_number": 1,
                        "event_status": "진행중",
                        "event_type": "상품(이미지)",
                        "is_display": "노출",
                        "product_count": 40,
                        "start_date": "Mon, 19 Oct 2020 00:00:00 GMT"
                    }
                ]

            History:
                2020-12-28(강두연): 초기 생성 및 조회 기능 작성
                2020-12-29(강두연): 이벤트 검색조건별 조회 작성

            Raises:
                400, {'message': 'event not exist', 'errorMessage': 'event does not exist'} : 이벤트 정보 조회 실패
        """

        total_count_sql = """
            SELECT
                COUNT(*) AS total_count
            FROM `events` AS `event`
                INNER JOIN event_types AS event_type
                    ON `event`.event_type_id = event_type.id
                INNER JOIN event_kinds AS event_kind
                   ON `event`.event_kind_id = event_kind.id
            WHERE
                `event`.is_deleted = 0
        """

        sql = """
            SELECT
                `event`.id AS event_number
                , `event`.`name` AS event_name
                , CASE WHEN NOW() BETWEEN `event`.start_date AND `event`.end_date THEN '진행중'
                     WHEN NOW() < `event`.start_date THEN '대기'
                     ELSE '종료' END AS event_status
                , event_type.`name` AS event_type
                , event_kind.`name` AS event_kind
                , `event`.start_date AS start_date
                , `event`.end_date AS end_date
                , CASE WHEN `event`.is_display = 0 THEN '비노출' ELSE '노출' END AS is_display
                , `event`.created_at AS created_at
                , (SELECT COUNT(CASE WHEN events_products.event_id = `event`.id THEN 1 END)
                    FROM events_products) AS product_count
            FROM `events` AS `event`
                INNER JOIN event_types AS event_type
                    ON `event`.event_type_id = event_type.id
                INNER JOIN event_kinds AS event_kind
                   ON `event`.event_kind_id = event_kind.id
            WHERE
                `event`.is_deleted = 0
        """

        # search option 1 : search by keyword (event_name or event_number)
        if data['name']:
            total_count_sql += ' AND `event`.`name` LIKE %(name)s'
            sql += ' AND `event`.`name` LIKE %(name)s'
        elif data['number']:
            total_count_sql += ' AND `event`.id = %(number)s'
            sql += ' AND `event`.id = %(number)s'

        # search option 2 : search by event_status
        if data['status'] == 'progress':
            total_count_sql += ' AND NOW() BETWEEN `event`.start_date AND `event`.end_date'
            sql += ' AND NOW() BETWEEN `event`.start_date AND `event`.end_date'
        elif data['status'] == 'wait':
            total_count_sql += ' AND NOW() < `event`.start_date'
            sql += ' AND NOW() < `event`.start_date'
        elif data['status'] == 'end':
            total_count_sql += ' AND NOW() > `event`.end_date'
            sql += ' AND NOW() > `event`.end_date'

        # search option 3 : exposure
        if data['exposure'] is not None and data['exposure']:
            total_count_sql += ' AND `event`.is_display = 1'
            sql += ' AND `event`.is_display = 1'
        elif data['exposure'] is not None and not data['exposure']:
            total_count_sql += ' AND `event`.is_display = 0'
            sql += ' AND `event`.is_display = 0'

        # search option 4 : event_registered_date
        if data['start_date'] and data['end_date']:
            total_count_sql += """
                AND `event`.created_at BETWEEN CONCAT(%(start_date)s, " 00:00:00") AND CONCAT(%(end_date)s, " 23:59:59")
            """
            sql += """
                AND `event`.created_at BETWEEN CONCAT(%(start_date)s, " 00:00:00") AND CONCAT(%(end_date)s, " 23:59:59")
            """

        sql += ' ORDER BY `event`.id DESC LIMIT %(page)s, %(length)s;'

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            events = cursor.fetchall()
            cursor.execute(total_count_sql, data)
            count = cursor.fetchall()
            if not events:
                raise EventDoesNotExist('event does not exist')
            return {'events': events, 'total_count': count[0]['total_count']}

    def get_products_list_to_post(self, connection, data):
        pass
        """ 기획전에 추가할 상품 조회

        Args:
            connection:
            data:

        Returns:

        """
        total_count_sql = """
            SELECT
                COUNT(*) AS total_count
        """

        sql = """
            SELECT 
                product.id
                , product_image.image_url AS thumbnail_image_url
                , product.product_code AS product_number
                , product.`name` AS product_name
                , seller.`name` AS seller_name
                , product.original_price AS original_price
                , prodcut.discounted_price AS discounted_price
                , product.discount_rate AS discount_rate
                , product.is_sale AS is_sale
                , product.is_display AS is_display
        """
        extra_sql = """
            FROM 
                products AS product
                INNER JOIN product_images AS product_image
                    ON product.id = product_image.product_id AND product_image.order_index = 1
                INNER JOIN sellers AS seller
                    ON product.seller_id = seller.id
            WHERE 
                product.is_deleted = 0
        """

        """
                # 검색하기 [최소 1개 필수] 상품명, 상품번호, 셀러명, 셀러번호, 상품 분류, 상품 등록일
                -- AND product.name LIKE CONCAT('%', %(product_name)s, '%')														# 상품명 -- like 어떻게 하는지 알아보기
                -- AND product.product_code = %(product_code)s																	# 상품번호
                -- AND seller.`name` = %(seller_name)s																			# 셀러명
                -- AND seller.account_id = %(seller_id)s																		# 셀러번호
                -- AND product.created_at BETWEEN CONCAT(%(YYYY-MM-DD)s, ' 00:00:00') AND CONCAT(%(YYYY-MM-DD)s, ' 23:59:59') 	# 상품 등록일 기준으로 상품 조회하기 [날짜 두개 들어와야함]
                # 상품분류 [셀러구분 셋 중 하나]
                -- AND seller.seller_attribute_type_id IN (1, 2, 3) 															# 트렌드 상품 불러오기
                -- AND seller.seller_attribute_type_id IN (4, 5, 6) 															# 브랜드 상품 블러오기
                -- AND seller.seller_attribute_type_id = 7																		# 뷰티 상품 불러오기
                    -- AND product.main_category_id = {main_category_id}														# 1차 카테고리에 맞게 상품 불러오기 [셀러 구분 선택시 선택가능]
                        -- AND product.sub_category_id = {sub_category_id}														# 2차 카테고리에 맞게 상품 불러오기 [1차 카테고리 선택시 선택가능]
            ORDER BY 
                product.id DESC
            LIMIT 0, 10;

        """

    def get_product_category(self, connection, data):
        """  기획전에 추가될 상품 조회 검색조건에서 카테고리 불러오기

        Args:
            connection:
            data:

        Returns:

       """
        if not data['menu_id'] and not data['first_category_id']:
            sql = """
                SELECT
                     id
                     , CASE WHEN id=4 THEN '트렌드' ELSE `name` END AS `name` 
                 FROM 
                    menus WHERE id = 4 OR id = 5 OR id = 6;
            """
        elif data['menu_id'] and not data['first_category_id']:
            sql = """
                SELECT 
                    id
                    , `name` 
                FROM 
                    main_categories 
                WHERE 
                    menu_id = %(menu_id)s;
            """
        elif data['menu_id'] and data['first_category_id']:
            validate_sql = """
                SELECT
                    id
                FROM
                    main_categories
                WHERE
                    menu_id = %(menu_id)s
                AND id = %(first_category_id)s;
            """

            sql = """
                SELECT
                    id
                    , `name`
                FROM
                    sub_categories
                WHERE
                    main_category_id = %(first_category_id)s;
            """
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(validate_sql, data)
                result = cursor.fetchone()
                if not result:
                    raise CategoryMenuDoesNotMatch('category and menu does not match')

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, data)
            result = cursor.fetchall()
            if not result:
                raise CategoryDoesNotExist
            return result
