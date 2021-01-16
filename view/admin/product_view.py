import traceback

from flask                          import jsonify, request, json, g
from flask.views                    import MethodView
from flask_request_validator.rules  import NotEmpty
from flask_request_validator        import Param, GET, PATH, FORM, Enum, MaxLength, validate_params

from utils.connection               import get_connection
from utils.const                    import ACCOUNT_ADMIN
from utils.custom_exceptions        import DatabaseCloseFail
from utils.decorator                import signin_decorator
from utils.rules                    import NumberRule, PageRule, DateRule, DefaultRule


class ProductRegistView(MethodView):
    """ Presentation Layer

        Attributes:
            service  : ProductManageService 클래스
            database : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 심원두

        History:
            2020-12-29(심원두): 초기 생성. products insert, product_code updated, product_histories 생성 기능 작성
            2020-12-30(심원두): 각 Param rules 추가, stock insert 기능 작성.
            2020-01-03(심원두): 상품 등록 Param rules 추가
            2021-01-13(심원두): refactoring 초기 작성
            2021-01-15(심원두):
                상품 등록 초기 화면 기능 작성 완료. 권한 타입 상수 생성. 권한에 따른 분기 처리 완료.
                파라미터 유효성 검증을 위한 RULE 설정 완료.
    """
    
    def __init__(self, service, database):
        self.service = service
        self.database = database
    
    @signin_decorator()
    @validate_params(
        Param('seller_name',      GET, str, required=False, rules=[NotEmpty(), MaxLength(20)]),
        Param('seller_id',        GET, str, required=False, rules=[NotEmpty(), NumberRule()]),
        Param('main_category_id', GET, str, required=False, rules=[NotEmpty(), NumberRule()]),
    )
    def get(self, *args):
        """ GET 메소드: 상품 등록 초기 화면
            
            Args:
                'seller_name'      : 셀러명
                'seller_id'        : 셀러 아이디
                'main_category_id' : 메인 카테고리 아이디
            
            Author: 심원두
            
            Returns:
                result - 아래의 조건에 따라 분기 처리
                    1. 관리자 권한 초기 화면            - 원산지, 색상, 사이즈 정보 출력
                    2. 관리자 권한 셀러 검색            - 셀러 정보 리스트 출력
                    3. 관리자 권한 셀러 선택            - 메인 카테고리 리스트 출력
                    4. 관리자&셀러 권한 메인 카테고리 선택 - 서브 카테고리 출력
                    5. 셀러 권한 초기화면               - 원산지, 색상, 사이즈, 메인 카테고리 정보 출력
                    
            Raises:
                
                400, {'message': 'internal_server_error',
                      'errorMessage': 'PERMISSION_ERROR' + format(e)}: 잘못된 권한
                
                500, {'message': 'fail to get main category list',
                      'errorMessage': 'fail_to_get_main_category_list'}: 메인 카테고리 정보 취득 실패
                      
                500, {'message': 'fail to get sub category list',
                      'errorMessage': 'fail_to_get_sub_category_list'}: 색상 정보 취득 실패
                
                500, {'message': 'fail to get color list',
                      'errorMessage': 'fail_to_get_color_list'}: 색상 정보 취득 실패
                
                500, {'message': 'fail to get size list',
                      'errorMessage': 'fail_to_get_size_list'}: 색상 정보 취득 실패
                
                500, {'message': 'fail to get product origin types',
                      'errorMessage': 'fail_to_get_product_origin_types'} : 원산지 정보 취득 실패
            
            History:
                2020-12-30(심원두): 초기생성
                2021-01-06(심원두): 로그인 데코레이터 처리 추가
                2021-01-15(심원두): 관리자/셀러 권한별 기능 분기 처리
        """
        
        connection = None
        
        try:
            connection = get_connection(self.database)
            
            data = {
                'seller_name'        : request.args.get('seller_name'),
                'seller_id'          : request.args.get('seller_id'),
                'main_category_id'   : request.args.get('main_category_id'),
                'permission_type_id' : g.permission_type_id
            }
            
            result = dict()
            
            if data['seller_name']:
                result['seller_list'] = self.service.\
                    get_seller_list_by_name_service(
                        connection,
                        data
                    )
                
                return jsonify({'message': 'success', 'result': result}), 200
            
            if data['seller_id']:
                result['main_category_list'] = self.service.\
                    get_main_category_list_service(
                        connection
                    )
            
            if data['main_category_id']:
                result['sub_category_list'] = self.service. \
                    get_sub_category_list_service(
                        connection,
                        data
                    )
                
                return jsonify({'message': 'success', 'result': result}), 200
            
            result['product_origin_types'] = self.service.get_product_origin_types_service(connection)
            result['color_list']           = self.service.get_color_list_service(connection)
            result['size_list']            = self.service.get_size_list_service(connection)
            
            return jsonify({'message': 'success', 'result': result}), 200
        
        except KeyError as e:
            traceback.print_exc()
            raise e
        
        except Exception as e:
            traceback.print_exc()
            raise e
        
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('DATABASE_CLOSE_FAIL')
    
    @signin_decorator()
    @validate_params(
        Param('seller_id'             , FORM, str , required = True  , rules = [NumberRule()]),
        Param('is_sale'               , FORM, bool , required = True  , rules = [Enum(0          , 1)]),
        Param('is_display'            , FORM, bool , required = True  , rules = [Enum(0          , 1)]),
        Param('main_category_id'      , FORM, str , required = True  , rules = [NumberRule()]),
        Param('sub_category_id'       , FORM, str , required = True  , rules = [NumberRule()]),
        Param('is_product_notice'     , FORM, bool , required = True  , rules = [Enum(0          , 1)]),
        Param('manufacturer'          , FORM, str , required = False , rules = [MaxLength(30)]),
        Param('manufacturing_date'    , FORM, str , required = False),
        Param('product_origin_type_id', FORM, str , required = False),
        Param('product_name'          , FORM, str , required = True  , rules = [NotEmpty()      , MaxLength(100)]),
        Param('description'           , FORM, str , required = False , rules = [MaxLength(200)]),
        Param('detail_information'    , FORM, str , required = True  , rules = [NotEmpty()]),
        Param('options'               , FORM, list, required = True),
        Param('minimum_quantity'      , FORM, str , required = False , rules = [NumberRule()]),
        Param('maximum_quantity'      , FORM, str , required = False , rules = [NumberRule()]),
        Param('origin_price'          , FORM, str , required = True  , rules = [NumberRule()]),
        Param('is_discount'           , FORM, str, required=True, rules=[NumberRule()]),
        Param('discount_rate'         , FORM, str , required = True  , rules = [NumberRule()]),
        Param('discounted_price'      , FORM, str , required = True  , rules = [NumberRule()]),
        Param('discount_start_date'   , FORM, str , required = False),
        Param('discount_end_date'     , FORM, str , required = False)
    )
    def post(self, *args):
        """ POST 메소드: 상품 정보 등록
            
            Args:
            - 사용자 입력 값(상품 이미지 최대 5개) : image_files
            - 사용자 입력 값(옵션 정보 리스트)    : options
            - 사용자 입력 값
            Form-Data: (
                'seller_id'
                'is_sale'
                'is_display'
                'main_category_id'
                'sub_category_id'
                'is_product_notice'
                'manufacturer'
                'manufacturing_date'
                'product_origin_type_id'
                'product_name'
                'description'
                'detail_information'
                'options'
                'minimum_quantity'
                'maximum_quantity'
                'origin_price'
                'discount_rate'
                'discounted_price'
                'discount_start_date'
                'discount_end_date'
            )
            
            Author: 심원두
            
            Returns:
                201, {'message': 'success'}                                                   : 상품 정보 등록 성공
            
            Raises:
                400, {'message': 'key_error',
                      'errorMessage': 'key_error_' + format(e)}                               : 잘못 입력된 키값

                400, {'message': 'required field is blank',
                      'errorMessage': 'required_manufacture_information'}                     : 제조 정보 필드 없음

                400, {'message': 'required field is blank',
                      'errorMessage': 'required_discount_start_or_end_date'}                  : 필수 입력 항목 없음

                400, {'message': 'compare quantity field check error',
                      'errorMessage': 'minimum_quantity_cannot_greater_than_maximum_quantity'}: 최소 구매 수량이 최대 보다 큼

                400, {'message': 'compare price field check error',
                      'errorMessage': 'discounted_price_cannot_greater_than_origin_price'}    : 할인가가 판매가 보다 큼

                400, {'message': 'compare price field check error',
                      'errorMessage': 'wrong_discounted_price'}                               : 판매가와 할인가 일치하지 않음

                400, {'message': 'compare price field check error',
                      'errorMessage': 'required_discount_start_or_end_date'}                  : 할인 시작, 종료 일자 필드 없음

                400, {'message': 'start date is greater than end date',
                      'errorMessage': 'start_date_cannot_greater_than_end_date'}              : 할인 시작일이 종료일 보다 큼

                400, {'message': 'compare price field check error',
                      'errorMessage': 'discounted_price_have_to_same_with_origin_price'}      : 할인가, 판매가 불일치(할인율 0)

                413, {'message': 'invalid file',
                      'errorMessage': 'invalid_file'}                                         : 파일 이름이 공백, 혹은 파일을 정상적으로 받지 못함

                413, {'message': 'file size too large',
                      'errorMessage': 'file_size_too_large'}                                  : 파일 사이즈 정책 위반 (4메가 이상인 경우)

                413, {'message': 'file scale too small, 640 * 720 at least',
                      'errorMessage': 'file_scale_at_least_640*720'}                          : 파일 스케일 정책 위반 (680*720 미만인 경우)

                413, {'message': 'only allowed jpg type',
                      'errorMessage': 'only_allowed_jpg_type'}                                : 파일 확장자 정책 위반 (JPG, JPEG 아닌 경우)

                500, {'message': 'image_file_upload_to_amazon_fail',
                      'errorMessage': 'image_file_upload_fail'}                               : 이미지 업로드 실패

                500, {'message': 'product create denied',
                      'errorMessage': 'unable_to_create_product'}                             : 상품 정보 등록 실패

                500, {'message': 'product code update denied',
                      'errorMessage': 'unable_to_update_product_code'}                        : 상품 코드 갱신 실패

                500, {'message': 'product code update denied',
                      'errorMessage': 'unable_to_update_product_code'}                        : 상품 코드 갱신 실패

                500, {'message': 'product image create denied',
                      'errorMessage': 'unable_to_create_product_image'}                       : 상품 이미지 등록 실패

                500, {'message': 'stock create denied',
                      'errorMessage': 'unable_to_create_stocks'}                              : 상품 옵션 정보 등록 실패

                500, {'message': 'product history create denied',
                      'errorMessage': 'unable_to_create_product_history'}                     : 상품 이력 등록 실패

                500, {'message': 'bookmark volumes create denied',
                      'errorMessage': 'unable_to_create_bookmark_volumes'}                    : 북마크 초기 등록 실패

                500, {'message': 'database_connection_fail',
                      'errorMessage': 'database_close_fail'}                                  : 커넥션 종료 실패

                500, {'message': 'database_error',
                      'errorMessage': 'database_error_' + format(e)}                          : 데이터베이스 에러

                500, {'message': 'internal_server_error',
                      'errorMessage': format(e)})                                             : 서버 에러
            
            History:
                2020-12-29(심원두): 초기 생성
                2021-01-03(심원두): 파라미터 유효성 검사 추가 Enum(), NotEmpty()
                2021-01-05(심원두): -이미지 저장 처리 순서를 3번째에서 가장 마지막으로 내림. 테이블 인서트 처리에 문제가 있을 경우,
                                    S3에 올라간 이미지는 롤백을 할 수 없는 이슈 반영.
                                   -북마크 테이블 초기 등록 처리 추가.
        """
        
        try:
            data = {
                'seller_id'             : request.form.get('seller_id'),
                'account_id'            : g.account_id,
                'is_sale'               : request.form.get('is_sale'),
                'is_display'            : request.form.get('is_display'),
                'main_category_id'      : request.form.get('main_category_id'),
                'sub_category_id'       : request.form.get('sub_category_id'),
                'is_product_notice'     : request.form.get('is_product_notice'),
                'manufacturer'          : request.form.get('manufacturer'),
                'manufacturing_date'    : request.form.get('manufacturing_date'),
                'product_origin_type_id': request.form.get('product_origin_type_id'),
                'product_name'          : request.form.get('product_name'),
                'description'           : request.form.get('description'),
                'detail_information'    : request.form.get('detail_information'),
                'minimum_quantity'      : request.form.get('minimum_quantity'),
                'maximum_quantity'      : request.form.get('maximum_quantity'),
                'origin_price'          : request.form.get('origin_price'),
                'discount_rate'         : request.form.get('discount_rate'),
                'discounted_price'      : request.form.get('discounted_price'),
                'discount_start_date'   : request.form.get('discount_start_date'),
                'discount_end_date'     : request.form.get('discount_end_date')
            }
            
            product_images = request.files.getlist("image_files")
            stocks         = json.loads(request.form.get('options'))
            connection     = get_connection(self.database)
            
            product_id = self.service.create_product_service(
                connection,
                data
            )
            
            product_code = self.service.update_product_code_service(
                connection,
                product_id
            )
            
            self.service.create_stock_service(
                connection,
                product_id,
                stocks
            )
            
            self.service.create_product_history_service(
                connection,
                product_id,
                data
            )
            
            self.service.create_product_sales_volumes_service(
                connection,
                product_id
            )
            
            self.service.create_bookmark_volumes_service(
                connection,
                product_id
            )
            
            self.service.create_product_images_service(
                connection,
                data['seller_id'],
                product_id,
                product_code,
                product_images
            )
            
            connection.commit()
            
            return jsonify({'message': 'success'}), 201
            
        except KeyError as e:
            traceback.print_exc()
            connection.rollback()
            raise e
    
        except Exception as e:
            traceback.print_exc()
            connection.rollback()
            raise e
    
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                traceback.print_exc()
                raise DatabaseCloseFail('database close fail')

            
