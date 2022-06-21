from django.shortcuts import render, redirect
from department import models
from django import forms
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import hashlib


def depart_list(request):
    """ 部门列表 """
    queryset = models.Department.objects.all()
    return render(request, 'depart_list.html', {'queryset': queryset})


def depart_add(request):
    """ 添加部门 """
    if request.method == "GET":
        return render(request, 'depart_add.html')

    title = request.POST.get("title")
    models.Department.objects.create(title=title)

    return redirect("/depart/list")


def depart_delete(request):
    """ 删除部门 """
    nid = request.GET.get('nid')

    models.Department.objects.filter(id=nid).delete()

    return redirect("/depart/list")


def depart_edit(request, nid):
    """ 修改部门 """
    if request.method == "GET":
        row_object = models.Department.objects.filter(id=nid).first()

        return render(request, 'depart_edit.html', {"row_object": row_object})

    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list/")


def personnel_list(request):
    """ 职工管理 """
    queryset = models.UserInfo.objects.all()
    """
    for obj in queryset:
        print(obj.id, obj.name, obj.employee_id, obj.age, obj.depart.title, obj.salary,
              obj.create_time.strftime("%Y-%m-%d"))
    """
    return render(request, 'personnel_list.html', {"queryset": queryset})


class PersonnelModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ["name", "employee_id", "depart", "age", "create_time", "salary"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}


def personnel_add(request):
    """ 添加职工 """
    if request.method == "GET":
        form = PersonnelModelForm()
        return render(request, 'personnel_add.html', {"form": form})

    form = PersonnelModelForm(data=request.POST)
    if form.is_valid():
        # 数据合法，保存至数据库
        # print(form.cleaned_data)
        form.save()
        return redirect('/personnel/list')

    return render(request, 'personnel_add.html', {"form": form})
    """
    <form method="post">
        {% csrf_token %}
        {% for field in form %}
            {{ field.label }} : {{ field }}
        {% endfor %}
    
    </form>
    """


def personnel_edit(request, nid):
    """ 编辑职工 """

    row_object = models.UserInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        form = PersonnelModelForm(instance=row_object)
        return render(request, 'personnel_edit.html', {"form": form})

    form = PersonnelModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/personnel/list/')
    return render(request, 'personnel_edit.html', {"form": form})


def personnel_delete(request, nid):
    """ 删除职工 """
    models.UserInfo.objects.filter(id=nid).delete()

    return redirect("/personnel/list")


def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()


class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=True,
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})

        # 生成随机字符串，并写入 cookie 和 session
        request.session["info"] = {'id': admin_object.id, 'name': admin_object.username}
        return redirect('/depart/list')
    return render(request, 'login.html', {'form': form})


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.path_info == "/login/":
            return

        info_dict = request.session.get("info")
        if info_dict:
            return

        return redirect('/login/')


def logout(request):
    """ 注销 """

    request.session.clear()

    return redirect('/login/')








