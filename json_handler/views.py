import asyncio
import os
import uuid

import aiofiles as aiofiles
from asgiref.sync import sync_to_async
from django.contrib import auth
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.views import View

from json_handler.models import JSONData
from laboratory_django import settings

data_lock = asyncio.Lock()


class MergeResult(View):
    async def post(self, request):
        user = await sync_to_async(auth.get_user)(request)
        if user.is_superuser:
            id_list = request.POST.get('ids')
            ids = id_list.split(",")

            data_to_write = ""
            for _id in ids:
                try:
                    obj = await asyncio.to_thread(JSONData.objects.get, id=_id)

                    async with data_lock:
                        data_to_write += str(obj.data)[1:-1] + ", "

                except JSONData.DoesNotExist:
                    print(f"Object with id {_id} does not exist.")

            file_name = str(uuid.uuid4())
            final_data = "{" + data_to_write[0:-2].replace("'", '"') + "}"

            # Write Final Data To Json File
            directory = f'{settings.MEDIA_ROOT}/files'
            if not os.path.exists(directory):
                os.makedirs(directory)

            with open(f'{directory}/{file_name}.json', 'a') as file:
                file.write(final_data)
            return redirect('json:download', name=file_name)
        else:
            return redirect('/admin')


class DownloadFileView(View):
    async def get(self, request, name):
        user = await sync_to_async(auth.get_user)(request)
        if user.is_superuser:
            file_path = os.path.join(settings.MEDIA_ROOT, 'files', f'{name}.json')
            if os.path.exists(file_path):
                async with aiofiles.open(file_path, mode='rb') as f:
                    file_content = await f.read()
                    response = HttpResponse(file_content, content_type='application/json')
                    response['Content-Disposition'] = f'attachment; filename="{name}.json"'
                    return response
            else:
                raise Http404("File does not exist")
        else:
            return redirect('/admin')

