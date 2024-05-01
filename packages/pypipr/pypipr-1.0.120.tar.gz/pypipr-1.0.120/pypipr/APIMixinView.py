from django.http.response import HttpResponse


class APIMixinView:
    """
    APIView adalah class view untuk membuat Website API

    Cara kerjanya adalah dengan menggunakan variabel GET
    untuk menerima data.
    Cara ini dipilih untuk menghindari CORS protection.

    Key dan value dari parameter get akan disimpan
    dalam variabel dictionary APIDict yg bisa langsung
    diakses.

    Class ini tidak bisa digunakan sendiri.
    Class ini harus menjadi mixin Class View karena
    perlu trigger untuk memanggil method get().


    ```py
    class ExampleAPIView(APIMixinView, View):
        pass
    ```
    """

    APIDict = {}

    def get(self, *args, **kwargs):
        self.get_data(*args, **kwargs)
        if self.process_data(*args, **kwargs):
            return self.success(*args, **kwargs)
        return self.failure(*args, **kwargs)

    def get_data(self, *args, **kwargs):
        iterator = self.APIDict or self.request.GET
        for k, v in iterator.items():
            self.APIDict[k] = self.request.GET.get(k, v)

    def process_data(self, *args, **kwargs):
        return True

    def success(self, *args, **kwargs):
        return HttpResponse(status=200)

    def failure(self, *args, **kwargs):
        return HttpResponse(status=500)
