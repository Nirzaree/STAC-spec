import requests
from pypgstac.db import PgstacDB
from pypgstac.load import Loader, Methods
from pystac import Catalog

# CATALOG_URL = "https://raw.githubusercontent.com/Nirzaree/STAC-spec/refs/heads/stac-spec-common/data/CorestackCatalogs_merged_collection/catalog.json"
# CATALOG_URL = "https://spatio-temporal-asset-catalog.s3.ap-south-1.amazonaws.com/CorestackCatalogs_merged_collection/catalog.json"
CATALOG_URL = "https://spatio-temporal-asset-catalog.s3.ap-south-1.amazonaws.com/CorestackCatalogs_merged_collection/tehsil_wise/catalog.json"

#CONN_STR = "postgresql://postgres:stac_password@stac-api_db_1:5432/postgis"
CONN_STR = "postgresql://stackuser:StackDBCoreStack%40234@localhost:5432/stackapi"

def register_queryables(db):
    # to permanently register keywords as a searchable array property
    print("Registering keywords as a queryable property...")

    queryable_sql = """
    INSERT INTO pgstac.queryables (name, definition)
    SELECT 'keywords', '{"title": "Keywords", "type": "array", "items": {"type": "string"}}'
    WHERE NOT EXISTS (
    SELECT 1 FROM pgstac.queryables WHERE name = 'keywords'
    );
    """
    # Use the existing pypgstac DB connection to run the SQL
    with db.connect() as conn:
        with conn.cursor() as cur:
            cur.execute(queryable_sql)


def ingest():
    db = PgstacDB(CONN_STR)
    register_queryables(db)
    loader = Loader(db)
    
    print(f"Fetching catalog from GitHub...")
    res = requests.get(CATALOG_URL)
    cat = Catalog.from_dict(res.json())
    cat.set_self_href(CATALOG_URL)

    # 1. Gather ALL collections (including nested ones)
    all_collections = list(cat.get_all_collections())
    print(f"Found {len(all_collections)} collections. Registering them...")
    
    for col in all_collections:
        print(f"  Registering Collection: {col.id}")
        loader.load_collections([col.to_dict()], insert_mode=Methods.upsert)

    # 2. Now that all collections exist, load the items
    for col in all_collections:
        items = [item.to_dict() for item in col.get_items()]
        if items:
            print(f"  Ingesting {len(items)} items for {col.id}...")
            loader.load_items(items, insert_mode=Methods.upsert)
    
    print("Successfully mirrored all nested data to local Database.")

if __name__ == "__main__":
    ingest()
