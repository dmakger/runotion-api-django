def order_by(request):
    return request.query_params.get('ordering', '-created_at')

