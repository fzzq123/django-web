import os
from django.shortcuts import render, get_object_or_404
from django.http import StreamingHttpResponse, Http404
from django.core.paginator import Paginator
from db.models import DLdoc


def read_file(file_name, size):
    """分批读取文件，用于流式下载"""
    with open(file_name, mode='rb') as fp:
        while True:
            c = fp.read(size)
            if c:
                yield c
            else:
                break


def getDoc(request, id):
    """流式下载文件（通过 DLdoc 模型 ID）"""
    doc = get_object_or_404(DLdoc, id=id)
    filepath = doc.file.path
    if not os.path.exists(filepath):
        raise Http404('文件不存在')
    filename = os.path.basename(filepath)
    response = StreamingHttpResponse(read_file(filepath, 512))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)
    return response


def download(request):
    """资料下载列表页（从 DLdoc 模型读取）"""
    submenu = 'download'
    doc_qs = DLdoc.objects.all().order_by('-publishDate')

    # 为每条记录计算文件大小
    docList = []
    for doc in doc_qs:
        try:
            size_bytes = doc.file.size if doc.file else 0
        except Exception:
            size_bytes = 0
        if size_bytes < 1024:
            size_str = '%d B' % size_bytes
        elif size_bytes < 1024 * 1024:
            size_str = '%.1f KB' % (size_bytes / 1024)
        else:
            size_str = '%.1f MB' % (size_bytes / (1024 * 1024))
        docList.append({
            'id': doc.id,
            'title': doc.title,
            'size': size_str,
            'publishDate': doc.publishDate,
        })

    p = Paginator(docList, 5)
    if p.num_pages <= 1:
        pageData = ''
    else:
        page = int(request.GET.get('page', 1))
        newList = p.page(page)
        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        total_pages = p.num_pages
        page_range = p.page_range
        if page == 1:
            right = page_range[page:page + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page == total_pages:
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]
            right = page_range[page:page + 2]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        pageData = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'total_pages': total_pages,
            'page': page,
        }
    return render(
        request, 'docList.html', {
            'active_menu': 'service',
            'sub_menu': submenu,
            'docList': docList,
            'pageData': pageData,
        })
