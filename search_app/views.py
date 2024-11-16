from django.shortcuts import render, get_object_or_404, redirect 
from .models import Product, Category 
from .forms import ProductForm, SearchForm 
from django.core.paginator import Paginator 
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.cache import cache 
from .models import SearchHistory 
import csv 
from django.http import HttpResponse 
from .models import SearchSettings
from django.contrib.auth import login
from .forms import SignUpForm
from django.views import View
from django.db.models import Q
from django.http import JsonResponse
from .models import Product, CartItem

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def search_view(request):
    query = request.GET.get('query', '').strip()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort')
    products = Product.objects.all()

    # 部分一致検索
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # 最低価格、最高価格フィルタリング
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # 並び順
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')

    # ページネーション設定
    paginator = Paginator(products, 10)  # 1ページに表示するアイテム数
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'search.html', {'page_obj': page_obj, 'query': query})
 
def export_search_results(request):
    query = request.GET.get('query', '').strip()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort')
    
    # 検索条件に基づいてProductをフィルタリング
    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # 並び順
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')

    # CSVエクスポート
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="search_results.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Description', 'Price', 'Category'])
    for product in products:
        writer.writerow([product.name, product.description, product.price, product.category.name])

    return response

def save_search_settings(request): 
    query = request.GET.get('query') 
    sort = request.GET.get('sort') 
    min_price = request.GET.get('min_price') 
    max_price = request.GET.get('max_price') 
 
    SearchSettings.objects.update_or_create( 
        user=request.user, 
        defaults={'query': query, 'sort': sort, 'min_price': min_price, 'max_price': max_price} 
    )

# カートに商品を追加するビュー
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # 現在のユーザーと商品に紐づくカートアイテムを取得、存在しない場合は新規作成
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,  # ユーザーを追加
        product=product,
        defaults={'quantity': 1},
    )
    
    # 既存のカートアイテムの場合は数量を増加
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return JsonResponse({
        'message': f'{product.name}がカートに追加されました',
        'quantity': cart_item.quantity,
    })

# カートの商品一覧を表示するビュー
def cart_list(request):
    # カート内の商品を取得
    cart_items = CartItem.objects.filter(user=request.user)
    
    # 合計金額を計算
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    return render(request, 'cart_list.html', {
        'cart_items': cart_items,
        'total_price': total_price,  # 合計金額をテンプレートに渡す
    })

# カートから商品を削除するビュー
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart_list')