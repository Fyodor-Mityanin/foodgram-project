from django.shortcuts import redirect


def simple_middleware(get_response):

    def middleware(request):
        tag_list = request.GET.getlist('tag')
        request.tags = tag_list
        response = get_response(request)
        # с пагинацией придумал только так, как сделать функцией я не придумал
        if request.GET.get('page'):
            num_pages = response.context_data['paginator'].num_pages
            if int(request.GET.get('page')) > num_pages:
                curent_url = request.path
                query_dict = request.GET.copy()
                query_dict['page'] = num_pages
                query_string = query_dict.urlencode()
                url = '{}?{}'.format(curent_url, query_string)
                return redirect(url)
        return response

    return middleware
