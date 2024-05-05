import requests


def g2g_account_list(page):
    """
    传递一个页码作为参数，只获取这一页的产品ID
    """
    products_list = []

    url = "https://sls.g2g.com/offer/search"

    try:
        params = {
            "seo_term": "new-world-account",
            "sort": "highest_price",
            "page_size": "100",
            "currency": "usd",
            "country": "us",
            "page": str(page),
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            results_value = data["payload"]["results"]
            for result in results_value:
                product_dict = {
                    "display_price": result["display_price"],
                    "offer_id": result["offer_id"],
                    "service_id": result["service_id"],
                    "brand_id": result["brand_id"],
                    "region_id": result["region_id"],
                    "title": result["title"],
                    "description": result["description"],
                    "available_qty": result["available_qty"],
                    "min_qty": result["min_qty"],
                    "collection_id": result["offer_attributes"][0]["collection_id"],
                    "dataset_id": result["offer_attributes"][0]["dataset_id"],
                }
                products_list.append(product_dict)
    except requests.exceptions.RequestException as e:
        print("网络请求错误:", e)

    return products_list


# # 调用函数并打印结果
# 结果 = g2g_account_list(1)
# for product in 结果:
#     print(product)


