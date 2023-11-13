# json_upload/admin.py
import json

from django.contrib import admin
from django.db.models import QuerySet

from .forms import JSONDataForm
from .models import JSONData


@admin.register(JSONData)
class JSONDataAdmin(admin.ModelAdmin):
    form = JSONDataForm
    search_fields = ['data']
    list_display = ['json_file']
    # search_help_text = "Search in JSON data like this:  KEY:VALUE&&KEY2:VALUE2 "

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        queryset = self.get_queryset(request)
        search_term = request.GET.get('q', None)
        if search_term:
            try:
                search_results = self.get_search_results(request, queryset, search_term)
                object_ids = []
                for item in search_results:
                    if not isinstance(item, bool):
                        if isinstance(item, tuple) and len(item) > 0:
                            object_ids.append(item[0].id)
                        elif isinstance(item, QuerySet) and item.exists():
                            object_ids.extend(item.values_list('id', flat=True))
                extra_context['objects'] = object_ids
            except:
                pass
        return super().changelist_view(request, extra_context=extra_context)

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request,
            queryset,
            search_term,
        )

        queryset |= self.model.objects.all()
        if search_term:
            try:
                key_value_pairs = search_term.split('&&')
                json_results = []
                for obj in queryset:
                    if isinstance(obj.data, dict):
                        json_data = obj.data
                    else:
                        json_data = json.loads(obj.data)  # Convert the JSON string to a Python object
                    try:
                        if self.check_key_value_pairs(json_data, key_value_pairs):
                            json_results.append(obj)
                    except json.JSONDecodeError:
                        # Handle the JSON decoding error
                        pass
                    queryset = self.model.objects.filter(
                        pk__in=[item.pk for item in json_results])  # Convert the list to a queryset
            except:
                return queryset, may_have_duplicates

        return queryset, may_have_duplicates

    def check_key_value_pairs(self, data, key_value_pairs):
        # Check key value pairs
        for key_value_pair in key_value_pairs:
            search_key, search_value = key_value_pair.split(':', 1)
            if not self.search_json(data, search_key, search_value):
                return False
        return True

    def search_json(self, data, search_key, search_value):
        # Search in json key value
        if isinstance(data, dict):
            for key, value in data.items():
                if search_key.lower() == key.lower() and search_value in str(value):
                    return True
                if isinstance(value, (dict, list)):
                    if self.search_json(value, search_key, search_value):
                        return True
        elif isinstance(data, list):
            for item in data:
                if self.search_json(item, search_key, search_value):
                    return True
        return False

    def save_model(self, request, obj, form, change):
        if not change:
            old_data = obj.data  # assuming 'data' is the field containing the JSON data
            new_json_file = obj.upload
            try:
                new_data = json.loads(new_json_file.read())

                if old_data != new_data:  # compare the old and new data
                    # Perform the saving process for new data
                    try:
                        for key, value in new_data.items():
                            if not self.model.objects.filter(data={key: value}).exists():
                                new_obj = JSONData(upload=new_json_file, data={key: value})
                                new_obj.save()
                    except:
                        pass

            except Exception as e:
                raise e
        else:
            super().save_model(request, obj, form, change)

    @staticmethod
    def json_file(obj):
        keys_list = list(obj.data.keys())
        return keys_list[0]
