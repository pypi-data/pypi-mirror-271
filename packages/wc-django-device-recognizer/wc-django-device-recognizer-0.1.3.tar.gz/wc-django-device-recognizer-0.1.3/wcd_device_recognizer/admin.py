from django.contrib import admin
from django.utils.translation import pgettext_lazy

from .models import InterlocutorNetwork, Interlocutor, App, OS, Device


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = 'id', 'family', 'version',
    list_filter = 'family',
    search_fields = 'id', 'family',
    date_hierarchy = 'created_at'


@admin.register(OS)
class OSAdmin(admin.ModelAdmin):
    list_display = 'id', 'family', 'arch', 'version',
    list_filter = 'family', 'arch',
    search_fields = 'id', 'family', 'arch',
    date_hierarchy = 'created_at'


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'brand', 'model', 'family', 'bitness', 'memory', 'dpr', 'viewport_width',
    )
    list_filter = 'family', 'model', 'brand', 'bitness',
    search_fields = 'id', 'family', 'model', 'brand', 'bitness',
    date_hierarchy = 'created_at'


class InterlocutorNetworkInline(admin.TabularInline):
    extra = 0
    model = InterlocutorNetwork


@admin.register(Interlocutor)
class InterlocutorAdmin(admin.ModelAdmin):
    list_display = 'id', 'os', 'device', 'app', 'outer_id',
    list_filter = 'os', 'device', 'app',
    autocomplete_fields = 'os', 'device', 'app'
    date_hierarchy = 'created_at'
    search_fields = (
        'id', 'user_agent', 'client_hints', 'outer_id',
        'device__id', 'os__id', 'app__id', 'network_connections__ip'
    )
    # inlines = InterlocutorNetworkInline,

    def get_queryset(self, request):
        return super().get_queryset(request).with_relateds().distinct()


@admin.register(InterlocutorNetwork)
class InterlocutorNetworkAdmin(admin.ModelAdmin):
    list_display = 'ip', 'get_os', 'get_device', 'get_app', 'get_outer_id', 'created_at',
    list_filter = 'interlocutor__os', 'interlocutor__device', 'interlocutor__app',
    autocomplete_fields = 'interlocutor',
    search_fields = (
        'ip',
        'interlocutor__user_agent', 'interlocutor__client_hints', 'interlocutor__outer_id',
        'interlocutor__device__id', 'interlocutor__os__id',
        'interlocutor__app__id', 'interlocutor__network_connections__ip'
    )
    list_select_related = 'interlocutor', 'interlocutor__os', 'interlocutor__device', 'interlocutor__app',

    def get_os(self, obj):
        return str(obj.interlocutor.os)
    get_os.short_description = pgettext_lazy('wcd_device_recognizer', 'OS')
    get_os.admin_order_field = 'interlocutor__os__id'

    def get_app(self, obj):
        return str(obj.interlocutor.app)
    get_app.short_description = pgettext_lazy('wcd_device_recognizer', 'App')
    get_app.admin_order_field = 'interlocutor__app__id'

    def get_device(self, obj):
        return str(obj.interlocutor.device)
    get_device.short_description = pgettext_lazy('wcd_device_recognizer', 'Device')
    get_device.admin_order_field = 'interlocutor__device__id'

    def get_outer_id(self, obj):
        return str(obj.interlocutor.outer_id)
    get_outer_id.short_description = pgettext_lazy('wcd_outer_id_recognizer', 'Outer id')
    get_outer_id.admin_order_field = 'interlocutor__outer_id'
