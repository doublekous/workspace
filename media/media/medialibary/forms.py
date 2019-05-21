# from django import forms
#
#
# class MedialibaryForm(forms.Form):
#     url = forms.CharField(required=True, max_length=50, error_messages={
#         'required': 'url必填',
#         'max_length': 'url长度不能超过50'
#     })
#     secondpage = forms.CharField(required=True, max_length=50, error_messages={
#         'required': 'secondpage必填',
#         'max_length': 'secondpage长度不能超过50'
#     })
#     thirdpage = forms.CharField(required=True, max_length=50, error_messages={
#         'required': 'thirdpage必填',
#         'max_length': 'thirdpage长度不能超过50'
#     })
#     xunxun_nickname = forms.CharField(required=True, max_length=50, error_messages={
#         'required': 'xunxun_nickname必填',
#         'max_length': 'xunxun_nickname长度不能超过50'
#     })
#     sousou_nickname = forms.CharField(required=True, max_length=50, error_messages={
#         'required': 'sousou_nicknamel必填',
#         'max_length': 'sousou_nickname长度不能超过50'
#     })
#     website = forms.CharField(required=True, max_length=50, error_messages={
#         'required': 'website必填',
#         'max_length': 'website长度不能超过50'
#     })
#     sitetype = forms.CharField(required=True, max_length=50, error_messages={
#         'required': 'sitetype必填',
#         'max_length': 'sitetype长度不能超过50'
#     })
#     regional = forms.CharField(required=True, max_length=50, error_messages={
#         'required': 'regional必填',
#         'max_length': 'regional长度不能超过50'
#     })
#     fetchlevel = forms.IntegerField(required=True, max_length=50, error_messages={
#         'required': 'fetchlevel必填',
#         'max_length': 'fetchlevel长度不能超过50'
#     })
#     yesterdaycapture = forms.IntegerField(required=True, max_length=50, error_messages={
#         'required': 'yesterdaycapture必填',
#         'max_length': 'yesterdaycapture长度不能超过50'
#     })
#     is_author = forms.IntegerField(required=True, max_length=50, error_messages={
#         'required': 'is_author必填',
#         'max_length': 'is_author长度不能超过50'
#     })
#     addpaper = forms.CharField(required=True, max_length=50, error_messages={
#         'required': 'addpaper必填',
#         'max_length': 'addpaper长度不能超过50'
#     })
#     fetchstatus = forms.IntegerField(required=True, max_length=50, error_messages={
#         'required': 'fetchstatus必填',
#         'max_length': 'fetchstatus长度不能超过50'
#     })
#     latestfetchtime = forms.DateTimeField(required=True, max_length=50, error_messages={
#         'required': 'latestfetchtime必填',
#         'max_length': 'latestfetchtime长度不能超过50'
#     })
#     is_process = forms.IntegerField(required=True, max_length=50, error_messages={
#         'required': 'is_process必填',
#         'max_length': 'is_process长度不能超过50'
#     })
#     note = forms.CharField(required=True, max_length=50, error_messages={
#         'required': 'note必填',
#         'max_length': 'note长度不能超过50'
#     })
#     is_xuxu = forms.IntegerField(required=True, max_length=50, error_messages={
#         'required': 'is_xuxu必填',
#         'max_length': 'is_xuxu长度不能超过50'
#     })
#     is_sousou = forms.IntegerField(required=True, max_length=50, error_messages={
#         'required': 'is_sousou必填',
#         'max_length': 'is_sousou长度不能超过50'
#     })
#     manu_choice = forms.IntegerField(required=True, max_length=50, error_messages={
#         'required': 'manu_choice必填',
#         'max_length': 'manu_choice长度不能超过50'
#     })
#     def clean(self):
#         return self.cleaned_data