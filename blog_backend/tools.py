def upload_file(file, dirname=''):
    path = f'/{dirname}/' + file.name
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
