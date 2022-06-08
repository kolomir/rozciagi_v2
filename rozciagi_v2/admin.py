from django.contrib import admin
from .models import GrupaRobocza, Przekroje, Narzedzia, Author, Rozciagi, Listy


@admin.register(Listy)
class ListyAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'aktywna')
    list_filter = ('nazwa', 'aktywna')
    search_fields = ('nazwa', 'aktywna')


@admin.register(GrupaRobocza)
class GrupaRoboczaAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'aktywna')
    list_filter = ('nazwa', 'aktywna')
    search_fields = ('nazwa', 'aktywna')


@admin.register(Narzedzia)
class NarzedziaAdmin(admin.ModelAdmin):
    list_display = ('grupa', 'uwagi', 'aktywny')
    list_filter = ('grupa', 'uwagi', 'aktywny')
    search_fields = ('grupa', 'uwagi', 'aktywny')


@admin.register(Przekroje)
class PrzekrojeAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'aktywny')
    list_filter = ('nazwa', 'aktywny')
    search_fields = ('nazwa', 'aktywny')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'dzial')
    list_filter = ('user', 'dzial')
    search_fields = ('user', 'dzial')


@admin.register(Rozciagi)
class RozciagiAdmin(admin.ModelAdmin):
    list_display = ('nr_zlecenia', 'nr_pozycji', 'lista', 'nr_pracownika', 'rozciag', 'przekrojePrzewodow', 'indeks_kontaktu', 'poprawkowe', 'narzedzia', 'grupa_robocza', 'wysokosc', 'narzedzia_rodzaj', 'potwierdzenie', 'zalogowany_user')
    list_filter = ('przekrojePrzewodow', 'grupa_robocza', 'narzedzia_rodzaj', 'zalogowany_user')
    search_fields = ('nr_zlecenia', 'nr_pozycji', 'nr_pracownika', 'indeks_kontaktu', 'narzedzia', 'narzedzia_rodzaj', 'zalogowany_user')