class ProductManageSearchView(MethodView):
    """ Presentation Layer

        Attributes:
            service  : MainCategoryListService 클래스
            database : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 심원두

        History:
            2020-12-31(심원두): 초기 작성
            2021-01-03(심원두): 상품 리스트 검색 기능 구현
    """
    def __init__(self, service, database):
        self.service = service
        self.database = database
    
    @signin_decorator()
    @validate_params(
        Param('lookup_start_date', GET, str, required=False, rules=[DateRule(), NotEmpty()]),
        Param('lookup_end_date'  , GET, str, required=False, rules=[DateRule(), NotEmpty()]),
        Param('seller_name'      , GET, str, required=False, rules=[DefaultRule(), NotEmpty(), MaxLength(20)]),
        Param('product_name'     , GET, str, required=False, rules=[DefaultRule(), NotEmpty(), MaxLength(100)]),
        Param('product_id'       , GET, str, required=False, rules=[NumberRule() , NotEmpty()]),
        Param('product_code'     , GET, str, required=False, rules=[DefaultRule(), NotEmpty(), MaxLength(20)]),
        Param('is_sale'          , GET, int, required=False, rules=[Enum(1, 2)]),
        Param('is_display'       , GET, int, required=False, rules=[Enum(1, 2)]),
        Param('is_discount'      , GET, int, required=False, rules=[Enum(1, 2)]),
        Param('page_number'      , GET, int, required=True , rules=[PageRule()]),
        Param('limit'            , GET, int, required=True , rules=[Enum(10, 20, 50)])
    )
    def get(self, *args):
        """GET 메소드: 특정 조건에 해당하는 상품 리스트를 조회한다.
            
            Args:
                'lookup_start_date'       : 조회 시작 기간
                'lookup_end_date'         : 조회 종료 기간
                'seller_name'             : 셀러명
                'product_name'            : 상품명
                'product_id'              : 상품 아이디
                'product_code'            : 상품 코드
                'seller_attribute_type_id : 셀러 속성
                'is_sale'                 : 할인 여부
                'is_display'              : 진열 여부
                'is_discount'             : 할인 여부
                'page_number'             : 페이지 번호
                'limit'                   : 한 화면에 보여줄 상품의 갯수
                
            Author: 심원두
            
            Returns:
                return {"message": "success", "result": result}
            
            Raises:
                400, {'message': 'key error',
                      'errorMessage': 'key_error' + format(e)} : 잘못 입력된 키값
                      
                400, {'message': 'both date field required',
                      'errorMessage': 'both_date_field_required'}: 필수 값 유효성 체크 에러
                      
                400, {'message': 'start date is greater than end date',
                      'errorMessage': 'start_date_is_greater_than_end_date'}: 날짜 비교 유효성 체크 에러
                
                400, {'message': 'invalid seller attribute type',
                      'errorMessage': 'invalid_seller_attribute_type'}: 셀러 타입 유효성 체크 에러
            
            History:
                2020-12-31(심원두): 초기생성
                2021-01-03(심원두): 상품 리스트 검색 기능 구현, Login Decorator 구현 예정
        """
        
        try:
            search_condition = {
                'seller_id'                 : g.account_id if g.permission_type_id == 2 else None,
                'lookup_start_date'         : request.args.get('lookup_start_date', None),
                'lookup_end_date'           : request.args.get('lookup_end_date', None),
                'seller_name'               : request.args.get('seller_name', None),
                'product_name'              : request.args.get('product_name', None),
                'product_id'                : request.args.get('product_id', None),
                'product_code'              : request.args.get('product_code', None),
                'seller_attribute_type_ids' : json.loads(request.args.get('seller_attribute_type_id'))
                                              if request.args.get('seller_attribute_type_id')
                                              else None,
                'is_sale'                   : request.args.get('is_sale', None),
                'is_display'                : request.args.get('is_display', None),
                'is_discount'               : request.args.get('is_discount', None),
                'page_number'               : request.args.get('page_number'),
                'limit'                     : request.args.get('limit')
            }
            
            connection = get_connection(self.database)
            result     = self.service.search_product_service(connection, search_condition)
            
            return jsonify({'message': 'success', 'result': result})
        
        except KeyError as e:
            traceback.print_exc()
            raise e
        
        except Exception as e:
            traceback.print_exc()
            raise e
        
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')


