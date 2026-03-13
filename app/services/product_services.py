import pandas as pd
from flask import jsonify
from sqlalchemy import asc, desc
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.extensions import db
from app.logger import logger
from app.models.product import Product
from app.extensions import cache

ALLOWED_SORT = {
    "id": Product.id,
    "name": Product.name,
    "price": Product.price

}

def get_all_products(
        user_id,
        search=None,
        sort_by="id",
        min_price=None,
        max_price=None,
        order="desc",
        page=1,
        limit=10
):

        try:
            
            # cache_key = (
            #     f"products:{user_id}:"
            #     f"{search}:{min_price}:{max_price}:"
            #     f"{sort_by}:{order}:{page}:{limit}"
            # )
            
            version_key = f"products_version:{user_id}"
            version = cache.get(version_key)
            
            if version is None:
                version = 1
                cache.set(version_key, version)

            
            cache_key = f"products:{user_id}:v{version}:{search}:{min_price}:{max_price}:{sort_by}:{order}:{page}:{limit}"

            
            cached = cache.get(cache_key)
            
            if cached:
                print("Serving from Redis")
                return cached

            print("Fetching from DB")
            
            query = Product.query.filter_by(user_id=user_id)

            if search:
                query = query.filter(Product.name.ilike(f"%{search}%"))

            if min_price is not None:
                query = query.filter(Product.price >= min_price)

            if max_price is not None:
                query = query.filter(Product.price <= max_price)

            sort_column = ALLOWED_SORT.get(sort_by, Product.id)

            if order.lower() == "asc":
                query = query.order_by(asc(sort_column))
            else:
                query = query.order_by(desc(sort_column))

            limit = min(limit, 100)

            pagination = query.paginate(
                page = page,
                per_page = limit,
                error_out = False
            )



            result = [
                {
                    "id": p.id,
                    "name": p.name,
                    "model_number": p.model_number,
                    "specification": p.specification,
                    "price": float(p.price),
                    "stock": int(p.stock),
                    "images": p.images or []
                }
                for p in pagination.items
            ]

            response_data = {
                "success": True,
                "total": pagination.total,
                "pages": pagination.pages,
                "current_page": pagination.page,
                "limit": limit,
                "data": result
            }, 200
            
            cache.set(cache_key,response_data,timeout=300) # Cache for 5 minutes(5*60sec)
            
            return response_data

        except SQLAlchemyError as e:
            logger.error("Database error while fetching products", exc_info=True)

            return {
                "success": False,
                "error": "Database error while fetching products"
            }, 500


def get_product_by_id(product_id,user_id):

        try:
            product = Product.query.filter_by(
                id=product_id,
                user_id=user_id
            ).first()

            if not product:
                return {
                    "success": False,
                    "error": "Product not found"
                }, 404

            return {
                "success": True,
                "data": {
                    "id": product.id,
                    "name": product.name,
                    "model_number": product.model_number,
                    "specification": product.specification,
                    "price": float(product.price),
                    "stock": int(product.stock),
                    "images": product.images or []
                }
            }, 200

        except SQLAlchemyError:
            return {
                "success": False,
                "error": "Database error"
            }, 500


def create_product(data, user_id):

        try:
            product = Product(**data, user_id=user_id)

            db.session.add(product)
            db.session.commit()
            
            # cache.delete_pattern(f"products:{user_id}:*")
            
            version_key = f"products_version:{user_id}"
            current_version = cache.get(version_key) or 1
            cache.set(version_key, current_version + 1)

            return {
                "success": True,
                "message": "Product created successfully",
                "product_id": product.id
            }, 201

        except IntegrityError:
            db.session.rollback()

            return {
                "success": False,
                "error": "Product with same name or model already exists"
            }, 409

        except SQLAlchemyError:
            db.session.rollback()

            return {
                "success": False,
                "error": "Database error while creating product"
            }, 500


