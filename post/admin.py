from django.contrib import admin

from .models import Post  #Post modelini import etmek için. aynı dizinde bulunduğu için . koyuyoruz.  ( ders 8)

#from post.models import Post

# Register your models here. 
# Model oluşturduğumuz zaman modelin yönetim arayüzünü sağlamak için burada tanımla yapmamız gerekiyor.

class PostAdmin(admin.ModelAdmin):  # Admin modeli oluşturduk ( ders 9 - Admin panelini özelleştirme )

    list_display = ['title', 'publishing_date', 'slug'] # Ekranda hangi alanların görüleceği belirtir ( ders 9)
    list_display_links = [ 'publishing_date']           # Ekranda tıklanıp detaya gidilecek olan kısımlar için ( ders 9)
    list_filter = ['publishing_date']                   # Filtreleme özelliği  ( ders 9)
    search_fields = ['title', 'content']                # Search özelliği  ( ders 9)        
    list_editable = ['title']                           # Kayırtları güncelleme yapmak için. Burada olan kısımlar display links kısmında olmamalı  ( ders 9)  


    class Meta: # Admin modelinin hangi uygulama paneline ait olduğu ( ders 9)
        model = Post

admin.site.register(Post, PostAdmin)  # Post modelini admin paneline bağlamak için (ders 8)