class ProductManageDetailView(MethodView):
    """ Presentation Layer

        Attributes:
            service  : ProductManageDetailView 클래스
            database : app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)

        Author: 심원두

        History:
            2021-01-02(심원두): 초기 작성
    """
    def __init__(self, service, database):
        self.service = service
        self.database = database
    
    @signin_decorator()
    @validate_params(
        Param('product_code', PATH, str, required=True, rules=[NotEmpty(), MaxLength(20)]),
    )
    def get(self, *args):
        """GET 메소드: 상품 코드에 해당하는 상품 정보를 불러온다.

            Args:
                'product_code' : 상품 코드
    
            Author: 심원두

            Returns:
                return {"message": "success", "result": result}
            
            Raises:
                500, {'message': 'product does not exist',
                      'errorMessage': 'product_does_not_exist'} : 상품 정보 취득 실패
                      
                500, {'message': 'product image not exist',
                      'errorMessage': 'product_image_not_exist'}: 상품 이미지 정보 취득 실패
                      
                500, {'message': 'stock info not exist',
                      'errorMessage': 'stock_does_not_exist'}: 옵션 정보 취득 실패
            
            History:
                2021-01-02(심원두): 초기 작성
        """
        
        try:
            data = {
                'product_code' : request.view_args['product_code']
            }
            
            connection = get_connection(self.database)
            result     = self.service.detail_product_service(connection, data)
            
            return jsonify({'message': 'success', 'result': result})
        
        except Exception as e:
            raise e
        
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')
