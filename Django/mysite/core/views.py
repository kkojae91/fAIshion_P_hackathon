from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages

from .forms import StudyGroupForm
from .models import StudyGroup


class Home(TemplateView):
    template_name = 'home.html'


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'makestudy.html', context)


def studygroups_list(request):
    books = StudyGroup.objects.all()
    return render(request, 'studygroup_list.html', {
        'books': books
    })


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

def upload_book(request):
    if request.method == 'POST':
        form = StudyGroupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = StudyGroupForm()
    return render(request, 'upload_book.html', {
        'form': form
    })


def delete_book(request, pk):
    if request.method == 'POST':
        book = StudyGroup.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')


class BookListView(ListView):
    model = StudyGroup
    template_name = 'class_book_list.html'
    context_object_name = 'books'


class MakeStudyView(CreateView):
    model = StudyGroup
    form_class = StudyGroupForm
    success_url = reverse_lazy('studygroup_list')
    template_name = 'makestudy.html'

