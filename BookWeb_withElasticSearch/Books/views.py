from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render

from .models import Book

# Sửa password lại theo từng server
HOST = "https://localhost:9200"
ELASTIC_USER = "elastic"
# The password for the 'elastic' user generated by Elasticsearch
ELASTIC_PASSWORD = "yLkHabXo_wWKzb0UxO1P"
# The path of ca certificates
CA_CERTS = "C:/elasticsearch/config/certs/http_ca.crt"

# Create the client instance
es = Elasticsearch(
    hosts=HOST,
    ca_certs=CA_CERTS,
    http_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
)

# Define index name of project
index_name = 'books_index'
type_name = "_search"


def search(query, size):
    global index_name, es
    return es.search(index=index_name,
                     body={
                         "query": query,
                         "from": 0,
                         "size": size,
                         "sort":
                             {
                                 "_score":
                                     {
                                         "order": "desc"
                                     }
                             }
                     })


# Create your views here.
def index_view(request):
    """
    Hiển thị tất cả các sách tỏng dataset
    """
    listBooks = []

    # Truy vấn tất cả dữ liệu trong index bằng match_all()
    ## query all
    query = {
        "match_all": {},
    }
    search_result = search(query, 300)

    # Lấy kết quả query sang object Books
    for hit in search_result['hits']['hits']:
        JSbook = hit.get('_source')
        ObBook = Book()
        ObBook.DanhMuc = JSbook.get('Danh mục')
        ObBook.LinkImage = JSbook.get('LinkImage')
        ObBook.Ten = JSbook.get('Tên')
        ObBook.MaSanPham = JSbook.get('Mã sản phẩm')
        ObBook.TacGia = JSbook.get('Tác giả')
        ObBook.NhaXuatBan = JSbook.get('Nhà xuất bản')

        if (JSbook.get('Số trang') is not None):
            ObBook.SoTrang = int(JSbook.get('Số trang'))

        ObBook.KichThuoc = JSbook.get('Kích thước')

        if (JSbook.get('Ngày phát hành') is not None):
            ObBook.NgayPhatHanh = datetime.strptime(JSbook.get('Ngày phát hành'), '%d-%m-%Y')

        ObBook.GiaBia = JSbook.get('Giá bìa')
        ObBook.GiaNhaNam = JSbook.get('Giá Nhã Nam')
        ObBook.GioiThieuSach = JSbook.get('Giới thiệu sách')

        print(ObBook.Ten)
        listBooks.append(ObBook)

    indexContext = {
        "Books": listBooks
    }
    return render(request=request,
                  template_name='index.html',
                  context=indexContext)


def detail_view(request, book):
    """
    Hiện thị thông tin của 1 quyển sách
        và top 20 quyển sách khác có liên quan
    Input: 1 quyển sách
    """
    detailContext = {

    }
    return render(request=request,
                  template_name='detail.html',
                  context=detailContext)


def search_keyword_view(request):
    """
    Hiển thị danh sách các quyển sách có liên quan đến
        từ khóa được tìm kiếm theo thứ tự
    Input: Từ khóa nhập vào thanh Search
    """
    keyword = request.GET.get('keyword')
    if (keyword is None):
        return index_view(request)

    listBooks = []

    # Truy vấn dữ liệu
    query = {
        "bool": {
            "should": [
                {
                    "match": {
                        "Danh mục": keyword
                    }
                },
                {
                    "match": {
                        "Tác giả": keyword
                    }
                },
                {
                    "match": {
                        "Tên": keyword
                    }
                },
                {
                    "match": {
                        "Dịch giả": keyword
                    }
                },
                {
                    "match": {
                        "Nhà xuất bản": keyword
                    }
                },
                {
                    "match": {
                        "Giới thiệu sách": keyword
                    }
                }
            ],
            "minimum_should_match": 1
        }
    }
    search_result = search(query, 300)

    # Lấy kết quả query sang object Books
    for hit in search_result['hits']['hits']:
        JSbook = hit.get('_source')
        ObBook = Book()
        ObBook.DanhMuc = JSbook.get('Danh mục')
        ObBook.LinkImage = JSbook.get('LinkImage')
        ObBook.Ten = JSbook.get('Tên')
        ObBook.MaSanPham = JSbook.get('Mã sản phẩm')
        ObBook.TacGia = JSbook.get('Tác giả')
        ObBook.NhaXuatBan = JSbook.get('Nhà xuất bản')

        if (JSbook.get('Số trang') is not None):
            ObBook.SoTrang = int(JSbook.get('Số trang'))

        ObBook.KichThuoc = JSbook.get('Kích thước')

        if (JSbook.get('Ngày phát hành') is not None):
            ObBook.NgayPhatHanh = datetime.strptime(JSbook.get('Ngày phát hành'), '%d-%m-%Y')

        ObBook.GiaBia = JSbook.get('Giá bìa')
        ObBook.GiaNhaNam = JSbook.get('Giá Nhã Nam')
        ObBook.GioiThieuSach = JSbook.get('Giới thiệu sách')

        print(ObBook.Ten)
        listBooks.append(ObBook)

    searchContext = {
        "Books": listBooks
    }
    return render(request=request,
                  template_name='index.html',
                  context=searchContext)
