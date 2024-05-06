from .base_page import BasePage


class Router:
    routes: dict = {}

    def register_routes(self, routes: dict):
        if routes is None:
            return

        for key, value in routes.items():
            self.register_route(key, value)

    def register_route(self, key: str, page_class: BasePage):
        self.routes[key] = page_class

    def get_page(self, app, key: str):
        page_class = self.routes.get(key)

        if page_class is None:
            return None

        return page_class(app)
