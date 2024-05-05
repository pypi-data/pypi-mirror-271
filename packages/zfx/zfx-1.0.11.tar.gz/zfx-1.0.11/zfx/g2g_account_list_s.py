import requests


def g2g_account_list_s():
    """
        #无需传递任何参数，自动获取所有的产品ID，等待时间较久，根据网络情况决定
    """
    products_list = []
    url = "https://sls.g2g.com/offer/search"
    page = 1

    try:
        while True:
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
                if not results_value:
                    break
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
                page += 1
            else:
                # print("请求失败，状态码:", response.status_code)
                break
    except requests.exceptions.RequestException as e:
        print("网络请求错误:", e)

    return products_list


# # 调用函数并打印结果
# 结果 = g2g_account_list_s()
# for product in 结果:
#     print(product)
