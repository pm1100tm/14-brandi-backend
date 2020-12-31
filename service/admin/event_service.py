class EventService:

    def __init__(self, event_dao):
        self.event_dao = event_dao

    def get_events_service(self, connection, data):
        try:
            data['page'] = (data['page']-1) * data['length']
            if data['name']:
                data['name'] = '%' + data['name'] + '%'
            return self.event_dao.get_events_list(connection, data)

        except Exception as e:
            raise e

    def get_products_category_service(self, connection, data):
        try:
            return self.event_dao.get_product_category(connection, data)

        except Exception as e:
            raise e

    def get_products_to_post_service(self, connection, data):
        pass
        """ 기획전에 추가할 상품 조회

        Args:
            connection:
            data:

        Returns:

        """