def update_product(product_id, data, user_id):

            try:
                product = Product.query.filter_by(
                    id=product_id,
                    user_id=user_id
                ).first()

                if not product:
                    return {
                        "success": False,
                        "error": "Product not found"
                    }, 404

                for key, value in data.items():
                    setattr(product, key, value)

                db.session.commit()
                
                # cache.delete_pattern(f"products:{user_id}:*")
                
                version_key = f"products_version:{user_id}"
                current_version = cache.get(version_key) or 1
                cache.set(version_key, current_version + 1)

                return {
                    "success": True,
                    "message": "Product updated successfully"
                }, 200

            except IntegrityError:
                db.session.rollback()

                return {
                    "success": False,
                    "error": "Duplicate name or model number"
                }, 409

            except SQLAlchemyError:
                db.session.rollback()

                return {
                    "success": False,
                    "error": "Database error"
                }, 500


def delete_product(product_id,user_id):

            try:
                product = Product.query.filter_by(
                    id=product_id,
                    user_id=user_id
                ).first()

                if not product:
                    return {
                        "success": False,
                        "error": "Product not found"
                    }, 404

                db.session.delete(product)
                db.session.commit()
                
                cache.delete_pattern(f"products:{user_id}:*")

                return {
                    "success": True,
                    "message": "Product deleted successfully"
                }, 200

            except SQLAlchemyError:
                db.session.rollback()

                return {
                    "success": False,
                    "error": "Database error"
                }, 500


def create_multiple_products(products_data, user_id):

        created = []
        errors = []

        try:
            for index, data in enumerate(products_data):

                exists = Product.query.filter_by(
                    name=data.get("name"),
                    model_number=data.get("model_number"),
                    user_id=user_id
                ).first()

                if exists:
                    errors.append(f"Product {index + 1} already exists")
                    continue

                product = Product(**data, user_id=user_id)
                db.session.add(product)
                created.append(product)

            db.session.commit()

            return {
                "success": True,
                "created_count": len(created),
                "errors": errors
            }, 201

        except SQLAlchemyError:
            db.session.rollback()

            return {
                "success": False,
                "error": "Database error"
            }, 500

def bulk_sheet_upload_service(file, user_id):
    try:
        df = pd.read_excel(file)


        df.columns = df.columns.str.strip().str.lower()

        required_columns = [
            "name",
            "model_number",
            "specification",
            "price",
            "stock",
            "images"
        ]

        if not all(col in df.columns for col in required_columns):
            return {"error": "Invalid Excel format"}, 400


        df = df.dropna(how="all")
        df = df.dropna(subset=["name", "model_number", "price"])
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df["stock"] = pd.to_numeric(df["stock"], errors="coerce").fillna(0)

        df = df.dropna(subset=["price"])


        df["name"] = df["name"].astype(str).str.strip()

        df["model_number"] = df["model_number"].astype(str).str.strip()

        df["images"] = df["images"].astype(str).str.replace('"', '')


        df = df.drop_duplicates(subset=["name", "model_number"])


        existing_products = db.session.query(
            Product.name,
            Product.model_number
        ).all()

        existing_set = {
            (p.name.lower(), p.model_number.lower())
            for p in existing_products
        }

        products_to_insert = []
        duplicate_count = 0

        user_id = int(user_id)

        valid_df = df[(df["price"] >=0) & (df["stock"] >=0)]
        invalid_df = df[(df["price"] < 0) | (df["stock"] < 0)]


        for row in valid_df.itertuples(index=False):

            key = (row.name.lower(), row.model_number.lower())

            if key in existing_set:
                duplicate_count += 1
                continue

            product = Product(
                user_id=user_id,
                name=row.name,
                model_number=row.model_number,
                specification=row.specification,
                price=float(row.price),
                stock=int(row.stock),
                images=row.images
            )

            products_to_insert.append(product)


            existing_set.add(key)

        if products_to_insert:
            db.session.bulk_save_objects(products_to_insert)
            db.session.commit()
            
            version_key = f"products_version:{user_id}"
            current_version = cache.get(version_key) or 1
            cache.set(version_key, current_version + 1)

        return {
            "inserted": f"{len(products_to_insert)} rows inserted in database",
            "duplicates": f"{duplicate_count} duplicate entries found in database",
            "Invalid_rows": f"{len(invalid_df)} invalid rows",
            "total_rows_in_excel": f"{len(df)} total rows present in file"
        }, 201

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
