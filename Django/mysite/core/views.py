from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.generic import TemplateView, ListView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from simplejson import dumps, loads, JSONEncoder
from .forms import StudyGroupForm
from .models import StudyGroup, Book
import json


class Home(TemplateView):
    template_name = 'home.html'


# 스터디그룹 리스트 뷰
class StudyGroupsListView(ListView):
    model = StudyGroup
    paginate_by = 10
    template_name = 'studygroup_list.html'  # DEFAULT : <app_label>/<model_name>_list.html
    context_object_name = 'studygroup_list'  # DEFAULT : <app_label>_list

    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        studygroup_list = StudyGroup.objects.order_by('-id')

        if search_keyword:
            if len(search_keyword) > 1:
                if search_type == 'all':
                    search_studygroup_list = studygroup_list.filter(
                        Q(title__icontains=search_keyword) | Q(content__icontains=search_keyword) | Q(
                            author__icontains=search_keyword))
                elif search_type == 'title_content':
                    search_studygroup_list = studygroup_list.filter(
                        Q(title__icontains=search_keyword) | Q(content__icontains=search_keyword))
                elif search_type == 'title':
                    search_studygroup_list = studygroup_list.filter(title__icontains=search_keyword)
                elif search_type == 'content':
                    search_studygroup_list = studygroup_list.filter(content__icontains=search_keyword)
                elif search_type == 'author':
                    search_studygroup_list = studygroup_list.filter(author__icontains=search_keyword)

                # if not search_studygroup_list :
                #     messages.error(self.request, '일치하는 검색 결과가 없습니다.')
                return search_studygroup_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return studygroup_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')

        if len(search_keyword) > 1:
            context['q'] = search_keyword
        context['type'] = search_type
        return context


def studygroup_detail_view(request, pk):
    studygroup = get_object_or_404(StudyGroup, pk=pk)
    # notice = Notice.objects.filter(id=pk)

    context = {
        'studygroup': studygroup,
    }

    studygroup.hits += 1
    studygroup.save()
    return render(request, 'studygroup_detail.html', context)


def makestudy(request):
    if request.method == 'POST':
        StudyGroup.objects.create(
            field=request.POST['field'],
            title=request.POST['title'],
            content=request.POST['content'],
            author=request.POST['author'],
        )
        return redirect('studygroup_list')

    return render(request, 'makestudy.html')

def searchData(request):
    print("searchData 입장")
    if 'searchwords' in request.GET:
        findthis = request.GET['searchwords']
        print(findthis)
        books = Book.objects.filter(field=findthis).values()
        title = []
        image_url = []
        url = []
        for book in books:
            title.append(book['title'])
            image_url.append(book['image_url'])
            url.append(book['url'])
        print(title)
        print(image_url)
        print(url)
        context = {
            'title': title,
            'image_url': image_url,
            'url': url,
        }
        json = dumps(context)

        return HttpResponse(json)

