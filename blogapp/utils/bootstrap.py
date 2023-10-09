from django import forms

class BootStrap:
    # 不需要用bootstrap格式的字段
    bootstrap_exclude_fields = []

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # 循环ModelForm中所有字段，给每个字段的插件设置
        for name,field in self.fields.items():
            if name in self.bootstrap_exclude_fields:
                continue
            # 字段中有属性，保留原来的属性；没属性，才增加
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    "class":"form-control",
                    "placeholder":field.label
                }

class BootStrapModelForm(BootStrap,forms.ModelForm):
    pass

class BootStrapForm(BootStrap,forms.Form):
    pass


