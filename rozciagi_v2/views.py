from django.shortcuts import render, redirect
from .models import Rozciagi, Listy, Przekroje, GrupaRobocza, Narzedzia, Author, User
from .forms import RozciagiForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponse
import csv


# == WYSZUKANIE AUTORA ====================================================================================
def get_author(user):
    if user.is_anonymous:
        guest_user = User.objects.get(username="guest")  # or whatever ID or name you use for the placeholder user that no one will be assigned
        qs = Author.objects.filter(user=guest_user)
        if qs.exists():
            return qs[0]
        return None
    else:
        qs = Author.objects.filter(user=user)
        if qs.exists():
            return qs[0]
        return None


# == NOWY WPIS ====================================================================================
def nowy_wpis(request):
    form = RozciagiForm(request.POST or None, request.FILES or None)
    rozciag = Rozciagi.objects.all().order_by('-id')[:1000]
    lista = Listy.objects.filter(aktywna=True)
    przekroje = Przekroje.objects.filter(aktywny=True)
    grupy = GrupaRobocza.objects.filter(aktywna=True)
    rodzaj = Narzedzia.objects.filter(aktywny=True)

    moja_Data = datetime.now()
    #print(moja_Data)
    data_dodania = moja_Data.strftime("%Y-%m-%d")

    liczba = 0
    zleRim = 0

    if form.is_valid():
        author = get_author(request.user)
        print('* test danych *****************************************************')
        indeks_kontaktu_test = request.POST.get('indeks_kontaktu')
        indeks_kontaktu_test = indeks_kontaktu_test.strip()
        ile = len(indeks_kontaktu_test)
        print('ile: ',ile)
        if ile == 8:
            if indeks_kontaktu_test[0].capitalize()+indeks_kontaktu_test[1].capitalize()+indeks_kontaktu_test[2].capitalize() == 'RIM':
                try:
                    liczba = int(indeks_kontaktu_test[3]+indeks_kontaktu_test[4]+indeks_kontaktu_test[5]+indeks_kontaktu_test[6]+indeks_kontaktu_test[7])
                except:
                    zleRim = 1
                else: indeks_kontaktu_test = 'RIM' + str(liczba)
        else:
            zleRim = 1
        print('indeks_kontaktu:', indeks_kontaktu_test)

        nr_zlecenia_test = request.POST.get('nr_zlecenia')
        nr_pozycji_test = request.POST.get('nr_pozycji')
        lista_test = request.POST.get('lista')
        rozciag_test = request.POST.get('rozciag')
        nr_pracownika_test = request.POST.get('nr_pracownika')
        przekrojePrzewodow_test = request.POST.get('przekrojePrzewodow')
        poprawkowe_test = request.POST.get('poprawkowe')
        narzedzia_test = request.POST.get('narzedzia')
        grupa_robocza_test = request.POST.get('grupa_robocza')
        wysokosc_test = request.POST.get('wysokosc')
        data_serwis_test = request.POST.get('data_serwis')
        data_dodania_test = request.POST.get('data_dodania')
        narzedzia_rodzaj_test = request.POST.get('narzedzia_rodzaj')
        potwierdzenie_test = request.POST.get('potwierdzenie')
        print('nr_zlecenia:', nr_zlecenia_test)
        print('nr_pozycji:', nr_pozycji_test)
        print('lista:', lista_test)
        print('rozciag:', rozciag_test)
        print('nr_pracownika:', nr_pracownika_test)
        print('przekrojePrzewodow:', przekrojePrzewodow_test)
        print('poprawkowe:', poprawkowe_test)
        print('narzedzia:', narzedzia_test)
        print('grupa_robocza:', grupa_robocza_test)
        print('wysokosc:', wysokosc_test)
        print('data_serwis:', data_serwis_test)
        print('data_dodania:', data_dodania_test)
        print('narzedzia_rodzaj:', narzedzia_rodzaj_test)
        print('potwierdzenie:', potwierdzenie_test)
        print('autor:', author)
        print('* koniec testu ****************************************************')


        form.instance.zalogowany_user = author
        form.instance.data_serwis = data_serwis_test
        form.instance.data_dodania = data_dodania_test
        form.instance.indeks_kontaktu = indeks_kontaktu_test
        if zleRim == 0:
            form.save()
            messages.info(request, f"Dane zostały zapisane.")
            return redirect(wszystkie_wpisy)

    context = {
        'rozciag': rozciag,
        'lista': lista,
        'przekroje': przekroje,
        'grupy': grupy,
        'rodzaj': rodzaj,
        'data_dodania': data_dodania,
    }

    return render(request, 'rozciagi/wpis_form.html', context)
# =============================================================================================


