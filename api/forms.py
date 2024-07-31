from django import forms


class TagForm(forms.Form):
    name = forms.CharField(label='Name', max_length=32)
    type = forms.CharField(label='Tag Type', max_length=16)
    description = forms.CharField(label='Description', max_length=300)
    community_id = forms.IntegerField(label='Community ID')


class TagSetForm(forms.Form):
    community_id = forms.IntegerField(label='Community ID')
    tags = forms.JSONField(label='Tags List')
    name = forms.CharField(label='Name', max_length=120)
    type = forms.CharField(label='type', max_length=120)
    start_date = forms.DateTimeField(label='Start Date')
    end_date = forms.DateTimeField(label='End Date')


class CommunityForm(forms.Form):
    name = forms.CharField(label='Name', max_length=32)
    community_type = forms.CharField(label='Community Type', max_length=16)
    private = forms.IntegerField(label='Private')
    global_link = forms.IntegerField(label='Global Link', required=False)
    description = forms.CharField(label='Description', max_length=300)


