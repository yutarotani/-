from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

from django.views.generic import ListView,DetailView

from django.views.generic.edit import CreateView,UpdateView,DeleteView

from django_filters.views import FilterView


from .models import Item

from .filters import ItemFilter

from .forms import ItemFrom



#検索一覧画面
class ItemFilterView(LoginRequiredMixin,FilterView):
    model=Item
    filterset_class=ItemFilter
    
    #デフォルトの並び順を新しい順とする
    queryset=Item.objects.all().order_by('-created_at')
    
    #クエリ未指定の時に全件検索を行うために以下のオプションを指定(django-filter2.0以降）
    strict=False
    
    #1ページ当たりの表示件数
    paginate_by=10
    
    #検索セッションに保存する　or 呼び出す
    def get(self,request,**kwards):
        if request.GET:
            request.session['query']=request.GET
        else:
            request.GET=request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key]=request.session['query'][key]
        
        return super().get(request,*kwards)
        
#詳細画面
class ItemDetailView(LoginRequiredMixin,DetailView):
    model=Item
    
#登録画面
class ItemCreateView(LoginRequiredMixin,CreateView):
    model=Item
    form_class=ItemFrom
    success_url=reverse_lazy('index')
    
#更新画面
class ItemUpdateView(LoginRequiredMixin,UpdateView):
    model=Item
    form_class=ItemFrom
    success_url=reverse_lazy('index')
    
#削除画面
class ItemDeleteView(LoginRequiredMixin,DeleteView):
    model=Item
    success_url=reverse_lazy('index')


