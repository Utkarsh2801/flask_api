from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price", required=True, type=float,
                        help="This field can't be blank")

    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        else:
            return {"message": "Item Not Found"}, 400

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists".format(name)}, 400

        data = self.parser.parse_args()
        item = ItemModel(name, data['price'])
        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting an item."}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if(item):
            item.delete_from_db()

        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items":  [item.json() for item in ItemModel.query.all()]}
