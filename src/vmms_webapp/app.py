"""Vending Machine Management System Webapp.

This script allows the user to manage vending machines and their the product
stocks by interacting with the database. It is assumed that the products table
in the database is not empty.

This file can also be imported as a module and contains the following
functions:

    * create_app - returns a flask app
"""
import http

from flask import Flask, Response, jsonify, make_response, render_template, request
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.exc import NoResultFound

from vmms_webapp.database import utils
from vmms_webapp.database.database_service import DatabaseService


def create_app(database_service: DatabaseService) -> Flask:
    """Create flask app.

    Args:
        database_service (DatabaseService): The object used to interact with database

    Returns:
        Flask: An app
    """
    app = Flask(__name__)

    csrf = CSRFProtect()
    csrf.init_app(app)

    # SECURITY WARNING:
    # make sure the secret key is complex and secret in production
    # this will be used to encrypt the cookies
    app.secret_key = "use-more-complex-secret-key-please"
    app.config["SQLALCHEMY_DATABASE_URI"] = database_service.get_uri()

    @app.route("/")
    def index() -> str:
        vending_machines = utils.get_vending_machines(database_service)
        return render_template(
            "index.html",
            data=[
                (
                    vending_machine,
                    utils.get_product_choices_by_vm_id(
                        database_service, vending_machine.id
                    ),
                    utils.get_stocks_by_vm_id(database_service, vending_machine.id),
                )
                for vending_machine in vending_machines
            ],
        )

    @app.route("/vending_machines/add")
    def add_vending_machine() -> str:
        return render_template("add.html")

    @app.route("/vending_machines/update/<int:vm_id>")
    def update_vending_machine(vm_id: int) -> str:
        vending_machine = utils.get_vending_machine_by_id(database_service, vm_id)
        return render_template("update.html", vending_machine=vending_machine)

    @app.route("/api/vending_machines/add", methods=["POST"])
    def api_add_vending_machine() -> Response:
        status_code = http.HTTPStatus.OK
        try:
            vending_machine = utils.create_vending_machine_from_request(request)
            response = utils.add_vending_machine(database_service, vending_machine)
        except Exception as e:
            print("api_add_vending_machine:", e)
            status_code = http.HTTPStatus.BAD_REQUEST
            response = {
                "status": "error",
                "data": {"post": {}},
                "message": "unable to add new vending machine",
            }
        return make_response(jsonify(response), status_code)

    @app.route("/api/vending_machines/update/<int:vm_id>", methods=["POST"])
    def api_update_vending_machine(vm_id: int) -> Response:
        status_code = http.HTTPStatus.OK
        try:
            if utils.get_vending_machine_by_id(database_service, vm_id):
                new_vending_machine = utils.create_vending_machine_from_request(request)
                response = utils.update_vending_machine(
                    database_service, new_vending_machine, vm_id
                )
            else:
                raise NoResultFound(f"vending machine {vm_id} does not exist")
        except Exception as e:
            print("api_update_vending_machine:", e)
            status_code = http.HTTPStatus.BAD_REQUEST
            response = {
                "status": "error",
                "data": {"post": {}},
                "message": f"unable to update vending machine {vm_id}",
            }
        return make_response(jsonify(response), status_code)

    @app.route("/api/vending_machines/delete/<int:vm_id>", methods=["POST"])
    def api_delete_vending_machine(vm_id: int) -> Response:
        status_code = http.HTTPStatus.OK
        try:
            if utils.get_vending_machine_by_id(database_service, vm_id):
                response = utils.delete_vending_machine(database_service, vm_id)
            else:
                raise NoResultFound(f"vending machine {vm_id} does not exist")
        except Exception as e:
            print("api_delete_vending_machine:", e)
            status_code = http.HTTPStatus.BAD_REQUEST
            response = {
                "status": "error",
                "data": None,
                "message": f"unable to delete vending machine {vm_id}",
            }
        return make_response(jsonify(response), status_code)

    @app.route("/api/product_stocks/add/<int:vm_id>", methods=["POST"])
    def api_add_product_stock(vm_id: int) -> Response:
        status_code = http.HTTPStatus.OK
        try:
            if utils.get_vending_machine_by_id(database_service, vm_id):
                product_stock = utils.create_product_stock_from_request(request, vm_id)
                response = utils.add_product_stock(database_service, product_stock)
            else:
                raise NoResultFound(f"vending machine {vm_id} does not exist")
        except Exception as e:
            print("api_add_product_stock:", e)
            status_code = http.HTTPStatus.BAD_REQUEST
            response = {
                "status": "error",
                "data": {"post": {}},
                "message": f"unable to add new product stock to vending machine {vm_id}",
            }
        return make_response(jsonify(response), status_code)

    @app.route("/api/product_stocks/update/<int:vm_id>/<int:prod_id>", methods=["POST"])
    def api_update_product_stock(vm_id: int, prod_id: int) -> Response:
        status_code = http.HTTPStatus.OK
        try:
            if utils.get_stock_by_vm_id_and_prod_id(database_service, vm_id, prod_id):
                new_product_stock = utils.create_product_stock_from_request(
                    request, vm_id, prod_id
                )
                response = utils.update_product_stock(
                    database_service, new_product_stock
                )
            else:
                raise NoResultFound(
                    f"product {prod_id} stock in vending machine {vm_id} does not exist"
                )
        except Exception as e:
            print("api_update_product_stock:", e)
            status_code = http.HTTPStatus.BAD_REQUEST
            response = {
                "status": "error",
                "data": {"post": {}},
                "message": f"unable to update product {prod_id} in vending machine {vm_id}",
            }
        return make_response(jsonify(response), status_code)

    @app.route("/api/product_stocks/delete/<int:vm_id>/<int:prod_id>", methods=["POST"])
    def api_delete_product_stock(vm_id: int, prod_id: int) -> Response:
        status_code = http.HTTPStatus.OK
        try:
            if utils.get_stock_by_vm_id_and_prod_id(database_service, vm_id, prod_id):
                response = utils.delete_product_stock(database_service, vm_id, prod_id)
            else:
                raise NoResultFound(
                    f"product {prod_id} stock in vending machine {vm_id} does not exist"
                )
        except Exception as e:
            print("api_delete_product_stock:", e)
            status_code = http.HTTPStatus.BAD_REQUEST
            response = {
                "status": "error",
                "data": None,
                "message": f"unable to delete product {prod_id} from vending machine {vm_id}",
            }
        return make_response(jsonify(response), status_code)

    return app


if __name__ == "__main__":
    database_path = utils.DATABASE_PATH
    database_service = DatabaseService(database_path)
    app = create_app(database_service)
    app.run(debug=True)