# == WSZYSTKIE WPISY ====================================================================================
def wszystkie_wpisy(request):
    rozciag = Rozciagi.objects.all().order_by('-id')[:1000]

    context = {
        'rozciag': rozciag
    }

    return render(request, 'rozciagi/wszystkie_wpisy.html', context)
# =============================================================================================


# == LOGIN ====================================================================================
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info( request, f"Witaj {username}! Właśnie się zalogowałeś.")
                return redirect("/")
            else:
                messages.error(request, f"Błędny login lub hasło")
        else:
            messages.error(request, f"- Błędny login lub hasło -")
    form = AuthenticationForm()

    context = {
        "form": form
    }
    return render(request, "rozciagi/login.html", context)


def logout_request(request):
    logout(request)
    messages.info(request, "Właśnie się wylogowałeś")
    return redirect(wszystkie_wpisy)
# =============================================================================================


# == EKSPORT DANYCH ===========================================================================
def is_valid_queryparam(param):
    return param != '' and param is not None

def filtrowanie11(request):
    qs = Rozciagi.objects.all()

    #poprawkowe_test = request.POST.get('poprawkowe')
    pracownik_contains_query = request.POST.get('pracownik_2')
    print('pracownik_contains_query', pracownik_contains_query)

    context = {
        'queryset': qs,
    }
    return render(request, 'rozciagi/eksport223.html', context)


def filtrowanie(request):
    qs = Rozciagi.objects.all()
    indeks_kontaktu_contains_query = request.POST.get('indeks_kontaktu_contains')
    numer_zlecenia_contains_query = request.POST.get('numer_zlecenia_contains')
    pracownik_contains_query = request.POST.get('pracownik_contains')
    narzedzia_contains_query = request.POST.get('narzedzia_contains')
    data_od = request.POST.get('data_od')
    data_do = request.POST.get('data_do')
    data_serwis_od = request.POST.get('data_serwis_od')
    data_serwis_do = request.POST.get('data_serwis_do')
    eksport = request.POST.get('eksport')

    print('eksport', eksport)
    print('pracownik_contains_query', numer_zlecenia_contains_query)
    print('data_od', data_od)

    if is_valid_queryparam(indeks_kontaktu_contains_query):
        qs = qs.filter(indeks_kontaktu__icontains=indeks_kontaktu_contains_query)

    elif is_valid_queryparam(numer_zlecenia_contains_query):
        qs = qs.filter(nr_zlecenia__icontains=numer_zlecenia_contains_query)

    elif is_valid_queryparam(pracownik_contains_query):
        qs = qs.filter(nr_pracownika=pracownik_contains_query)

    elif is_valid_queryparam(narzedzia_contains_query):
        qs = qs.filter(narzedzia=narzedzia_contains_query)

    if is_valid_queryparam(data_od):
        qs = qs.filter(data_dodania__gte=data_od)

    if is_valid_queryparam(data_do):
        qs = qs.filter(data_dodania__lte=data_do)

    if is_valid_queryparam(data_serwis_od):
        qs = qs.filter(data_serwis__gte=data_serwis_od)

    if is_valid_queryparam(data_serwis_do):
        qs = qs.filter(data_serwis__lte=data_serwis_do)
    print(qs)
    if eksport == 'on':

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="eksport.csv"'
        response.write(u'\ufeff'.encode('utf8'))

        writer = csv.writer(response, dialect='excel', delimiter=';')
        writer.writerow(
            [
                'nr_zlecenia',
                'indeks_kontaktu',
                'poprawkowe',
                'nr_pozycji',
                'lista',
                'przekroj_przewodu',
                'rozciag',
                'wysokosc',
                'potwierdzenie',
                'nr_narzedzia',
                'narzedzia_rodzaj',
                'nr_pracownika',
                'grupa_robocza',
                'data_serwis',
                'data_dodania',
                'dział'
            ]
        )

        for obj in qs:
            if obj.poprawkowe:
                popraw = 'tak'
            else:
                popraw = 'nie'

            if obj.potwierdzenie:
                potw = 'tak'
            else:
                potw = 'nie'

            writer.writerow(
                [
                    obj.nr_zlecenia,#
                    obj.indeks_kontaktu,#
                    popraw,
                    #obj.poprawkowe,#
                    obj.nr_pozycji,#
                    obj.lista,#
                    obj.przekrojePrzewodow,#
                    obj.rozciag,#
                    obj.wysokosc,#
                    potw,
                    #obj.potwierdzenie,#
                    obj.narzedzia,#
                    obj.narzedzia_rodzaj,#
                    obj.nr_pracownika,#
                    obj.grupa_robocza,#
                    obj.data_serwis,#
                    obj.data_dodania,#
                    obj.zalogowany_user.dzial,
                ]
            )
        return response

    context = {
        'queryset': qs,
    }

    return render(request, 'rozciagi/eksport.html', context)
# =============================================================================================