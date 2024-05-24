import os
from django.conf import settings
import requests
from django.core.files.storage import default_storage
# from PIL import Image
from django.conf import settings
from django.shortcuts import render, HttpResponse
from .daraz_scraping import scrape_daraz
from .models import Product
import csv
from django.shortcuts import redirect
from django.urls import reverse

# Views

def dashboard(request):
    return render(request, 'dashboard.html')


# # View to display data in tables
def scraped_data(request):
    
    context = {}  # Define context dictionary outside the if block
    # Retrieve the scraped data from the database
    products = Product.objects.all()
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        if search_query:
            print(f"Search query: {search_query}")
            products = scrape_daraz(search_query)
            # print(f"Products: {products}")
    # Retrieve the scrape data from the database
    products = Product.objects.all()
    product_data = []
    for product in products:
        product_data.append({
            'Product_Name': product.product_name,
            'Delivery': product.delivery,
            'Discounted_Price': product.discounted_price,
            'Actual_Price': product.actual_price
        })
    context = {
        "product_data": product_data,
    }
    return render(request, 'scraped_datas.html', context)


# # View to download CSV file and save data into database and View data in Tables
# def download_and_save(request):
#     context = {}  # Define context dictionary outside the if block
#     product_data = []  # Define product_data as an empty list
#     if request.method == 'POST':
#         search_query = request.POST.get('search_query')
#         if search_query:
#             print(f"Search query: {search_query}")
#             products = scrape_daraz(search_query)  # Assume scrape_daraz is a function to scrape daraz.np
#             product_data = products.to_dict(orient='records')
            

#             # Save the scraped data to the database
#             for product in product_data:
#                 Product.objects.create(
#                     product_name=product['Product_Name'],
#                     delivery=product['Delivery'],
#                     actual_price=product['Actual_Price'],
#                     discounted_price=product['Discounted_Price']
#                 )

#             # Generate the CSV file for download
#             response = HttpResponse(content_type='text/csv')
#             response['Content-Disposition'] = 'attachment; filename="products.csv"'

#             writer = csv.writer(response)
#             writer.writerow(['Product Name', 'Delivery', 'Actual Price', 'Discounted Price'])
#             for product in product_data:
#                 writer.writerow([product['Product_Name'], product['Delivery'], product['Actual_Price'], product['Discounted_Price']])

#             return response# Return the CSV file for download
       # Retrieve the scrape data from the database
    # products = Product.objects.all()
    # product_data = []
    # for product in products:
    #     product_data.append({
    #         'Product_Name': product.product_name,
    #         'Delivery': product.delivery,
    #         'Discounted_Price': product.discounted_price,
    #         'Actual_Price': product.actual_price
    #     })
    # context = {
    #     "product_data": product_data,
    # }
    # return render(request, 'scraped_datas.html', context)



def download_and_save(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        if search_query:
            products = scrape_daraz(search_query)

            # Save the scraped data to the database
            for i in range(len(products)):
                product = products.loc[i]
                Product.objects.create(
                    product_name=product['Product_Name'],
                    delivery=product['Delivery'],
                    actual_price=product['Actual_Price'],
                    discounted_price=product['Discounted_Price']
                )

            # Generate the CSV file for download
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="product.csv"'

            writer = csv.writer(response)
            writer.writerow(['Product Name', 'Delivery', 'Actual Price', 'Discounted Price'])
            for i in range(len(products)):
                product = products.loc[i]
                writer.writerow([product['Product_Name'], product['Delivery'], product['Actual_Price'], product['Discounted_Price']])

            # Redirect to a new page after downloading the CSV file
            return response
        else:
            print("No search query provided")

    return HttpResponse("No data to download.")





